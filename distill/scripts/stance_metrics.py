"""Lexicon-based stance profile (hedges, boosters, limitations, self-mention) for zh/en research prose.

Rates are per 1,000 English words or per 1,000 Chinese characters, so compare within a language only.
Lexicons follow Hyland's metadiscourse categories, trimmed to forms that are rarely non-epistemic in
education research (e.g. 潜在 is excluded because of 潜在变量/潜在剖面).
"""
from pathlib import Path
import argparse, csv, glob, json, re, statistics

EN = {
    'hedge': r"\b(may|might|could|would|possibly|possible|perhaps|maybe|likely|unlikely|probably|probable|plausibl[ey]|presumably|apparently|seem(?:s|ed|ingly)?|appear(?:s|ed)?|suggest(?:s|ed|ing|ive)?|tend(?:s|ed)? to|somewhat|relatively|partly|partially|largely|to (?:some|a certain) extent|in part|tentative(?:ly)?|potentially|not necessarily|uncertain|unclear|preliminary|speculative|arguably|conceivably)\b",
    'booster': r"\b(clearly|evident(?:ly)?|obviously|certainly|definitely|undoubtedly|indeed|in fact|of course|strongly|substantially|considerably|markedly|robust(?:ly)?|demonstrat(?:e|es|ed|ing)|prov(?:e|es|ed|en)|establish(?:es|ed)?|confirm(?:s|ed|ing)?|reveal(?:s|ed|ing)?|show(?:s|ed|n|ing)?|(?:find|finds|found) that|highlight(?:s|ed)?)\b",
    'limitation': r"\b(limitations?|limited|caution(?:s|ary)?|cautious(?:ly)?|generali[sz]\w*|cannot|unable|caveats?|should be interpreted|not possible to|future (?:research|studies|work))\b",
    'self': r"\b(we|our|us|this (?:study|research|paper|article)|the (?:present|current) (?:study|research))\b",
    'deontic': r"\b(should|must|need to|needs to|ought to|recommend(?:s|ed)?)\b",
    # Negated inference: a claim followed by what it does NOT show
    'disclaimer': r"\b((?:does|do|did|can|could|should|is|are|was|were)(?:n't| not|not)\s+(?:necessarily\s+|directly\s+|simply\s+|by itself\s+|alone\s+)?(?:be\s+)?(?:mean|imply|show|establish|prove|indicate|demonstrate|identify|determine|equate|generali[sz]e|attribut|interpret|tak|read|license|warrant|support a causal|evidence)\w*|not (?:evidence|proof) (?:of|that)|cannot (?:rule out|distinguish|separate|tell))",
}
ZH = {
    'hedge': r"(或许|也许|大概|大致|似乎|好像|一定程度|某种程度|相对(?!于|应)|较为|基本上|倾向于|推测|初步|有待|尚需|尚待|仍需|不一定|未必|或可|可以认为|不排除|可能)",
    'booster': r"(明显|充分|确实|无疑|必然|有力|切实|极大|深刻|根本上|尤为|十分|高度|表明|证实|证明|揭示|显示|发现)",
    'limitation': r"(局限|不足|未能|无法|难以|谨慎|有限|不宜|尚未|推广|未来研究|后续研究)",
    'self': r"(本研究|本文|笔者|我们)",
    'deontic': r"(应当|应该|必须|务必|亟需|亟待|需要)",
    # Negated inference: 尚不能证明 / 不宜视为 / 不等于 / 并不意味着 ...
    'disclaimer': r"((?:尚|并|还|仍|也)?不能(?:据此|由此|因此|直接|简单地?|仅凭|仅据|就此|以此|完全)?(?:说明|证明|表明|推断|推导|推出|认定|断言|得出|归因|归结|确定|区分|代表|视为|解释为|理解为|等同|判断|外推|推广到)|不能(?:把|将)[^，。；]{0,24}?(?:理解为|解释为|视为|等同|归因|归结|当作|看作|推导为)|不能因[^，。；]{0,30}?就(?:断言|认定|认为|推断|判断)|不宜(?:视为|理解为|解读为|推广|外推|据此|直接|过度|简单)|不宜(?:把|将)[^，。；]{0,24}?(?:视为|理解为|等同|当作)|不足以(?:说明|证明|支持|表明|推断|形成|确定)|尚无法|无法(?:确定|区分|判断|排除|推断|证明|说明)|难以(?:判断|区分|确定|排除|推断)|尚待(?:检验|验证)|有待(?:进一步)?(?:检验|验证))",
}
STAT = {'en': r"\bsignifican(?:t|tly|ce)\b", 'zh': r"(显著)"}
HEADINGS = [('STOP', r'^(references|bibliography|参考文献|注释)'), ('ABSTRACT', r'(abstract|摘要)'),
            ('LIMITATIONS', r'(limitation|局限|不足与展望|研究不足)'), ('IMPLICATIONS', r'(implication|启示|建议|对策)'),
            ('CONCLUSION', r'(conclu|结论|结语)'), ('DISCUSSION', r'(discussion|讨论)'), ('RESULTS', r'(result|finding|结果|发现)'),
            ('METHOD', r'(method|研究设计|研究方法|participant)'), ('LITERATURE', r'(literature|theor|文献|理论)'),
            ('INTRODUCTION', r'(introduction|引言|问题的?提出|导言)')]
FOCUS = {'DISCUSSION', 'CONCLUSION', 'LIMITATIONS', 'IMPLICATIONS'}

def lang_of(text):
    return 'zh' if len(re.findall(r'[一-鿿]', text)) > len(re.findall(r'[A-Za-z]+', text)) else 'en'

def sections(text):
    """Return [(tags, body)]. Uses '## TAG | heading' markers when present, else markdown/numbered headings."""
    out, tags, buf = [], {'BODY'}, []
    marked = bool(re.search(r'^## [A-Z+]+ \|', text, re.M))
    for line in text.splitlines():
        s = line.strip()
        if marked and re.match(r'^## [A-Z+]+ \|', s):
            out.append((tags, '\n'.join(buf))); buf = []; tags = set(s[3:].split('|')[0].strip().split('+')); continue
        head = re.match(r'^(#{1,4}\s+|[一二三四五六七八九十]+、|\d+(\.\d+)*\.?\s+)(.{1,40})$', s)
        if not marked and head:
            low = head.group(3).lower()
            for tag, pat in HEADINGS:
                if re.search(pat, low):
                    out.append((tags, '\n'.join(buf))); buf = []; tags = {tag}; break
            else:
                buf.append(s)
            continue
        if tags == {'STOP'}:
            continue
        buf.append(s)
    out.append((tags, '\n'.join(buf)))
    return [(t, b) for t, b in out if b.strip() and t != {'STOP'}]

def sentences(text, lang):
    parts = re.split(r'(?<=[。！？；!?;])' if lang == 'zh' else r'(?<=[.!?])\s+(?=[A-Z“"(])', text)
    return [p.strip() for p in parts if len(p.strip()) > (8 if lang == 'zh' else 20)]

def profile(secs, lang, region):
    lex = ZH if lang == 'zh' else EN
    flags = 0 if lang == 'zh' else re.I
    chosen = [(t, b) for t, b in secs if region == 'all' or t & FOCUS]
    text = '\n'.join(b for _, b in chosen)
    units = len(re.findall(r'[一-鿿]', text)) if lang == 'zh' else len(re.findall(r"[A-Za-z][A-Za-z'-]*", text))
    if units == 0:
        return None
    row = {'units': units}
    for k, pat in lex.items():
        row[k + '_per1k'] = round(1000 * len(re.findall(pat, text, flags)) / units, 2)
    row['stat_sig_per1k'] = round(1000 * len(re.findall(STAT[lang], text, flags)) / units, 2)
    sents = [(t, s) for t, b in chosen for s in sentences(b, lang)]
    n = len(sents) or 1
    hedge_counts = [len(re.findall(lex['hedge'], s, flags)) for _, s in sents]
    lim = [(t, s) for t, s in sents if re.search(lex['limitation'], s, flags)]
    row.update({'sentences': len(sents),
                'hedged_sent_pct': round(100 * sum(c >= 1 for c in hedge_counts) / n, 1),
                'stacked_hedge_sent_pct': round(100 * sum(c >= 2 for c in hedge_counts) / n, 1),
                'limitation_sent_pct': round(100 * len(lim) / n, 1),
                'disclaimer_sent_pct': round(100 * sum(bool(re.search(lex['disclaimer'], s, flags)) for _, s in sents) / n, 1),
                'limitation_in_own_section_pct': round(100 * sum('LIMITATIONS' in t for t, _ in lim) / len(lim), 1) if lim else None,
                'booster_hedge_ratio': round(row['booster_per1k'] / row['hedge_per1k'], 2) if row['hedge_per1k'] else None})
    return row

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--groups', required=True, help='JSON {group: [glob, ...]} (globs relative to --root)')
    ap.add_argument('--root', default='.')
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    root, out = Path(a.root), Path(a.out); out.mkdir(parents=True, exist_ok=True)
    groups = json.loads(Path(a.groups).read_text(encoding='utf-8'))
    rows = []
    for group, patterns in groups.items():
        files = sorted({f for p in patterns for f in glob.glob(str(root / p), recursive=True)})
        for f in files:
            text = Path(f).read_text(encoding='utf-8', errors='ignore')
            lang, secs = lang_of(text), sections(text)
            for region in ('all', 'dcl'):
                r = profile(secs, lang, region)
                if r:
                    rows.append({'group': group, 'doc': Path(f).relative_to(root).as_posix(), 'lang': lang, 'region': region, **r})
    keys = list(rows[0].keys())
    with open(out / 'stance_by_doc.csv', 'w', newline='', encoding='utf-8-sig') as fh:
        w = csv.DictWriter(fh, keys); w.writeheader(); w.writerows(rows)
    metrics = [k for k in keys if k not in ('group', 'doc', 'lang', 'region', 'units', 'sentences')]
    summary = []
    for g in groups:
        for lang in ('zh', 'en'):
            for region in ('all', 'dcl'):
                sub = [r for r in rows if r['group'] == g and r['lang'] == lang and r['region'] == region]
                if not sub:
                    continue
                s = {'group': g, 'lang': lang, 'region': region, 'n_docs': len(sub), 'units_total': sum(r['units'] for r in sub)}
                for m in metrics:
                    vals = sorted(r[m] for r in sub if r[m] is not None)
                    if vals:
                        q = statistics.quantiles(vals, n=4) if len(vals) >= 4 else [vals[0], statistics.median(vals), vals[-1]]
                        s[m] = f"{statistics.median(vals):.2f} [{q[0]:.2f}–{q[2]:.2f}]"
                summary.append(s)
    with open(out / 'stance_summary.csv', 'w', newline='', encoding='utf-8-sig') as fh:
        fields = sorted({k for s in summary for k in s}, key=lambda k: (['group', 'lang', 'region', 'n_docs', 'units_total'] + metrics).index(k))
        w = csv.DictWriter(fh, fields); w.writeheader(); w.writerows(summary)
    print(f'{len(rows)} profiles -> {out}')

if __name__ == '__main__':
    main()
