from pathlib import Path
import fitz
import json
import sys

source = Path(sys.argv[1])
outdir = Path(sys.argv[2])
outdir.mkdir(parents=True, exist_ok=True)
records = []
with fitz.open(source) as doc:
    for index, page in enumerate(doc):
        image = outdir / f'page-{index+1}.png'
        page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5), annots=True).save(image)
        annotations = []
        for annotation in page.annots() or []:
            annotations.append({'xref': annotation.xref, 'type': annotation.type, 'info': annotation.info, 'colors': annotation.colors, 'vertices': annotation.vertices})
        records.append({'page': index+1, 'image': str(image), 'text': page.get_text(), 'annotations': annotations})
    summary = {'reader': 'PyMuPDF', 'version': fitz.VersionBind, 'source': str(source), 'opened_successfully': True, 'pages': len(doc), 'records': records}
(outdir / 'opening-and-rendering.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'opened': str(source), 'pages': len(records), 'render_directory': str(outdir)}, ensure_ascii=False))
