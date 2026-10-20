"""Freeze the actual skill bytes used by a writing run; never overwrite a snapshot.

Run from either checkout. The manifest uses repository-relative paths so another
reader can verify the same tree without the developer's local directory names.
This records inputs, not model determinism or writing quality.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--label', required=True)
    parser.add_argument('--purpose', default='development comparison; not final holdout freeze',
                        help='State whether this freeze is for development or independent final validation.')
    args = parser.parse_args()
    root, out = args.source.resolve(), args.out.resolve()
    manifest = args.manifest.resolve()
    if out.exists() or manifest.exists():
        parser.error('Output directory and manifest must both be new.')
    if out == root or root in out.parents:
        parser.error('Keep the snapshot outside the source repository.')
    paths = sorted(set(p.decode('utf-8') for p in git(
        root, 'ls-files', '-z', '--cached', '--others', '--exclude-standard',
        '--', 'skills').split(b'\0') if p))
    if 'skills/edu-writing/SKILL.md' not in paths:
        parser.error('The source must contain the edu-writing skill.')
    records, buffers = [], []
    for rel in paths:
        src = root / rel
        if src.is_symlink() or root not in src.resolve().parents:
            parser.error(f'Not a regular in-repository source: {rel}')
        data = src.read_bytes()
        records.append({'path': rel, 'sha256': hashlib.sha256(data).hexdigest(),
                        'bytes': len(data)})
        buffers.append((rel, data))
    tree = hashlib.sha256(json.dumps(records, ensure_ascii=False,
                                    separators=(',', ':')).encode('utf-8')).hexdigest()
    result = {
        'label': args.label,
        'purpose': args.purpose,
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'source_head': git(root, 'rev-parse', 'HEAD').decode().strip(),
        'source_skill_status': git(root, 'status', '--porcelain', '--', 'skills').decode(),
        'tree_sha256': tree,
        'hash_definition': 'SHA256 of UTF-8 compact JSON records in sorted path order',
        'files': records,
    }
    out.mkdir(parents=True)
    for rel, data in buffers:
        target = out / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        if hashlib.sha256(target.read_bytes()).hexdigest() != next(
                r['sha256'] for r in records if r['path'] == rel):
            raise RuntimeError(f'Snapshot copy mismatch: {rel}')
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'label': args.label, 'files': len(records), 'tree_sha256': tree}))


if __name__ == '__main__':
    main()
