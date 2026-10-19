from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import time

started = time.perf_counter()
root = Path(__file__).resolve().parents[1]
review = root / 'edu_output' / 'review' / 'submission-review'
snapshot = Path(r'<experiment>\snapshot\skills')
inputs = Path(r'<experiment>\inputs-final')
resources = [
    (snapshot / 'edu-review' / 'SKILL.md', 'frozen skill instructions', 'f42fecfdbb027a0e75f6fc0187b46ea7a07903443a88ddfd0b513750139c6f95'),
    (snapshot / 'edu-review' / 'references' / 'review-criteria.md', 'frozen supporting resource read', 'b985a1d6b3f5a45f72ff0cd3803137bbdfa92e8bc0647f73c80cd151ea84929f'),
    (snapshot / 'edu-review' / 'references' / 'annotations.md', 'frozen supporting resource read', '1a4118a70f93fd85b0201413b00040f7334b098f6dbbe17fb4d90c4c6315162a'),
    (snapshot / 'edu-shared' / 'references' / 'integrity.md', 'frozen supporting resource read', 'e1ec232adb87b32484c1d9bd49823acc41f813432bd40088b0c4865b9e18f8d6'),
    (snapshot / 'edu-review' / 'requirements.txt', 'frozen requirements read', '4bdb9b968b1e0fd3a0748b1ce9a3f72564f09a10c9a0113e0af99f72a3777342'),
    (snapshot / 'edu-review' / 'scripts' / 'annotate_manuscript.py', 'frozen helper read and executed; inventory directly, apply and verify from identical preserved copy', 'f5d3e3c66e74aa3dfc0986fd311813b15a3861e504916ac070d3c0af62eed65c'),
    (inputs / 'qual_silence.pdf', 'assigned raw manuscript read, never modified', '1e9a81033e49dff50247f8435bb07f924588f3714b65ceae08cfed1aa94aebe6'),
    (inputs / 'request.md', 'assigned request read', '6725d3cb74fc268488a1d9a9e7e57d494e6c7b4419c07c68a3e60b65816d7110')
]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

manifest = []
for path, role, expected in resources:
    actual = sha(path)
    assert actual == expected, str(path)
    manifest.append({'path': str(path), 'role': role, 'sha256': actual})
assert sha(root / 'executed-helpers' / 'annotate_manuscript-frozen.py') == resources[5][2]

commands = json.loads((root / 'command-transcript.json').read_text(encoding='utf-8'))
command_dir = root / 'command-artifacts'
command_dir.mkdir(exist_ok=True)
for entry in commands:
    number = entry['id']
    if 'command' in entry:
        (command_dir / f'{number:02d}-command.ps1').write_text(entry['command'], encoding='utf-8')
        (command_dir / f'{number:02d}-output.txt').write_text(entry['output'], encoding='utf-8')

output = review / 'qual_silence_审稿标注版.pdf'
final_response = root / 'final-response.md'
observations = json.loads((review / 'validation-observations.json').read_text(encoding='utf-8'))
assert output.is_file() and final_response.is_file()
assert len(json.loads((review / 'annotations-v2.json').read_text(encoding='utf-8'))['annotations']) == 3
completion = {'status': 'complete', 'user_deliverable': str(output),
              'final_response_receipt': str(final_response), 'run_record': str(root / 'run-record.json'),
              'source_sha256_unchanged': True, 'structural_verification': 'passed',
              'rendered_page_visual_inspection': 'both pages passed',
              'interactive_popup_visual_inspection': 'not performed'}
completion_text = json.dumps(completion, ensure_ascii=False, indent=2)
(root / 'finalization-result.json').write_text(completion_text + '\n', encoding='utf-8')
final_command = "python -X utf8 '<experiment>\\runs\\qual\\executed-helpers\\finalize-record-v1.py'"
self_entry = {'id': len(commands)+1, 'command': final_command, 'exit_code': 0,
              'output': completion_text, 'outcome': 'All finalization assertions passed; record and receipt written.',
              'wall_time_seconds_measured_inside_helper': time.perf_counter()-started}
commands.append(self_entry)
(command_dir / f"{self_entry['id']:02d}-command.ps1").write_text(final_command, encoding='utf-8')
(command_dir / f"{self_entry['id']:02d}-output.txt").write_text(completion_text + '\n', encoding='utf-8')
artifacts = [{'path': str(path.relative_to(root)), 'sha256': sha(path), 'bytes': path.stat().st_size}
             for path in sorted(root.rglob('*')) if path.is_file() and path.name != 'run-record.json']
record = {
    'schema_version': 1, 'case': 'qual', 'status': 'complete',
    'recorded_utc': datetime.now(timezone.utc).isoformat(),
    'scope': 'Independent forward execution of frozen edu-review skill; only assigned source/request, necessary frozen resources and own outputs read. No external research, repository edits, commits or third-party messages.',
    'initial_plan': 'plan-v1.md', 'workflow_plan_versions': ['plan-v1.md', 'plan-v2.md'],
    'annotation_plan_versions': ['edu_output/review/submission-review/annotations-v1.json', 'edu_output/review/submission-review/annotations-v2.json'],
    'frozen_resources_and_inputs': manifest,
    'commands_and_tool_openings': commands,
    'receipt_file_creation_tool': 'apply_patch',
    'receipt_files_created': ['final-response.md', 'command-transcript.json', 'edu_output/review/submission-review/validation-observations.json', 'executed-helpers/finalize-record-v1.py'],
    'user_facing_deliverables': [{'path': str(output), 'sha256': sha(output), 'description': 'Original PDF with three English native highlight comments; existing author note preserved.'}],
    'final_user_response': {'path': str(final_response), 'sha256': sha(final_response), 'text': final_response.read_text(encoding='utf-8')},
    'validation': observations,
    'artifact_manifest': artifacts,
    'self_hash_note': 'The run-record.json file is excluded from its own artifact hash manifest.'
}
(root / 'run-record.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
loaded = json.loads((root / 'run-record.json').read_text(encoding='utf-8'))
assert loaded['status'] == 'complete'
assert loaded['final_user_response']['text'] == final_response.read_text(encoding='utf-8')
print(completion_text)
