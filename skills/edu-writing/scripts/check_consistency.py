"""Scan a whole manuscript for internal inconsistencies that reviewers find first.

    python check_consistency.py --draft 论文.docx|.md|.txt [--term-group 学习投入=学习投入|学业投入|学习参与] [--json]
                                [--fail-on-findings]

Checks (Chinese and English manuscripts):
  abstract    numbers in the abstract that never occur in the body (a body value that rounds to it counts)
  sample      every sample-size statement (N = 512, 有效问卷 498 份, 312 students), grouped by value
  precision   one value printed at different precision (0.418 here, 0.42 there) and mixed p-value styles
  terms       variants of one construct supplied with --term-group, and stray self-reference variants
  acronyms    abbreviations used before their definition or defined more than once
  displays    tables and figures mentioned but not captioned, captioned but never mentioned, or first mentioned
              out of order
  citations   numbered citations [n] missing from the reference list, listed but never cited, or not numbered
              in order of first citation (GB/T 7714 sequential style)
Findings are prompts to re-read the passage, not automatic corrections: two equal numbers may be different
quantities, and two terms may name a real distinction.
"""
from pathlib import Path
import argparse
import json
import re
import sys
from collections import Counter, defaultdict

NUM = r'(?<![A-Za-z0-9_.])(\d+(?:,\d{3})*(?:\.\d+)?|\.\d+)(?![A-Za-z0-9_])'
SELF = {'zh': ['本研究', '本文', '笔者', '我们'], 'en': ['this study', 'this paper', 'this article', 'the present study',
                                                     'the current study', 'this work']}
# Chinese manuscripts write operators full-width (p＝0.03, F（2，495）) and minus as U+2212
FULLWIDTH = str.maketrans({'＝': '=', '＜': '<', '＞': '>', '（': '(', '）': ')', '−': '-', '＋': '+'})
SAMPLE = [r'\b[Nn]\s*=\s*(\d[\d,]*)', r'(?:有效|回收|共|获得|收集到?|发放)[^\d。；;]{0,8}?(\d[\d,]*)\s*(?:份|名|人|位)',
          r'样本(?:量|容量|规模)?(?:为|是|共)\s*(\d[\d,]*)', r'(\d[\d,]*)\s*(?:名|位)[一-鿿]{0,6}?(?:学生|教师|大学生|中学生|小学生|本科生|研究生|博士生|学习者|被试|受访者|参与者|儿童|幼儿)',
          r'\b(\d[\d,]*)\s+(?:participants|students|teachers|respondents|undergraduates|pupils|children|adults)\b']


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


def norm(n):
    n = n.replace(',', '')
    if '.' in n:
        n = n.rstrip('0').rstrip('.') or '0'
    return n[1:] if n.startswith('0.') else n


def decimals(n):
    return len(n.split('.')[1]) if '.' in n else 0


def ctx(text, start, end, width=30):
    return text[max(0, start - width):end + width].replace('\n', ' ').strip()


def split_parts(text, lang):
    """Return (abstract, body, references) using the usual headings; missing parts are empty strings."""
    lines = text.splitlines()
    abs_re = r'^\s*(?:#+\s*)?[【\[]?\s*摘\s*要\s*[】\]]?\s*[:：]?' if lang == 'zh' else r'^\s*(?:#+\s*)?abstract\b[:.]?'
    kw_re = (r'^\s*(?:#+\s*)?(?:\*\*)?[【\[]?\s*关键词\s*[】\]]?' if lang == 'zh'
             else r'^\s*(?:#+\s*)?(?:\*\*|_)?key\s*words?\b')
    ref_re = r'^\s*(?:#+\s*)?(?:参考文献|references|bibliography)\s*[:：]?\s*$'
    flags = re.I
    a_start = next((i for i, l in enumerate(lines) if re.match(abs_re, l, flags)), None)
    r_start = next((i for i, l in enumerate(lines) if re.match(ref_re, l, flags)), len(lines))
    abstract, body_start = '', 0
    if a_start is not None:
        end = next((i for i in range(a_start + 1, r_start) if re.match(kw_re, lines[i], flags) or re.match(r'^\s*#', lines[i])), None)
        if end is None:  # no keyword line or heading: the abstract is the first paragraph after its label
            i = a_start if re.sub(abs_re, '', lines[a_start], count=1, flags=flags).strip() else a_start + 1
            while i < r_start and not lines[i].strip():
                i += 1
            while i < r_start and lines[i].strip():
                i += 1
            end = i
        abstract = re.sub(abs_re, '', '\n'.join(lines[a_start:end]), count=1, flags=flags)
        body_start = end + 1 if end < r_start and re.match(kw_re, lines[end], flags) else end
    body = '\n'.join(lines[body_start:r_start])
    refs = '\n'.join(lines[r_start + 1:])
    return abstract, body, refs


def numbers(text):
    return [(m.group(1), m.start(), m.end()) for m in re.finditer(NUM, text)]


def check_abstract(abstract, body):
    values = {norm(n) for n, *_ in numbers(body)}
    floats = [float(v) for v in values if v]
    out = []
    for n, s, e in numbers(abstract):
        v = norm(n)
        if v in values or re.fullmatch(r'(19|20)\d\d', v) or re.fullmatch(r'\d', v):
            continue
        d, target = decimals(v if not v.startswith('.') else '0' + v), float(v)
        if any(abs(round(f * k, d) - target) < 1e-9 for f in floats for k in (1, 100, 0.01)):
            continue
        out.append({'value': n, 'context': ctx(abstract, s, e)})
    return out


def check_sample(text):
    found = defaultdict(list)
    for pattern in SAMPLE:
        for m in re.finditer(pattern, text):
            found[m.group(1).replace(',', '')].append(ctx(text, m.start(), m.end(), 20))
    return {k: v for k, v in sorted(found.items(), key=lambda kv: -int(kv[0]))}


STAT_LABEL = (r'(β|B|b|d\*?|g|r|R²|R2|p|t|F|z|OR|M|SD|SE|α|ω|CFI|TLI|RMSEA|SRMR|AVE|CR|HTMT|ICC(?:\([A-Z],\s*\d\))?|'
              r'η²|ηp²|χ²|f²)\s*(?:\([^)]{0,12}\))?\s*=\s*-?$')


def check_precision(text):
    """One statistic printed at different precision (β = 0.42 here, β = 0.418 there). Only numbers that follow the
    same statistic label are compared; unlabelled table cells and thresholds are left alone."""
    seen = defaultdict(lambda: defaultdict(set))
    for n, s, e in numbers(text):
        lab = re.search(STAT_LABEL, text[max(0, s - 16):s])
        if lab and '.' in n:
            seen[lab.group(1)][norm(n)].add(n)
    out = []
    for label, values in seen.items():
        for long in sorted(values, key=lambda v: -decimals('0' + v if v.startswith('.') else v)):
            dl = decimals('0' + long if long.startswith('.') else long)
            for d in range(1, dl):
                short = norm(f'{float(long):.{d}f}')
                printed = sorted(values.get(short, ()), key=decimals)
                if (printed and short != long and float('0' + short if short.startswith('.') else short) != 0
                        and decimals(printed[0]) < decimals(sorted(values[long])[0])):  # fewer printed decimals
                    out.append({'value': f'{label} = {sorted(values[long])[0]}', 'also_printed_as': printed[0]})
                    break
    p_styles = Counter('leading zero' if re.match(r'0\.', m.group(1)) else 'no leading zero'
                       for m in re.finditer(r'\b[pP]\s*[<=>≤]\s*(0?\.\d+)', text))
    zero = [ctx(text, m.start(), m.end(), 15) for m in re.finditer(r'\b[pP]\s*=\s*0?\.0+(?!\d*[1-9])', text)]
    return out, dict(p_styles) if len(p_styles) > 1 else {}, zero


FUNCTION_CHARS = set('的了在和与是对中为及等或也而被把从向于以之其这那各该本')


def keyword_groups(text, lang, full):
    """Variants one character away from a Chinese keyword (学习投入 / 学业投入), found without --term-group.
    Only inner characters are replaced, so a keyword followed by 的 or 在 is not taken for a variant."""
    if lang != 'zh':
        return []
    m = re.search(r'^\s*(?:#+\s*)?[【\[]?\s*关键词\s*[】\]]?\s*[:：]?\s*(.+)$', full, re.M)
    if not m:
        return []
    keywords = [k.strip() for k in re.split(r'[；;，,、\s]+', m.group(1)) if re.fullmatch(r'[一-鿿]{4,8}', k.strip())]
    groups = []
    for kw in keywords:
        variants = set()
        for i in range(1, len(kw) - 1):
            for v in re.findall(re.escape(kw[:i]) + r'([一-鿿])' + re.escape(kw[i + 1:]), text):
                cand = kw[:i] + v + kw[i + 1:]
                if cand != kw and v not in FUNCTION_CHARS and cand not in keywords:
                    variants.add(cand)
        if variants:
            groups.append((f'keyword {kw}', [kw, *sorted(variants)]))
    return groups


def check_terms(text, lang, groups, full=''):
    out = []
    groups = list(groups) + [g for g in keyword_groups(text, lang, full or text) if g[0].split(' ', 1)[1] not in sum((v for _, v in groups), [])]
    low = text.lower() if lang == 'en' else text
    for name, variants in groups:
        counts = {v: len(re.findall(re.escape(v.lower() if lang == 'en' else v), low)) for v in variants}
        if sum(1 for c in counts.values() if c) > 1:
            minority = [v for v, c in counts.items() if c and c < max(counts.values())]
            examples = [ctx(text, m.start(), m.end(), 20) for v in minority
                        for m in list(re.finditer(re.escape(v), text, re.I if lang == 'en' else 0))[:3]]
            out.append({'group': name, 'counts': counts, 'minority_contexts': examples})
    counts = {v: len(re.findall(re.escape(v), low)) for v in SELF[lang]}
    total = sum(counts.values())
    stray = [v for v, c in counts.items() if c and total >= 5 and c / total <= 0.15]
    self_ref = {'counts': {k: v for k, v in counts.items() if v}, 'stray': stray}
    return out, self_ref


COMMON_ABBR = {'AI', 'SD', 'SE', 'M', 'CI', 'OR', 'ICC', 'CFI', 'TLI', 'RMSEA', 'SRMR', 'AVE', 'CR', 'HTMT', 'ANOVA',
               'ANCOVA', 'DOI', 'URL', 'ID', 'PDF', 'APP', 'IT', 'GPA', 'IQ'}
ID_LIKE = r'(?:RQ|H|Q|S|T|R|E|N|C|P|M|A|B)\d+[a-z]?'


def check_acronyms(text, lang, body_offset=0):
    """Abbreviations used in the body before the body defines them, defined only in the abstract, or defined more
    than once in body prose. Definitions are 术语（ABC）, ABC＝术语 and ABC为术语 (English: term (ABC)); table rows,
    notes (注…) and numbering such as RQ1, H3 or Q12 are ignored, as are common statistical abbreviations."""
    pats = ([r'([一-鿿]{2,20})\s*[（(]\s*([A-Z][A-Za-z0-9\-]{1,9})\s*[）)]',
             r'(?<![A-Za-z])()([A-Z][A-Za-z0-9\-]{1,9})\s*(?:[=＝]|为|指)\s*[一-鿿]'] if lang == 'zh'
            else [r'([A-Za-z][A-Za-z\- ]{3,60}?)\s*\(\s*([A-Z][A-Za-z0-9\-]{1,9})\s*\)'])
    defs = defaultdict(list)  # acronym -> [(position, counts toward duplicates)]
    pos = 0
    for line in text.split('\n'):
        stripped = line.lstrip()
        if not stripped.startswith('|'):
            prose = pos >= body_offset and not re.match(r'(注|Note)', stripped)
            for pat in pats:
                for m in re.finditer(pat, line):
                    acr = m.group(2)
                    if (sum(ch.isupper() for ch in acr) >= 2 and acr not in COMMON_ABBR
                            and not re.fullmatch(ID_LIKE, acr)):
                        defs[acr].append((pos + m.start(2), prose))
        pos += len(line) + 1
    out = []
    for acr, found in defs.items():
        found.sort()
        body_defs = [p for p, _ in found if p >= body_offset]
        uses = [m.start() for m in re.finditer(r'(?<![A-Za-z])' + re.escape(acr) + r'(?![A-Za-z])', text)]
        body_uses = [u for u in uses if u >= body_offset]
        if body_defs and body_uses and body_uses[0] < body_defs[0] - 2 and '\n' in text[body_uses[0]:body_defs[0]]:
            u = body_uses[0]
            out.append({'acronym': acr, 'issue': 'used in the body before its definition', 'context': ctx(text, u, u + len(acr))})
        elif not body_defs and body_uses and body_offset:
            out.append({'acronym': acr, 'issue': 'defined only in the abstract'})
        prose_defs = sum(1 for _, prose in found if prose)
        if prose_defs > 1:
            out.append({'acronym': acr, 'issue': f'defined {prose_defs} times in the body'})
    return out


def check_displays(text, lang):
    out = []
    for kind, zh, en in [('table', '表', 'Table'), ('figure', '图', 'Figure|Fig\\.')]:
        cap = re.compile(rf'^[ \t]*(?:#+[ \t]*)?(?:{zh}\s*(\d+)(?=[\s:：.．、]|$)|(?:{en})\s*(\d+)[.:])', re.M)
        captions = {int(m.group(1) or m.group(2)) for m in cap.finditer(text)}
        caption_spans = {m.start() for m in cap.finditer(text)}
        mention = re.compile(rf'(?:{zh})\s*(\d+)|(?:{en})\s*(\d+)')
        mentions = []
        for m in mention.finditer(text):
            line_start = text.rfind('\n', 0, m.start()) + 1
            if line_start in caption_spans and text[line_start:m.start()].strip(' #') == '':
                continue  # the caption itself
            mentions.append(int(m.group(1) or m.group(2)))
        for n in sorted(set(mentions) - captions):
            out.append({'display': f'{kind} {n}', 'issue': 'mentioned but no caption found'})
        for n in sorted(captions - set(mentions)):
            out.append({'display': f'{kind} {n}', 'issue': 'captioned but never mentioned in the text'})
        order = list(dict.fromkeys(mentions))
        if order != sorted(order):
            out.append({'display': kind, 'issue': 'first mentions are out of order: ' + ', '.join(map(str, order))})
    return out


def expand(token):
    nums = []
    for part in re.split(r'[,，]', token):
        part = part.strip()
        m = re.fullmatch(r'(\d+)\s*[-–—~]\s*(\d+)', part)
        if m:
            nums += list(range(int(m.group(1)), int(m.group(2)) + 1))
        elif part.isdigit():
            nums.append(int(part))
    return nums


def check_citations(body, refs):
    cited = []
    for m in re.finditer(r'\[(\d+(?:\s*[,，\-–—~]\s*\d+)*)\]', body):
        cited += expand(m.group(1))
    listed = {int(m.group(1)) for m in re.finditer(r'^\s*\[(\d+)\]', refs, re.M)}
    if not cited and not listed:
        return []
    out = []
    if listed:
        missing = sorted(set(cited) - listed)
        unused = sorted(listed - set(cited))
        if missing:
            out.append({'issue': 'cited but not in the reference list', 'numbers': missing})
        if unused:
            out.append({'issue': 'in the reference list but never cited', 'numbers': unused})
    order = list(dict.fromkeys(cited))
    if order and order != list(range(1, len(order) + 1)):
        first_bad = next(i for i, n in enumerate(order) if n != i + 1)
        out.append({'issue': 'not numbered in order of first citation', 'first_mismatch': order[first_bad],
                    'expected': first_bad + 1})
    return out


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--draft', required=True, type=Path)
    ap.add_argument('--lang', choices=['zh', 'en'])
    ap.add_argument('--term-group', action='append', default=[], help='name=variant1|variant2|...')
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--fail-on-findings', action='store_true')
    a = ap.parse_args()
    text = read(a.draft)
    lang = a.lang or ('zh' if len(re.findall(r'[一-鿿]', text)) > len(re.findall(r'[A-Za-z]+', text)) else 'en')
    groups = []
    for g in a.term_group:
        name, _, variants = g.partition('=')
        groups.append((name.strip(), [v.strip() for v in variants.split('|') if v.strip()]))
    abstract, body, refs = split_parts(text.translate(FULLWIDTH), lang)
    precision, p_styles, p_zero = check_precision(abstract + '\n' + body)
    terms, self_ref = check_terms(abstract + '\n' + body, lang, groups, text)
    report = {
        'language': lang,
        'abstract_found': bool(abstract.strip()),
        'abstract_numbers_not_in_body': check_abstract(abstract, body) if abstract.strip() else [],
        'sample_sizes': check_sample(abstract + '\n' + body),
        'precision_drift': precision, 'p_value_styles': p_styles, 'p_equals_zero': p_zero,
        'term_groups': terms, 'self_reference': self_ref,
        'acronyms': check_acronyms(abstract + '\n' + body, lang, len(abstract) + 1 if abstract.strip() else 0),
        'displays': check_displays(body, lang),
        'citations': check_citations(body, refs),
    }
    findings = (len(report['abstract_numbers_not_in_body']) + len(precision) + len(p_zero) + bool(p_styles) + len(terms)
                + len(self_ref['stray']) + len(report['acronyms']) + len(report['displays']) + len(report['citations'])
                + (len(report['sample_sizes']) > 1))
    if a.json:
        print(json.dumps(report, ensure_ascii=False, indent=1))
    else:
        print(f'Language: {lang} | abstract found: {report["abstract_found"]} | findings to inspect: {findings}')
        print(f'\nAbstract numbers not found in the body: {len(report["abstract_numbers_not_in_body"])}')
        for h in report['abstract_numbers_not_in_body']:
            print(f'  {h["value"]}: …{h["context"]}…')
        print(f'\nSample-size statements ({len(report["sample_sizes"])} distinct values; check each is a named subsample):')
        for value, where in report['sample_sizes'].items():
            print(f'  {value}: ' + ' / '.join(f'…{w}…' for w in where[:3]))
        print(f'\nSame value at different precision: {len(precision)}')
        for h in precision:
            print(f'  {h["value"]} also printed as {h["also_printed_as"]}')
        if p_styles:
            print('  p-value styles are mixed: ' + ', '.join(f'{k} {v}' for k, v in p_styles.items()))
        for z in p_zero:
            print(f'  p printed as zero (write p < .001 / p < 0.001): …{z}…')
        print(f'\nTerm variants: {len(terms)}')
        for t in terms:
            print(f'  {t["group"]}: {t["counts"]}')
            for c in t['minority_contexts']:
                print(f'    …{c}…')
        if self_ref['counts']:
            print('  self-reference: ' + ', '.join(f'{k} {v}' for k, v in self_ref['counts'].items())
                  + (f' (stray: {", ".join(self_ref["stray"])})' if self_ref['stray'] else ''))
        print(f'\nAbbreviations: {len(report["acronyms"])}')
        for h in report['acronyms']:
            print(f'  {h["acronym"]}: {h["issue"]}' + (f' …{h["context"]}…' if h.get('context') else ''))
        print(f'\nTables and figures: {len(report["displays"])}')
        for h in report['displays']:
            print(f'  {h["display"]}: {h["issue"]}')
        print(f'\nNumbered citations: {len(report["citations"])}')
        for h in report['citations']:
            print('  ' + h['issue'] + ': ' + json.dumps({k: v for k, v in h.items() if k != 'issue'}, ensure_ascii=False))
    if a.fail_on_findings and findings:
        sys.exit(1)


if __name__ == '__main__':
    main()
