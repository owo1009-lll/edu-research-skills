"""Run the supplied local checks and retain UTF-8 outputs in this task directory."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json
import re
import subprocess
import sys

OUT = Path(__file__).resolve().parent
SKILL = Path('C:/Users/Administrator/Downloads/edu-writing-snapshot-p01-20261018/skills/edu-writing')
SOURCE = Path('C:/Users/Administrator/Downloads/edu-research-skills-work/evals/writing-20261018/inputs/H2-materials.md')
stage = sys.argv[1]
if stage not in ('first', 'final'):
    raise SystemExit('Expected first or final')
draft = OUT / (stage + '.md')
checks = {
    'voice': [str(SKILL / 'scripts/check_voice.py'), '--draft', str(draft), '--source', str(SOURCE)],
    'prose': [str(SKILL / 'scripts/check_prose.py'), '--draft', str(draft)],
    'consistency': [str(SKILL / 'scripts/check_consistency.py'), '--draft', str(draft), '--term-group', 'food_security=food insecurity|low food security|low or very low food security', '--term-group', 'accounts=written accounts|written statements|interviews'],
}

def run(item):
    name, arguments = item
    command = [sys.executable, '-X', 'utf8', *arguments]
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', cwd=OUT)
    output = result.stdout
    if result.stderr:
        output += '\nSTDERR\n' + result.stderr
    destination = OUT / f'{stage}_{name}.txt'
    destination.write_text(output, encoding='utf-8')
    return name, {'command': command, 'exit_code': result.returncode, 'output': destination.name}, output

report = {}
with ThreadPoolExecutor(max_workers=3) as pool:
    for name, metadata, output in pool.map(run, checks.items()):
        report[name] = metadata
        print(f'[{stage}: {name}; exit {metadata["exit_code"]}]\n{output}')

text = draft.read_text(encoding='utf-8')
body = text.split('## Discussion\n', 1)[1].split('## References', 1)[0]
body = re.sub(r'^#+ .*$', '', body, flags=re.MULTILINE).strip()
count = len(body.split())
lexical = len(re.findall(r"\b\w+(?:[-’']\w+)*\b", body))
report['word_count'] = {'discussion_and_conclusion_whitespace': count, 'lexical': lexical, 'target': [650, 800], 'within_range': 650 <= count <= 800}
(OUT / f'{stage}_checks.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report['word_count'], ensure_ascii=False))
if any(item['exit_code'] for key, item in report.items() if key != 'word_count') or not report['word_count']['within_range']:
    raise SystemExit(1)
