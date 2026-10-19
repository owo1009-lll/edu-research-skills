"""Build an isolated two-arm development comparison from a frozen snapshot.

The control snapshot is made with ../writing-20261018/snapshot.py first.
This helper never edits a runtime skill or overwrites an existing variant.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--control', type=Path, required=True)
    parser.add_argument('--control-manifest', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--manifest', type=Path, required=True)
    args = parser.parse_args()
    control, out = args.control.resolve(), args.out.resolve()
    if out.exists() or args.manifest.exists():
        parser.error('Variant directory and manifest must both be new.')
    if out == control or control in out.parents or out in control.parents:
        parser.error('Variant and control must be separate directories.')
    baseline = json.loads(args.control_manifest.read_text(encoding='utf-8'))
    for item in baseline['files']:
        assert hashlib.sha256((control / item['path']).read_bytes()).hexdigest() == item['sha256']
    shutil.copytree(control, out)
    relative = 'skills/edu-writing/references/quantitative-discussion.md'
    addition = Path(__file__).with_name('candidate-addition.md').read_bytes()
    target = out / relative
    target.write_bytes(target.read_bytes().rstrip() + b'\n\n' + addition.lstrip())
    records = []
    for old in baseline['files']:
        data = (out / old['path']).read_bytes()
        records.append({'path': old['path'], 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)})
    changed = [r['path'] for r, old in zip(records, baseline['files']) if r != old]
    assert changed == [relative], changed
    tree = hashlib.sha256(json.dumps(records, ensure_ascii=False, separators=(',', ':')).encode('utf-8')).hexdigest()
    result = {
        'label': 'qc01-example-only', 'purpose': 'development comparison; not final holdout freeze',
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'source_head': baseline['source_head'],
        'control_tree_sha256': baseline['tree_sha256'],
        'addition_sha256': hashlib.sha256(addition).hexdigest(),
        'changed_files': changed, 'tree_sha256': tree,
        'hash_definition': baseline['hash_definition'], 'files': records,
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'files': len(records), 'changed': changed, 'tree_sha256': tree}))


if __name__ == '__main__':
    main()
