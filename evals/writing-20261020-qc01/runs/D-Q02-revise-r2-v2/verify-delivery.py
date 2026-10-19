"""Verify the saved delivery and its provenance without changing manuscript text."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

resources_path = root / 'loaded-resources.json'
resources = json.loads(resources_path.read_text(encoding='utf-8'))
for row in resources['resources']:
    assert sha(Path(row['path'])) == row['sha256'], row['path']
resources['resources'].append({
    'path': str(Path(__file__).resolve()), 'sha256': sha(Path(__file__)),
    'actions': ['executed'], 'role': 'run-local final delivery verification helper',
})
write_json(resources_path, resources)
inputs = json.loads((root / 'input-hashes.json').read_text(encoding='utf-8'))
for row in inputs['inputs']:
    assert sha(Path(row['path'])) == row['sha256'], row['path']
assert sha(root / 'draft-1.md') == '3a51e9251f67bb1f176c9e2a2b792df70c4559874f13d6a347f53209779425a5'
assert (root / 'final.md').read_bytes() == (root / 'draft-2.md').read_bytes()
counts = json.loads((root / 'checks/draft-2-word-count.json').read_text(encoding='utf-8'))
assert counts['body_words'] == 153 and counts['body_paragraphs'] == 1
assert counts['attribution_heading_words'] == 8 and counts['within_140_170_words']
required = ['draft-1.md', 'draft-2.md', 'self-review.md', 'final.md', 'rationale.md',
            'changes-and-source-checks.md', 'loaded-resources.json', 'input-hashes.json',
            'executed-commands.jsonl', 'execution-record.md']
for name in required:
    content = (root / name).read_text(encoding='utf-8')
    assert '\ufffd' not in content, name
record = {
    'stage': 'delivery-verification', 'finished_utc': datetime.now(timezone.utc).isoformat(),
    'argv': [sys.executable, str(Path(__file__).resolve())],
    'command_line': subprocess.list2cmdline([sys.executable, str(Path(__file__).resolve())]),
    'returncode': 0, 'result': 'All delivery assertions passed',
}
with (root / 'executed-commands.jsonl').open('a', encoding='utf-8') as log:
    log.write(json.dumps(record, ensure_ascii=False) + '\n')
report = {'status': 'passed', 'body_words': 153, 'attribution_heading_words': 8,
          'body_paragraphs': 1, 'final_equals_checked_draft_2': True,
          'first_draft_unchanged': True, 'input_and_resource_hashes_verified': True,
          'required_artifacts': required, 'final_sha256': sha(root / 'final.md')}
write_json(root / 'delivery-validation.json', report)
print(json.dumps(report, ensure_ascii=False, indent=2))
