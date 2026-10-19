from pathlib import Path
import json
import fitz
base=Path.cwd()/'edu_output/review/mixed-review'
results=[]
for filename in ['source-preview.pdf','annotated-body-preview.pdf','annotated-markup-preview.pdf']:
    path=base/filename
    if not path.exists():
        results.append({'file':filename,'available':False})
        continue
    with fitz.open(path) as doc:
        pages=[]
        for i,p in enumerate(doc):
            png=base/(path.stem+f'-page-{i+1}.png')
            p.get_pixmap(matrix=fitz.Matrix(1.4,1.4),alpha=False).save(png)
            pages.append({'page':i+1,'image':str(png),'text':p.get_text()})
        results.append({'file':filename,'available':True,'page_count':len(doc),'pages':pages})
(base/'render-inspection.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(results,ensure_ascii=False,indent=2))
