"""Fetch public evaluation sources to a NEW local folder; do not republish full texts.

Requires requests and pypdf (in edu-ppt requirements). Raw-source hashes
are compared with the frozen run; extraction layout may differ by tool version.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import requests
import xml.etree.ElementTree as ET

SOURCES = {
    'H1.xml': 'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12232635/fullTextXML',
    'H1-correction.xml': 'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12403119/fullTextXML',
    'H2.pdf': 'https://educationaltechnologyjournal.springeropen.com/counter/pdf/10.1186/s41239-023-00434-1',
    'T2.pdf': 'https://educationaltechnologyjournal.springeropen.com/counter/pdf/10.1186/s41239-023-00411-8',
}


def fetch(out):
    out.mkdir(parents=True, exist_ok=False)
    frozen = json.loads(Path(__file__).with_name('holdout-sources.json').read_text(encoding='utf-8'))
    expected = {x['file']: x['sha256'] for x in frozen['source_hashes']}
    records = []
    for name, url in SOURCES.items():
        record = {'file': name, 'url': url, 'retrieved_at': datetime.now(timezone.utc).isoformat()}
        try:
            response = requests.get(url, timeout=40)
            response.raise_for_status()
            raw = response.content
            path = out / name
            if path.suffix == '.pdf' and not raw.startswith(b'%PDF-'):
                raise ValueError('Server returned a non-PDF response; not accepted as article text')
            path.write_bytes(raw)
            digest = hashlib.sha256(raw).hexdigest()
            record.update(sha256=digest, status='downloaded', frozen_match=digest == expected[name] if name in expected else None)
            if path.suffix == '.pdf':
                from pypdf import PdfReader
                pages = PdfReader(path).pages
                doi = url.rsplit('/', 1)[-1].removesuffix('.pdf')
                if doi not in pages[0].extract_text():
                    raise ValueError('Expected article identifier absent from PDF first page')
                text = '\n\n'.join(f'--- PDF page {i+1} ---\n{page.extract_text()}' for i, page in enumerate(pages))
            else:
                # Whole main XML, including tables and references, for reading.
                tree = ET.fromstring(raw)
                text = '\n'.join(t.strip() for t in tree.itertext() if t.strip())
            path.with_suffix('.txt').write_text(text, encoding='utf-8', newline='\n')
        except Exception as exc:
            record.update(status='failed', error=str(exc))
        records.append(record)
    (out/'fetch-record.json').write_text(json.dumps(records, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
    return records


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = fetch(args.out)
    print(json.dumps(result, indent=2))
    if any(r['status'] == 'failed' for r in result):
        raise SystemExit(1)
