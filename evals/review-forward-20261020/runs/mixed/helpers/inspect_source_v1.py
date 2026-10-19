from pathlib import Path
from zipfile import ZipFile
from lxml import etree as ET
import json
base = Path.cwd()
out = base / 'edu_output/review/mixed-review'
ns = {'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
with ZipFile(base/'mixed_feedback.docx') as z:
    names = z.namelist()
    root = ET.fromstring(z.read('word/document.xml'))
    info = {'parts': names, 'existing_comments': [], 'tracked_changes': [], 'media': []}
    if 'word/comments.xml' in names:
        comments = ET.fromstring(z.read('word/comments.xml'))
        for c in comments:
            info['existing_comments'].append({'id':c.get('{'+ns['w']+'}id'), 'author':c.get('{'+ns['w']+'}author'), 'text':''.join(c.itertext())})
    for node in root.xpath('//w:ins | //w:del', namespaces=ns):
        info['tracked_changes'].append(ET.tostring(node, encoding='unicode'))
    for name in names:
        if name.startswith('word/media/'):
            target = out/Path(name).name
            target.write_bytes(z.read(name))
            info['media'].append(str(target))
(out/'source-object-inspection.json').write_text(json.dumps(info,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(info,ensure_ascii=False,indent=2))
