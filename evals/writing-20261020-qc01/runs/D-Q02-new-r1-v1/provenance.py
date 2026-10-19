from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone

OUT = Path(__file__).resolve().parent
BASE = OUT.parents[1]
SKILLS = BASE / 'variants' / 'v1' / 'skills'
resources = [
    ('edu-writing/SKILL.md', 'read'),
    ('edu-writing/references/argument.md', 'read'),
    ('edu-writing/references/voice-en.md', 'read'),
    ('edu-writing/references/framing-results.md', 'read'),
    ('edu-writing/references/quantitative-discussion.md', 'read'),
    ('edu-shared/references/integrity.md', 'read'),
    ('edu-writing/scripts/check_voice.py', 'read'),
    ('edu-writing/scripts/check_prose.py', 'read'),
]

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

manifest = {
    'scope': 'Only the specified v1 snapshot; the initial full check_prose.py tool response was truncated, and its first 95 lines were read in a separate call.',
    'resources': [{'path': str(SKILLS / rel), 'sha256': digest(SKILLS / rel), 'actions': [action]} for rel, action in resources],
}
(OUT / 'loaded-resources.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
inputs = [BASE / 'inputs' / 'D-Q02' / name for name in ('new-request.md', 'source-pack.md')]
(OUT / 'input-file-hashes.json').write_text(json.dumps({'inputs': [{'path': str(p), 'sha256': digest(p)} for p in inputs]}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# These commands were actually executed through exec_command before this file was created.
initial_order = [SKILLS / resources[0][0], *inputs, *[SKILLS / rel for rel, _ in resources[1:]]]
commands = []
for p in initial_order:
    command = f"Get-FileHash -LiteralPath '{p}' -Algorithm SHA256 | Select-Object Path, Hash | ConvertTo-Json -Compress\nGet-Content -LiteralPath '{p}' -Raw -Encoding UTF8"
    commands.append({'stage': 'resource-and-input-reading', 'shell': 'powershell', 'command': command, 'exit_code': 0})
commands.append({'stage': 'script-import-inspection', 'shell': 'powershell', 'command': f"Get-Content -LiteralPath '{SKILLS / 'edu-writing/scripts/check_prose.py'}' -Encoding UTF8 -TotalCount 95", 'exit_code': 0})
commands.append({'stage': 'provenance-initialization', 'command': f'python "{Path(__file__).resolve()}"', 'started_utc': datetime.now(timezone.utc).isoformat()})
(OUT / 'executed-commands.json').write_text(json.dumps(commands, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Wrote resource manifest, separate input hashes, and actual command record.')
