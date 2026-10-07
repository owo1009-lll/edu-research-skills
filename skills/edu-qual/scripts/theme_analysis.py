"""Organize and version source-linked, AI-assisted reflexive thematic analysis.

Interpretation is performed by Codex/researcher, never by keyword counts here.
Raw and prepared transcripts must remain under the project's edu_output/private/ directory.
"""
from pathlib import Path
import argparse
import csv
import datetime
import hashlib
import json
import re
import sys


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, obj):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')


def private_path(root, path):
    p = (root / path).resolve()
    if not p.is_relative_to(root / 'edu_output' / 'private'):
        raise ValueError('Transcript work must stay under edu_output/private; export reviewed excerpts separately')
    return p


def prepare(root, source, output, redactions):
    source = private_path(root, source)
    output = private_path(root, output)
    if output.exists():
        raise ValueError('New prepared directory required; originals are immutable')
    mappings = json.loads(private_path(root, redactions).read_text(encoding='utf-8'))
    if not isinstance(mappings, dict) or not all(k and isinstance(v,str) and v for k,v in mappings.items()):
        raise ValueError('Redactions must be an explicit nonempty-string mapping')
    rows = list(csv.DictReader(source.open(encoding='utf-8-sig', newline='')))
    if not rows or not {'document_id','speaker','text','source_locator'} <= rows[0].keys():
        raise ValueError('Assistant-normalized CSV needs document_id,speaker,text,source_locator')
    segments = []
    source_hash = digest(source)
    for i, row in enumerate(rows, 1):
        if row['speaker'] not in {'participant','observer','interviewer','context','ambiguous'} or not all(row[k].strip() for k in ['document_id','text','source_locator']):
            raise ValueError('Missing source locator/text or unexplained speaker role')
        text = row['text']
        changes = []
        for old, new in sorted(mappings.items(), key=lambda item:len(item[0]), reverse=True):
            if old in text:
                text = text.replace(old,new); changes.append({'replaced':old,'with':new})
        segment_id = 'S'+hashlib.sha256(f'{source_hash}:{i}'.encode()).hexdigest()[:12]
        segments.append({'id':segment_id, 'document_id':row['document_id'], 'speaker':row['speaker'],
                         'text':text,'source_locator':row['source_locator'], 'original_text_sha256':hashlib.sha256(row['text'].encode()).hexdigest(),
                         'redactions':changes})
    output.mkdir(parents=True)
    write_json(output/'segments.json', segments)
    receipt={'source':str(source.relative_to(root)), 'source_sha256':source_hash,'redactions_sha256':digest(private_path(root,redactions)),
             'segments_sha256':digest(output/'segments.json'),'segment_count':len(segments), 'anonymization':'Explicit substitutions, not a privacy certification',
             'prepared_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    write_json(output/'preparation.json',receipt)
    return output


def validate(annotation, segments):
    index={s['id']:s for s in segments}
    required={'question','approach','memo','document_memos','codes','assignments','themes','unresolved','change_reason'}
    if not required <= annotation.keys():
        raise ValueError('Incomplete analytic record: '+str(required-annotation.keys()))
    if annotation['approach']!='AI-assisted reflexive thematic analysis; semantic/contextual':
        raise ValueError('This adapter is explicitly scoped to reflexive thematic analysis')
    if not all(annotation[k].strip() for k in ['question','memo','change_reason']):
        raise ValueError('Question, reflexive memo and revision reason required')
    documents={s['document_id'] for s in segments}
    if set(annotation['document_memos'])!=documents or not all(annotation['document_memos'].values()):
        raise ValueError('Familiarization memo required for every selected document')
    codes={c['id']:c for c in annotation['codes']}
    if len(codes)!=len(annotation['codes']) or not codes:
        raise ValueError('Unique nonempty codebook required')
    for c in codes.values():
        if not all(c.get(k) for k in ['label','definition','include','exclude','category']):
            raise ValueError('Codes need definition, inclusion/exclusion conditions and category')
    assignments={a['id']:a for a in annotation['assignments']}
    if len(assignments)!=len(annotation['assignments']) or not assignments:
        raise ValueError('Unique nonempty assignment IDs required')
    for a in assignments.values():
        if a.get('code') not in codes or a.get('segment') not in index or a.get('role') not in {'support','counterexample','context','alternative'} or not a.get('interpretation'):
            raise ValueError('Invalid source/code/analytic role in assignment')
        s=index[a['segment']]
        if s['speaker']=='observer':
            if a.get('evidence_kind')!='observation_note':
                raise ValueError('Observer narrative must be explicitly observation_note, never participant speech')
        elif s['speaker']=='participant':
            if a.get('evidence_kind','participant_statement')!='participant_statement':
                raise ValueError('Participant evidence must retain participant_statement attribution')
        else:
            raise ValueError('Ambiguous/interviewer text stays in context, not direct participant or observer evidence')
        if not a.get('excerpt') or a['excerpt'] not in s['text']:
            raise ValueError('Excerpt is not an exact substring of the preserved, declared-redacted segment')
    if 'reviewed_uncoded' in annotation:
        coded={a['segment'] for a in assignments.values()}
        remaining={s['id'] for s in segments if s['speaker'] in {'participant','observer'}}-coded
        if set(annotation['reviewed_uncoded'])!=remaining or not all(annotation['reviewed_uncoded'].values()):
            raise ValueError('Uncoded review must give a reason for every remaining participant/observer segment')
    themes={t['id']:t for t in annotation['themes']}
    if len(themes)!=len(annotation['themes']) or not themes:
        raise ValueError('Unique candidate themes required')
    for t in themes.values():
        if not all(t.get(k) for k in ['name','central_idea','boundary','alternative_explanation','counterexample_review']):
            raise ValueError('Theme needs central idea, boundary, alternative and counterexample review')
        if t.get('status')!='candidate_AI_assisted' or not t.get('support'):
            raise ValueError('This batch exports candidate AI-assisted themes with explicit support')
        for role in ['support','counterexamples']:
            if not set(t.get(role,[])) <= assignments.keys():
                raise ValueError('Theme points to an unknown assignment')
        if any(assignments[k]['role']!='support' for k in t['support']):
            raise ValueError('Theme support must be labeled support')
        if any(assignments[k]['role'] not in {'counterexample','alternative'} for k in t.get('counterexamples',[])):
            raise ValueError('Counterevidence must retain its analytic role')
    return index, codes, assignments, themes


def commit(root, prepared, annotation_path, actor, parent=None):
    prepared=private_path(root,prepared)
    receipt=json.loads((prepared/'preparation.json').read_text(encoding='utf-8'))
    if digest(prepared/'segments.json')!=receipt['segments_sha256'] or digest(root/receipt['source'])!=receipt['source_sha256']:
        raise ValueError('Prepared segments or raw normalized source changed; prepare a new version')
    annotation=json.loads(private_path(root,annotation_path).read_text(encoding='utf-8'))
    segments=json.loads((prepared/'segments.json').read_text(encoding='utf-8'))
    index,codes,assignments,themes=validate(annotation,segments)
    revisions=prepared/'revisions';latest=prepared/'latest.json'
    previous=None
    if latest.exists():
        current=json.loads(latest.read_text(encoding='utf-8'))['revision']
        if parent!=current:
            raise ValueError('Missing/stale parent revision; do not overwrite another edit')
        prior_history=json.loads((revisions/current/'history.json').read_text(encoding='utf-8'))
        if digest(revisions/current/'analysis.json')!=prior_history['annotation_sha256']:
            raise ValueError('Parent revision changed; preserve edits as a new explicit annotation')
        previous=json.loads((revisions/current/'analysis.json').read_text(encoding='utf-8'))
    elif parent:
        raise ValueError('Parent does not exist')
    stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    directory=revisions/stamp;directory.mkdir(parents=True)
    write_json(directory/'analysis.json',annotation)
    (directory/'analysis_script.py').write_bytes(Path(__file__).read_bytes())
    history={'revision':stamp,'parent':parent,'actor':actor,'change_reason':annotation['change_reason'],
             'input_sha256':receipt['source_sha256'],'segments_sha256':receipt['segments_sha256'],'annotation_sha256':digest(directory/'analysis.json'),
             'script_sha256':digest(directory/'analysis_script.py')}
    if previous:
        history['changes']={k:{'before_sha256':hashlib.sha256(json.dumps(previous.get(k),sort_keys=True,ensure_ascii=False).encode()).hexdigest(),
                               'after_sha256':hashlib.sha256(json.dumps(annotation.get(k),sort_keys=True,ensure_ascii=False).encode()).hexdigest()}
                            for k in set(previous)|set(annotation) if previous.get(k)!=annotation.get(k)}
    write_json(directory/'history.json',history)
    with (directory/'evidence.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['assignment','code','category','segment','document','locator','speaker','evidence_kind','role','excerpt','interpretation']);w.writeheader()
        for a in assignments.values():
            s=index[a['segment']];c=codes[a['code']]
            w.writerow({'assignment':a['id'],'code':c['label'],'category':c['category'],'segment':s['id'],'document':s['document_id'],
                        'locator':s['source_locator'],'speaker':s['speaker'],'evidence_kind':a.get('evidence_kind','participant_statement'),
                        'role':a['role'],'excerpt':a['excerpt'],'interpretation':a['interpretation']})
    coded={a['segment'] for a in assignments.values()}
    participants={s['id'] for s in segments if s['speaker']=='participant'}
    observations={s['id'] for s in segments if s['speaker']=='observer'}
    write_json(directory/'coverage.json',{'total_segments':len(segments),'participant_segments':len(participants),'coded_participant_segments':len(coded&participants),
                                       'uncoded_participant_segments':sorted(participants-coded),'observer_segments':len(observations),'coded_observer_segments':len(coded&observations),
                                       'uncoded_observer_segments':sorted(observations-coded),'meaning':'Coverage inventory, not thematic importance or saturation'})
    lines=['# 候选主题与原文检验','',f"研究问题：{annotation['question']}",'','AI辅助的反思性主题分析；候选解释，不是独立人工编码。','']
    for t in themes.values():
        lines.extend([f"## {t['id']} {t['name']}",'',t['central_idea'],'',f"适用边界：{t['boundary']}",f"替代解释：{t['alternative_explanation']}",f"反例复查：{t['counterexample_review']}",''])
        for k in t['support']+t.get('counterexamples',[]):
            a=assignments[k];s=index[a['segment']]
            lines.extend([f"- [{k}; {a['role']}; {s['speaker']}; {s['document_id']}; {s['source_locator']}] {a['excerpt']}",f"  解释：{a['interpretation']}"])
        lines.append('')
    (directory/'themes.md').write_text('\n'.join(lines),encoding='utf-8')
    write_json(latest,{'revision':stamp})
    return directory


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--workspace',type=Path,default=Path('.'))
    sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('prepare');p.add_argument('--input',required=True);p.add_argument('--output',required=True);p.add_argument('--redactions',required=True)
    c=sub.add_parser('commit');c.add_argument('--prepared',required=True);c.add_argument('--annotation',required=True);c.add_argument('--parent');c.add_argument('--actor',choices=['AI_assistant','researcher','simulated_researcher_test'],required=True)
    args=parser.parse_args();root=args.workspace.resolve()
    try:
        if args.command=='prepare': result=prepare(root,args.input,args.output,args.redactions)
        else: result=commit(root,args.prepared,args.annotation,args.actor,args.parent)
        print(result)
    except (ValueError,KeyError,FileNotFoundError) as error:
        parser.exit(2,str(error)+'\n')


if __name__=='__main__':main()
