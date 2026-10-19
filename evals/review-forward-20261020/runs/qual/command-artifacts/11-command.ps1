$runDir = '<experiment>\runs\qual'
@'
from pathlib import Path
import json
import hashlib
import platform
import fitz
root = Path(__file__).resolve().parents[1]
review = root / 'edu_output' / 'review' / 'submission-review'
source = Path(r'<experiment>\inputs-final\qual_silence.pdf')
output = review / 'qual_silence_审稿标注版.pdf'
annotations = []
with fitz.open(output) as doc:
    for i, page in enumerate(doc):
        page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5), annots=True).save(review / 'previews' / f'annotated-page-{i+1}.png')
        annotations.extend({'page': i+1, 'xref': a.xref, 'type': a.type, 'info': a.info,
                            'color': a.colors, 'opacity': a.opacity,
                            'vertices': a.vertices} for a in (page.annots() or []))
    result = {'pdf_opened': True, 'reader_engine': 'PyMuPDF', 'pymupdf_version': fitz.VersionBind,
              'python_version': platform.python_version(), 'pages': len(doc),
              'all_pages_rendered_with_annotations': True,
              'new_comments': len([a for a in annotations if a['info']['title'] == 'AI 模拟审稿']),
              'existing_author_notes': len([a for a in annotations if a['info']['title'] == 'Original Author']),
              'source_sha256_after': hashlib.sha256(source.read_bytes()).hexdigest(),
              'output_sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
              'interactive_popup_visual_check': 'Not established by engine rendering; recorded separately from structural validation.'}
assert result['source_sha256_after'] == '1e9a81033e49dff50247f8435bb07f924588f3714b65ceae08cfed1aa94aebe6'
assert result['new_comments'] == 3 and result['existing_author_notes'] == 1
(review / 'native-annotations-readback.json').write_text(json.dumps(annotations, ensure_ascii=False, indent=2), encoding='utf-8')
(review / 'render-open-validation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
for a in annotations:
    print(json.dumps({'page': a['page'], 'author': a['info']['title'], 'comment': a['info']['content']}, ensure_ascii=False))
'@ | Set-Content -LiteralPath (Join-Path $runDir 'executed-helpers\render-validate-v1.py') -Encoding utf8
python -X utf8 (Join-Path $runDir 'executed-helpers\render-validate-v1.py')