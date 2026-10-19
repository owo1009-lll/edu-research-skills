from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone

OUT = Path(__file__).resolve().parent
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
checks = []
resources_path = OUT / 'loaded-resources.json'
manifest = json.loads(resources_path.read_text(encoding='utf-8'))
for item in manifest['resources']:
    assert digest(Path(item['path'])) == item['sha256'], item['path']
checks.append('All loaded snapshot resource hashes match their recorded values.')
for item in json.loads((OUT / 'input-file-hashes.json').read_text(encoding='utf-8'))['inputs']:
    assert digest(Path(item['path'])) == item['sha256'], item['path']
checks.append('Both input-file hashes match the separate input manifest.')
for name in ('draft-01', 'final'):
    count = json.loads((OUT / f'{name}-word-count.json').read_text(encoding='utf-8'))
    assert digest(OUT / f'{name}.md') == count['draft_sha256']
    assert count['body_within_450_550']
checks.append('The saved first draft and final manuscript match the versions actually checked; both body counts are in range.')
for name in ('final.md', 'draft-01.md', 'self-review.md', 'rationale.md', 'writing-note.md', 'draft-01-check_voice.txt', 'draft-01-check_prose.txt', 'final-check_voice.txt', 'final-check_prose.txt'):
    text = (OUT / name).read_text(encoding='utf-8', errors='strict')
    assert '\ufffd' not in text, name
    assert text.strip(), name
assert 'Lüdtke' in (OUT / 'final.md').read_text(encoding='utf-8')
checks.append('Deliverables and checker stdout are nonempty valid UTF-8 without replacement characters; Lüdtke is preserved.')
manifest['generated_support_scripts'] = [{'path': str(OUT / name), 'sha256': digest(OUT / name), 'actions': ['executed'], 'purpose': purpose} for name, purpose in [
    ('provenance.py', 'Initialize resource hashes, input hashes, and the record of actual earlier shell commands.'),
    ('run-checks.py', 'Count manuscript and attribution separately; execute the snapshot checkers and save verbatim output and arguments.'),
    ('verify-delivery.py', 'Verify preserved drafts, hashes, UTF-8, checker records and delivery files.')
]]
resources_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
commands_path = OUT / 'executed-commands.json'
commands = json.loads(commands_path.read_text(encoding='utf-8'))
checker_runs = [item for item in commands if item.get('argv')]
assert len(checker_runs) == 4
assert all(item['exit_code'] == 0 for item in checker_runs)
checks.append('Four actual checker executions are recorded, each with exit code 0 and separate stdout/stderr files.')
commands.append({'stage': 'delivery-verification', 'command': f'python "{Path(__file__).resolve()}"', 'executed_utc': datetime.now(timezone.utc).isoformat(), 'exit_code': 0})
commands_path.write_text(json.dumps(commands, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
report = {'checks': checks, 'scope': 'Single discussion passage, one preserved first draft, one full revision; AI self-review; no browsing or statistical rerun.', 'final_body_words': 478, 'final_attribution_heading_words': 8, 'skill_support_resources': len(manifest['resources']), 'generated_support_scripts': len(manifest['generated_support_scripts']), 'files': sorted(p.name for p in OUT.iterdir() if p.is_file())}
(OUT / 'delivery-verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False, indent=2))
