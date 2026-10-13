"""Behavioral checks for discovery provenance, identity ambiguity and reading limits."""
import copy
import importlib.util
from pathlib import Path
import sys
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / 'skills/edu-writing/scripts'
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location('journal_search', SCRIPTS / 'search_journal.py')
js = importlib.util.module_from_spec(spec); spec.loader.exec_module(js)


def source():
    return {'url': 'https://example.edu/source', 'checked_at': '2026-10-13', 'locator': 'Synthetic fixture'}


def brief():
    editor = {'id': 'kim', 'name': 'Alex Kim', 'status': 'current', 'role': 'associate_editor',
              'role_evidence': source(), 'identity': {'status': 'confirmed', 'orcid': '0000-0001-0000-0001',
              'evidence': source(), 'basis': 'Fixture institutional author profile'}, 'search_terms': ['feedback']}
    return {'journal': {'name': 'Example Journal', 'publisher': 'Example', 'homepage': 'https://example.edu',
                       'issn': ['1234-567X'], 'evidence': source()},
            'manuscript': {k: 'Synthetic task' for k in ['question', 'concepts', 'theory', 'population', 'methods', 'findings']},
            'editors': [editor], 'queries': {'A': ['feedback'], 'C': ['contrary feedback evidence']}}


def item():
    return {'DOI': '10.0000/test', 'title': ['Feedback'], 'container-title': ['Other Journal'],
            'author': [{'given': 'Alex', 'family': 'Kim', 'ORCID': 'https://orcid.org/0000-0001-0000-0001'}],
            'published': {'date-parts': [[2025]]}}


def decision():
    return {'doi': '10.0000/test', 'purpose': 'citation', 'decision': 'include', 'relation': 'Same task',
            'claim': 'Students reported difficulty', 'placement': 'Introduction', 'reason': 'Clarifies the question',
            'reading': {'status': 'abstract', **source()}, 'support': 'The abstract reports this difficulty',
            'editor_links': [{'editor_id': 'kim', 'status': 'confirmed', 'author_orcid': '0000-0001-0000-0001',
                              'basis': 'Matching deposited identifier and official profile', 'evidence': source()}]}


class JournalSearchTest(unittest.TestCase):
    def test_cross_journal_candidates_are_retained_but_not_certified(self):
        calls = []
        def fetch(params):
            calls.append(params); return [item()]
        record = js.search(brief(), fetcher=fetch)
        self.assertEqual({x['stream'] for x in record['works']['10.0000/test']['found_by']}, {'A', 'B', 'C'})
        author = next(p for p in calls if 'query.author' in p)
        self.assertNotIn('filter', author)
        self.assertEqual(record['works']['10.0000/test']['reading'], 'metadata_only')
        self.assertEqual(record['works']['10.0000/test']['metadata']['venue'], 'Other Journal')

    def test_former_admin_unresolved_and_unselected_guest_are_not_editor_queries(self):
        b = brief(); prototype = b['editors'][0]
        for name, changes in [('past', {'status': 'former'}), ('admin', {'role': 'copyeditor'}),
                              ('unknown', {'identity': {'status': 'unresolved'}}),
                              ('guest', {'role': 'guest_editor'})]:
            e = copy.deepcopy(prototype); e.update(id=name, **changes); b['editors'].append(e)
        queries, skipped = js.query_plan(b)
        self.assertEqual([q['editor_id'] for q in queries if q['stream'] == 'B'], ['kim'])
        self.assertEqual(len(skipped), 4)
        b['target_issue'] = 'Feedback'; b['editors'][-1]['issue'] = 'Feedback'
        self.assertEqual(len([q for q in js.query_plan(b)[0] if q['stream'] == 'B']), 2)

    def test_official_page_identifier_conflict_requires_resolution(self):
        b = brief(); second = copy.deepcopy(b['editors'][0]); second.update(id='other', name='Different Person')
        b['editors'].append(second)
        with self.assertRaisesRegex(ValueError, 'ORCID assigned'):
            js.query_plan(b)

    def test_same_name_different_orcid_cannot_be_confirmed(self):
        record = js.search(brief(), fetcher=lambda _: [item()]); d = decision()
        d['editor_links'][0]['author_orcid'] = '0000-0002-0000-0002'
        result = js.check_recommendations(record, [d])
        self.assertEqual(result['status'], 'failed')
        self.assertTrue(any('ORCID conflict' in x for x in result['issues']))

    def test_name_hit_alone_is_unresolved_but_relevant_paper_can_be_cited(self):
        record = js.search(brief(), fetcher=lambda _: [item()]); d = decision()
        d['editor_links'] = [{'editor_id': 'kim', 'status': 'unresolved'}]
        result = js.check_recommendations(record, [d])
        self.assertEqual(result['status'], 'passed')
        self.assertEqual(result['source_truth_check'], 'not_performed')
        d['editor_links'][0]['status'] = 'confirmed'
        self.assertEqual(js.check_recommendations(record, [d])['status'], 'failed')

    def test_primary_record_does_not_silently_override_conflicting_deposit(self):
        other = item(); other['author'][0]['ORCID'] = 'https://orcid.org/0000-0002-0000-0002'
        record = js.search(brief(), fetcher=lambda _: [other]); d = decision()
        d['editor_links'][0]['basis_type'] = 'primary_author_record'
        self.assertEqual(js.check_recommendations(record, [d])['status'], 'failed')

    def test_abstract_can_support_its_claim_but_metadata_cannot(self):
        record = js.search(brief(), fetcher=lambda _: [item()]); d = decision()
        self.assertEqual(js.check_recommendations(record, [d])['status'], 'passed')
        d['reading']['status'] = 'metadata_only'
        self.assertEqual(js.check_recommendations(record, [d])['status'], 'failed')
        d['decision'] = 'exclude'; d['claim'] = 'No claim supported'; d['placement'] = 'None'
        self.assertEqual(js.check_recommendations(record, [d])['status'], 'passed')

    def test_no_editor_citation_quota_and_network_failure_is_not_no_results(self):
        b = brief(); b['editors'] = []
        record = js.search(b, fetcher=lambda _: [item()]); d = decision(); d['editor_links'] = []
        self.assertEqual(js.check_recommendations(record, [d])['status'], 'passed')
        def broken(_):
            raise OSError('service unavailable')
        failed = js.search(b, fetcher=broken)
        self.assertEqual(failed['status'], 'partial')
        self.assertTrue(all(q['status'] == 'failed' for q in failed['queries']))


if __name__ == '__main__':
    unittest.main()
