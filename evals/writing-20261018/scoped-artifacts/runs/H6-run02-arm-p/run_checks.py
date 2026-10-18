from pathlib import Path
import json
import subprocess
import sys

out = Path(__file__).resolve().parent
skill = Path('C:/Users/Administrator/Downloads/edu-writing-snapshot-p01-20261018/skills/edu-writing')
source = Path('C:/Users/Administrator/Downloads/edu-research-skills-work/evals/writing-20261018/inputs/H6-materials.md')
stage = sys.argv[1]
if stage not in ('first', 'final'):
    raise SystemExit('Use first or final')
draft = out / (stage + '.md')
commands = {
    'voice': [sys.executable, '-X', 'utf8', str(skill / 'scripts/check_voice.py'), '--draft', str(draft), '--source', str(source)],
    'prose': [sys.executable, '-X', 'utf8', str(skill / 'scripts/check_prose.py'), '--draft', str(draft)],
    'consistency': [sys.executable, '-X', 'utf8', str(skill / 'scripts/check_consistency.py'), '--draft', str(draft), '--term-group', 'confidence=confidence in learning difficult physics with effort|growth mindset'],
}
records = []
for name, command in commands.items():
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', errors='strict')
    output_file = out / (stage + '_' + name + '.txt')
    output_file.write_text(result.stdout + ('\nSTDERR:\n' + result.stderr if result.stderr else ''), encoding='utf-8')
    records.append({'check': name, 'command': command, 'exit_code': result.returncode, 'output': output_file.name})
    print(name + ': exit ' + str(result.returncode) + ', ' + output_file.name)
text = draft.read_text(encoding='utf-8')
main = text.split('## References')[0]
sections = {}
for heading in ('Introduction', 'Discussion', 'Conclusion'):
    part = main.split('## ' + heading + '\n', 1)[1].split('\n## ', 1)[0]
    sections[heading] = len(part.split())
counts = {'method': 'Whitespace-delimited tokens; section headings and references excluded.', 'sections': sections, 'section_prose_total': sum(sections.values()), 'including_exercise_label': sum(sections.values()) + len(main.split('## Introduction')[0].split())}
(out / (stage + '_check_summary.json')).write_text(json.dumps({'checks': records, 'word_counts': counts}, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps(counts, ensure_ascii=False))
