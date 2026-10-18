"""Run only the supplied writing checks and save their exact UTF-8 output."""
from pathlib import Path
import json
import re
import subprocess
import sys

root = Path(__file__).resolve().parent
skill = Path('C:/Users/Administrator/Downloads/edu-writing-snapshot-p01-20261018/skills/edu-writing')
source = Path('C:/Users/Administrator/Downloads/edu-research-skills-work/evals/writing-20261018/inputs/H3-materials.md')
stage = sys.argv[1]
if stage not in {'first', 'final'}:
    raise SystemExit('stage must be first or final')
draft = root / (stage + '.md')
records = []
for check in ('voice', 'prose'):
    command = [sys.executable, '-X', 'utf8', str(skill / 'scripts' / ('check_' + check + '.py')), '--draft', str(draft)]
    if check == 'voice':
        command += ['--source', str(source)]
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', errors='strict')
    output = root / (stage + '_' + check + '.txt')
    output.write_text(result.stdout + ('\nSTDERR:\n' + result.stderr if result.stderr else ''), encoding='utf-8')
    records.append({'check': check, 'command': command, 'exit_code': result.returncode, 'output': str(output)})
    if result.returncode:
        raise SystemExit(result.returncode)
body = draft.read_text(encoding='utf-8').split('# 发现与讨论', 1)[1].strip()
report = {
    'stage': stage,
    'body_han_chars': len(re.findall(r'[一-鿿]', body)),
    'body_nonwhitespace_chars': len(re.sub(r'\s', '', body)),
    'body_paragraphs': len([p for p in body.split('\n\n') if p.strip()]),
    'checks': records,
}
(root / (stage + '_checks.json')).write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False, indent=2))
