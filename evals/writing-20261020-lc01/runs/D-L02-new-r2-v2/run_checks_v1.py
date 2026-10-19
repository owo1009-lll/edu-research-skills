"""Preserved helper v1: run checkers and retain their actual outputs and hashes."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parent
SNAPSHOT = BASE.parent.parent / 'variants' / 'v2' / 'skills'
INPUTS = BASE.parent.parent / 'inputs' / 'D-L02'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def log(value):
    with (BASE / 'executed-commands.jsonl').open('a', encoding='utf-8') as stream:
        stream.write(json.dumps(value, ensure_ascii=False) + '\n')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--draft', required=True)
    parser.add_argument('--stage', required=True)
    args = parser.parse_args()
    draft = (BASE / args.draft).resolve()
    assert draft.parent == BASE
    assert re.fullmatch(r'[a-z0-9-]+', args.stage)
    out = BASE / 'checks' / args.stage
    out.mkdir(parents=True, exist_ok=False)
    resources = [
        ('edu-writing/SKILL.md', ['read']),
        ('edu-writing/references/argument.md', ['read']),
        ('edu-writing/references/voice-en.md', ['read']),
        ('edu-writing/references/qualitative-narrative.md', ['read']),
        ('edu-shared/references/integrity.md', ['read']),
        ('edu-writing/references/methods/cases-develop-explanations.md', ['read']),
        ('edu-writing/references/prose-en.md', ['read']),
        ('edu-writing/scripts/check_voice.py', ['read', 'executed']),
        ('edu-writing/scripts/check_prose.py', ['read', 'executed']),
    ]
    manifest = [{'path': str(SNAPSHOT / path), 'sha256': digest(SNAPSHOT / path), 'operations': operations}
                for path, operations in resources]
    manifest.append({'path': str(Path(__file__).resolve()), 'sha256': digest(Path(__file__).resolve()),
                     'operations': ['created', 'executed'], 'role': 'preserved run helper'})
    write_json(BASE / 'loaded-resources.json', manifest)
    hashes = [{'path': str(INPUTS / name), 'sha256': digest(INPUTS / name)}
              for name in ['new-request.md', 'source-pack.md']]
    if (BASE / 'input-hashes.json').exists():
        assert json.loads((BASE / 'input-hashes.json').read_text(encoding='utf-8')) == hashes
    else:
        write_json(BASE / 'input-hashes.json', hashes)
    log({'kind': 'helper invocation', 'argv': [sys.executable, str(Path(__file__).resolve()), *sys.argv[1:]],
         'time_utc': datetime.now(timezone.utc).isoformat(), 'helper_sha256': digest(Path(__file__).resolve())})
    for checker in ['check_voice.py', 'check_prose.py']:
        command = [sys.executable, str(SNAPSHOT / 'edu-writing' / 'scripts' / checker), '--draft', str(draft)]
        if checker == 'check_voice.py':
            command += ['--source', str(INPUTS / 'source-pack.md')]
        result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', cwd=BASE)
        stem = checker.removesuffix('.py')
        (out / (stem + '.stdout.txt')).write_text(result.stdout, encoding='utf-8')
        (out / (stem + '.stderr.txt')).write_text(result.stderr, encoding='utf-8')
        log({'kind': 'checker', 'stage': args.stage, 'argv': command, 'exit_code': result.returncode,
             'stdout': str(out / (stem + '.stdout.txt')), 'stderr': str(out / (stem + '.stderr.txt')),
             'draft_sha256': digest(draft), 'time_utc': datetime.now(timezone.utc).isoformat()})
        print(checker, 'exit code:', result.returncode)
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        if result.returncode:
            raise SystemExit(result.returncode)
    text = draft.read_text(encoding='utf-8')
    heading, body = text.split('\n', 1)
    assert heading.startswith('# ')
    words = re.findall(r"[A-Za-z0-9]+(?:['’\-][A-Za-z0-9]+)*", body)
    count = {'draft': str(draft), 'sha256': digest(draft), 'excluded_initial_heading': heading,
             'body_words': len(words), 'whitespace_words': len(body.split()),
             'method': 'ASCII letters/digits with internal apostrophes or hyphens counted as one word; initial heading excluded',
             'within_350_450': 350 <= len(words) <= 450}
    write_json(out / 'word-count.json', count)
    print(json.dumps(count, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
