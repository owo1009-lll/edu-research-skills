"""Check a grant-application draft: word counts (total and per section), identity leaks, unsupported superlatives.

Usage: python check_proposal.py --draft 活页.docx|.md|.txt [--preset qgjk] [--limit 7000]
                                [--section-limit 选题说明=300] [--identity "姓名,单位"]
--preset qgjk applies the 2026 National Education Science Planning review-sheet limits (total 7000; 选题说明 and
研究基础 300 each); check the current year's template and override with --limit / --section-limit when they change.
Counts follow Word for Chinese text: each Chinese character or full-width punctuation mark counts as one, and each
run of Latin letters or digits as one word. Sub-headings such as （一） or 3.1 count toward their parent section.
"""
from pathlib import Path
import argparse
import re
import sys

TOP = [re.compile(r'^#{1,2}\s*(.+)$'), re.compile(r'^[一二三四五六七八九十]+[、.．]\s*(.+)$'),
       re.compile(r'^\d+\s*[.．、]\s*\[([^\]]+)\]'), re.compile(r'^\d+\s*[.．、]\s*(\S.{0,20})$'), re.compile(r'^\[([^\]]+)\]')]
PRESETS = {'qgjk': {'total': 7000, 'sections': {'选题说明': 300, '研究基础': 300}}}
IDENTITY = [r'本人(?:主持|承担|负责|前期|已|曾)', r'我校', r'我院', r'我所', r'本单位', r'笔者所在', r'课题负责人[:：]', r'申请人[:：]']
OVERCLAIM = [r'填补[了]?\S{0,8}空白', r'(?:国内|国际|国内外)首次', r'首次(?:提出|将|系统|构建)', r'首创', r'率先', r'开创性', r'国际领先',
             r'国内领先', r'前所未有', r'独创']


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


def count(text):
    cjk = len(re.findall(r'[一-鿿　-〿＀-￯]', text))
    return cjk + len(re.findall(r'[A-Za-z0-9]+(?:[.\'-][A-Za-z0-9]+)*', text))


def top_heading(line):
    if re.match(r'^(#{3,}|（[一二三四五六七八九十]+）|\d+\.\d+)', line):
        return None  # sub-heading: belongs to the current section
    for pattern in TOP:
        m = pattern.match(line)
        if m and len(m.group(1)) <= 24:
            return re.sub(r'[\[\]【】]', '', m.group(1)).strip()
    return None


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser()
    ap.add_argument('--draft', required=True, type=Path)
    ap.add_argument('--preset', choices=sorted(PRESETS))
    ap.add_argument('--limit', type=int, help='total word limit from the current call for applications')
    ap.add_argument('--section-limit', action='append', default=[], help='name=limit, e.g. 研究基础=300')
    ap.add_argument('--identity', default='', help='comma-separated names and units that must not appear')
    a = ap.parse_args()
    preset = PRESETS.get(a.preset, {'total': None, 'sections': {}})
    total_limit = a.limit or preset['total']
    section_limits = dict(preset['sections'])
    for item in a.section_limit:
        name, _, value = item.partition('=')
        section_limits[name.strip()] = int(value)
    text = read(a.draft)
    sections, current = {}, '（开头）'
    for line in text.splitlines():
        line = line.strip()
        name = top_heading(line) if line else None
        if name:
            current = name; sections.setdefault(current, 0); continue
        sections[current] = sections.get(current, 0) + count(line)
    total = count(text)
    print(f'Total words: {total}' + (f' / limit {total_limit} ({"OVER by " + str(total - total_limit) if total > total_limit else "within limit"})' if total_limit else ''))
    for name, n in sections.items():
        limit = next((v for k, v in section_limits.items() if k in name), None)
        if n or limit:
            print(f'  {name}: {n}' + (f' / {limit} ({"OVER" if n > limit else "ok"})' if limit else ''))
    missing = [k for k in section_limits if not any(k in name for name in sections)]
    if missing:
        print('  sections with a limit that were not found: ' + ', '.join(missing))
    terms = [t.strip() for t in a.identity.split(',') if t.strip()]
    lines = text.splitlines()
    hits = [(t, l.strip()) for l in lines for t in terms if t in l]
    hits += [(re.search(p, l).group(0), l.strip()) for l in lines for p in IDENTITY if re.search(p, l)]
    print(f'\nPossible identity leaks: {len(hits)}')
    for t, l in hits:
        print(f'  [{t}] {l[:100]}')
    claims = [(re.search(p, l).group(0), l.strip()) for l in lines for p in OVERCLAIM if re.search(p, l)]
    print(f'\nClaims that need support from the literature review: {len(claims)}')
    for t, l in claims:
        print(f'  [{t}] {l[:100]}')


if __name__ == '__main__':
    main()
