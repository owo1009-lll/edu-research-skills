"""Shared plan validation and readable exports. No model API or hidden analysis."""
from pathlib import Path
import hashlib
import json
import math


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_plan(path):
    value = json.loads(Path(path).read_text(encoding='utf-8-sig'))
    validate(value)
    return value


def validate(plan):
    def require(test, message):
        if not test:
            raise ValueError(message)

    def nonempty(value):
        return isinstance(value, str) and bool(value.strip())

    def number(value):
        return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)

    require(plan.get('route') in ('own', 'article'), 'route must be own or article')
    require(nonempty(plan.get('title')), 'title is required')
    require(number(plan.get('minutes')) and plan['minutes'] > 0, 'minutes must be positive')
    if plan['route'] == 'own':
        require(plan.get('stage') in ('completed', 'proposal', 'progress'), 'own requires stage')
    require(isinstance(plan.get('sources'), list) and plan['sources'], 'sources are required')
    sources = {}
    for source in plan['sources']:
        require(nonempty(source.get('id')) and source['id'] not in sources, 'source ids must be unique')
        require(nonempty(source.get('title')), 'source title is required')
        require(source.get('access') in ('fulltext', 'abstract', 'title', 'author_material'), 'invalid reading scope')
        sources[source['id']] = source
    require(isinstance(plan.get('slides'), list) and plan['slides'], 'slides are required')
    ids = set()
    for slide in plan['slides']:
        sid = slide.get('id')
        require(nonempty(sid) and sid not in ids, 'slide ids must be nonempty and unique')
        ids.add(sid)
        for field in ('title', 'message', 'notes', 'visual_plan'):
            require(nonempty(slide.get(field)), f'{sid}: {field} is required')
        require(number(slide.get('seconds')) and slide['seconds'] > 0, f'{sid}: positive seconds required')
        require(slide.get('role') in ('finding', 'author_interpretation', 'presenter_comment', 'plan', 'background', 'method'), f'{sid}: invalid role')
        require(slide.get('status') in ('completed', 'preliminary', 'planned', 'not_applicable'), f'{sid}: explicit status required')
        require(isinstance(slide.get('body', []), list) and all(nonempty(x) for x in slide.get('body', [])), f'{sid}: body must contain text')
        evidence = slide.get('evidence')
        require(isinstance(evidence, list) and evidence, f'{sid}: evidence or rationale source required')
        for ref in evidence:
            require(ref.get('source') in sources, f'{sid}: unknown source')
            require(nonempty(ref.get('location')) and nonempty(ref.get('supports')), f'{sid}: source location and supported claim required')
            if sources[ref['source']]['access'] == 'title':
                require(slide['role'] in ('background', 'presenter_comment'), f'{sid}: title-only source cannot support methods/results')
        if plan.get('stage') == 'proposal':
            require(slide['role'] != 'finding' or slide['status'] == 'preliminary', f'{sid}: a proposal cannot imply completed findings')
        visual = slide.get('visual', {})
        kind = visual.get('type')
        require(kind in (None, 'table', 'chart', 'interval', 'image', 'process', 'quote'), f'{sid}: unsupported visual type')
        if kind == 'table':
            columns, rows = visual.get('columns', []), visual.get('rows', [])
            require(bool(columns) and bool(rows) and all(len(row) == len(columns) for row in rows), f'{sid}: ragged/empty table')
        if kind == 'chart':
            require(visual.get('kind', 'column') in ('column', 'bar', 'line'), f'{sid}: invalid chart kind')
            require(bool(visual.get('categories')) and bool(visual.get('series')), f'{sid}: chart data missing')
            for series in visual['series']:
                require(nonempty(series.get('name')) and len(series.get('values', [])) == len(visual['categories']) and all(number(x) for x in series['values']), f'{sid}: invalid chart series')
            require(nonempty(visual.get('unit')), f'{sid}: chart units required')
        if kind == 'interval':
            bounds = visual.get('range', [])
            require(len(bounds) == 2 and all(number(x) for x in bounds) and bounds[0] < bounds[1], f'{sid}: interval range invalid')
            require(bool(visual.get('rows')) and nonempty(visual.get('unit')), f'{sid}: interval data and unit required')
            for row in visual['rows']:
                require(all(number(row.get(k)) for k in ('estimate', 'low', 'high')), f'{sid}: interval values invalid')
                require(bounds[0] <= row['low'] <= row['estimate'] <= row['high'] <= bounds[1], f'{sid}: clipped/reversed confidence interval')
        if kind == 'process':
            require(bool(visual.get('steps')) and all(nonempty(x) for x in visual['steps']), f'{sid}: process steps required')
        if kind == 'image':
            require(nonempty(visual.get('path')) and nonempty(visual.get('caption')), f'{sid}: image path/caption required')
        if kind == 'quote':
            require(nonempty(visual.get('text')) and nonempty(visual.get('attribution')), f'{sid}: quote text/attribution required')
    return plan


def reference_text(plan, slide):
    sources = {s['id']: s for s in plan['sources']}
    parts = []
    for ref in slide['evidence']:
        src = sources[ref['source']]
        label = src.get('short', src['id'])
        text = f"{label} · {ref['location']}"
        if text not in parts:
            parts.append(text)
    return '; '.join(parts)


def readable_visual(visual):
    def table(columns, rows):
        cell = lambda value: str(value).replace('|', '\\|').replace('\n', '<br>')
        line = lambda row: '| ' + ' | '.join(cell(v) for v in row) + ' |'
        return [line(columns), line(['---'] * len(columns)), *[line(row) for row in rows], '']

    kind = visual['type']
    if kind == 'table':
        result = table(visual['columns'], visual['rows'])
    elif kind == 'interval':
        result = table(['项目', '估计', '区间下限', '区间上限'],
                       [[r['label'], r['estimate'], r['low'], r['high']] for r in visual['rows']])
        result += [f"单位：{visual['unit']}；显示范围：{visual['range'][0]} 至 {visual['range'][1]}。", '']
    elif kind == 'chart':
        result = table(['类别', *[s['name'] for s in visual['series']]],
                       [[label, *[s['values'][i] for s in visual['series']]] for i, label in enumerate(visual['categories'])])
        result += [f"图表单位：{visual['unit']}。", '']
    elif kind == 'process':
        result = [f'{i}. {step}' for i, step in enumerate(visual['steps'], 1)] + ['']
    elif kind == 'quote':
        result = ['> ' + line for line in visual['text'].split('\n')] + ['', visual['attribution'], '']
    else:
        result = [f"原图文件：{visual['path']}。按图表安排插入，保留原图标签与比例。", '']
    if visual.get('caption'):
        result += ['图注：' + visual['caption'], '']
    return result


def export_text(plan, out):
    out = Path(out)
    stage = {'completed': '完成论文', 'proposal': '研究方案', 'progress': '阶段进展'}.get(plan.get('stage'), '文章解读')
    content = [f"# {plan['title']}", '', f"汇报类型：{stage}；计划时长：{plan['minutes']}分钟。", '']
    notes = [f"# {plan['title']}：逐页讲稿", '']
    for i, slide in enumerate(plan['slides'], 1):
        heading = f"## {i}. {slide['title']}"
        content += [heading, '', f"核心信息：{slide['message']}", '']
        if slide.get('body'):
            content += ['上屏正文：', '']
            content += ['- ' + text.replace('\n', '\n  ') for text in slide['body']]
        content += ['', f"图表安排：{slide['visual_plan']}", '']
        if slide.get('visual'):
            content += readable_visual(slide['visual'])
        content += [f"来源：{reference_text(plan, slide)}", f"预计：{slide['seconds']}秒", '', '讲稿：', '', slide['notes'], '']
        notes += [heading, '', f"预计{slide['seconds']}秒", '', slide['notes'], '', f"来源：{reference_text(plan, slide)}", '']
    content += ['## 来源与阅读范围', '']
    for src in plan['sources']:
        scope = {'fulltext': '全文', 'abstract': '摘要', 'title': '仅题名', 'author_material': '作者提供的材料'}[src['access']]
        content += [f"- [{src['id']}] {src['title']} ({src.get('year', 'n.d.')}); {src.get('authors', '')}; {src.get('venue', '')}. DOI: {src.get('doi', '—')}. {src.get('url', '')} 阅读范围：{scope}。"]
    out.mkdir(parents=True, exist_ok=True)
    (out / 'content.md').write_text('\n'.join(content) + '\n', encoding='utf-8')
    (out / 'speaker_notes.md').write_text('\n'.join(notes) + '\n', encoding='utf-8')
