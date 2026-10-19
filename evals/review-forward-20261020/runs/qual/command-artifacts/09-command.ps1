$runDir = '<experiment>\runs\qual'
@'
from pathlib import Path
import json
import fitz
root = Path(__file__).resolve().parents[1]
review = root / 'edu_output' / 'review' / 'submission-review'
plan = json.loads((review / 'annotations-v1.json').read_text(encoding='utf-8'))
plan['annotations'][1]['comment'] = plan['annotations'][1]['comment'].replace('These are reporting details to verify from the actual study records, not a requirement to add frequency counts, statistical tests or a particular coding-agreement metric.', 'Verify these reporting details from the actual study records; their absence from the excerpt does not establish that these analytic procedures were omitted.')
plan['annotations'][2]['comment'] = plan['annotations'][2]['comment'].replace(' This is an internal evidence-to-conclusion problem, not a consequence of lacking statistical tests.', '')
(review / 'annotations-v2.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding='utf-8')
(review / 'annotation-plan-changes.md').write_text('# Annotation plan revision\n\nv1 to v2: removed unnecessary contrasts with quantitative testing and retained the substantive qualitative evidence-to-conclusion concerns. No anchors or categories changed.\n', encoding='utf-8')
source = Path(r'<experiment>\inputs-final\qual_silence.pdf')
with fitz.open(source) as doc:
    existing = [{'page': i+1, 'xref': a.xref, 'type': a.type, 'info': a.info} for i,p in enumerate(doc) for a in (p.annots() or [])]
(review / 'source-existing-annotations.json').write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'annotation_plan': 'annotations-v2.json', 'existing_source_annotations': existing}, ensure_ascii=False, indent=2))
'@ | Set-Content -LiteralPath (Join-Path $runDir 'executed-helpers\revise-plan-v2.py') -Encoding utf8
python -X utf8 (Join-Path $runDir 'executed-helpers\revise-plan-v2.py')