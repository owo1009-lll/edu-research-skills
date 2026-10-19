"""Create anonymous review inputs from four finished runs of one operation."""
import argparse
import hashlib
import json
from pathlib import Path
import random
import shutil
from manuscript import body_text


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--operation', choices=['new', 'revise'], required=True)
    parser.add_argument('--case', default='D-Q02', help='Frozen input directory and run ID prefix')
    args = parser.parse_args()
    target = args.root / 'blind' / args.operation
    key_path = args.root / 'keys' / (args.operation + '.json')
    if target.exists() or key_path.exists():
        raise SystemExit('Refusing to replace an existing review package')
    runs = [f'{args.case}-{args.operation}-r{r}-v{v}' for r in [1, 2] for v in [1, 2]]
    originals = {rid: (args.root / 'runs' / rid / 'final.md').read_bytes() for rid in runs}
    random.SystemRandom().shuffle(runs)
    target.mkdir(parents=True)
    key_path.parent.mkdir(parents=True, exist_ok=True)
    records = []
    for label, rid in zip('ABCD', runs):
        original = originals[rid]
        body = body_text(original.decode('utf-8'))
        data = body.encode('utf-8')
        (target / f'{label}.md').write_bytes(data)
        records.append({'label': label, 'run': rid, 'original_sha256': sha(original),
                        'anonymous_sha256': sha(data), 'body_whitespace_words': len(body.split())})
    for name in ['source-pack.md', args.operation + '-request.md'] + (['original.md'] if args.operation == 'revise' else []):
        shutil.copyfile(args.root / 'inputs' / args.case / name, target / name)
    key_path.write_text(json.dumps({'operation': args.operation, 'records': records,
        'transformation': 'Initial title/attribution heading and separate final Attribution section removed when present; body wording unchanged; line endings normalized to LF.'}, indent=2) + '\n', encoding='utf-8')
    (args.root / 'reviews' / args.operation).mkdir(parents=True)
    print('Prepared four anonymous English manuscripts for', args.operation)


if __name__ == '__main__':
    main()
