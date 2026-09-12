import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
import zipfile

SCRIPT = Path(__file__).parents[1] / 'scripts' / 'compare_pack.py'


class CompareTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not SCRIPT.exists():
            return
        spec = importlib.util.spec_from_file_location('compare_pack', SCRIPT)
        cls.tool = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.tool)

    def test_tool_exists(self):
        self.assertTrue(SCRIPT.exists(), 'Reusable comparison tool has not been implemented')

    def tool_or_skip(self):
        if not SCRIPT.exists():
            self.skipTest('Waiting for implementation')
        return self.tool

    def test_three_way_preserves_local_change(self):
        t = self.tool_or_skip()
        b, l = {'sha256': 'base'}, {'sha256': 'local'}
        self.assertEqual(t.classify(b, b, l), 'keep_local')
        self.assertEqual(t.classify(b, {'sha256': 'new'}, l), 'conflict')

    def test_deletion_is_never_an_automatic_install_action(self):
        t = self.tool_or_skip()
        b = {'sha256': 'base'}
        self.assertEqual(t.classify(b, None, b), 'upstream_removal_review')
        self.assertEqual(t.classify(b, b, None), 'keep_local_deletion')
        self.assertEqual(t.classify(None, None, b), 'local_only')

    def test_missing_base_is_not_overwrite_permission(self):
        t = self.tool_or_skip()
        self.assertEqual(t.classify(None, {'sha256': 'new'}, {'sha256': 'local'}), 'unknown_baseline_conflict')

    def test_zip_compression_is_not_a_content_change(self):
        t = self.tool_or_skip()
        def packed(compression):
            stream = io.BytesIO()
            with zipfile.ZipFile(stream, 'w', compression=compression) as z:
                z.writestr('data/example/recipe/a.json', '{"type":"minecraft:crafting_shapeless"}')
            return stream.getvalue()
        a = t.fingerprint(packed(zipfile.ZIP_STORED), 'example.zip')
        b = t.fingerprint(packed(zipfile.ZIP_DEFLATED), 'example.zip')
        self.assertNotEqual(a['sha256'], b['sha256'])
        self.assertTrue(t.equivalent(a, b))

    def test_index_hash_can_match_local_file(self):
        t = self.tool_or_skip()
        local = t.fingerprint(b'jar bytes', 'mod.jar')
        self.assertTrue(t.equivalent(local, {'sha1': local['sha1']}))
        self.assertEqual(t.classify(None, {'unresolved': True}, local), 'unresolved')

    def test_archive_rejects_duplicate_and_escape_paths(self):
        t = self.tool_or_skip()
        with tempfile.TemporaryDirectory() as root:
            for entry in ['overrides/../outside.txt', 'overrides/C:/outside.txt']:
                path = Path(root)/'bad.zip'
                with zipfile.ZipFile(path, 'w') as z:
                    z.writestr(entry, 'bad')
                with self.assertRaises(ValueError):
                    t.inventory(path)
            path = Path(root)/'duplicate.zip'
            with zipfile.ZipFile(path, 'w') as z:
                z.writestr('overrides/config/a.txt', 'one')
                z.writestr('overrides/config/A.txt', 'two')
            with self.assertRaises(ValueError):
                t.inventory(path)

    def test_output_cannot_be_inside_input(self):
        t = self.tool_or_skip()
        with tempfile.TemporaryDirectory() as root:
            source = Path(root)/'main'
            source.mkdir()
            with self.assertRaises(ValueError):
                t.validate_output(source/'report.json', [source])

    def test_existing_output_hardlink_cannot_overwrite_input(self):
        t = self.tool_or_skip()
        with tempfile.TemporaryDirectory() as root:
            source = Path(root)/'main'
            source.mkdir()
            original = source/'config.txt'
            original.write_text('personal')
            output = Path(root)/'report.json'
            os.link(original, output)
            with self.assertRaises(ValueError):
                t.validate_output(output, [source])
            self.assertEqual(original.read_text(), 'personal')

    def test_unsupported_or_empty_layout_cannot_report_deletions(self):
        t = self.tool_or_skip()
        with tempfile.TemporaryDirectory() as root:
            root = Path(root)
            extracted = root/'extracted'
            (extracted/'overrides/config').mkdir(parents=True)
            (extracted/'overrides/config/a.txt').write_text('author')
            (extracted/'modrinth.index.json').write_text('{"files":[]}')
            empty = root/'empty'
            empty.mkdir()
            archive = root/'raw.zip'
            with zipfile.ZipFile(archive, 'w') as z:
                z.writestr('config/a.txt', 'author')
            for path in [extracted, empty, archive]:
                with self.subTest(path=path), self.assertRaises(ValueError):
                    t.inventory(path)

    def test_index_side_constraints_are_retained_and_need_review(self):
        t = self.tool_or_skip()
        with tempfile.TemporaryDirectory() as root:
            archive = Path(root)/'author.zip'
            env = {'client':'unsupported', 'server':'required'}
            with zipfile.ZipFile(archive, 'w') as z:
                z.writestr('modrinth.index.json', json.dumps({'files':[
                    {'path':'mods/server.jar', 'hashes':{'sha1':'abc'}, 'env':env}]}))
            record = t.inventory(archive)['files']['mods/server.jar']
            self.assertEqual(record['env'], env)
            self.assertEqual(t.classify(None, record, None), 'unresolved')

    def test_end_to_end_inventory_preserves_inputs(self):
        t = self.tool_or_skip()
        with tempfile.TemporaryDirectory() as root:
            root = Path(root)
            local = root/'local'
            (local/'config').mkdir(parents=True)
            (local/'config/a.txt').write_text('personal')
            (local/'saves').mkdir()
            (local/'saves/private.txt').write_text('world')
            archive = root/'author.zip'
            with zipfile.ZipFile(archive, 'w') as z:
                z.writestr('overrides/config/a.txt', 'author')
            snapshot = t.inventory(local)
            self.assertEqual(list(snapshot['files']), ['config/a.txt'])
            self.assertIn('config/a.txt', t.inventory(archive)['files'])
            self.assertEqual((local/'config/a.txt').read_text(), 'personal')


if __name__ == '__main__':
    unittest.main()
