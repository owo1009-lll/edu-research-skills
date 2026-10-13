"""Public metadata search and DOI verification; candidates are not full-text readings."""
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import quote
import argparse
import json
import requests


def get_json(url, params=None):
    response = requests.get(url, params=params, headers={'User-Agent': 'edu-ppt/0.11 (education literature search)'}, timeout=40)
    response.raise_for_status()
    return response.json()


def crossref_item(item):
    dates = item.get('published', item.get('issued', {})).get('date-parts', [[]])
    return {'title': (item.get('title') or [''])[0],
            'authors': [f"{a.get('given', '')} {a.get('family', '')}".strip() for a in item.get('author', [])],
            'year': dates[0][0] if dates and dates[0] else None,
            'venue': (item.get('container-title') or [''])[0], 'doi': item.get('DOI'),
            'url': item.get('URL'), 'type': item.get('type'),
            'links': item.get('link', []), 'licenses': item.get('license', []),
            'access': 'metadata', 'selection': 'not_reviewed'}


def search(query=None, doi=None, limit=10):
    output = {'retrieved_utc': datetime.now(timezone.utc).isoformat(), 'query': query,
              'doi_requested': doi, 'scope': 'public candidate discovery; not a systematic review',
              'crossref': [], 'europe_pmc': [], 'errors': []}
    try:
        if doi:
            clean = doi.removeprefix('https://doi.org/').strip()
            response = get_json('https://api.crossref.org/works/' + quote(clean, safe=''))
            output['crossref'] = [crossref_item(response['message'])]
        else:
            response = get_json('https://api.crossref.org/works', {'query.bibliographic': query, 'rows': limit})
            output['crossref'] = [crossref_item(item) for item in response['message']['items']]
    except (requests.RequestException, KeyError, ValueError) as exc:
        output['errors'].append('Crossref: ' + str(exc))
    try:
        term = 'DOI:' + doi.removeprefix('https://doi.org/') if doi else query
        response = get_json('https://www.ebi.ac.uk/europepmc/webservices/rest/search',
                            {'query': term, 'format': 'json', 'pageSize': limit, 'resultType': 'core'})
        for item in response.get('resultList', {}).get('result', []):
            output['europe_pmc'].append({'title': item.get('title'), 'authors': item.get('authorString'),
                'year': item.get('pubYear'), 'doi': item.get('doi'), 'pmcid': item.get('pmcid'),
                'venue': item.get('journalInfo', {}).get('journal', {}).get('title'),
                'abstract': item.get('abstractText'), 'is_open_access': item.get('isOpenAccess'),
                'fulltext_locations': item.get('fullTextUrlList', {}).get('fullTextUrl', []),
                'access': 'abstract' if item.get('abstractText') else 'metadata', 'selection': 'not_reviewed'})
    except (requests.RequestException, KeyError, ValueError) as exc:
        output['errors'].append('Europe PMC: ' + str(exc))
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--query'); group.add_argument('--doi')
    parser.add_argument('--limit', type=int, default=10)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    if not 1 <= args.limit <= 100:
        parser.error('limit must be 1–100')
    if args.out.exists():
        parser.error('Output exists; use a fresh search record')
    result = search(args.query, args.doi, args.limit)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'crossref': len(result['crossref']), 'europe_pmc': len(result['europe_pmc']), 'errors': result['errors']}, ensure_ascii=False))
    if not result['crossref'] and not result['europe_pmc']:
        raise SystemExit(1)
