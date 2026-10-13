"""Discover journal/editor literature; verify identities and claim support by reading sources.

The checker validates records and identifier conflicts, not the truth of reader judgments.
"""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import time
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from verify_references import metadata_from_message, normalized

ACADEMIC = {'lead_editor', 'associate_editor', 'area_editor', 'guest_editor'}


def orcid(value):
    return (value or '').rstrip('/').rsplit('/', 1)[-1].upper()


def evidence(record):
    return (isinstance(record, dict) and record.get('url', '').startswith('https://')
            and bool(record.get('locator')) and bool(record.get('checked_at')))


def validate_brief(brief):
    errors = []
    journal = brief.get('journal', {})
    for field in ['name', 'publisher', 'homepage', 'issn']:
        if not journal.get(field):
            errors.append('journal.' + field + ': required')
    if not evidence(journal.get('evidence')):
        errors.append('journal.evidence: official URL, date and location required')
    if not all(re.fullmatch(r'\d{4}-\d{3}[\dX]', x) for x in journal.get('issn', [])):
        errors.append('journal.issn: invalid ISSN format')
    for field in ['question', 'concepts', 'theory', 'population', 'methods', 'findings']:
        if not brief.get('manuscript', {}).get(field):
            errors.append('manuscript.' + field + ': required (unknown/not yet collected is allowed)')
    if not brief.get('queries', {}).get('A') or not brief.get('queries', {}).get('C'):
        errors.append('queries: A and C search terms required')
    ids, identifiers = set(), {}
    for editor in brief.get('editors', []):
        ident = editor.get('id')
        if not ident or ident in ids:
            errors.append('editors: missing or duplicate ID ' + str(ident))
        ids.add(ident)
        if not editor.get('name') or not evidence(editor.get('role_evidence')):
            errors.append(str(ident) + ': name and official role evidence required')
        identity = editor.get('identity', {})
        code = orcid(identity.get('orcid'))
        if code:
            if not re.fullmatch(r'\d{4}-\d{4}-\d{4}-\d{3}[\dX]', code):
                errors.append(str(ident) + ': invalid ORCID format')
            if code in identifiers and normalized(editor['name']) != identifiers[code]:
                errors.append(str(ident) + ': ORCID assigned to different names; resolve source conflict')
            identifiers[code] = normalized(editor['name'])
        if identity.get('status') == 'confirmed' and (not evidence(identity.get('evidence')) or not identity.get('basis')):
            errors.append(str(ident) + ': confirmed identity requires source and matching basis')
    return errors


def query_plan(brief, limit=8):
    errors = validate_brief(brief)
    if errors:
        raise ValueError('\n'.join(errors))
    if not 1 <= limit <= 100:
        raise ValueError('limit must be 1..100')
    queries, skipped = [], []
    for term in brief['queries']['A']:
        for issn in brief['journal']['issn']:
            queries.append({'stream': 'A', 'params': {'query.bibliographic': term, 'filter': 'issn:' + issn, 'rows': limit}})
    for editor in brief.get('editors', []):
        reason = None
        if editor.get('status') != 'current' or editor.get('role') not in ACADEMIC:
            reason = 'not a current academic editor'
        elif editor['role'] == 'guest_editor' and (not brief.get('target_issue') or editor.get('issue') != brief['target_issue']):
            reason = 'guest editor is not attached to this target issue'
        elif editor.get('identity', {}).get('status') != 'confirmed':
            reason = 'author identity remains unresolved'
        elif not editor.get('search_terms'):
            reason = editor.get('skip_reason', 'no substantively relevant query recorded')
        if reason:
            skipped.append({'editor_id': editor['id'], 'reason': reason})
            continue
        for term in editor['search_terms']:
            # Name queries retrieve candidates, including possible namesakes. Do not
            # restrict B to the target journal or to incomplete ORCID deposits.
            queries.append({'stream': 'B', 'editor_id': editor['id'], 'params': {
                'query.author': editor['name'], 'query.bibliographic': term, 'rows': limit}})
    for term in brief['queries']['C']:
        queries.append({'stream': 'C', 'params': {'query.bibliographic': term, 'rows': limit}})
    return queries, skipped


def fetch(params):
    url = 'https://api.crossref.org/works?' + urlencode(params)
    request = Request(url, headers={'User-Agent': 'edu-writing (journal literature discovery)'})
    for attempt in range(3):
        try:
            with urlopen(request, timeout=35) as response:
                return json.load(response)['message']['items']
        except HTTPError as exc:
            if exc.code not in {429, 503} or attempt == 2:
                raise
            retry = exc.headers.get('Retry-After', '') if exc.headers else ''
            time.sleep(min(float(retry), 10) if retry.isdigit() else 2 ** (attempt + 1))


def search(brief, limit=8, fetcher=fetch):
    queries, skipped = query_plan(brief, limit)
    works = {}
    for query in queries:
        query['url'] = 'https://api.crossref.org/works?' + urlencode(query['params'])
        query['retrieved_at'] = datetime.now(timezone.utc).isoformat()
        try:
            items = fetcher(query['params'])
            query.update(status='completed', returned=len(items))
            for item in items:
                metadata = metadata_from_message(item)
                doi = metadata['doi']
                row = works.setdefault(doi, {'metadata': metadata, 'found_by': [], 'reading': 'metadata_only'})
                origin = {'stream': query['stream']}
                if query.get('editor_id'):
                    origin['candidate_editor_id'] = query['editor_id']
                if origin not in row['found_by']:
                    row['found_by'].append(origin)
        except Exception as exc:
            query.update(status='failed', error=str(exc))
    return {'brief': brief, 'queries': queries, 'skipped_editors': skipped, 'works': works,
            'status': 'partial' if any(q['status'] == 'failed' for q in queries) else 'completed',
            'scope': 'Bounded candidate discovery, not systematic coverage. B hits do not establish editor authorship.'}


def check_recommendations(record, decisions):
    issues = validate_brief(record['brief'])
    editors = {e['id']: e for e in record['brief'].get('editors', [])}
    seen = set()
    for row in decisions:
        doi = row.get('doi', '').lower().removeprefix('https://doi.org/')
        prefix = doi + ': '
        if doi in seen:
            issues.append(prefix + 'duplicate decision')
        seen.add(doi)
        work = record['works'].get(doi)
        if not work:
            issues.append(prefix + 'not in discovery or documented supplemental records')
            continue
        if row.get('decision') not in {'include', 'backup', 'exclude'}:
            issues.append(prefix + 'decision must be include/backup/exclude')
        if row.get('purpose') not in {'citation', 'writing_example', 'editorial_scope'}:
            issues.append(prefix + 'separate citation, writing exemplar and editorial scope purposes')
        for field in ['relation', 'claim', 'placement', 'reason']:
            if not row.get(field):
                issues.append(prefix + field + ' required')
        reading = row.get('reading', {})
        if reading.get('status') not in {'full_text', 'source_excerpt', 'abstract', 'metadata_only', 'not_read'}:
            issues.append(prefix + 'explicit reading scope required')
        if row.get('decision') == 'include' and row.get('purpose') == 'citation':
            if reading.get('status') in {'metadata_only', 'not_read', None}:
                issues.append(prefix + 'cannot support a manuscript claim from metadata alone')
            if not evidence(reading) or not row.get('support'):
                issues.append(prefix + 'claim support requires actual source location and reader explanation')
        for link in row.get('editor_links', []):
            editor = editors.get(link.get('editor_id'))
            if not editor:
                issues.append(prefix + 'unknown editor link')
                continue
            if link.get('status') not in {'confirmed', 'unresolved', 'different_person'}:
                issues.append(prefix + 'editor link status required')
            if link.get('status') != 'confirmed':
                continue  # Paper may still be relevant as A/C without an editor link.
            if not evidence(link.get('evidence')) or not link.get('basis'):
                issues.append(prefix + 'editor authorship needs identity evidence beyond a name hit')
            expected = orcid(editor.get('identity', {}).get('orcid'))
            claimed = orcid(link.get('author_orcid'))
            if claimed and expected and claimed != expected:
                issues.append(prefix + 'ORCID conflict: same/similar name is a different or unresolved person')
            author_name = normalized(link.get('author_name', editor['name']))
            for author in work['metadata'].get('authors', []):
                name = normalized(author.get('name') or (author.get('given', '') + ' ' + author.get('family', '')))
                deposited = orcid(author.get('ORCID'))
                if name == author_name and deposited and expected and deposited != expected:
                    issues.append(prefix + 'deposited author ORCID conflicts with editor; primary-record override cannot hide the conflict')
            if claimed and not any(orcid(a.get('ORCID')) == claimed for a in work['metadata'].get('authors', [])):
                if link.get('basis_type') != 'primary_author_record':
                    issues.append(prefix + 'ORCID absent from deposited authors; locate primary author record')
    return {'status': 'failed' if issues else 'passed', 'issues': issues,
            'unreviewed_dois': sorted(set(record['works']) - seen),
            'source_truth_check': 'not_performed', 'claim_semantics_check': 'not_performed',
            'scope': 'Record completeness and declared identifier consistency only; relevance, official status and reading support require human/source review.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('search'); p.add_argument('--brief', type=Path, required=True); p.add_argument('--limit', type=int, default=8)
    p.add_argument('--out', type=Path, required=True)
    p = sub.add_parser('check'); p.add_argument('--record', type=Path, required=True); p.add_argument('--decisions', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        parser.error('Output exists; preserve earlier evidence and choose a new path')
    read = lambda p: json.loads(p.read_text(encoding='utf-8'))
    try:
        report = search(read(args.brief), args.limit) if args.command == 'search' else check_recommendations(read(args.record), read(args.decisions))
    except ValueError as exc:
        parser.error(str(exc))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps({'status': report['status'], 'issues': report.get('issues', []), 'works': len(report.get('works', {}))}))
    if report['status'] in {'failed', 'partial'}:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
