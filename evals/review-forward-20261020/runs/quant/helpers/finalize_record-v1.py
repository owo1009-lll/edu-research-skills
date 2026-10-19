from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import sys

root = Path(__file__).resolve().parents[1]
source_root = root.parents[1]
frozen = source_root / 'snapshot' / 'skills'
paths = [
    ('frozen skill instructions', frozen / 'edu-review' / 'SKILL.md'),
    ('frozen review criteria', frozen / 'edu-review' / 'references' / 'review-criteria.md'),
    ('frozen annotation instructions', frozen / 'edu-review' / 'references' / 'annotations.md'),
    ('frozen integrity instructions', frozen / 'edu-shared' / 'references' / 'integrity.md'),
    ('frozen annotation helper read and executed', frozen / 'edu-review' / 'scripts' / 'annotate_manuscript.py'),
    ('request', source_root / 'inputs-final' / 'request.md'),
    ('raw source manuscript', source_root / 'inputs-final' / 'quant_retrieval.pdf'),
]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

resources = [{'role': role, 'path': str(path), 'sha256': sha(path)} for role, path in paths]
assert resources[-1]['sha256'] == 'e34001bd995d49249190adc39f60b2fa6164fb27bbdc2f8b7d1e733ea16624ce'
assert sha(root / 'helpers' / 'annotate_manuscript-frozen.py') == resources[4]['sha256']
validation = json.loads((root / 'validation-report.json').read_text(encoding='utf-8'))
commands = json.loads((root / 'command-log.json').read_text(encoding='utf-8'))
commands.append({
    'command': (root / 'final-command.txt').read_text(encoding='utf-8').strip(),
    'outcome': 'success',
    'exit_code': 0,
    'details': 'Resource and artifact hashes computed; source hash unchanged; frozen helper archive matches executed source; final response and validation record present; run-record.json written.',
})
artifacts = []
for path in sorted(root.rglob('*')):
    if path.is_file() and path.name != 'run-record.json':
        artifacts.append({'path': str(path.relative_to(root)), 'sha256': sha(path), 'bytes': path.stat().st_size})
record = {
    'schema_version': 1,
    'completed_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
    'task': 'Independent forward test of the frozen edu-review skill on the assigned quantitative excerpt.',
    'scope': 'Only assigned raw manuscript, request, frozen resources listed below, and own outputs were read; no outside research or sibling-case access.',
    'resources_read_or_executed': resources,
    'plans_in_order': ['plan-v1.md', 'plan-v2.md', 'edu_output/review/retrieval/annotations-v1.json'],
    'executed_helpers': [
        {'source': str(frozen / 'edu-review' / 'scripts' / 'annotate_manuscript.py'), 'archived_exact_version': 'helpers/annotate_manuscript-frozen.py', 'sha256': resources[4]['sha256']},
        {'path': 'helpers/render_pdf-v1.py', 'sha256': sha(root / 'helpers' / 'render_pdf-v1.py')},
        {'path': 'helpers/build_plan-v1.py', 'sha256': sha(root / 'helpers' / 'build_plan-v1.py')},
        {'path': 'helpers/finalize_record-v1.py', 'sha256': sha(root / 'helpers' / 'finalize_record-v1.py')},
    ],
    'actual_commands_and_outcomes': commands,
    'validation': validation,
    'user_facing_deliverables': ['edu_output/review/retrieval/quant_retrieval_审稿标注版.pdf'],
    'exact_final_user_facing_response': {'path': 'final-response.md', 'sha256': sha(root / 'final-response.md'), 'text': (root / 'final-response.md').read_text(encoding='utf-8')},
    'artifacts': artifacts,
    'limitations': ['Review restricted to this excerpt.', 'No data/code reanalysis or literature verification.', 'PDF opened and all page renders visually inspected, but GUI comment popups were not tested interactively.'],
}
(root / 'run-record.json').write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'run_record': str(root / 'run-record.json'), 'resources_hashed': len(resources), 'artifacts_hashed': len(artifacts), 'deliverable': record['user_facing_deliverables'][0], 'success': True}, ensure_ascii=False))

