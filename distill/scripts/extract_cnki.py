"""Extract CNKI journal PDFs (one- or two-column) into section-tagged text for stance analysis.

Output format matches the English corpus: '# title', then '## TAG | heading' markers.
Usage: python extract_cnki.py --list ids.json --src <pdf dir> --out <dir>
ids.json: [{"id": "ZH01", "file": "<pdf name>"}, ...]
"""
from pathlib import Path
import argparse, json, re, sys
import fitz

TOP = re.compile(r'^([一二三四五六七八九十]+)\s*[、.．]\s*(.{1,40})$')
SUB = re.compile(r'^[（(]([一二三四五六七八九十]+)[）)]\s*(.{1,40})$')
DROP = re.compile(r'(收稿日期|修回日期|DOI编码|DOI：|基金项目|作者简介|中图分类号|文献标识码|文章编号|Vol\.|China Academic Journal|^·\s*\d+\s*·$|^\d+$|网络首发|引用格式|本文系)')
STOP = re.compile(r'^[\[【（(]?\s*(参\s*考\s*文\s*献|注\s*释|责任编辑)')
TAGS = [('LIMITATIONS', r'(局限|不足|展望)'), ('IMPLICATIONS', r'(启示|建议|对策|政策含义|策略|路径)'),
        ('DISCUSSION', r'讨论'), ('CONCLUSION', r'(结论|结语|结束语|总结|小结)'),
        ('RESULTS', r'(研究结果|研究发现|结果|数据分析|实证分析|分析与|发现)'),
        ('METHOD', r'(研究设计|研究方法|研究对象|数据来源|方法|设计)'),
        ('LITERATURE', r'(文献|理论|假设|框架|概念|综述|回顾)'),
        ('INTRODUCTION', r'(引言|问题的?提出|导言|研究背景|缘起)')]

def tags_for(heading, top):
    found = []
    for tag, pat in TAGS:
        if not top and tag == 'IMPLICATIONS':
            pat = r'(启示|建议|对策|政策含义)'  # 路径/策略 in subheadings usually name a finding
        if re.search(pat, heading) and tag not in found:
            found.append(tag)
    end = [t for t in found if t in ('DISCUSSION', 'CONCLUSION', 'IMPLICATIONS', 'LIMITATIONS')]
    if end:
        return '+'.join(sorted(end, key=['DISCUSSION', 'CONCLUSION', 'IMPLICATIONS', 'LIMITATIONS'].index))
    if not top:
        return None  # ordinary subheading
    return found[0] if found else 'OTHER'

def norm(t):
    """Full-width ASCII letters/digits/brackets to half-width; keep Chinese punctuation."""
    out = []
    for ch in t:
        c = ord(ch)
        if 0xFF10 <= c <= 0xFF19 or 0xFF21 <= c <= 0xFF3A or 0xFF41 <= c <= 0xFF5A or ch in '［］．＠－＋＝／＜＞＿':
            ch = chr(c - 0xFEE0)
        out.append(ch)
    return ''.join(out).replace('\xa0', ' ').replace('　', ' ')

def page_lines(page):
    """Return lines in reading order as (x0, base_x0, text); merges fragments that share a baseline."""
    w, h = page.rect.width, page.rect.height
    mid = w / 2
    raw = []
    for b in page.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            t = norm(''.join(s['text'] for s in l['spans'])).strip()
            if not t:
                continue
            x0, y0, x1, y1 = l['bbox']
            if y0 < 80 or y0 > h - 60:
                continue  # running heads, page numbers
            raw.append([y0, x0, x1, t])
    # merge fragments that share a baseline and nearly touch ("[摘" + "要]...") before assigning columns
    raw.sort(key=lambda f: f[0])
    rows = []
    for f in raw:  # cluster into visual rows, then left to right
        if rows and abs(rows[-1][0][0] - f[0]) < 5:
            rows[-1].append(f)
        else:
            rows.append([f])
    raw = [f for row in rows for f in sorted(row, key=lambda f: f[1])]
    merged = []
    for f in raw:
        # only tiny leading fragments, so a left-column line never fuses with the right column
        if merged and abs(merged[-1][0] - f[0]) < 5 and 0 <= f[1] - merged[-1][2] < 15 and len(merged[-1][3]) <= 4:
            merged[-1][3] += f[3]; merged[-1][2] = f[2]
        else:
            merged.append(f)
    lines = []
    for y0, x0, x1, t in merged:
        col = 'R' if x0 >= mid - 5 else ('L' if x1 <= mid + 15 else 'F')
        lines.append([col, y0, x0, x1, t])
    lines = [l for l in lines if len(l[4]) > 2 or re.search(r'[一-鿿]{2}', l[4])]  # stray '*', postcodes
    left_y = [l[1] for l in lines if l[0] == 'L' and len(l[4]) > 8]
    right_y = [l[1] for l in lines if l[0] == 'R' and len(l[4]) > 8]
    full = [l for l in lines if l[0] == 'F' and len(l[4]) > 8]
    if len(full) > len(left_y) + len(right_y):  # single-column page (short paragraph ends look like 'L')
        ordered = sorted(lines, key=lambda l: l[1])
    else:
        # the two-column area starts where both columns carry body text
        top_y = max(min(left_y), min(right_y)) if left_y and right_y else min(left_y or right_y)
        top_y = min([l[1] for l in lines if l[0] in 'LR' and l[1] >= top_y - 200 and len(l[4]) > 8] + [top_y])
        head = sorted([l for l in lines if l[0] == 'F' and l[1] < top_y], key=lambda l: l[1])
        # full-width lines inside the column area (tables, captions, first-page footnotes) are dropped
        ordered = head + sorted([l for l in lines if l[0] == 'L'], key=lambda l: l[1]) + sorted([l for l in lines if l[0] == 'R'], key=lambda l: l[1])
    out = []
    for group in ('F', 'L', 'R'):
        xs = [round(l[2]) for l in ordered if l[0] == group]
        base = max(set(xs), key=xs.count) if xs else 0
        for l in ordered:
            if l[0] == group:
                l.append(base)
    return [(l[2], l[5], l[4]) for l in ordered]

def extract(pdf):
    doc = fitz.open(pdf)
    paras, cur = [], ''
    for page in doc:
        for x, base, t in page_lines(page):
            if DROP.search(t):
                continue
            is_head = bool(TOP.match(t) or SUB.match(t))
            indented = 12 <= x - base <= 34
            marker = bool(re.match(r'^[\[【]?(摘\s*要|关\s*键\s*词|Abstract|Key\s*words)', t))
            if is_head or indented or marker:
                if cur:
                    paras.append(cur)
                cur = t
                if is_head:
                    paras.append(cur); cur = ''
            else:
                cur += (' ' if cur and cur[-1].isascii() and cur[-1].isalnum() and t[0].isascii() and t[0].isalnum() else '') + t
    if cur:
        paras.append(cur)
    return paras

def tag(paras, title, overrides=None):
    out = [f'# {title}']
    started = False
    for p in paras:
        cjk = r'[一-鿿，。；：、“”（）《》—]'
        p = re.sub(rf'(?<={cjk})\s+|\s+(?={cjk})', '', p)
        p = re.sub(r'\s+', ' ', p).strip()
        if STOP.match(p):
            break
        if re.match(r'^[\[【]?摘\s*要[\]】]?[：:]?', p):
            out.append('## ABSTRACT | 摘要'); out.append(re.sub(r'^[\[【]?摘\s*要[\]】]?[：:]?\s*', '', p)); started = True; continue
        if re.match(r'^[\[【]?关\s*键\s*词', p):
            out.append(p); continue
        if not started:
            continue  # title block, authors, affiliations
        if len(re.findall(r'[A-Za-z]', p)) > 2 * len(re.findall(r'[一-鿿]', p)):
            continue  # English abstract, keywords or author block
        m_top, m_sub = TOP.match(p), SUB.match(p)
        if m_top or m_sub:
            t = next((v for k, v in (overrides or {}).items() if p.startswith(k)), None) or tags_for(p, top=bool(m_top))
            if t:
                out.append(f'## {t} | {p}'); continue
        out.append(p)
    return '\n'.join(out) + '\n'

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser()
    ap.add_argument('--list', required=True); ap.add_argument('--src', required=True); ap.add_argument('--out', required=True)
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    for item in json.loads(Path(a.list).read_text(encoding='utf-8')):
        paras = extract(Path(a.src) / item['file'])
        text = tag(paras, item['title'], item.get('overrides'))
        (out / f"{item['id']}.txt").write_text(text, encoding='utf-8')
        heads = re.findall(r'^## ([A-Z+]+) \| (.+)$', text, re.M)
        n = len(re.findall(r'[一-鿿]', text))
        print(item['id'], n, ' / '.join(f'{t}:{h[:14]}' for t, h in heads))

if __name__ == '__main__':
    main()
