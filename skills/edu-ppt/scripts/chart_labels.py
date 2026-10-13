"""Declared label intent and OOXML plot -> series -> point correspondence.

Automatic labels keep Excel format codes. Literal custom text is checked only
when its numeric format can be resolved here; external/field labels fail closed.
"""
from decimal import Decimal, ROUND_HALF_UP, localcontext
import re

FLAGS = {'series': 'showSerName', 'category': 'showCatName', 'value': 'showVal'}
OTHER_FLAGS = ('showLegendKey', 'showPercent', 'showBubbleSize')


def label_spec(data, series=None, point=None):
    result = dict(visible=data.get('labels', True), content=data.get('label_content', ['value']),
                  number_format=data.get('number_format', 'General'), separator=data.get('label_separator', '\n'))
    for override in data.get('label_overrides', []):
        if (override['series'], override['point']) == (series, point):
            result.update({k: v for k, v in override.items() if k not in ('series', 'point')})
    return result


def validate_labels(data):
    overrides = data.get('label_overrides', [])
    if not isinstance(overrides, list):
        raise ValueError('label_overrides must be a list')
    seen = set()
    for item in overrides:
        if not isinstance(item, dict) or set(item) - {'series', 'point', 'visible', 'content', 'number_format', 'separator'}:
            raise ValueError('unsupported label override; use series/point and declared label settings')
        s, p = item.get('series'), item.get('point')
        if type(s) is not int or type(p) is not int or not (0 <= s < len(data['series']) and 0 <= p < len(data['categories'])):
            raise ValueError('label override index outside chart')
        if (s, p) in seen:
            raise ValueError('duplicate label override')
        seen.add((s, p))
    for spec in [label_spec(data), *[label_spec(data, s, p) for s, p in seen]]:
        content = spec['content']
        if not isinstance(content, list) or any(x not in FLAGS for x in content) or content != [x for x in FLAGS if x in content]:
            raise ValueError('label content must use series/category/value once, in that order')
        if type(spec['visible']) is not bool or (spec['visible'] and not content):
            raise ValueError('visible labels require content; visible/labels must be boolean')
        if not isinstance(spec['number_format'], str) or not spec['number_format'].strip() or not isinstance(spec['separator'], str):
            raise ValueError('label format and separator must be strings')


def _set(element, tag, value):
    from pptx.oxml.ns import qn
    from pptx.oxml.xmlchemy import OxmlElement
    child = element.find(qn('c:' + tag))
    if child is None:
        child = OxmlElement('c:' + tag)
        element.append(child)
    child.set('val', '1' if value else '0')


def apply_spec(element, spec, point=False):
    from pptx.oxml.ns import qn
    from pptx.oxml.xmlchemy import OxmlElement
    # OOXML uses a choice: delete OR the formatting/content group, not both.
    for deleted in element.findall(qn('c:delete')):
        element.remove(deleted)
    if point and not spec['visible']:
        for child in list(element):
            if child.tag != qn('c:idx'):
                element.remove(child)
        deleted = OxmlElement('c:delete')
        deleted.set('val', '1')
        element.append(deleted)
        return
    fmt = element.find(qn('c:numFmt'))
    if fmt is None:
        fmt = OxmlElement('c:numFmt')
        element.insert_element_before(fmt, 'c:spPr', 'c:txPr', 'c:dLblPos', 'c:showLegendKey',
                                      'c:showVal', 'c:showCatName', 'c:showSerName', 'c:showPercent',
                                      'c:showBubbleSize', 'c:separator', 'c:showLeaderLines', 'c:extLst')
    fmt.set('formatCode', spec['number_format'])
    fmt.set('sourceLinked', '0')
    for part, flag in FLAGS.items():
        _set(element, flag, spec['visible'] and part in spec['content'])
    for flag in OTHER_FLAGS:
        _set(element, flag, False)
    sep = element.find(qn('c:separator'))
    if sep is None:
        sep = OxmlElement('c:separator')
        element.insert_element_before(sep, 'c:showLeaderLines', 'c:leaderLines', 'c:extLst')
    sep.text = spec['separator']


def configure_labels(chart, data):
    base = label_spec(data)
    if chart.plots[0].has_data_labels:
        apply_spec(chart.plots[0].data_labels._element, base)
    touched = set()
    for item in data.get('label_overrides', []):
        si, pi = item['series'], item['point']
        series = chart.series[si]
        group = series._element.get_or_add_dLbls()
        if si not in touched:
            apply_spec(group, base)  # preserve defaults for the other points
            touched.add(si)
        point = series.points[pi].data_label._get_or_add_dLbl()
        apply_spec(point, label_spec(data, si, pi), point=True)


def format_literal(value, code):
    """Resolve common numeric formats, never guess an unsupported Excel format."""
    if code == 'General':
        return str(value).removesuffix('.0')
    match = re.fullmatch(r'(?P<pre>"[^"]*")?(?P<num>(?:#,##)?0(?:\.0+)?)(?P<pct>%?)(?P<post>"[^"]*")?', code)
    if not match:
        raise ValueError('literal label with unsupported Excel format ' + repr(code))
    number = Decimal(str(value)) * (100 if match['pct'] else 1)
    places = len(match['num'].split('.')[1]) if '.' in match['num'] else 0
    with localcontext() as ctx:
        ctx.prec = max(40, len(str(value)) + places + 10)
        rounded = number.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)
    text = format(rounded, (',' if ',' in match['num'] else '') + f'.{places}f')
    return (match['pre'] or '').strip('"') + text + match['pct'] + (match['post'] or '').strip('"')


def expected_text(data, si, pi, spec):
    parts = {'series': data['series'][si]['name'], 'category': data['categories'][pi]}
    if 'value' in spec['content']:
        parts['value'] = format_literal(data['series'][si]['values'][pi], spec['number_format'])
    return spec['separator'].join(parts[x] for x in spec['content'])


def check_labels(chart, data):
    from pptx.oxml.ns import qn
    issues = []

    def issue(scope, field, expected, actual, unverified=False):
        issues.append((scope, ('unverified.' if unverified else '') + field, expected, actual))

    def one(parent, tag, scope):
        matches = parent.findall(qn('c:' + tag)) if parent is not None else []
        if len(matches) > 1:
            issue(scope, tag, 'one setting', f'{len(matches)} settings', True)
        return matches[0] if matches else None

    def point_map(group, scope, count):
        result = {}
        if group is None:
            return result
        for label in group.findall(qn('c:dLbl')):
            idx = one(label, 'idx', scope)
            raw = idx.get('val') if idx is not None else None
            try:
                i = int(raw)
                if i < 0 or i >= count or i in result:
                    raise ValueError()
                result[i] = label
            except (ValueError, TypeError):
                issue(scope, 'point index', 'unique in-range point', raw, True)
        return result

    plot = one(chart.plots[0]._element, 'dLbls', 'plot')
    plot_points = point_map(plot, 'plot', len(data['categories']))
    for si, series in enumerate(chart.series):
        if si >= len(data['series']):
            continue  # existing series/order check reports the extra series
        group = one(series._element, 'dLbls', f'series[{si}]')
        points = point_map(group, f'series[{si}]', len(data['categories']))
        # Series-level extension labels (e.g. cell ranges) may sit outside dLbls.
        if series._element.xpath('./c:extLst'):
            issue(f'series[{si}]', 'label source', 'supported native labels', 'series extension not verified', True)
        for pi in range(len(data['categories'])):
            scope = f'series[{si}]/point[{pi}]'
            expected = label_spec(data, si, pi)
            actual = {flag: False for flag in (*FLAGS.values(), *OTHER_FLAGS)}
            actual.update(delete=False, number_format='General', linked=True, separator='\n', text=None)
            # A series dLbls replaces the plot group completely; its point
            # dLbl then overrides individual properties within that group.
            layers = [group, points.get(pi)] if group is not None else [plot, plot_points.get(pi)]
            for layer in layers:
                if layer is None:
                    continue
                known = {'idx','dLbl','delete','layout','tx','numFmt','spPr','txPr','dLblPos','separator',
                         'showLeaderLines','leaderLines',*FLAGS.values(),*OTHER_FLAGS}
                for child in layer:
                    if child.tag not in {qn('c:' + tag) for tag in known}:
                        issue(scope, 'label source', 'supported native settings', child.tag, True)
                for flag in (*FLAGS.values(), *OTHER_FLAGS, 'delete'):
                    node = one(layer, flag, scope)
                    if node is not None:
                        raw = node.get('val', '1')
                        if raw not in ('0','1','true','false'):
                            issue(scope, flag, 'boolean', raw, True)
                        actual[flag] = raw in ('1','true')
                fmt = one(layer, 'numFmt', scope)
                if fmt is not None:
                    actual['number_format'] = fmt.get('formatCode')
                    actual['linked'] = fmt.get('sourceLinked', '1') not in ('0','false')
                sep = one(layer, 'separator', scope)
                if sep is not None:
                    actual['separator'] = sep.text or ''
                tx = one(layer, 'tx', scope)
                if tx is not None:
                    rich = tx.find(qn('c:rich'))
                    if rich is None or len(tx) != 1 or rich.xpath('.//a:fld'):
                        issue(scope, 'label source', 'literal rich text or automatic components', 'reference/field text not verified', True)
                    else:
                        from pptx.text.text import TextFrame
                        actual['text'] = TextFrame(rich, None).text
            shown = not actual['delete'] and (actual['text'] is not None or any(actual[f] for f in (*FLAGS.values(), *OTHER_FLAGS)))
            if shown != expected['visible']:
                issue(scope, 'label visibility', expected['visible'], shown)
            if not shown:
                continue
            if actual['text'] is not None:
                try:
                    wanted = expected_text(data, si, pi, expected)
                    if actual['text'] != wanted:
                        issue(scope, 'custom label text', wanted, actual['text'])
                except ValueError as exc:
                    issue(scope, 'custom label format', 'resolvable planned display', str(exc), True)
            else:
                if actual['linked'] and actual['showVal']:
                    issue(scope, 'number format source', 'explicit format (sourceLinked=false)', 'workbook-linked format not verified', True)
                if actual['showVal'] and actual['number_format'] != expected['number_format']:
                    issue(scope, 'number format', expected['number_format'], actual['number_format'])
                content = [part for part, flag in FLAGS.items() if actual[flag]]
                if content != expected['content']:
                    issue(scope, 'label content', expected['content'], content)
                if len(content) > 1 and actual['separator'] != expected['separator']:
                    issue(scope, 'label separator', expected['separator'], actual['separator'])
                for flag in OTHER_FLAGS:
                    if actual[flag]:
                        issue(scope, flag, False, True, flag in ('showPercent','showBubbleSize'))
    return issues
