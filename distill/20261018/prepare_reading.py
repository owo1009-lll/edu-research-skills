"""Create stable local paragraph locators and a public acquisition-only digest."""
import argparse
import hashlib
import json
from pathlib import Path
from bs4 import BeautifulSoup, Tag
import fitz


def xml_blocks(data):
    soup = BeautifulSoup(data, 'xml')
    blocks = []
    for node in soup.select('article-title, abstract'):
        if node.find_parent('ref-list') is None:
            blocks.append(('Front matter', node.get_text(' ', strip=True)))
    for node in soup.find('body').descendants:
        if not isinstance(node, Tag) or node.name not in ['title', 'p', 'fig', 'table-wrap']:
            continue
        if any(p.name in ['fig', 'table-wrap', 'p'] for p in node.parents):
            continue
        section = node.find_parent('sec')
        heading = section.find('title', recursive=False) if section else None
        locator = heading.get_text(' ', strip=True) if heading else 'Main article'
        blocks.append((locator, node.get_text(' ', strip=True)))
    return blocks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cache', type=Path, required=True)
    parser.add_argument('--digest', type=Path, required=True)
    parser.add_argument('--manifest', type=Path, default=Path(__file__).with_name('new-sources.json'))
    args = parser.parse_args()
    registered = {s['id']: s for s in json.loads(args.manifest.read_text(encoding='utf-8'))['sources']}
    records = json.loads((args.cache / 'acquisition.json').read_text(encoding='utf-8'))
    digest = []
    for record in records:
        folder = args.cache / record['id']
        if record['status'] != 'downloaded_for_reading':
            digest.append(record)
            continue
        pages = registered.get(record['id'], {}).get('pdf_pages')
        if record['format'] == 'pdf' and pages:
            pdf = fitz.open(folder / 'source.pdf')
            blocks = [(f'PDF page {i+1}', pdf[i].get_text(sort=False)) for i in range(pages[0]-1, pages[1])]
            record['article_pdf_pages'] = pages
            record['file_note'] = registered[record['id']]['file_note']
        elif record['format'] == 'xml':
            blocks = xml_blocks((folder / 'source.xml').read_bytes())
        else:
            blocks = [('Extracted block; PDF page or HTML heading retained', b.strip()) for b in (folder / 'body.txt').read_text(encoding='utf-8').split('\n\n') if b.strip()]
        text = '\n\n'.join(f'[B{i:03d} | {section}]\n{body}' for i, (section, body) in enumerate(blocks, 1)) + '\n'
        (folder / 'reading.txt').write_text(text, encoding='utf-8', newline='\n')
        digest.append(record | {'reading_sha256': hashlib.sha256(text.encode()).hexdigest(), 'reading_blocks': len(blocks), 'reading_characters': len(text), 'rights_note': 'Full text remains outside the public repository; download does not establish reading or endorsement. Reading status here is acquisition-time status; consult reading-coverage.json for later coverage.'})
    args.digest.write_text(json.dumps(digest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps([{'id': r['id'], 'format': r.get('format'), 'blocks': r.get('reading_blocks'), 'characters': r.get('text_characters')} for r in digest], indent=2))


if __name__ == '__main__':
    main()
