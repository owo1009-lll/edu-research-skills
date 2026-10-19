from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone

OUT = Path(__file__).resolve().parent
BASE = OUT.parents[1]
SKILL = BASE / 'variants' / 'v1' / 'skills' / 'edu-writing'
SOURCE = BASE / 'inputs' / 'D-Q02' / 'source-pack.md'
draft = OUT / sys.argv[1]
if draft.parent.resolve() != OUT:
    raise ValueError('Draft must be in this output directory')
command_path = OUT / 'executed-commands.json'
commands = json.loads(command_path.read_text(encoding='utf-8'))
commands.append({'stage': 'checker-runner', 'command': f'python "{Path(__file__).resolve()}" {sys.argv[1]}', 'started_utc': datetime.now(timezone.utc).isoformat()})
text = draft.read_text(encoding='utf-8')
lines = text.splitlines()
if not lines or not lines[0].startswith('# '):
    raise ValueError('Expected one attribution heading at the top')
heading = lines[0][2:]
body = '\n'.join(lines[1:]).strip()
assert not any(line.startswith('#') for line in body.splitlines())
word_pattern = r"[^\W_]+(?:['’.,–-][^\W_]+)*"
count = lambda value: len(re.findall(word_pattern, value, re.UNICODE))
counts = {'file': draft.name, 'count_method': 'Unicode word tokens; internal apostrophes, decimals, hyphens, and en dashes remain within a token', 'manuscript_body_words': count(body), 'attribution_heading_words': count(heading), 'total_words': count(text), 'body_within_450_550': 450 <= count(body) <= 550, 'paragraphs': len(re.split(r'\n\s*\n', body)), 'draft_sha256': hashlib.sha256(draft.read_bytes()).hexdigest()}
count_path = OUT / f'{draft.stem}-word-count.json'
count_path.write_text(json.dumps(counts, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(counts, ensure_ascii=False))

manifest_path = OUT / 'loaded-resources.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
for name, extra in [('check_voice.py', ['--source', str(SOURCE)]), ('check_prose.py', [])]:
    script = SKILL / 'scripts' / name
    argv = [sys.executable, '-B', str(script), '--draft', str(draft), *extra]
    started = datetime.now(timezone.utc).isoformat()
    result = subprocess.run(argv, capture_output=True, encoding='utf-8', errors='strict')
    log = OUT / f'{draft.stem}-{script.stem}.txt'
    log.write_text(result.stdout, encoding='utf-8')
    (OUT / f'{draft.stem}-{script.stem}.stderr.txt').write_text(result.stderr, encoding='utf-8')
    commands.append({'stage': draft.stem, 'argv': argv, 'started_utc': started, 'exit_code': result.returncode, 'stdout_file': log.name, 'stderr_file': f'{draft.stem}-{script.stem}.stderr.txt'})
    for item in manifest['resources']:
        if Path(item['path']) == script and 'executed' not in item['actions']:
            item['actions'].append('executed')
    print(f'\n{name}: exit {result.returncode}\n{result.stdout}')
    if result.stderr:
        print(result.stderr)
command_path.write_text(json.dumps(commands, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
