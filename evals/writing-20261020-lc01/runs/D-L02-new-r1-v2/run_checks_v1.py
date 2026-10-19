"""Preserved v1: run assigned checkers and record actual inputs, outputs and hashes."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SEED = json.loads((ROOT / 'prerun-record-v1.json').read_text(encoding='utf-8'))

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def write_json(name, value):
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def record(value):
    value['recorded_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with (ROOT / 'executed-commands.jsonl').open('a', encoding='utf-8') as stream:
        stream.write(json.dumps(value, ensure_ascii=False) + '\n')

if len(sys.argv) != 3:
    raise SystemExit('usage: run_checks_v1.py <draft filename> <output prefix>')
draft = (ROOT / sys.argv[1]).resolve()
prefix = sys.argv[2]
if draft.parent != ROOT or not re.fullmatch(r'[a-z0-9-]+', prefix):
    raise SystemExit('All draft and output paths must remain in this run folder.')
record({'kind': 'helper invocation', 'argv': [sys.executable, str(Path(__file__).resolve()), *sys.argv[1:]], 'helper_sha256': digest(__file__)})

resources = []
for value in SEED['resources']:
    path = Path(value)
    usage = ['read']
    if path.name in ('check_voice.py', 'check_prose.py'):
        usage.append('executed')
    resources.append({'path': str(path), 'sha256': digest(path), 'usage': usage, 'origin': 'assigned v2 snapshot'})
resources.append({'path': str(Path(__file__).resolve()), 'sha256': digest(__file__), 'usage': ['executed'], 'origin': 'preserved local helper v1'})
write_json('loaded-resources.json', {'resources': resources, 'scope': 'Skill/support files actually read or executed; Python standard-library internals are not task support resources.'})
write_json('input-hashes.json', {'inputs': [{'path': path, 'sha256': digest(path)} for path in SEED['inputs']]})

body = draft.read_text(encoding='utf-8').split('\n', 1)[1].strip()
counts = {'draft': str(draft), 'sha256': digest(draft), 'excluded': 'Initial attribution heading only', 'whitespace_word_count': len(body.split()), 'lexical_word_count': len(re.findall(r"[A-Za-z0-9]+(?:['’.-][A-Za-z0-9]+)*", body)), 'whitespace_method': 'Split body on whitespace; internal hyphens count within one word.'}
counts['within_350_450_words'] = 350 <= counts['whitespace_word_count'] <= 450
write_json(prefix + '-word-count.json', counts)
print(json.dumps(counts, ensure_ascii=False, indent=2))

skill_dir = Path(SEED['resources'][0]).parent
environment = os.environ.copy()
environment['PYTHONIOENCODING'] = 'utf-8'
environment['PYTHONDONTWRITEBYTECODE'] = '1'
for checker in ('check_voice.py', 'check_prose.py'):
    args = [sys.executable, '-B', str(skill_dir / 'scripts' / checker), '--draft', str(draft)]
    if checker == 'check_voice.py':
        args += ['--source', SEED['inputs'][1]]
    stem = prefix + '-' + checker.removesuffix('.py')
    completed = subprocess.run(args, capture_output=True, env=environment, cwd=str(ROOT))
    (ROOT / (stem + '.stdout.txt')).write_bytes(completed.stdout)
    (ROOT / (stem + '.stderr.txt')).write_bytes(completed.stderr)
    result = {'kind': 'checker execution', 'argv': args, 'exit_code': completed.returncode, 'draft_sha256': digest(draft), 'script_sha256': digest(skill_dir / 'scripts' / checker), 'stdout': stem + '.stdout.txt', 'stderr': stem + '.stderr.txt'}
    record(result)
    write_json(stem + '.execution.json', result)
    print('\n' + checker + ' exit=' + str(completed.returncode))
    print(completed.stdout.decode('utf-8', errors='replace'))
    if completed.stderr:
        print(completed.stderr.decode('utf-8', errors='replace'))
    if completed.returncode:
        raise SystemExit(completed.returncode)
