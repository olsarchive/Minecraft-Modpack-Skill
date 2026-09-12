import importlib.util
from pathlib import Path
import sys
import unittest

SCRIPT = Path(__file__).parents[1]/'scripts/merge_quests.py'

class QuestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location('merge_quests', SCRIPT)
        cls.tool = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = cls.tool
        spec.loader.exec_module(cls.tool)

    def test_ftb_optional_commas_and_typed_arrays_roundtrip(self):
        t=self.tool
        original=t.parse('{ id: "A" tasks: [{ id: "B" count: 2L }] uuid: [I; 1, -2, 3] enabled: true }')
        self.assertEqual(t.parse(t.dump(original)),original)

    def test_strings_do_not_lose_command_escapes(self):
        t=self.tool
        original=t.parse(r'{ command: "tellraw @s {\"text\":\"hello\"}" }')
        self.assertEqual(t.parse(t.dump(original)),original)

    def test_duplicate_keys_fail(self):
        with self.assertRaises(ValueError): self.tool.parse('{ id: "A" id: "B" }')

    def test_identical_duplicate_requires_explicit_audit_list(self):
        t=self.tool
        duplicates=[]
        self.assertEqual(t.parse('{ title: "same" title: "same" }',duplicates),{'title':'same'})
        self.assertEqual(duplicates,['title'])
        with self.assertRaises(ValueError): t.parse('{ title: "a" title: "b" }',[])

    def test_explicit_last_wins_records_old_local_override(self):
        t=self.tool
        audit=[]
        self.assertEqual(t.parse('{ title: "forest" title: "moon" }',audit,last_wins=True),{'title':'moon'})
        self.assertEqual(audit,[{'key':'title','previous':'"forest"','selected':'"moon"'}])
        with self.assertRaises(ValueError): t.parse('{ title: "a" title: "b" }',last_wins=True)

    def test_preserve_local_reward_and_import_new_quest(self):
        t=self.tool
        b=t.parse('{ quests: [{ id: "A" reward: 5 }] }')
        u=t.parse('{ quests: [{ id: "A" reward: 2 } { id: "B" reward: 1 }] }')
        l=t.parse('{ quests: [{ id: "A" reward: 750 } { id: "C" reward: 8 }] }')
        conflicts=[]
        result=t.merge(b,u,l,conflicts)
        self.assertEqual([q['id'] for q in result['quests']],['A','C','B'])
        self.assertEqual(result['quests'][0]['reward'],t.Atom('750'))
        self.assertTrue(conflicts)

    def test_upstream_removal_cannot_drop_saved_task_id(self):
        t=self.tool
        b=t.parse('{ quests: [{ id: "A" }] }')
        u=t.parse('{ quests: [] }')
        notes=[]
        self.assertEqual(t.merge(b,u,b,notes),b)
        self.assertTrue(notes)

    def test_duplicate_ids_fail(self):
        t=self.tool
        bad=t.parse('{ quests: [{ id: "A" } { id: "A" }] }')
        with self.assertRaises(ValueError): t.merge({},bad,{},[])

    def test_unchanged_local_field_accepts_author_fix(self):
        t=self.tool
        b=t.parse('{ description: "old" }')
        u=t.parse('{ description: "fixed" }')
        self.assertEqual(t.merge(b,u,b,[]),u)

    def test_root_identity_cannot_be_replaced(self):
        t=self.tool
        b=t.parse('{ id: "AAAA" quests: [{ id: "BBBB" }] }')
        u=t.parse('{ id: "CCCC" quests: [{ id: "BBBB" }] }')
        notes=[]
        self.assertEqual(t.merge(b,u,b,notes)['id'],'AAAA')
        self.assertTrue(notes)

    def test_bare_id_and_list_type_change_preserve_identity(self):
        t=self.tool
        b=t.parse('{ quests: [{ id: ABCDEF0123456789 }] }')
        for source in ['{ quests: [] }','{ quests: "invalid" }']:
            notes=[]
            self.assertEqual(t.merge(b,t.parse(source),b,notes),b)
            self.assertTrue(notes)

    def test_missing_baseline_id_collision_is_not_silent_union(self):
        t=self.tool
        u=t.parse('{ quests: [{ id: "AAAA" title: "new" }] }')
        l=t.parse('{ quests: [{ id: "AAAA" reward: 750 }] }')
        notes=[]
        self.assertEqual(t.merge(t.MISSING,u,l,notes),l)
        self.assertTrue(notes)

    def test_mixed_missing_ids_cannot_hide_duplicate(self):
        t=self.tool
        bad=t.parse('{ quests: [{ id: "AAAA" } { id: "AAAA" } { title: "missing" }] }')
        with self.assertRaises(ValueError): t.merge({},bad,{},[])

if __name__=='__main__': unittest.main()
