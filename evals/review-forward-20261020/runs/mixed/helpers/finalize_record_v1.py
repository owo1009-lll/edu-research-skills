from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

base = Path.cwd()
frozen = Path(r'<experiment>\snapshot\skills')
inputs = Path(r'<experiment>\inputs-final')
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
resources = [
    ('edu-review/SKILL.md', 'f42fecfdbb027a0e75f6fc0187b46ea7a07903443a88ddfd0b513750139c6f95', 'read'),
    ('edu-review/references/review-criteria.md', 'b985a1d6b3f5a45f72ff0cd3803137bbdfa92e8bc0647f73c80cd151ea84929f', 'read'),
    ('edu-review/references/annotations.md', '1a4118a70f93fd85b0201413b00040f7334b098f6dbbe17fb4d90c4c6315162a', 'read'),
    ('edu-shared/references/integrity.md', 'e1ec232adb87b32484c1d9bd49823acc41f813432bd40088b0c4865b9e18f8d6', 'read'),
    ('edu-review/scripts/annotate_manuscript.py', 'f5d3e3c66e74aa3dfc0986fd311813b15a3861e504916ac070d3c0af62eed65c', 'read; exact preserved copy executed for inventory, apply and verify'),
    ('edu-writing/scripts/render_word.ps1', 'e21370f68e1c92b2b2f07d28504942f884a9b6d81b9055e71cc21c1e7aebd8eb', 'read; exact preserved copy executed for Word opening and PDF rendering'),
]
frozen_records = []
for relative, expected, usage in resources:
    path = frozen/relative
    actual = sha(path)
    assert actual == expected, (relative, actual)
    frozen_records.append({'path':str(path),'sha256':actual,'usage':usage})
input_records = []
for name, expected in [
    ('mixed_feedback.docx','97b46f82ed7ce34a42b9bc573867b4ad98b1183c5e7791fbfff737a652c4b696'),
    ('request.md','6725d3cb74fc268488a1d9a9e7e57d494e6c7b4419c07c68a3e60b65816d7110')
]:
    source,copy = inputs/name, base/name
    assert sha(source)==sha(copy)==expected
    input_records.append({'source_path':str(source),'working_copy':str(copy),'sha256':expected,'source_unchanged':True})
output = base/'edu_output/review/mixed-review/final/mixed_feedback_审稿标注版.docx'
assert sha(output)=='730a4cf36a98269906749dc838bfcbb609c8d9d00c7e09a4804ef36985789323'
receipt=base/'final-response.md'
assert receipt.exists()
history=json.loads((base/'command-history.json').read_text(encoding='utf-8'))
assembly_command = r'python -X utf8 .\helpers\finalize_record_v1.py'
report={
    'schema_version':1,
    'task':'Independent forward use of frozen edu-review skill on the supplied mixed_feedback manuscript',
    'run_directory':str(base),
    'completed_utc':datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),
    'initial_plan':'plan-v1.md',
    'subsequent_plans':['plan-v2.md','plan-v3.md'],
    'annotation_plans':['edu_output/review/mixed-review/annotations-v1.json','edu_output/review/mixed-review/annotations-v2.json'],
    'source_and_request':input_records,
    'frozen_resources_read_or_executed':frozen_records,
    'command_history':history,
    'final_record_assembly':{'cmd':assembly_command,'workdir':str(base),'exit_code':0,'outcome':'All input/resource/output hash assertions passed; run-record.json written.'},
    'user_facing_deliverables':[{'path':str(output),'sha256':sha(output),'type':'Annotated DOCX with five native English comments and highlights'}],
    'exact_final_response':{'path':str(receipt),'sha256':sha(receipt),'text':receipt.read_text(encoding='utf-8')},
    'internal_artifacts_not_deliverables':True,
    'validation':{
        'structural':'Frozen verifier passed for final DOCX; original text, table, figure, formatting except planned highlights, original comment and two tracked revisions preserved.',
        'application':'Word 16.0 opened first annotated copy and inspected exact native ranges/text; final deliverable opened in two fresh Word sessions and exported successfully.',
        'visual':'All two final body pages and all two final markup pages inspected as images; all complete final comments and original tracked changes visible. First-preview C5 clipping fixed by shortening comments in v2.',
        'research_limit':'Only supplied synthetic excerpt reviewed. No raw data, interview transcripts, literature section, journal template, or external research available/used.',
        'nonblocking_incidents':['Initial command used a nonexistent working directory; rerun created directory.', 'Initial default PowerShell decoding produced mojibake; reread with UTF-8.', 'First combined Word inspection/export and live retry stalled; native inspection had completed. Only the identified run-owned Word process was stopped; shells interrupted. Fresh isolated frozen rendering succeeded.', 'MuPDF emitted a structure-tree warning for markup exports; pages and text were produced, and final visual inspection passed.']
    },
    'artifacts':[]
}
for path in sorted(base.rglob('*')):
    if path.is_file() and path.name!='run-record.json':
        report['artifacts'].append({'relative_path':str(path.relative_to(base)),'sha256':sha(path),'bytes':path.stat().st_size})
(base/'run-record.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'status':'complete','record':'run-record.json','frozen_resources':len(frozen_records),'comments':5,'deliverable':str(output),'sha256':sha(output),'validation':'structural, Word opening, and final page/comment visuals passed'},ensure_ascii=False,indent=2))

