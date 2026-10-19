"""Preserved helper v1: record completed commands and deliver the accepted draft."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import sys

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent.parent
SKILLS = ROOT / 'variants' / 'v2' / 'skills'
INPUTS = ROOT / 'inputs' / 'D-L02'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(path, obj):
    assert not path.exists(), str(path)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def read_cmd(path, utf8=True):
    return "Get-Content -LiteralPath '" + str(path) + "'" + (' -Encoding UTF8' if utf8 else '') + ' -Raw'

commands = []
def record(command, purpose):
    commands.append({'sequence': len(commands) + 1, 'shell': 'powershell', 'command': command, 'purpose': purpose})

skill = SKILLS / 'edu-writing' / 'SKILL.md'
for utf8 in [False, True]:
    record(read_cmd(skill, utf8), 'Read assigned skill' + (' with corrected UTF-8' if utf8 else ''))
    record(read_cmd(INPUTS / 'new-request.md', utf8) + '; ' + read_cmd(INPUTS / 'source-pack.md', utf8),
           'Read assigned task inputs' + (' with corrected UTF-8' if utf8 else ''))
for relative in ['edu-writing/references/argument.md', 'edu-writing/references/voice-en.md',
                 'edu-writing/references/qualitative-narrative.md', 'edu-shared/references/integrity.md',
                 'edu-writing/scripts/check_voice.py', 'edu-writing/scripts/check_prose.py']:
    record(read_cmd(SKILLS / relative), 'Read assigned support resource; combined tool output was truncated')
for relative in ['edu-writing/references/voice-en.md', 'edu-writing/references/qualitative-narrative.md',
                 'edu-shared/references/integrity.md']:
    record(read_cmd(SKILLS / relative), 'Reread support resource after combined-output truncation')
record("Select-String -Path '" + str(SKILLS / 'edu-writing/scripts/check_voice.py') + "','" +
       str(SKILLS / 'edu-writing/scripts/check_prose.py') +
       "' -Pattern '^import |^from |read_text|open\\(' -Encoding UTF8", 'Inspect checker imports and reads')
for relative in ['edu-writing/references/methods/cases-develop-explanations.md', 'edu-writing/references/prose-en.md']:
    record(read_cmd(SKILLS / relative), 'Read applicable qualitative and English prose guidance')
for stage in ['draft-01', 'draft-02']:
    record("python '" + str(BASE / 'run_checks_v1.py') + "' --draft " + stage + '.md --stage ' + stage,
           'Run preserved helper; actual child commands and results recorded in executed-commands.jsonl')
record("python '" + str(Path(__file__).resolve()) + "'", 'Finalize accepted second draft and command record')
save(BASE / 'shell-commands.json', {'note': 'Exact shell command text from tool calls; early read commands recorded from the visible call history. No drafting stage was reconstructed. Within independent batches, listed order is launch order, not a claim about completion order.', 'commands': commands})

source = BASE / 'draft-02.md'
target = BASE / 'final.md'
assert not target.exists()
shutil.copyfile(source, target)
assert source.read_bytes() == target.read_bytes()

manifest = json.loads((BASE / 'loaded-resources.json').read_text(encoding='utf-8'))
manifest.append({'path': str(Path(__file__).resolve()), 'sha256': sha(Path(__file__).resolve()),
                 'operations': ['created', 'executed'], 'role': 'preserved finalization helper'})
(BASE / 'loaded-resources.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
with (BASE / 'executed-commands.jsonl').open('a', encoding='utf-8') as stream:
    stream.write(json.dumps({'kind': 'helper invocation', 'argv': [sys.executable, str(Path(__file__).resolve())],
                            'helper_sha256': sha(Path(__file__).resolve()), 'time_utc': datetime.now(timezone.utc).isoformat(),
                            'operation': 'shutil.copyfile', 'source': str(source), 'target': str(target),
                            'copied_sha256': sha(target)}, ensure_ascii=False) + '\n')

count = json.loads((BASE / 'checks/draft-02/word-count.json').read_text(encoding='utf-8'))
count['draft'] = str(target)
count['copied_from'] = str(source)
count['exact_copy_verified'] = True
save(BASE / 'final-word-count.json', count)

required = ['draft-01.md', 'draft-02.md', 'self-review.md', 'final.md', 'rationale.md',
            'editorial-source-notes.md', 'loaded-resources.json', 'input-hashes.json',
            'executed-commands.jsonl', 'shell-commands.json', 'run_checks_v1.py', 'finalize_v1.py',
            'final-word-count.json']
for phase in ['draft-01', 'draft-02']:
    for name in ['check_voice.stdout.txt', 'check_voice.stderr.txt', 'check_prose.stdout.txt', 'check_prose.stderr.txt', 'word-count.json']:
        required.append('checks/' + phase + '/' + name)
assert all((BASE / name).is_file() for name in required)
save(BASE / 'artifact-manifest.json', [{'path': str(BASE / name), 'sha256': sha(BASE / name)} for name in required])
print(json.dumps({'final': str(target), 'body_words': count['body_words'], 'exact_copy_verified': True,
                  'required_files_verified': len(required), 'resource_entries': len(manifest)}, indent=2))
