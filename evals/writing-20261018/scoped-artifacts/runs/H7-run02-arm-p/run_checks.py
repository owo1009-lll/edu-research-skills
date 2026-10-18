"""Run the supplied writing checks without writing outside this task directory."""
from pathlib import Path
import json
import os
import re
import subprocess
import sys

out = Path(__file__).resolve().parent
scripts = Path('C:/Users/Administrator/Downloads/edu-writing-snapshot-p01-20261018/skills/edu-writing/scripts')
source = Path('C:/Users/Administrator/Downloads/edu-research-skills-work/evals/writing-20261018/inputs/H7-materials.md')
stage = sys.argv[1]
if stage not in ('first', 'final'):
    raise ValueError('Expected first or final')
draft = out / (stage + '.md')
env = dict(os.environ)
env['PYTHONDONTWRITEBYTECODE'] = '1'
env['PYTHONUTF8'] = '1'
checks = [
    ('voice', ['--source', str(source), '--lang', 'en']),
    ('prose', []),
    ('consistency', ['--lang', 'en', '--term-group', 'model=8A-Model|8A model|8-A Model',
                     '--term-group', 'grade=GPA|GPAs']),
]
records = []
for name, extra in checks:
    command = [sys.executable, '-X', 'utf8', str(scripts / ('check_' + name + '.py')), '--draft', str(draft), *extra]
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', env=env, cwd=out)
    output = out / (stage + '_' + name + '.txt')
    output.write_text(result.stdout + ('\nSTDERR:\n' + result.stderr if result.stderr else ''), encoding='utf-8')
    records.append({'check': name, 'command': command, 'returncode': result.returncode, 'output': output.name})
    print(name + ': returncode=' + str(result.returncode) + '; saved ' + output.name)

text = draft.read_text(encoding='utf-8')
body = text.split('## Discussion\n', 1)[1].split('## Reference\n', 1)[0]
discussion, conclusion = body.split('## Conclusion\n', 1)
count = lambda value: len(re.findall(r'\S+', value.strip()))
body_count = count(discussion) + count(conclusion)
attribution = text.split('## Discussion\n', 1)[0]
word_counts = {'method': 'Whitespace-delimited tokens; headings and reference excluded; attribution also reported separately.',
               'discussion': count(discussion), 'conclusion': count(conclusion), 'total_body': body_count,
               'attribution': count(attribution), 'body_plus_attribution': body_count + count(attribution),
               'within_650_800': 650 <= body_count <= 800}
report = {'stage': stage, 'checks': records, 'word_counts': word_counts}
(out / (stage + '_checks.json')).write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(word_counts, ensure_ascii=False, indent=2))
if any(record['returncode'] != 0 for record in records):
    raise SystemExit(1)
if not word_counts['within_650_800']:
    raise SystemExit(2)
