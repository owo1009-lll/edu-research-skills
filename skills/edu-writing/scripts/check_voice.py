"""Check the stance of a discussion or manuscript draft against published education articles.

Lists disclaimer sentences ("cannot establish", 尚不能证明), stacked hedges and limitation sentences
outside the limitations unit, and compares rates in the discussion/conclusion region with the corpus
medians in voice-en.md / voice-zh.md. Usage: python check_voice.py --draft <file.md|.txt|.docx>
"""
from pathlib import Path
import argparse, re, sys

LEX = {
    'en': {
        'hedge': r"\b(may|might|could|would|possibly|possible|perhaps|maybe|likely|unlikely|probably|probable|plausibl[ey]|presumably|apparently|seem(?:s|ed|ingly)?|appear(?:s|ed)?|suggest(?:s|ed|ing|ive)?|tend(?:s|ed)? to|somewhat|relatively|partly|partially|largely|to (?:some|a certain) extent|in part|tentative(?:ly)?|potentially|not necessarily|uncertain|unclear|preliminary|speculative|arguably|conceivably)\b",
        'limitation': r"\b(limitations?|limited|caution(?:s|ary)?|cautious(?:ly)?|generali[sz]\w*|cannot|unable|caveats?|should be interpreted|not possible to|future (?:research|studies|work))\b",
        'self': r"\b(we|our|us|this (?:study|research|paper|article)|the (?:present|current) (?:study|research))\b",
        'disclaimer': r"\b((?:does|do|did|can|could|should|is|are|was|were)(?:n't| not|not)\s+(?:necessarily\s+|directly\s+|simply\s+|by itself\s+|alone\s+)?(?:be\s+)?(?:mean|imply|show|establish|prove|indicate|demonstrate|identify|determine|equate|generali[sz]e|attribut|interpret|tak|read|license|warrant|support a causal|evidence)\w*|not (?:evidence|proof) (?:of|that)|cannot (?:rule out|distinguish|separate|tell))",
    },
    'zh': {
        'hedge': r"(或许|也许|大概|大致|似乎|好像|一定程度|某种程度|相对(?!于|应)|较为|基本上|倾向于|推测|初步|有待|尚需|尚待|仍需|不一定|未必|或可|可以认为|不排除|可能)",
        'limitation': r"(局限|不足之处|研究不足|存在不足|未能|谨慎|不宜推广|推广到|推广性|代表性|样本量较小|样本较小|未来研究|后续研究)",
        'self': r"(本研究|本文|笔者|我们)",
        'disclaimer': r"((?:尚|并|还|仍|也)?不能(?:据此|由此|因此|直接|简单地?|仅凭|仅据|就此|以此|完全)?(?:说明|证明|表明|推断|推导|推出|认定|断言|得出|归因|归结|确定|区分|代表|视为|解释为|理解为|等同|判断|外推|推广到)|不能(?:把|将)[^，。；]{0,24}?(?:理解为|解释为|视为|等同|归因|归结|当作|看作|推导为)|不能因[^，。；]{0,30}?就(?:断言|认定|认为|推断|判断)|不宜(?:视为|理解为|解读为|推广|外推|据此|直接|过度|简单)|不宜(?:把|将)[^，。；]{0,24}?(?:视为|理解为|等同|当作)|不足以(?:说明|证明|支持|表明|推断|形成|确定)|尚无法|无法(?:确定|区分|判断|排除|推断|证明|说明)|难以(?:判断|区分|确定|排除|推断)|尚待(?:检验|验证)|有待(?:进一步)?(?:检验|验证))",
    },
}
# (published median, bound of the typical range) in the discussion/conclusion region; see voice-*.md.
# Chinese papers rarely have a limitations section and use few self-mentions, so only disclaimers are compared.
REFERENCE = {
    'en': {'disclaimer_sent_pct': (0.9, 1.7), 'self_per1k': (10.8, 7.8), 'limitation_in_unit_pct': (66.7, 28.6)},
    'zh': {'disclaimer_sent_pct': (0.0, 2.0)},
}
LIMIT_HEAD = r'(limitation|局限|不足与展望|研究不足|研究展望)'
FOCUS_HEAD = r'(discussion|conclu|implication|limitation|讨论|结论|结语|启示|建议|局限|不足|展望)'
STOP_HEAD = (r'^(\d+(\.\d+)*\.?\s*)?(references|bibliography|参考文献|注释|声明|致谢|附录|基金|利益冲突|作者贡献|数据可用性|'
             r'declarations?|acknowledg|funding|appendix|data availability|conflicts? of interest|author contributions)')

def read(path):
    """Text of a .docx in document order (headings as '#' lines, table rows as '| a | b |') or of a text file."""
    if path.suffix.lower() == '.docx':
        import docx
        from docx.oxml.ns import qn
        d = docx.Document(path)
        names = {s.style_id: s.name for s in d.styles}
        parts = []
        for child in d.element.body.iterchildren():
            if child.tag == qn('w:p'):
                text = ''.join(t.text or '' for t in child.iter(qn('w:t')))
                style = child.find(qn('w:pPr') + '/' + qn('w:pStyle'))
                name = names.get(style.get(qn('w:val')), '') if style is not None else ''
                level = 1 if name == 'Title' else int(name[8:]) if re.fullmatch(r'Heading \d', name) else 0
                parts.append('#' * level + ' ' + text if level and text.strip() else text)
            elif child.tag == qn('w:tbl'):
                for tr in child.iter(qn('w:tr')):
                    cells = [''.join(t.text or '' for t in tc.iter(qn('w:t'))) for tc in tr.iter(qn('w:tc'))]
                    parts.append('| ' + ' | '.join(cells) + ' |')
        return '\n'.join(parts)
    return path.read_text(encoding='utf-8', errors='ignore')


def paragraphs(text):
    """Yield (heading_kind, paragraph) with kind in {'focus', 'limits', 'other'}."""
    kind, out = 'other', []
    kind_level = 0  # level of the heading that set the current kind
    marked = bool(re.search(r'^## [A-Z+]+ \|', text, re.M))
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        head = re.match(r'^(## [A-Z+]+ \|\s*|#{1,4}\s+|[一二三四五六七八九十]+、|（[一二三四五六七八九十]+）|\d+(\.\d+)*\.?\s+)(.{1,80})$', s)
        if head and (not marked or s.startswith('## ')):
            title = head.group(3).lower() + (s if marked else '').lower()
            if re.search(STOP_HEAD, head.group(3).lower()):
                break
            mark = head.group(1).strip()
            level = (1 if marked else len(mark) if mark.startswith('#') else 1 if mark.endswith('、') else 2 if mark.startswith('（') else mark.count('.') + 1)
            sub = re.match(r'^(（[一二三四五六七八九十]+）|\d+(\.\d+)*\.?)', head.group(3))
            if sub:  # '## （一）…' or '### 5.1 …': the number sets the depth
                level += 1
            if re.search(LIMIT_HEAD, title):
                kind, kind_level = 'limits', level
            elif re.search(FOCUS_HEAD, title):
                kind, kind_level = 'focus', level
            elif kind in ('focus', 'limits') and level > kind_level:
                pass  # an untitled-by-keyword subsection inherits its parent's kind
            else:
                kind, kind_level = 'other', level
            continue
        out.append((kind, s))
    if not any(k in ('focus', 'limits') for k, _ in out):
        out = [('focus', p) for _, p in out]  # a bare discussion text
    # without a heading, a paragraph that opens on limitations is the limitations unit
    lead = r'^[^.。]{0,60}?(limitations?\b|limits\b|局限|不足之处|存在(?:以下|一定的?|若干)?不足)'
    return [('limits' if k == 'focus' and re.search(lead, p, re.I) else k, p) for k, p in out]

def sentences(p, lang):
    parts = re.split(r'(?<=[。！？；!?;])' if lang == 'zh' else r'(?<=[.!?])\s+(?=[A-Z“"(])', p)
    return [x.strip() for x in parts if len(x.strip()) > (8 if lang == 'zh' else 20)]

# ASCII boundaries: in Python \w also matches Chinese characters, which would hide every number written as 为0.42
NUM = r'(?<![A-Za-z0-9_.])(\d+(?:[.,]\d+)?|\.\d+)(?![A-Za-z0-9_])'
CITE = r'\[\d+(?:\s*[,，\-–—~]\s*\d+)*\]'  # GB/T 7714 citation marks such as [7,8] or [12-15]

def norm_num(n):
    n = n.replace(',', '')
    if '.' in n:
        n = n.rstrip('0').rstrip('.') or '0'
        n = n[1:] if n.startswith('0.') else n
    return n

WORDS = {w: str(i) for i, w in enumerate('zero one two three four five six seven eight nine ten eleven twelve'.split())}
TIME = r'(\d+(?:\.\d+)?)\s*-?\s*(分钟|小时|天|周|个月|min(?:ute)?s?\b|h\b|hours?\b|days?\b|weeks?\b|months?\b)'
UNIT = {'分钟': 'min', '小时': 'h', '天': 'd', '周': 'w', '个月': 'mo'}

def time_pairs(text):
    text = re.sub(r'\b(' + '|'.join(WORDS) + r')\b', lambda m: WORDS[m.group(1).lower()], text, flags=re.I)
    pairs = set()
    for n, u in re.findall(TIME, text, re.I):
        u = u.lower()
        key = UNIT.get(u) or ('min' if u.startswith('min') else 'h' if u.startswith('h') else u[0] if u[0] in 'dw' else 'mo')
        pairs.add((norm_num(n), key))
    return pairs

def manuscript_text(text):
    """The whole draft up to the references or back matter, for the number check."""
    lines = []
    for line in text.splitlines():
        head = re.match(r'^(#{1,4}\s*|[一二三四五六七八九十]+、)?(.{1,80})$', line.strip())
        if head and re.search(STOP_HEAD, head.group(2).strip().lower()):
            break
        if re.match(r'^\s*#{1,6}\s', line):
            continue  # section numbers in headings are not claims
        lines.append(line)
    return '\n'.join(lines)

def unsupported_numbers(draft, sources):
    """Numbers (and number+time-unit pairs) in the draft that never occur in the source materials."""
    texts = [re.sub(CITE, ' ', read(src)) for src in sources]
    draft = re.sub(CITE, ' ', draft)
    known = {norm_num(m) for t in texts for m in re.findall(NUM, t)}
    values = {float(k) for k in known if k}
    known_time = set().union(*(time_pairs(t) for t in texts))

    def rounded_from_source(n):
        """A draft value counts as sourced when a source value rounds to it, also as a percentage (0.418 -> 0.42 or 41.8%)."""
        digits = len(n.split('.')[1]) if '.' in n else 0
        target = float(n)
        return any(abs(round(v * f, digits) - target) < 1e-9 for v in values for f in (1, 100, 0.01))

    hits = []
    for m in re.finditer(NUM, draft):
        n = norm_num(m.group(1))
        if n in known or re.fullmatch(r'(19|20)\d\d', n) or re.fullmatch(r'\d', n) or rounded_from_source(n):
            continue
        hits.append(draft[max(0, m.start() - 24):m.end() + 12].replace('\n', ' '))
    for m in re.finditer(TIME, draft, re.I):
        if not time_pairs(m.group(0)) <= known_time:
            hits.append(draft[max(0, m.start() - 24):m.end() + 12].replace('\n', ' '))
    return hits

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser()
    ap.add_argument('--draft', required=True, type=Path)
    ap.add_argument('--lang', choices=['zh', 'en'])
    ap.add_argument('--source', type=Path, nargs='*', default=[], help='materials, results or manuscript the draft is based on')
    a = ap.parse_args()
    text = read(a.draft)
    lang = a.lang or ('zh' if len(re.findall(r'[一-鿿]', text)) > len(re.findall(r'[A-Za-z]+', text)) else 'en')
    lex, flags = LEX[lang], (0 if lang == 'zh' else re.I)
    paras = [(k, p) for k, p in paragraphs(text) if k in ('focus', 'limits')]
    sents = [(k, i, s) for i, (k, p) in enumerate(paras, 1) for s in sentences(p, lang)]
    body = '\n'.join(p for _, p in paras)
    units = len(re.findall(r'[一-鿿]', body)) if lang == 'zh' else len(re.findall(r"[A-Za-z][A-Za-z'-]*", body))
    if not sents or not units:
        print('No discussion/conclusion text found.'); return
    disc = [(i, s) for k, i, s in sents if k == 'focus' and re.search(lex['disclaimer'], s, flags)]
    # counterfactual tests ("if X, we would have expected Y" / 若……则应……) are reasoning, not stacked hedges
    counterfactual = r'\bif\b[^.]*\bwould(?: not)? have\b|\bwould(?: not)? have\b[^.]*\bif\b|若[^。]{0,40}则应|如果[^。]{0,40}应当会'
    stacked = [(i, s) for k, i, s in sents if len(re.findall(lex['hedge'], s, flags)) >= 2
               and not re.search(counterfactual, s, re.I)]
    lims = [(k, i, s) for k, i, s in sents if re.search(lex['limitation'], s, flags)]
    stray = [(i, s) for k, i, s in lims if k != 'limits']
    focus = [s for k, _, s in sents if k == 'focus']  # the limitations unit may say what cannot be inferred
    disc_pct = 100 * len(disc) / len(focus) if focus else None
    self_rate = 1000 * len(re.findall(lex['self'], body, flags)) / units
    in_unit = 100 * (len(lims) - len(stray)) / len(lims) if lims else None
    unit = '千字' if lang == 'zh' else '1,000 words'
    print(f'Language: {lang} | discussion/conclusion sentences: {len(sents)} | paragraphs: {len(paras)}')
    ref = REFERENCE[lang]
    def line(name, val, key, higher_is_better):
        if val is None:
            print(f'  {name}: n/a'); return
        msg = f'  {name}: {val:.1f}'
        if key in ref:
            med, bound = ref[key]
            bad = val < bound if higher_is_better else val > bound
            msg += f'  (published median {med}; {"outside" if bad else "within"} typical range)'
        print(msg)
    line('Disclaimer sentences in the discussion body (%)', disc_pct, 'disclaimer_sent_pct', False)
    line(f'Self-mention per {unit}', self_rate, 'self_per1k', True)
    line('Limitation sentences inside the limitations unit (%)', in_unit, 'limitation_in_unit_pct', True)
    for title, items in (('Disclaimer sentences in the discussion body', disc),
                         ('Sentences with two or more hedges', stacked),
                         ('Limitation sentences outside the limitations unit', stray)):
        print(f'\n{title}: {len(items)}')
        for i, s in items:
            print(f'  [para {i}] {s[:160]}')
    if a.source:
        hits = unsupported_numbers(manuscript_text(text), a.source)
        print(f'\nNumbers not found in the sources (derived values are fine; invented details are not): {len(hits)}')
        for h in hits:
            print(f'  …{h}…')

if __name__ == '__main__':
    main()
