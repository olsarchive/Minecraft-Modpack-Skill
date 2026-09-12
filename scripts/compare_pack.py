"""Read-only, path-based three-way comparison; never an installation plan.

Python 3.11+, standard library only. Supports instance folders and modrinth ZIPs.
Remote index entries stay hash references: this program never downloads files.
"""
import argparse
import collections
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import zipfile

SCOPES = {'mods', 'config', 'defaultconfigs', 'kubejs', 'datapacks',
          'global_packs', 'resourcepacks', 'shaderpacks', 'patchouli_books', 'options.txt'}
IGNORE_DIRS = {'.connector', '.cache', 'logs', '__pycache__'}


def safe_name(name):
    name = name.replace('\\', '/')
    parts = PurePosixPath(name).parts
    if not parts or name.startswith('/') or ':' in name or '..' in parts:
        raise ValueError(f'Unsafe archive path: {name}')
    return '/'.join(parts)


def fingerprint(data, name):
    result = {a: hashlib.new(a, data).hexdigest() for a in ['sha1', 'sha256', 'sha512']}
    result['size'] = len(data)
    if name.lower().endswith('.zip'):
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            members = {}
            folded = set()
            for info in z.infolist():
                if info.is_dir():
                    continue
                path = safe_name(info.filename)
                if path.casefold() in folded:
                    raise ValueError(f'Duplicate ZIP member: {name}: {path}')
                folded.add(path.casefold())
                members[path] = hashlib.sha256(z.read(info)).hexdigest()
        canonical = json.dumps(members, sort_keys=True, ensure_ascii=False, separators=(',', ':'))
        result['zip_members_sha256'] = hashlib.sha256(canonical.encode('utf-8')).hexdigest()
        result['zip_members'] = members
    return result


def equivalent(a, b):
    if a is None or b is None:
        return a is b
    common = [k for k in ['zip_members_sha256', 'sha512', 'sha256', 'sha1'] if k in a and k in b]
    return a[common[0]] == b[common[0]] if common else None


def classify(base, upstream, local):
    if any(x and x.get('unresolved') for x in [base, upstream, local]):
        return 'unresolved'
    if equivalent(local, upstream) is True:
        return 'already_synced' if local else 'absent'
    if base is None:
        if local is None:
            return 'add_candidate'
        return 'local_only' if upstream is None else 'unknown_baseline_conflict'
    if equivalent(upstream, base) is True:
        return 'keep_local' if local else 'keep_local_deletion'
    if upstream is None:
        return 'upstream_removal_review' if equivalent(local, base) is True else 'conflict_upstream_removed'
    if local is None:
        return 'conflict_local_deleted'
    if equivalent(local, base) is True:
        return 'update_candidate'
    if any(equivalent(a, b) is None for a,b in [(base,upstream),(base,local),(upstream,local)]):
        return 'unresolved'
    return 'conflict'


def inventory(path):
    path = Path(path).resolve(strict=True)
    result = {'source': str(path), 'files': {}}
    folded = set()
    def add(name, record):
        name = safe_name(name)
        if name.casefold() in folded:
            raise ValueError(f'Duplicate effective path: {path}: {name}')
        folded.add(name.casefold())
        if name.split('/')[0] in SCOPES:
            result['files'][name] = record
    if path.is_dir():
        if (path/'modrinth.index.json').exists() or (path/'overrides').exists():
            raise ValueError('Extracted pack directory is unsupported; supply its original Modrinth ZIP')
        for scope in sorted(SCOPES):
            root = path/scope
            candidates = sorted(root.rglob('*')) if root.is_dir() else [root] if root.is_file() else []
            for file in candidates:
                relative = file.relative_to(path)
                if any(p in IGNORE_DIRS for p in relative.parts) or not file.is_file():
                    continue
                if file.is_symlink() or not file.resolve().is_relative_to(path):
                    raise ValueError(f'Input link requires review: {file}')
                before = file.stat()
                record = fingerprint(file.read_bytes(), str(file))
                after = file.stat()
                if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
                    raise ValueError(f'File changed during audit: {file}')
                add(relative.as_posix(), record)
    else:
        with zipfile.ZipFile(path) as z:
            names = z.namelist()
            if len(names) != len(set(names)):
                raise ValueError(f'Duplicate archive entries: {path}')
            if 'modrinth.index.json' in names:
                index = json.loads(z.read('modrinth.index.json'))
                result['dependencies'] = index.get('dependencies', {})
                for entry in index.get('files', []):
                    hashes = {k:v for k,v in entry.get('hashes', {}).items() if k in ['sha1','sha256','sha512']}
                    env = entry.get('env', {})
                    side_review = any(value != 'required' for value in env.values())
                    add(entry['path'], {**hashes, 'downloads': entry.get('downloads', []), 'env': env,
                                        'source': 'remote_index', 'unresolved': not bool(hashes) or side_review})
            for info in z.infolist():
                name = safe_name(info.filename)
                if not info.is_dir() and name.startswith('overrides/'):
                    relative = name[len('overrides/'):]
                    add(relative, fingerprint(z.read(info), relative))
                elif not info.is_dir() and name.startswith(('client-overrides/', 'server-overrides/')):
                    raise ValueError('Side-specific overrides require an explicit side projection before comparison')
    if not result['files']:
        raise ValueError(f'No supported files found; verify input layout and scopes: {path}')
    return result


def validate_output(output, sources):
    output = Path(output).resolve()
    if output.exists():
        raise ValueError('Output must be a new file; existing files and hard links cannot be overwritten')
    for source in sources:
        source = Path(source).resolve()
        if output == source or (source.is_dir() and output.is_relative_to(source)):
            raise ValueError('Output must be outside every input to preserve read-only behavior')


def compare(base, upstream, local):
    rows = []
    for name in sorted(base.keys() | upstream.keys() | local.keys()):
        b, u, l = base.get(name), upstream.get(name), local.get(name)
        row = {'path':name, 'status':classify(b,u,l)}
        if l and u and 'zip_members' in l and 'zip_members' in u:
            a,c = l['zip_members'],u['zip_members']
            row['zip_delta'] = {'added':len(c.keys()-a.keys()),'removed':len(a.keys()-c.keys()),'changed':sum(a[k]!=c[k] for k in a.keys()&c.keys())}
        rows.append(row)
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', type=Path, required=True)
    parser.add_argument('--upstream', type=Path, required=True)
    parser.add_argument('--local', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    sources = [args.base,args.upstream,args.local]
    validate_output(args.out, sources)
    snapshots = dict(zip(['base','upstream','local'], [inventory(p) for p in sources]))
    rows = compare(*(snapshots[k]['files'] for k in ['base','upstream','local']))
    summary = dict(collections.Counter(row['status'] for row in rows))
    report = {'schema_version':1,'mode':'read_only_path_comparison','runtime_verified':False,
              'notice':'Paths are not mod identities. Resolve renames, loader replacements, dependencies, patches and load order before installation. World files are excluded.',
              'summary':summary,'snapshots':snapshots,'comparison':rows}
    args.out.parent.mkdir(parents=True,exist_ok=True)
    with args.out.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps(summary,ensure_ascii=False))


if __name__ == '__main__':
    main()
