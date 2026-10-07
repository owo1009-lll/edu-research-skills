"""Version a source-linked qualitative content analysis, without automatic coding.

Codex/researcher supplies interpreted assignments after reading source/context.
No independent coder, member check, or agreement coefficient is manufactured.
"""
from pathlib import Path
import argparse
import collections
import datetime
import hashlib
import json
import uuid


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def private(root, value):
    path = (root / value).resolve()
    if not path.is_relative_to(root) or 'private' not in path.relative_to(root).parts:
        raise ValueError('Full sources and interpreted coding stay in project private directories')
    return path


def validate(a, segments):
    required = {'question', 'approach', 'units', 'codebook', 'assignments',
                'uncoded', 'category_interpretations', 'case_memos', 'reflexive_memo',
                'change_reason', 'scope', 'coder_design'}
    if not required <= a.keys():
        raise ValueError('Incomplete content analysis record: ' + str(required - a.keys()))
    if a['approach'] not in {'inductive_codebook_content_analysis', 'directed_codebook_content_analysis'}:
        raise ValueError('Choose content-analysis orientation explicitly; reflexive themes use their separate adapter')
    if a['coder_design'] != 'single_AI_assistant_pending_researcher_review':
        raise ValueError('This execution has no genuine independent human coders; do not manufacture agreement')
    if any(k in a for k in ['kappa', 'intercoder_reliability', 'independent_validation_passed']):
        raise ValueError('Unsupported independent-coder or validation claim')
    if not all(a[k] for k in ['question', 'units', 'reflexive_memo', 'scope', 'change_reason']):
        raise ValueError('Question, meaning/context units, reflexivity, scope, revision reason required')
    index = {s['id']: s for s in segments}
    if len(index) != len(segments) or not index:
        raise ValueError('Unique preserved segment IDs required')
    cases = {s['document_id'] for s in segments}
    if set(a['case_memos']) != cases or not all(a['case_memos'].values()):
        raise ValueError('Familiarization/context memo required for each selected case')
    codes = {c['id']: c for c in a['codebook']}
    if len(codes) != len(a['codebook']) or not codes:
        raise ValueError('Unique nonempty codebook required')
    for c in codes.values():
        if not all(c.get(k) for k in ['label', 'definition', 'include', 'exclude', 'origin', 'example', 'counterexample']):
            raise ValueError('Operational code definitions, provenance, example and exclusion counterexample required')
        if a['approach'].startswith('directed') and not c.get('framework_source'):
            raise ValueError('Directed categories need a located framework source, including any explicitly emergent additions')
    assigned = set()
    ids = set()
    for z in a['assignments']:
        if z.get('id') in ids or z.get('segment') not in index or z.get('code') not in codes:
            raise ValueError('Unique assignments must link preserved segment and declared code')
        ids.add(z['id'])
        s = index[z['segment']]
        expected = {'participant': 'participant_statement', 'observer': 'observation_note'}.get(s['speaker'])
        if not expected or z.get('evidence_kind') != expected:
            raise ValueError('Interviewer/ambiguous/context text cannot become participant or observation evidence')
        if not z.get('excerpt') or z['excerpt'] not in s['text']:
            raise ValueError('Evidence excerpt must be an exact substring of the preserved redacted source')
        if not z.get('reason') or z.get('role') not in {'support', 'counterevidence', 'alternative', 'context'}:
            raise ValueError('Every assignment needs an interpretation and analytic role')
        assigned.add(z['segment'])
    eligible = {s['id'] for s in segments if s['speaker'] in {'participant', 'observer'}}
    if set(a['uncoded']) != eligible - assigned or not all(a['uncoded'].values()):
        raise ValueError('Every remaining eligible segment needs an explicit uncoded review reason')
    if set(a['category_interpretations']) != set(codes):
        raise ValueError('Interpret each category; category counts alone are not qualitative findings')
    for code, interpretation in a['category_interpretations'].items():
        if not all(interpretation.get(k) for k in ['finding', 'boundary', 'counterevidence_review']):
            raise ValueError('Category interpretation needs finding, boundary, and counterevidence review')
        if not any(z['code'] == code for z in a['assignments']) and interpretation.get('status') != 'not_observed_in_selected_material':
            raise ValueError('An unobserved theoretical category cannot be reported as an observed finding')
    return index, codes


def commit(root, segments_path, annotation_path, output_parent, parent=None):
    root = Path(root).resolve()
    segments_path = private(root, segments_path)
    annotation_path = private(root, annotation_path)
    segments = json.loads(segments_path.read_text(encoding='utf-8'))
    a = json.loads(annotation_path.read_text(encoding='utf-8'))
    index, codes = validate(a, segments)
    previous = None
    if parent:
        pp = private(root, parent)
        previous = json.loads((pp / 'annotation.json').read_text(encoding='utf-8'))
        receipt = json.loads((pp / 'receipt.json').read_text(encoding='utf-8'))
        if digest(pp / 'annotation.json') != receipt['annotation_sha256'] or digest(pp / 'segments.json') != receipt['segments_sha256']:
            raise ValueError('Immutable parent version changed')
        if digest(segments_path) != receipt['segments_sha256']:
            raise ValueError('Source segment universe changed: start a separately documented source version')
    parent_dir = private(root, output_parent)
    output = parent_dir / (datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '-' + uuid.uuid4().hex[:8])
    output.mkdir(parents=True)
    (output / 'segments.json').write_bytes(segments_path.read_bytes())
    (output / 'annotation.json').write_bytes(annotation_path.read_bytes())
    source_map = [{'assignment': z['id'], 'code': z['code'], 'segment': z['segment'],
                   'document': index[z['segment']]['document_id'], 'source_locator': index[z['segment']]['source_locator'],
                   'excerpt': z['excerpt'], 'reason': z['reason'], 'role': z['role'], 'evidence_kind': z['evidence_kind']}
                  for z in a['assignments']]
    counts = collections.Counter((z['code'], z['segment']) for z in a['assignments'])
    summary = [{'code': c, 'label': spec['label'],
                'unique_coded_segments': sum(1 for cc, _ in counts if cc == c),
                **a['category_interpretations'][c]} for c, spec in codes.items()]
    for filename, value in [('source_map.json', source_map), ('categories.json', summary),
                             ('coverage.json', {'selected_segments': len(segments), 'eligible_segments': len(a['uncoded']) + len({z['segment'] for z in a['assignments']}),
                                                'coded_segments': len({z['segment'] for z in a['assignments']}), 'uncoded': a['uncoded'],
                                                'count_meaning': 'Describes this selected coding corpus; not prevalence, importance or an outcome effect'})]:
        (output / filename).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
    changed = []
    if previous:
        for k in ['approach', 'codebook', 'assignments', 'uncoded', 'category_interpretations', 'scope']:
            if previous[k] != a[k]:
                changed.append(k)
    receipt = {'status': 'AI_assisted_content_analysis_pending_researcher_review', 'orientation': a['approach'],
               'parent': str(pp.relative_to(root)) if parent else None, 'changed_fields': changed, 'change_reason': a['change_reason'],
               'segments_sha256': digest(output / 'segments.json'), 'annotation_sha256': digest(output / 'annotation.json'),
               'source_path': str(segments_path.relative_to(root)), 'annotation_path': str(annotation_path.relative_to(root)),
               'coder_design': a['coder_design'], 'scope': a['scope']}
    (output / 'receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding='utf-8')
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', default='.')
    parser.add_argument('--segments', required=True)
    parser.add_argument('--annotation', required=True)
    parser.add_argument('--output-parent', default='edu_output/private/content_versions')
    parser.add_argument('--parent')
    args = parser.parse_args()
    print(commit(args.workspace, args.segments, args.annotation, args.output_parent, args.parent))
