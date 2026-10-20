"""Check extraction against an acquired PMC article and an existing public PDF.

Uses local source bytes; no source text or local paths are emitted. This checks
content preservation and rejection of incomplete pages, not completed reading.
"""
import argparse
import importlib.util
import json
from pathlib import Path

from bs4 import BeautifulSoup


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--pdf', type=Path, required=True)
    args = parser.parse_args()
    module_path = Path(__file__).parents[1] / '20261018' / 'fetch_sources.py'
    spec = importlib.util.spec_from_file_location('source_fetch', module_path)
    fetcher = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fetcher)
    raw = args.source.read_bytes()
    soup = BeautifulSoup(raw, 'html.parser')
    article = soup.select_one('article section.main-article-body')
    assert article is not None, 'Expected an acquired PMC full article'
    refs = [n.get_text(' ', strip=True) for n in article.select('.ref-list cite')]
    tables = [n.get_text(' ', strip=True) for n in article.find_all('table')]
    assert refs and tables, 'The real source must exercise references and tables'
    kind, body, details = fetcher.extract(raw, 'text/html')
    preserved_refs = sum(r in body for r in refs)
    preserved_tables = sum(t in body for t in tables)
    report = {'format': kind, 'source_references': len(refs),
              'preserved_references': preserved_refs, 'source_tables': len(tables),
              'preserved_tables': preserved_tables, 'full_text_characters': len(body)}
    if preserved_refs != len(refs) or preserved_tables != len(tables):
        report['status'] = 'failed_content_preservation'
        print(json.dumps(report, indent=2))
        raise SystemExit(1)
    assert kind == 'html'
    assert '10.1080/09669760.2025.2522894' in body
    assert 'Building Professional Learning Communities in Head Start' in body
    # A 200 response with a challenge or abstract must not become full text.
    for incomplete in [b'<html>Checking your browser before accessing PMC</html>',
                       b'<article lang="en"><section class="main-article-body">'
                       b'<h2>Abstract</h2><p>Only the abstract.</p></section></article>']:
        try:
            fetcher.extract(incomplete, 'text/html')
        except ValueError:
            pass
        else:
            raise AssertionError('Incomplete page accepted as full text')
    pdf_kind, pdf_body, pdf_details = fetcher.extract(args.pdf.read_bytes(), 'application/pdf')
    assert pdf_kind == 'pdf' and pdf_details['pages'] == 12
    assert '10.29333/ajqr/11030' in pdf_body
    report.update(status='passed', rejected_incomplete_pages=2, pdf_regression_pages=12)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
