from pathlib import Path
import json
import re
import subprocess
import sys

out = Path(__file__).resolve().parent
snapshot = Path(r'@snapshot')
source = Path(r'@inputs\D-M01\source-pack.md')
draft = out / 'first-draft.md'
commands = [
    ('check-voice', [sys.executable, '-B', str(snapshot / 'skills/edu-writing/scripts/check_voice.py'), '--draft', str(draft), '--source', str(source)]),
    ('check-prose', [sys.executable, '-B', str(snapshot / 'skills/edu-writing/scripts/check_prose.py'), '--draft', str(draft)])
]
records = []
for name, command in commands:
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', errors='replace')
    (out / (name + '.txt')).write_text(result.stdout, encoding='utf-8')
    (out / (name + '.stderr.txt')).write_text(result.stderr, encoding='utf-8')
    records.append({'name': name, 'command': command, 'returncode': result.returncode, 'stdout': name + '.txt', 'stderr': name + '.stderr.txt'})
    print(name + ': exit ' + str(result.returncode))
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
body = re.sub(r'^# Discussion\s*', '', draft.read_text(encoding='utf-8'))
records.append({'draft_word_count_whitespace': len(body.split()), 'draft_paragraph_count': len(body.strip().split('\n\n'))})
(out / 'check-runs.json').write_text(json.dumps(records, indent=2), encoding='utf-8')
print(json.dumps(records[-1]))