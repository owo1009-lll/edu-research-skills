from pathlib import Path
import json
import fitz
base=Path.cwd()/'edu_output/review/mixed-review'
results=[]
for filename in ['final-body-preview.pdf','final-markup-preview.pdf']:
    path=base/filename
    with fitz.open(path) as doc:
        pages=[]
        for i,p in enumerate(doc):
            png=base/(path.stem+f'-page-{i+1}.png')
            p.get_pixmap(matrix=fitz.Matrix(1.6,1.6),alpha=False).save(png)
            pages.append({'page':i+1,'image':str(png),'text':p.get_text()})
        results.append({'file':filename,'page_count':len(doc),'pages':pages})
(base/'render-inspection-v3.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps([{'file':r['file'],'page_count':r['page_count'],'pages':[p['image'] for p in r['pages']]} for r in results],ensure_ascii=False,indent=2))

