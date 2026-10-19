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
from manuscript import body_text


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
    parser.add_argument('--case', default='D-Q02', help='Frozen input directory')
    parser.add_argument('--new-words', nargs=2, type=int, default=[450, 550], metavar=('MIN', 'MAX'))
    parser.add_argument('--revise-words', nargs=2, type=int, default=[140, 170], metavar=('MIN', 'MAX'))
    parser.add_argument('--historical-helper-gaps', type=Path,
                        help='Explicitly documented missing historical versions of mutable run helpers; never applies to frozen inputs or skills')
    args = parser.parse_args()
    for bounds in (args.new_words, args.revise_words):
        if not 0 < bounds[0] <= bounds[1]:
            parser.error('Word bounds must be positive and ordered.')
    root, out = args.root.resolve(), args.out.resolve()
    gaps = read_json(args.historical_helper_gaps) if args.historical_helper_gaps else []
    gap_index = {(r['run'], r['path'], r['reported_sha256']): r for r in gaps}
    assert len(gap_index) == len(gaps), 'Duplicate historical helper gaps'
    seen_gaps = set()
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
    loaded_checks, unverified_helpers, input_checks, bodies = [], [], [], []
    for run in read_json(out / 'run-config.json')['runs']:
        folder = root / 'runs' / run['id']
        for required in ['final.md', 'self-review.md', 'rationale.md', 'loaded-resources.json']:
            assert (folder / required).is_file(), (run['id'], required)
        for path, digest in path_hashes(read_json(folder / 'loaded-resources.json')):
            source = Path(path)
            if not source.is_absolute():
                source = root / 'variants' / run['version'] / path
            assert source.is_relative_to(root), path
            actual_digest = sha(source.read_bytes())
            if actual_digest != digest.lower():
                relative = source.relative_to(root).as_posix()
                key = (run['id'], relative, digest.lower())
                assert key in gap_index, path
                gap = gap_index[key]
                assert source.resolve().is_relative_to(folder.resolve()) and source.suffix == '.py', path
                assert gap['current_sha256'] == actual_digest and gap['reason'].strip(), path
                unverified_helpers.append(gap)
                seen_gaps.add(key)
                continue
            loaded_checks.append({'run': run['id'], 'path': source.relative_to(root).as_posix(), 'sha256': digest.lower()})
        seen_inputs = set()
        for f in folder.glob('*input*.json'):
            for path, digest in path_hashes(read_json(f)):
                source = Path(path)
                if not source.is_absolute():
                    source = root / 'inputs' / args.case / path
                assert source.is_relative_to(root / 'inputs'), path
                assert sha(source.read_bytes()) == digest.lower(), path
                seen_inputs.add(source.resolve())
                input_checks.append({'run': run['id'], 'path': source.relative_to(root).as_posix(), 'sha256': digest.lower()})
        required_inputs = [run['operation'] + '-request.md', 'source-pack.md']
        if run['operation'] == 'revise':
            required_inputs.append('original.md')
        expected_inputs = {(root / 'inputs' / args.case / name).resolve() for name in required_inputs}
        assert expected_inputs <= seen_inputs, (run['id'], 'Missing task input hash records', expected_inputs - seen_inputs)
        body = body_text((folder / 'final.md').read_text(encoding='utf-8')).strip()
        assert not re.search('[\u4e00-\u9fff\ufffd]', body), run['id']
        count = len(body.split())
        lower, upper = args.new_words if run['operation'] == 'new' else args.revise_words
        assert lower <= count <= upper, (run['id'], count)
        if run['operation'] == 'revise':
            assert len(re.split(r'\n\s*\n', body)) == 1
        bodies.append({'run': run['id'], 'body_whitespace_words': count, 'final_sha256': sha((folder / 'final.md').read_bytes())})
    assert seen_gaps == set(gap_index), 'Unused or mismatched historical helper gap records'
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
        'word_bounds': {'new': args.new_words, 'revise': args.revise_words},
        'agent_reported_resources_verified': loaded_checks, 'agent_reported_inputs_verified': input_checks,
        'unverified_historical_run_helpers': unverified_helpers,
        'manuscripts': bodies, 'artifacts': artifacts,
        'path_alias': '<EXPERIMENT_ROOT> is the external experiment directory. Only this prefix was replaced; original hashes refer to the external records.'}
    (out / 'archive-manifest.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'artifacts': len(artifacts), 'resources': len(loaded_checks), 'unverified_historical_helpers': len(unverified_helpers), 'inputs': len(input_checks), 'manuscripts': bodies}, indent=2))


if __name__ == '__main__':
    main()
