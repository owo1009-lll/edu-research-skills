"""Verify frozen inputs/resources and archive completed experimental artifacts.

Preserves original and published hashes. Replaces only the experiment-root path
in text records; archived helper scripts are records, not portable entrypoints.
Resource manifests are agent reports, not independent execution traces.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def path_hashes(value):
    if isinstance(value, dict):
        if 'sha256' in value and 'path' in value:
            yield value['path'], value['sha256']
        for child in value.values():
            yield from path_hashes(child)
    elif isinstance(value, list):
        for child in value:
            yield from path_hashes(child)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    root, out = args.root.resolve(), args.out.resolve()
    if any((out / x).exists() for x in ['runs', 'blind', 'keys', 'reviews', 'archive-manifest.json']):
        raise SystemExit('Refusing to overwrite an existing artifact archive')
    snapshot_checks = {}
    for version, name in [('v1', 'control'), ('v2', 'candidate')]:
        manifest = read_json(out / 'snapshots' / (name + '.json'))
        for row in manifest['files']:
            assert sha((root / 'variants' / version / row['path']).read_bytes()) == row['sha256']
        snapshot_checks[version] = len(manifest['files'])
    frozen_inputs = read_json(out / 'input-freeze.json')['files']
    for row in frozen_inputs:
        assert sha((root / row['path']).read_bytes()) == row['sha256']
        assert sha((out / row['path']).read_bytes()) == row['sha256']
    loaded_checks, input_checks, bodies = [], [], []
    for run in read_json(out / 'run-config.json')['runs']:
        folder = root / 'runs' / run['id']
        for required in ['final.md', 'self-review.md', 'rationale.md', 'loaded-resources.json']:
            assert (folder / required).is_file(), (run['id'], required)
        for path, digest in path_hashes(read_json(folder / 'loaded-resources.json')):
            source = Path(path)
            if not source.is_absolute():
                source = root / 'variants' / run['version'] / path
            assert source.is_relative_to(root), path
            assert sha(source.read_bytes()) == digest.lower(), path
            loaded_checks.append({'run': run['id'], 'path': source.relative_to(root).as_posix(), 'sha256': digest.lower()})
        for f in folder.glob('input*.json'):
            for path, digest in path_hashes(read_json(f)):
                source = Path(path)
                if not source.is_absolute():
                    source = root / 'inputs' / 'D-Q02' / path
                assert source.is_relative_to(root / 'inputs'), path
                assert sha(source.read_bytes()) == digest.lower(), path
                input_checks.append({'run': run['id'], 'path': source.relative_to(root).as_posix(), 'sha256': digest.lower()})
        body = '\n'.join((folder / 'final.md').read_text(encoding='utf-8').splitlines()[1:]).strip()
        assert not re.search('[\u4e00-\u9fff\ufffd]', body), run['id']
        count = len(body.split())
        lower, upper = (450, 550) if run['operation'] == 'new' else (140, 170)
        assert lower <= count <= upper, (run['id'], count)
        if run['operation'] == 'revise':
            assert len(re.split(r'\n\s*\n', body)) == 1
        bodies.append({'run': run['id'], 'body_whitespace_words': count, 'final_sha256': sha((folder / 'final.md').read_bytes())})
    for operation in ['new', 'revise']:
        for row in read_json(root / 'keys' / (operation + '.json'))['records']:
            assert sha((root / 'runs' / row['run'] / 'final.md').read_bytes()) == row['original_sha256']
            assert sha((root / 'blind' / operation / (row['label'] + '.md')).read_bytes()) == row['anonymous_sha256']
        for name in ['review.md', 'review.json']:
            assert (root / 'reviews' / operation / name).is_file()
    artifacts = []
    roots = sorted({str(root), root.as_posix(), str(root).replace('\\', '\\\\')}, key=len, reverse=True)
    for category in ['runs', 'blind', 'keys', 'reviews']:
        for source in sorted((root / category).rglob('*')):
            if not source.is_file() or '__pycache__' in source.parts:
                continue
            raw = source.read_bytes()
            content = raw.decode('utf-8')
            for prefix in roots:
                content = content.replace(prefix, '<EXPERIMENT_ROOT>')
            published = content.encode('utf-8')
            relative = source.relative_to(root)
            target = out / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(published)
            artifacts.append({'path': relative.as_posix(), 'original_sha256': sha(raw),
                              'published_sha256': sha(published), 'root_path_replaced': raw != published})
    report = {'verified_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Record integrity and task length/language compliance, not writing quality or source statistical validation.',
        'snapshot_files_verified': snapshot_checks, 'frozen_inputs_verified': len(frozen_inputs),
        'agent_reported_resources_verified': loaded_checks, 'agent_reported_inputs_verified': input_checks,
        'manuscripts': bodies, 'artifacts': artifacts,
        'path_alias': '<EXPERIMENT_ROOT> is the external experiment directory. Only this prefix was replaced; original hashes refer to the external records.'}
    (out / 'archive-manifest.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'artifacts': len(artifacts), 'resources': len(loaded_checks), 'inputs': len(input_checks), 'manuscripts': bodies}, indent=2))


if __name__ == '__main__':
    main()
