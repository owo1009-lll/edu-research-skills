"""Prepare paired manuscripts without changing manuscript text.

Keep --key outside the reviewer's allowed inputs until its review is saved.
Random assignment is recorded, not a claim of model random-seed control.
"""
import argparse
import hashlib
import json
from pathlib import Path
import secrets


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runs', type=Path, required=True)
    parser.add_argument('--inputs', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--key', type=Path, required=True)
    parser.add_argument('--stage', choices=('development', 'holdout'), default='development')
    parser.add_argument('--task', action='append', choices=('D1', 'D2', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7'))
    parser.add_argument('--arms', nargs=2, choices=('p', 'q', 'r'), default=('p', 'q'))
    parser.add_argument('--repeat', action='append', type=int, choices=(1, 2))
    args = parser.parse_args()
    if args.arms[0] == args.arms[1]:
        parser.error('The compared arms must be different.')
    if args.stage == 'holdout' and not args.task:
        parser.error('Select holdout tasks explicitly; not every task has two repeats.')
    if any(task.startswith('H') != (args.stage == 'holdout') for task in (args.task or [])):
        parser.error('Task IDs must match the selected stage.')
    if args.out.exists() or args.key.exists():
        parser.error('The output and key must both be new.')
    if args.out.resolve() in args.key.resolve().parents:
        parser.error('Keep the key outside the blind directory.')
    prepared, assignments = [], []
    for task in sorted(set(args.task or ('D1', 'D2'))):
        for repeat in sorted(set(args.repeat or (1, 2))):
            pair = f'{task}-pair{repeat:02d}'
            arms = list(args.arms)
            secrets.SystemRandom().shuffle(arms)
            mapping = {'pair': pair, 'assignment': {}}
            for letter, arm in zip(('A', 'B'), arms):
                rel = f'{task}-run{repeat:02d}-arm-{arm}/final.md'
                data = (args.runs / rel).read_bytes()
                if not data.strip():
                    raise ValueError(f'Empty manuscript: {rel}')
                prepared.append((f'{pair}/{letter}.md', data))
                mapping['assignment'][letter] = {
                    'run': rel, 'sha256': hashlib.sha256(data).hexdigest()}
            for name in ('request', 'materials'):
                prepared.append((f'{pair}/{name}.md',
                                 (args.inputs / f'{task}-{name}.md').read_bytes()))
            assignments.append(mapping)
    args.out.mkdir(parents=True)
    for rel, data in prepared:
        target = args.out / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    args.key.parent.mkdir(parents=True, exist_ok=True)
    args.key.write_text(json.dumps({
        'purpose': ('development comparison, not holdout' if args.stage == 'development'
                    else 'post-freeze holdout comparison'),
        'text_transform': 'none; exact final.md bytes, teaching notices retained',
        'pairs': assignments}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Prepared {len(assignments)} anonymous pairs. Key saved separately.')


if __name__ == '__main__':
    main()
