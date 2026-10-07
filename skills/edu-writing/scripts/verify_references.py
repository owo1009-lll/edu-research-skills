"""Resolve DOI identities; semantic support remains an explicit reader judgment."""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import html
import json
from pathlib import Path
import re
import unicodedata
import urllib.error
import urllib.parse
import urllib.request


def normalized(text):
    # Retain non-Latin letters: different Chinese titles/authors must not both become empty.
    text = html.unescape(re.sub(r'<[^>]*>', '', text))
    return ''.join(c for c in unicodedata.normalize('NFKD', text).casefold() if c.isalnum())


def metadata_from_message(message):
    dates = [message.get(k, {}).get('date-parts', [[]])[0] for k in
             ['published-print', 'published-online', 'published', 'issued']]
    years = sorted({d[0] for d in dates if d})
    plain = lambda value: ' '.join(html.unescape(re.sub(r'<[^>]*>', '', value)).split())
    return {'doi': message['DOI'].lower(), 'title': plain(message.get('title', [''])[0]),
            'authors': message.get('author', []), 'year': years[0] if years else None,
            'registered_years': years, 'venue': plain(message.get('container-title', [''])[0]),
            'volume': message.get('volume', ''), 'issue': message.get('issue', ''),
            'pages': message.get('page', message.get('article-number', '')),
            'type': message.get('type'), 'url': message.get('URL'),
            'update_to': message.get('update-to', []), 'relation': message.get('relation', {})}


def compare_identity(ref, metadata):
    errors = []
    expected = ref['expected']
    if (ref.get('doi') or '').lower().removeprefix('https://doi.org/') != (metadata.get('doi') or ''):
        errors.append('DOI identity differs')
    for field in ['title', 'venue']:
        if normalized(expected[field]) != normalized(metadata[field]):
            errors.append(field + ' differs')
    if expected['year'] not in metadata['registered_years']:
        errors.append('year differs')
    first = metadata['authors'][0].get('family', metadata['authors'][0].get('name', '')) if metadata.get('authors') else ''
    if normalized(first) != normalized(expected['first_author']):
        errors.append('first author differs or is not registered')
    return errors


def resolve(reference, cache_dir):
    doi = (reference.get('doi') or '').removeprefix('https://doi.org/').lower()
    url = 'https://api.crossref.org/works/' + urllib.parse.quote(doi, safe='')
    stamp = datetime.now(timezone.utc).isoformat()
    result = {'id': reference['id'], 'doi': doi, 'checked_utc': stamp,
              'lookup_url': url, 'status': 'not_found_or_unavailable'}
    try:
        # An assistant may supply a primary record from an actual publisher/browser read
        # or a prior saved DOI response. Never substitute an unlocated model recollection.
        if reference.get('primary_record'):
            record = reference['primary_record']
            evidence = Path(record['evidence_path'])
            raw = evidence.read_bytes()
            if hashlib.sha256(raw).hexdigest() != record['evidence_sha256']:
                raise ValueError('Primary-source evidence changed')
            if not record.get('url', '').startswith('https://') or not record.get('reader') or not record.get('locator'):
                raise ValueError('Primary record needs authority URL, reader and source locator')
            metadata = record['metadata']
            errors = compare_identity(reference, metadata)
            result.update(status='mismatch' if errors else 'verified', metadata=metadata,
                          identity_errors=errors, metadata_sha256=record['evidence_sha256'],
                          lookup_url=record['url'], checked_utc=record['checked_utc'],
                          verification_method=record['provider'], evidence_locator=record['locator'])
            return result
        if not doi:
            raise ValueError('No DOI: provide an actually read authoritative publisher/database record with stable URL')
        request = urllib.request.Request(url, headers={'User-Agent': 'edu-research-skills/0.4 (citation verification)'})
        for attempt in range(5):  # Crossref rate-limits bursts (HTTP 429); wait and retry instead of failing
            try:
                with urllib.request.urlopen(request, timeout=25) as response:
                    raw = response.read()
                break
            except urllib.error.HTTPError as http_error:
                if http_error.code not in (429, 503) or attempt == 4:
                    raise
                import time
                time.sleep(int(http_error.headers.get('Retry-After') or 2 ** attempt))
        message = json.loads(raw)['message']
        metadata = metadata_from_message(message)
        cache_dir.mkdir(parents=True, exist_ok=True)
        file = cache_dir / (reference['id'] + '.json')
        file.write_bytes(raw)
        errors = compare_identity(reference, metadata)
        # Keep the requested print/publication year if it is one of the registered dates.
        metadata['year'] = reference['expected']['year']
        result.update(status='mismatch' if errors else 'verified', metadata=metadata,
                      identity_errors=errors, metadata_sha256=hashlib.sha256(raw).hexdigest())
    except Exception as exc:
        result['error'] = str(exc)
    return result


def verify(ledger, output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    ids = [r['id'] for r in ledger['references']]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate reference identifiers')
    dois = [(r.get('doi') or '').lower().removeprefix('https://doi.org/') for r in ledger['references'] if r.get('doi')]
    if len(dois) != len(set(dois)):
        raise ValueError('Duplicate DOI entries; deduplicate before writing')
    # Independent lookups can run concurrently; preserve ledger order in the result.
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda r: resolve(r, output / 'metadata'), ledger['references']))
    by_id = {r['id']: r for r in ledger['references']}
    for result in results:
        ref = by_id[result['id']]
        result['reading'] = ref.get('reading', {'status': 'not_read'})
        result['notice_check'] = ref.get('notice_check', {'status': 'not_checked'})
        # Crossref metadata alone cannot certify no retraction. Capture known flags explicitly.
        result['correction_retraction_scope'] = 'Registered update/relation fields plus separately recorded publisher checks; not exhaustive certification'
    report = {'schema': 1, 'identity_results': results, 'semantic_review': ledger.get('claims', []),
              'limitations': ['Bibliographic identity does not establish claim support',
                              'Semantic statuses are reader judgments; the script does not assess meaning',
                              'Missing notice metadata is not proof of no correction or retraction']}
    (output / 'verified.json').write_bytes((json.dumps(report, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
    columns = ['id', 'doi', 'identity', 'reading', 'version', 'notice_status', 'checked_utc', 'lookup_url']
    with (output / 'citation_check.csv').open('w', newline='', encoding='utf-8-sig') as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        for r in results:
            writer.writerow({'id': r['id'], 'doi': r['doi'], 'identity': r['status'],
                             'reading': r['reading'].get('status'), 'version': r['reading'].get('version'),
                             'notice_status': r['notice_check'].get('status'), 'checked_utc': r['checked_utc'],
                             'lookup_url': r['lookup_url']})
    return report


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--ledger', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    result = verify(json.loads(args.ledger.read_text(encoding='utf-8')), args.output)
    print(json.dumps({'identity': {r['id']: r['status'] for r in result['identity_results']},
                      'semantic_check': 'separate reader judgment; not automatically validated'}, indent=2))
