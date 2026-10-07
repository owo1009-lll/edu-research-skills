"""Validate and version grounded-theory coding; export open-coding, axial-coding and saturation tables.

Run from the project folder after `theme_analysis.py prepare` has produced segments.json:
  python grounded_coding.py --prepared edu_output/private/<prepared dir> --coding edu_output/private/coding.csv
                            --actor AI_assistant [--parent <revision id>] [--order A,B,C] [--holdout C]
coding.csv columns: segment_id, quote, concept, category, main_category, coder
  segment_id comes from segments.json; quote must be an exact excerpt of that (redacted) segment.
--order lists the documents in the order they were coded; --holdout names documents kept back for the
saturation check. Each run writes a new revision under <prepared>/gt_revisions/ and never overwrites one.
"""
from pathlib import Path
import argparse
import csv
import datetime
import hashlib
import json
import shutil
import sys

COLUMNS = ['segment_id', 'quote', 'concept', 'category', 'main_category', 'coder']


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def private_path(root, value):
    p = (root / value).resolve()
    if not p.is_relative_to(root / 'edu_output' / 'private'):
        raise ValueError('Coding work must stay under edu_output/private')
    return p


def load(root, prepared, coding_path):
    prepared = private_path(root, prepared)
    receipt = json.loads((prepared / 'preparation.json').read_text(encoding='utf-8'))
    if digest(prepared / 'segments.json') != receipt['segments_sha256']:
        raise ValueError('segments.json changed after prepare; prepare a new version')
    segments = {s['id']: s for s in json.loads((prepared / 'segments.json').read_text(encoding='utf-8'))}
    coding_path = private_path(root, coding_path)
    rows = list(csv.DictReader(coding_path.open(encoding='utf-8-sig', newline='')))
    if not rows or set(COLUMNS) - set(rows[0]):
        raise ValueError('coding.csv needs columns: ' + ', '.join(COLUMNS))
    return prepared, segments, rows, coding_path


def validate(segments, rows):
    concept_cat, cat_main = {}, {}
    for i, r in enumerate(rows, 2):
        if not all((r.get(k) or '').strip() for k in COLUMNS):
            raise ValueError(f'Row {i}: every column needs a value')
        s = segments.get(r['segment_id'])
        if s is None:
            raise ValueError(f"Row {i}: unknown segment_id {r['segment_id']} (use the ids in segments.json)")
        if s['speaker'] not in ('participant', 'observer'):
            raise ValueError(f"Row {i}: {s['speaker']} text is context, not codable evidence")
        if r['quote'] not in s['text']:
            raise ValueError(f'Row {i}: quote is not an exact excerpt of segment {s["id"]}')
        for child, parent, table, level in [(r['concept'], r['category'], concept_cat, 'concept'),
                                            (r['category'], r['main_category'], cat_main, 'category')]:
            if table.setdefault(child, parent) != parent:
                raise ValueError(f'Row {i}: {level} "{child}" is placed under both "{table[child]}" and "{parent}"')
    return concept_cat, cat_main


def tables(segments, rows, concept_cat, cat_main, order, holdout):
    by_concept = {}
    for r in rows:
        by_concept.setdefault(r['concept'], []).append(r)
    open_rows = [[concept_cat[c], c, len(rs), len({segments[r['segment_id']]['document_id'] for r in rs}),
                  f"{segments[rs[0]['segment_id']]['document_id']}：{rs[0]['quote']}"] for c, rs in sorted(by_concept.items(), key=lambda kv: (concept_cat[kv[0]], kv[0]))]
    axial = {}
    for c, cat in concept_cat.items():
        axial.setdefault(cat_main[cat], {}).setdefault(cat, []).append(c)
    axial_rows = [[m, '；'.join(sorted(cats)), sum(len(v) for v in cats.values())] for m, cats in sorted(axial.items())]
    docs = order or sorted({segments[r['segment_id']]['document_id'] for r in rows})
    seen_c, seen_k, sat_rows = set(), set(), []
    for d in docs:
        dc = {r['concept'] for r in rows if segments[r['segment_id']]['document_id'] == d}
        dk = {concept_cat[c] for c in dc}
        sat_rows.append([d, 'holdout' if d in holdout else 'model building', len(dc - seen_c), len(dk - seen_k),
                         '；'.join(sorted(dk - seen_k))])
        seen_c |= dc; seen_k |= dk
    return open_rows, axial_rows, sat_rows


def write_csv(path, header, rows):
    with open(path, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)


def md(header, rows):
    return ['| ' + ' | '.join(header) + ' |', '|' + '---|' * len(header)] + ['| ' + ' | '.join(str(x) for x in r) + ' |' for r in rows]


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser()
    ap.add_argument('--workspace', type=Path, default=Path('.'))
    ap.add_argument('--prepared', required=True)
    ap.add_argument('--coding', required=True)
    ap.add_argument('--actor', choices=['AI_assistant', 'researcher', 'simulated_researcher_test'], required=True)
    ap.add_argument('--parent')
    ap.add_argument('--order', default='', help='documents in coding order, comma separated')
    ap.add_argument('--holdout', default='', help='documents kept back for the saturation check')
    a = ap.parse_args()
    root = a.workspace.resolve()
    try:
        prepared, segments, rows, coding_path = load(root, a.prepared, a.coding)
        concept_cat, cat_main = validate(segments, rows)
        revisions = prepared / 'gt_revisions'; latest = prepared / 'gt_latest.json'
        if latest.exists() and a.parent != json.loads(latest.read_text(encoding='utf-8'))['revision']:
            raise ValueError('Missing or stale --parent revision; do not overwrite another edit')
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        out = revisions / stamp; out.mkdir(parents=True)
        shutil.copy2(coding_path, out / 'coding.csv')
        order = [d for d in a.order.split(',') if d]; holdout = {d for d in a.holdout.split(',') if d}
        open_rows, axial_rows, sat_rows = tables(segments, rows, concept_cat, cat_main, order, holdout)
        write_csv(out / 'open_coding.csv', ['范畴', '初始概念', '片段数', '受访者数', '原始语句示例'], open_rows)
        write_csv(out / 'axial_coding.csv', ['主范畴', '对应范畴', '概念数'], axial_rows)
        write_csv(out / 'saturation.csv', ['文档', '用途', '新增概念', '新增范畴', '新增范畴名称'], sat_rows)
        held = [r for r in sat_rows if r[1] == 'holdout']
        if not held:
            verdict = '没有预留访谈，不能做理论饱和检验；报告逐份新增情况，写"未进行饱和检验"或"饱和情况有限"。'
        elif all(r[2] == 0 and r[3] == 0 for r in held):
            verdict = '预留访谈没有出现新概念和新范畴，可报告通过理论饱和检验（还需确认范畴关系没有变化）。'
        else:
            verdict = '预留访谈仍出现新概念或新范畴，未达到饱和；应继续收集资料，或如实报告。'
        history = {'revision': stamp, 'parent': a.parent, 'actor': a.actor, 'coding_sha256': digest(out / 'coding.csv'),
                   'segments_sha256': digest(prepared / 'segments.json'), 'concepts': len(concept_cat),
                   'categories': len(cat_main), 'main_categories': len(set(cat_main.values())), 'saturation': verdict}
        (out / 'history.json').write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding='utf-8')
        lines = ['# 扎根理论编码结果', '', f'编码者：{a.actor}；概念 {len(concept_cat)} 个，范畴 {len(cat_main)} 个，主范畴 {len(set(cat_main.values()))} 个。', '',
                 '## 开放式编码', ''] + md(['范畴', '初始概念', '片段数', '受访者数', '原始语句示例'], open_rows) + \
                ['', '## 主轴编码', ''] + md(['主范畴', '对应范畴', '概念数'], axial_rows) + \
                ['', '## 逐份新增与饱和', ''] + md(['文档', '用途', '新增概念', '新增范畴', '新增范畴名称'], sat_rows) + ['', verdict, '']
        (out / 'coding_tables.md').write_text('\n'.join(lines), encoding='utf-8')
        latest.write_text(json.dumps({'revision': stamp}), encoding='utf-8')
        print(json.dumps({'revision': str(out), 'saturation': verdict}, ensure_ascii=False))
    except (ValueError, KeyError, FileNotFoundError) as error:
        ap.exit(2, str(error) + '\n')


if __name__ == '__main__':
    main()
