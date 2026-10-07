"""Compare how a manuscript is written with published articles, section by section (Chinese or English).

    python check_prose.py --draft 稿件.docx|.md [--json]

Chinese drafts are compared with 27 CSSCI empirical articles (distill/results/writing_moves_zh.md). Sections are found
from headings (摘要, 引言/问题提出, 文献综述/理论基础/研究假设, 研究设计/方法, 研究结果, 讨论, 结论/建议/启示). For each
section it reports sentence length, citation density and author-led citations, statistics in the discussion,
reviewer-style sentences (proposing analyses, conceding on null results), signposting, paragraph-final value
sentences, stock phrases, self-reference and the density of 的.

English drafts (detected from the text) are compared with 31 SSCI empirical articles (writing_moves_en.md): citation
density, cited sentences, narrative "Author (year)" citations and bundles by section, numbers in the discussion and
results, sentence and paragraph length, we, passive voice, abbreviations, connectives, value-sentence paragraph
endings, signposting and AI-typical words.

Values outside the published range are flagged as prompts to reread the passage, not as errors.
"""
from pathlib import Path
import argparse
import json
import re
import statistics
import sys

KINDS = [  # first match wins; a heading that matches nothing keeps the current section
    ('stop', r'参考文献|references|bibliography|注释|声明|致谢|附录|作者贡献|利益冲突|基金项目'),
    ('abstract', r'摘\s*要|abstract'),
    ('results', r'结果与讨论|结果与分析|results and discussion'),  # combined sections report numbers
    ('discussion', r'讨论|discussion'),
    ('conclusion', r'结论|建议|启示|结语|对策|展望|conclusion|implication'),
    ('results', r'研究结果|结果与分析|结果分析|数据分析结果|^\s*(?:\S{0,6}\s)?结果\s*$|results'),
    ('method', r'研究设计|研究方法|研究对象|研究工具|数据来源|method'),
    ('review', r'文献综述|文献回顾|研究综述|理论基础|理论框架|研究假设|概念界定|literature|theor|hypothes'),
    ('intro', r'引言|问题提出|研究背景|绪论|introduction'),
]
HEADING = re.compile(r'^(?:#{1,6}\s*(.+)|([一二三四五六七八九十]+[、.．]\s*\S.{0,30})|([（(][一二三四五六七八九十]+[）)]\s*\S.{0,30})|'
                     r'(\d+(?:\.\d+)*\.?\s+\S.{0,30}))$')
CITE = re.compile(r'\[\d+(?:\s*[,，\-–—~]\s*\d+)*\]|[（(][^（）()\n]{0,60}?(?:19|20)\d{2}[a-z]?[）)]')
AUTHOR_LED = re.compile(r'^(?:[一-鿿·]{2,8}|[A-Z][A-Za-z\-]+)(?:等人?|和[一-鿿]{2,4}|与[一-鿿]{2,4}|\s*(?:and|&)\s*[A-Z][A-Za-z\-]+|\s*et al\.?)?\s*[（(](?:19|20)\d{2}')
STAT = re.compile(r'(?:β|\bB|\br|R²|\bp|\bt|\bF|\bz|χ²|\bd\*?|η²|ηp²|\bM|\bSD|\bN|\bn|CFI|TLI|RMSEA|SRMR|α|ICC)\s*(?:\([^)]{0,10}\))?\s*[=<>＝＜＞≤≥]'
                  r'|\[\s*-?\d*\.\d+\s*,\s*-?\d*\.\d+\s*\]|95%\s*(?:置信区间|CI)')
REVIEWER = re.compile(r'可以在现有数据上|可以分别检验|前者预测|后者预测|需要按.{0,12}单独(?:比较|分析)|这一比较可以|可以直接检验|'
                      r'仍是开放的问题|孰优孰劣|并不矛盾|无论.{0,15}多大程度上')
SIGNPOST = re.compile(r'下面分.{0,6}(?:方面|部分|点)|见下文|如下文|下文将|本节将|如前所述')
VALUE_END = re.compile(r'具有.{0,10}(?:意义|价值)|提供了?.{0,24}(?:参考|依据|借鉴|启示|思路|支撑|指导)|以期|不仅.{0,40}(?:更|还|也)|唯有.{0,24}才')
STOCK = re.compile(r'值得注意的是|具有重要意义|有待进一步|综上所述')
NOT_ONLY = re.compile(r'不仅.{0,40}?(?:更|还|也)')
PROVIDE = re.compile(r'为.{0,30}?提供.{0,20}?(?:参考|依据|借鉴|启示)')
BUZZ = re.compile(r'赋能|深度融合|高质量发展|数智')
SELF = re.compile(r'本研究|本文|笔者')

# Flags sit at the edge of what the 27 published articles do (checked by running this script on them), so a
# published article rarely triggers one; abstracts, methods and results are measured but not flagged.
PROSE = ('intro', 'review', 'discussion', 'conclusion')
RANGES = {  # (low, high) flags outside; None = not checked
    'sentence_median': (30, 90),
    'long_share': (None, 35),
    'author_led_share': {'review': (None, 50), 'intro': (None, 50)},
    'stats_per_k': {'discussion': (None, 3), 'conclusion': (None, 3)},
    'value_end_share': {'review': (None, 20), 'discussion': (None, 25), 'conclusion': (None, 45)},
}
DECIMAL = re.compile(r'(?<![\d.\[])\d+\.\d+(?![\d.])')
COMPARE = re.compile(r'一致|不一致|相符|不同于|印证|吻合|相悖|相左|consistent|contrary')


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


def sections(text):
    """[(kind, [paragraphs])] in order; text before the first recognised heading is 'front'."""
    out, kind = [], 'front'
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith('|') or re.match(r'^(表|图)\s*\d+\s', s) or re.match(r'^注[:：]', s):
            continue
        m = HEADING.match(s)
        if m:
            title = next(g for g in m.groups() if g)
            for k, pat in KINDS:
                if re.search(pat, title, re.I):
                    kind = k
                    break
            if kind == 'stop':
                break
            continue
        if re.match(r'^[\[【]?\s*关键词', s):
            continue
        if out and out[-1][0] == kind:
            out[-1][1].append(s)
        else:
            out.append((kind, [s]))
    merged = {}
    for k, paras in out:
        merged.setdefault(k, []).extend(paras)
    return merged


def chars(s):
    return len(re.findall(r'[一-鿿A-Za-z0-9]', s))


def sentences(paragraph):
    return [x for x in re.split(r'(?<=[。！？；?!])', paragraph) if chars(x) > 4]


def section_metrics(kind, paras):
    sents = [s for p in paras for s in sentences(p)]
    n = sum(chars(p) for p in paras) or 1
    lens = [chars(s) for s in sents] or [0]
    cited = [s for s in sents if CITE.search(s)]
    m = {
        'chars': n, 'paragraphs': len(paras), 'sentences': len(sents),
        'sentence_median': statistics.median(lens),
        'long_share': round(100 * sum(l > 100 for l in lens) / max(len(sents), 1), 1),
        'cite_per_k': round(1000 * sum(len(CITE.findall(p)) for p in paras) / n, 1),
        'cited_share': round(100 * len(cited) / max(len(sents), 1), 1),
        'author_led_share': round(100 * sum(bool(AUTHOR_LED.match(s.strip())) for s in cited) / max(len(cited), 1), 1),
        'stats_per_k': round(1000 * sum(len(STAT.findall(p)) for p in paras) / n, 1),
        'decimals_per_k': round(1000 * sum(len(DECIMAL.findall(p)) for p in paras) / n, 1),
        'value_end_share': round(100 * sum(bool(VALUE_END.search((sentences(p) or [''])[-1])) for p in paras) / max(len(paras), 1), 1),
        'self_per_k': round(1000 * sum(len(SELF.findall(p)) for p in paras) / n, 1),
        'de_per_100': round(100 * sum(p.count('的') for p in paras) / n, 1),
    }
    examples = {
        'reviewer': [s.strip()[:90] for s in sents if REVIEWER.search(s)],
        'signpost': [s.strip()[:90] for s in sents if SIGNPOST.search(s)],
        'compare': [s.strip()[:90] for s in sents if COMPARE.search(s)],
    }
    return m, examples


def flags_for(kind, m, ex):
    out = []

    def rng(key):
        r = RANGES.get(key)
        return r.get(kind) if isinstance(r, dict) else r

    if kind not in PROSE:
        return out
    for key in ['sentence_median', 'long_share', 'author_led_share', 'stats_per_k', 'value_end_share']:
        r = rng(key)
        if not r or m['sentences'] < 5 or m['chars'] < 400:  # rates on a few sentences say nothing
            continue
        lo, hi = r
        if lo is not None and m[key] < lo:
            out.append(f'{key} {m[key]} below the published range (>= {lo})')
        if hi is not None and m[key] > hi:
            out.append(f'{key} {m[key]} above the published range (<= {hi})')
    if kind in ('intro', 'review') and m['sentences'] >= 5 and m['cite_per_k'] < 3 and m['cited_share'] < 20:
        out.append(f'few citations ({m["cite_per_k"]} per 1,000 characters, {m["cited_share"]}% of sentences; published 7.5-9.6 and 36-50%)')
    if kind == 'discussion' and m['cite_per_k'] == 0 and m['sentences'] >= 5 and not ex['compare']:
        out.append('the discussion neither cites nor compares with earlier studies (published 0.6-2.9 citations per 1,000 characters)')
    if kind in ('discussion', 'conclusion') and ex['reviewer']:
        out.append(f'{len(ex["reviewer"])} reviewer-style sentences (proposing analyses or conceding on null results)')
    if ex['signpost']:
        out.append(f'{len(ex["signpost"])} signposting sentences')
    if kind in ('discussion', 'conclusion') and m['decimals_per_k'] > 6 and m['sentences'] >= 5:
        out.append(f'{m["decimals_per_k"]} decimal numbers per 1,000 characters (published discussions: mostly 0; restate findings in words)')
    if m['de_per_100'] > 5.5:
        out.append(f'的 {m["de_per_100"]} per 100 characters (published 1.2-4.7)')
    return out


def document_flags(text):
    body = text.split('参考文献')[0]
    n = chars(body) or 1
    per10k = lambda pat: round(10000 * len(pat.findall(body)) / n, 1)
    out = []
    stock = STOCK.findall(body)
    if len(stock) > 2:
        out.append(f'stock phrases used {len(stock)} times ({", ".join(sorted(set(stock)))}); published papers use them less than once per 10,000 characters')
    if n < 3000:  # frequencies per 10,000 characters need a manuscript-length text
        return out
    if per10k(NOT_ONLY) > 15:
        out.append(f'不仅……更/还/也 {per10k(NOT_ONLY)} per 10,000 characters (published median 6.5)')
    if per10k(PROVIDE) > 12:
        out.append(f'为……提供……参考/依据 {per10k(PROVIDE)} per 10,000 characters (published median 3.2)')
    if len(re.findall(r'以期', body)) > 1:
        out.append(f'以期 used {len(re.findall(r"以期", body))} times (keep one, at the end of the introduction)')
    if len(re.findall(r'唯有.{0,24}才', body)) > 1:
        out.append('唯有……才 used more than once')
    if per10k(BUZZ) > 15:
        out.append(f'赋能/深度融合/高质量发展/数智 {per10k(BUZZ)} per 10,000 characters (published p90 about 7, higher when in the title)')
    return out


def reference_flags(text):
    m = re.search(r'^\s*(?:#+\s*)?(?:参考文献|references)\s*$', text, re.M | re.I)
    if not m:
        return []
    entries = [l for l in text[m.end():].splitlines() if re.match(r'^\s*(?:\[\d+\]|\d+[.．、]|[A-Z一-鿿])', l) and len(l.strip()) > 15]
    chinese = [l for l in entries if re.search(r'[一-鿿]{4}', l)]
    if len(entries) >= 10 and not chinese:
        return [f'none of the {len(entries)} references is Chinese; Chinese journals expect verified domestic studies in the introduction and discussion']
    return []


def check(text):
    secs = sections(text)
    report = {'sections': {}, 'document': document_flags(text) + reference_flags(text)}
    argued = [p for k in PROSE for p in secs.get(k, [])]
    n = sum(chars(p) for p in argued)
    if n > 1000:
        rate = round(1000 * sum(len(SELF.findall(p)) for p in argued) / n, 1)
        if rate > 4:
            report['document'].append(f'本研究/本文/笔者 {rate} per 1,000 characters in the introduction, review, discussion '
                                      f'and conclusion (published 1.2-1.4)')
    for kind in ['abstract', 'intro', 'review', 'method', 'results', 'discussion', 'conclusion']:
        if kind in secs:
            m, ex = section_metrics(kind, secs[kind])
            report['sections'][kind] = {'metrics': m, 'flags': flags_for(kind, m, ex), 'examples': ex}
    return report


# ---- English manuscripts: 31 SSCI empirical articles (distill/results/writing_moves_en.md) ----

KINDS_EN = [  # matched against the heading without its number; first match wins
    ('stop', r'^(?:references?|bibliography|acknowledge?ments?|funding|declarations?|conflicts? of interest|competing interests?|'
             r'author contributions?|credit author|data availability|appendix|appendices|ethics|supplementary)'),
    ('abstract', r'^abstract'),
    ('results', r'^(?:results?|findings) and discussion'),
    ('discussion', r'discussion'),
    ('closing', r'conclu|implications?\b|limitations?\b|future (?:research|directions?|studies)|recommendations?\b|contributions?\b'),
    ('results', r'\bresults?\b|^findings\b'),
    ('method', r'^(?:methods?|methodology|materials and methods|research design|study design|participants|procedures?|measures|'
               r'data (?:collection|analysis|sources?)|instruments?|sample)\b'),
    ('present', r'^(?:the )?(?:present|current) (?:study|research|investigation)|^this study|^research questions?|^aims?\b'),
    ('review', r'literature|background|theor|framework|hypothes|prior (?:research|work)|related (?:work|research)|conceptual'),
    ('intro', r'^introduction'),
]
MAIN_EN = ('intro', 'review', 'present', 'discussion', 'closing')  # argued prose; methods and results are reported
PROTECT = ['et al.', 'e.g.', 'i.e.', 'cf.', 'vs.', 'Fig.', 'No.', 'pp.', 'p.', 'U.S.', 'U.K.', 'approx.', 'Eds.', 'Ed.',
           'Vol.', 'Ph.D.', 'etc.)', 'viz.', 'n.d.']
YEAR = r'(?:19|20)\d{2}[a-z]?|n\.d\.|in press'
MONTHS = r'January|February|March|April|May|June|July|August|September|October|November|December|Spring|Summer|Autumn|Fall|Winter'
NUM = re.compile(r'(?<![A-Za-z])[−\-]?\d*[.,]?\d+')
STAT_EN = re.compile(r'(?:β|\bb|\bB|\br|\bt|\bF|\bp|\bd|\bz|OR|χ2|χ²|\bM|\bSD|\bSE|CI|R2|R²|η2|η²|ηp2|\bn|\bN|\bdf|ICC|RMSEA|CFI|TLI|'
                     r'SRMR|α|ω)\s*(?:\([^()]{0,12}\))?\s*[=<>≤≥]')
PASSIVE = re.compile(r'\b(?:am|is|are|was|were|be|been|being)\s+(?:\w+ly\s+|not\s+|also\s+){0,2}(?:\w+ed|known|shown|found|given|'
                     r'taken|made|seen|done|held|led|thought|built|taught|written|drawn|chosen|told|kept|meant|understood|'
                     r'undertaken|grown|sought|spent|begun|sent|read|heard|said|bound|driven|proven|set|put)\b', re.I)
WE = re.compile(r'\b(?:we|our|us|ours|ourselves)\b', re.I)
ABBR = re.compile(r'\b(?=[A-Za-z0-9\-]*[A-Z][A-Za-z0-9\-]*[A-Z])[A-Za-z][A-Za-z0-9\-]{1,9}\b')
CONNECT = ['however', 'moreover', 'furthermore', 'in addition', 'additionally', 'first', 'firstly', 'second', 'secondly', 'third',
           'finally', 'lastly', 'similarly', 'likewise', 'in contrast', 'by contrast', 'conversely', 'nevertheless',
           'nonetheless', 'yet', 'thus', 'therefore', 'hence', 'consequently', 'accordingly', 'taken together', 'overall',
           'in sum', 'in summary', 'to summarize', 'in conclusion', 'importantly', 'notably', 'interestingly', 'specifically',
           'for example', 'for instance', 'also', 'next', 'then', 'another', 'further', 'beyond', 'in this context',
           'in light of', 'given', 'regarding', 'on the other hand', 'still', 'despite', 'although', 'while', 'whereas',
           'unlike', 'contrary to', 'consistent with', 'in line with']
WORDS_EN = {  # per 10,000 words of argued prose: (pattern, highest rate in the 31 articles)
    'crucial': (r'\bcrucial(?:ly)?\b', 20), 'highlight': (r'\bhighlight(?:s|ed|ing)?\b', 32.4), 'foster': (r'\bfoster(?:s|ed|ing)?\b', 19.9),
    'essential': (r'\bessential(?:ly)?\b', 15.9), 'insights': (r'\b(?:valuable|important|new|novel|useful|deeper|key|rich|further) insights?\b|'
                                                             r'\b(?:provid|offer|yield|gain)(?:e|es|ed|ing|s)? (?:\w+ )?insights?\b', 14.3),
    'notably': (r'\bnotably\b', 7.3), 'underscore': (r'\bunderscor(?:e|es|ed|ing)\b', 5.6), 'pivotal': (r'\bpivotal\b', 5.6),
    'nuanced': (r'\bnuanced?\b', 7.0), 'multifaceted': (r'\bmulti-?faceted\b', 7.8), 'leverage': (r'\bleverag(?:e|es|ed|ing)\b', 6.4),
    'navigate': (r'\bnavigat(?:e|es|ed|ing)\b', 6.7), 'robust': (r'\brobust(?:ly|ness)?\b', 8.3),
    'comprehensive': (r'\bcomprehensive(?:ly)?\b', 9.4), 'shed light on': (r'\bsh(?:ed|eds|edding) (?:new |some |further )?light\b', 9.6),
    'play a ... role': (r'\bplay(?:s|ed|ing)? an? (?:crucial|key|vital|pivotal|important|significant|central|essential|critical|major) role\b', 9.8),
    'it is important to': (r'\bit is (?:important|essential|crucial|vital|necessary) to\b|\bit should be noted\b', 11.3),
}
AI_WORDS = (r'\bit is worth (?:noting|mentioning)|\bnotably\b|\bnoteworthy\b|\bdelv(?:e|es|ed|ing)\b|\bcrucial(?:ly)?\b|\bpivotal\b|'
            r'\bsh(?:ed|eds|edding) (?:new |some |further )?light\b|\bpav(?:e|es|ed|ing) the way\b|\bgrowing body of\b|\bin today[’\']s\b|'
            r'\bunderscor(?:e|es|ed|ing)\b|\blandscapes?\b|\brealms?\b|\bintricac(?:y|ies)\b|\bintricate\b|\bmulti-?faceted\b|\bnuanced?\b|'
            r'\bholistic(?:ally)?\b|\bfoster(?:s|ed|ing)?\b|\bleverag(?:e|es|ed|ing)\b|\bnavigat(?:e|es|ed|ing)\b|\bparamount\b|'
            r'\bvital(?:ly)?\b|\bin conclusion\b|' + WORDS_EN['insights'][0])
RARE = (r'\bdelv(?:e|es|ed|ing)\b|\bin today[’\']s\b|\bpav(?:e|es|ed|ing) the way\b|\bgrowing body of\b|\bit is worth (?:noting|mentioning)|'
        r'\bnoteworthy\b|\brealms?\b|\bin conclusion\b|\bparamount\b|\bgarner(?:ed|s|ing)? (?:\w+ )?attention\b')
ADDITIVE = r'\bfurthermore\b|\bmoreover\b|\badditionally\b|\bin addition\b'
SIGNPOST_EN = (r'\bin this section\b|\bthe (?:remainder|rest) of (?:this|the) (?:paper|article)\b|\b(?:is|are) (?:organi[sz]ed|structured) '
               r'as follows\b|\bin the (?:next|following|subsequent) sections?\b|\bas (?:mentioned|noted|discussed|described|stated) '
               r'(?:above|earlier|previously)\b|\bin what follows\b|\bbelow, we\b')
VALUE_END_EN = re.compile(  # paragraph-final sentences that assert value instead of a finding or inference
    r'\b(?:highlight|underscore|emphasi[sz]e|reinforce|illustrate|demonstrate|reflect|reveal)(?:s|d|ed|ing)?\b[^.;]{0,40}?\b(?:importance|'
    r'need|significance|value|potential|complexity|relevance|necessity|promise)\b'
    r'|\b(?:important|significant|valuable|crucial|vital|far-reaching|profound|practical|theoretical) (?:and \w+ )?implications\b'
    r'|\b(?:more|further|additional|future) (?:research|studies|work|investigation)s? (?:is|are|would be|will be) (?:needed|warranted|required)\b'
    r'|\bwarrants? (?:further|more|additional) (?:research|investigation|attention|study|exploration)\b'
    r'|\bplay(?:s|ed|ing)? an? (?:crucial|key|vital|important|pivotal|central|essential|critical|significant) role\b'
    r'|\b(?:is|are|remains?|becomes?) (?:crucial|essential|vital|paramount|critical|indispensable|imperative)\b'
    r'|\bpav(?:e|es|ing) the way\b|\b(?:valuable|important|new|novel|deeper|rich) insights?\b'
    r'|\bcontribut\w* to (?:a |the )?(?:better|deeper|broader|more comprehensive|greater|fuller) understanding\b'
    r'|\bof (?:great|crucial|vital|paramount|utmost|particular) importance\b', re.I)
REVIEWER_EN = re.compile(  # analyses proposed inside the paper instead of run or moved to future research
    r'\b(?:could|can) be (?:tested|examined|checked) (?:with|in|on|using) (?:the|our|these) (?:present |current |existing )?data\b'
    r'|\b(?:the|our) (?:present|current|existing) data (?:could|can|would) (?:test|distinguish|separate)\b'
    r'|\b(?:these|the) two (?:accounts|explanations|interpretations) (?:make|yield|predict) different\b', re.I)


def en_words(s):
    return re.findall(r"[A-Za-z0-9][A-Za-z0-9'’\-.]*", s)


def en_sentences(paragraph):
    t = paragraph
    for a in PROTECT:
        t = t.replace(a, a.replace('.', '\x01'))
    t = re.sub(r'\b([A-Z])\.(?=\s+[A-Z])', lambda m: m.group(1) + '\x01', t)
    parts = re.split(r'(?<=[.!?])(?:["”’)\]*]*)\s+(?=["“‘(\[*]?[A-Z0-9])', t)
    return [p.replace('\x01', '.').strip() for p in parts if len(en_words(p)) > 2]


def en_cites(s):
    """(parenthetical citations, narrative citations, works per parenthesis, sentence opens with a narrative citation)."""
    paren, narr, bundles, lead = 0, 0, [], False
    for m in re.finditer(r'\(([^()]*)\)', s):
        c = m.group(1)
        if not re.search(YEAR, c) or (re.search(rf'\b(?:{MONTHS})\s+(?:19|20)\d{{2}}', c) and not re.search(r'[A-Z][a-z]+,', c)):
            continue
        if not re.sub(YEAR + r'|pp?\.\s*\d+(?:[-–]\d+)?|[,;:\s\-–]|see|cf\.|e\.g\.', '', c):  # "Smith (2020)": years only
            if re.search(r"(?:[A-Z][A-Za-z'’\-]+|et al\.)(?:['’]s)?\s*$", s[:m.start()]):
                narr += 1
                lead = lead or len(en_words(s[:m.start()])) <= 6
            continue
        if re.search(r'[A-Z]', c) and not re.search(r'[=<>]', c):
            paren += 1
            bundles.append(len(re.findall(YEAR, c)))
    for m in re.finditer(r'\[(\d+(?:\s*[,–\-]\s*\d+)*)\]', s):
        paren += 1
        bundles.append(sum(int(b) - int(a) + 1 if b else 1 for a, b in re.findall(r'(\d+)(?:\s*[–\-]\s*(\d+))?', m.group(1))))
    return paren, narr, bundles, lead


def en_heading(s):
    """(level or None, title) for a heading line, else None."""
    t = re.sub(r'^\*\*(.+)\*\*$', r'\1', s.strip())
    m = re.match(r'^(#{1,6})\s*(.+)$', t)
    if m:
        return len(m.group(1)), m.group(2).strip('* ')
    if len(t.split()) > 14 or re.search(r'[.!?:;,]$', t) or t[:1] in '|-*(["“':
        return None
    m = re.match(r'^(\d+(?:\.\d+)*)\.?\s+([A-Z].*)$', t)
    if m:
        return m.group(1).count('.') + 1, m.group(2)
    if re.match(r'^[A-Z][^.!?:;]*$', t) and len(t.split()) <= 12:
        return None, t
    return None


def en_kind(title):
    t = re.sub(r'^(?:\d+(?:\.\d+)*\.?|[IVX]+\.)\s*', '', title).strip().lower()
    return next((k for k, pat in KINDS_EN if re.search(pat, t)), None)


def sections_en(text):
    """{kind: [paragraphs]}. Top-level headings set the section; an unrecognised top-level heading between the
    introduction and the method is part of the review (reviews are often titled by topic); subheadings change the
    section only for a present-study part of the review or an implications/limitations part of the discussion."""
    lines = [l.strip() for l in text.splitlines()]
    heads = {i: h for i, h in ((i, en_heading(l)) for i, l in enumerate(lines) if l) if h}
    main = [lv for lv, t in heads.values() if lv is not None and en_kind(t) in ('intro', 'method', 'results', 'discussion')]
    top = min(main or [lv for lv, _ in heads.values() if lv is not None] or [1])
    out, kind, before_method, combined = {}, 'front', True, False
    for i, s in enumerate(lines):
        if (not s or s.startswith('|') or re.match(r'^(?:\*\*)?(?:table|figure|fig\.)\s*\d+', s, re.I)
                or re.match(r'^(?:\*\*|_)?(?:notes?|key\s*words?)\b', s, re.I)):
            continue
        if i in heads:
            lv, title = heads[i]
            k = en_kind(title)
            if lv is None:
                lv = top if k in ('intro', 'method', 'results', 'discussion', 'closing', 'abstract', 'stop') else top + 1
            if k == 'stop' and (lv <= top or kind in ('discussion', 'closing')):  # an ethics note inside the method goes on
                break
            if lv == top:
                kind = k or ('intro' if kind in ('front', 'abstract') else
                             'review' if kind in ('intro', 'review', 'present') and before_method else kind)
            elif lv > top and k == 'present' and kind in ('intro', 'review'):
                kind = 'present'
            elif lv > top and k == 'review' and kind == 'intro':
                kind = 'review'
            elif lv > top and k in ('discussion', 'closing') and (kind in ('discussion', 'closing') or combined):
                kind = k
            combined = lv == top and bool(re.search(r'and discussion', title, re.I)) or combined and lv > top
            before_method = before_method and kind != 'method'
            continue
        out.setdefault(kind, []).append(s)
    return out


def en_metrics(paras):
    sents = [s for p in paras for s in en_sentences(p)]
    lens = [len(en_words(s)) for s in sents] or [0]
    n = sum(lens) or 1
    long_paras = [p for p in paras if len(en_words(p)) >= 25]  # one-line hypotheses and RQs are not paragraphs
    cites = [en_cites(s) for s in sents]
    paren, narr = sum(c[0] for c in cites), sum(c[1] for c in cites)
    bundles = [b for c in cites for b in c[2]]
    bare = [re.sub(r'\([^()]*(?:19|20)\d{2}[^()]*\)|\[\d[\d,\s–\-]*\]', ' ', s) for s in sents]
    numeric = [len(NUM.findall(b)) for b in bare if NUM.search(b)]
    pct = lambda a, b: round(100 * a / b, 1) if b else 0.0
    return {
        'words': n, 'paragraphs': len(long_paras), 'sentences': len(sents),
        'sentence_median': statistics.median(lens), 'long_share': pct(sum(l > 40 for l in lens), len(sents)),
        'paragraph_median': statistics.median([len(en_words(p)) for p in long_paras] or [0]),
        'cite_per_k': round(1000 * (paren + narr) / n, 1),
        'cited_share': pct(sum(c[0] + c[1] > 0 for c in cites), len(sents)),
        'narrative_share': pct(narr, paren + narr), 'bundle3_share': pct(sum(b >= 3 for b in bundles), len(bundles)),
        'narrative_led_run': max((len(r) for r in re.findall(r'1+', ''.join('1' if c[3] else '0' for c in cites))), default=0),
        'number_share': pct(len(numeric), len(sents)),
        'numbers_per_numeric_sentence': statistics.median(numeric) if numeric else 0,
        'number_openings': pct(sum(bool(re.match(r'[(\[]?[−\-]?\.?\d', p) or STAT_EN.search(' '.join(p.split()[:3])))
                                   for p in long_paras), len(long_paras)),
        'we_per_k': round(1000 * sum(len(WE.findall(re.sub(r'“[^”]{20,}”|"[^"]{20,}"', ' ', p))) for p in paras) / n, 1),
        'passive_share': pct(sum(bool(PASSIVE.search(s)) for s in sents), len(sents)),
        'abbr_per_k': round(1000 * sum(len([a for a in ABBR.findall(p) if a not in ('II', 'III', 'IV') and not a.startswith('ChatGPT')])
                                       for p in paras) / n, 1),
        'connective_openings': pct(sum(any(re.match(re.escape(c) + r'\b', p.lower()) for c in CONNECT) for p in long_paras),
                                   len(long_paras)),
        'value_end_share': pct(sum(bool(VALUE_END_EN.search((en_sentences(p) or [''])[-1])) for p in long_paras), len(long_paras)),
    }, {'reviewer': [s[:110] for s in sents if REVIEWER_EN.search(s)],
        'signpost': [s[:110] for s in sents if re.search(SIGNPOST_EN, s, re.I)]}


# Flags sit at or just beyond the extremes of the 31 articles (checked by running this script on them), so a
# published article rarely triggers one. Rates need enough text: sections need 5 sentences and 150 words, the
# whole-text rates 1,500 words of argued prose.
SECTION_RULES_EN = {  # kind: [(metric, low, high, published median)]
    'intro': [('cite_per_k', 10, None, 23), ('cited_share', 25, None, 56)],
    'review': [('cite_per_k', 10, None, 25.5), ('cited_share', 20, None, 58), ('narrative_share', None, 65, 12),
               ('bundle3_share', None, 45, 10)],
    'discussion': [('cite_per_k', 3, None, 13.5), ('number_share', None, 35, 4), ('narrative_share', None, 65, 7)],
    'results': [('number_openings', None, 25, 0), ('numbers_per_numeric_sentence', None, 6, 2)],
}
DOC_RULES_EN = [
    ('sentence_median', 20, 33, 26.5), ('long_share', None, 30, 14.6), ('paragraph_median', 75, 230, 130),
    ('we_per_k', None, 18, 4.8), ('passive_share', 8, 50, 24), ('abbr_per_k', None, 65, 15),
    ('connective_openings', None, 45, 21), ('value_end_share', None, 25, 6),
]


def check_en(text):
    secs = sections_en(text)
    report = {'language': 'en', 'sections': {}, 'document': []}
    for kind in ['abstract', 'intro', 'review', 'present', 'method', 'results', 'discussion', 'closing']:
        if sum(len(en_words(p)) for p in secs.get(kind, [])) < 30:  # absent, or a placeholder for the authors' part
            continue
        m, ex = en_metrics(secs[kind])
        flags = []
        if m['sentences'] >= 5 and m['words'] >= 150:
            for key, lo, hi, med in SECTION_RULES_EN.get(kind, []):
                if (lo is not None and m[key] < lo) or (hi is not None and m[key] > hi):
                    flags.append(f'{key} {m[key]} outside the published range ({"<" if lo is not None else ">"} {lo if lo is not None else hi} '
                                 f'flags; published median {med})')
        if kind == 'discussion' and m['sentences'] >= 5 and m['cite_per_k'] == 0:
            flags.append('the discussion cites no earlier study (published: 76% of discussion points compare with 2-4 cited studies)')
        if kind == 'review' and m['narrative_led_run'] >= 4:
            flags.append(f'{m["narrative_led_run"]} consecutive sentences open with "Author (year)": the review lists studies one by one '
                         '(published reviews synthesise first and illustrate with one or two studies)')
        if kind in ('discussion', 'closing') and ex['reviewer']:
            flags.append(f'{len(ex["reviewer"])} sentences propose analyses instead of reporting them (run them or move them to future research)')
        report['sections'][kind] = {'metrics': m, 'flags': flags, 'examples': ex}
    argued = [p for k in MAIN_EN for p in secs.get(k, [])]
    m, ex = en_metrics(argued)
    body = '\n'.join(argued).lower()
    count = lambda pat: len(re.findall(pat, body))
    per10k = lambda pat: round(10000 * count(pat) / m['words'], 1)
    doc = report['document']
    rare = re.findall(RARE, body)
    if len(rare) >= 4:
        doc.append(f'{len(rare)} rare stock phrases ({", ".join(sorted(set(rare)))}); published articles use at most 3 in total')
    if m['words'] >= 1500:
        for key, lo, hi, med in DOC_RULES_EN:
            if (lo is not None and m[key] < lo) or (hi is not None and m[key] > hi):
                doc.append(f'{key} {m[key]} in the argued sections, outside the published range (published median {med})')
        if per10k(SIGNPOST_EN) > 10:
            doc.append(f'signposting {per10k(SIGNPOST_EN)} per 10,000 words (published median 0, max 8)')
        if per10k(ADDITIVE) > 45:
            doc.append(f'furthermore/moreover/additionally/in addition {per10k(ADDITIVE)} per 10,000 words (published median 14.6, max 41)')
        if per10k(AI_WORDS) > 70:
            doc.append(f'AI-typical words {per10k(AI_WORDS)} per 10,000 words (published median 20, max 82 in one article)')
        over = [f'{w} {per10k(p)}' for w, (p, mx) in WORDS_EN.items() if count(p) >= 3 and per10k(p) > mx * 1.05]
        if over:
            doc.append('above the highest published rate per 10,000 words: ' + ', '.join(over))
    report['argued'] = m
    return report


def print_en(report):
    names = {'abstract': 'Abstract', 'intro': 'Introduction', 'review': 'Literature review', 'present': 'Present study',
             'method': 'Method', 'results': 'Results', 'discussion': 'Discussion', 'closing': 'Implications, limitations, conclusion'}
    published = {'intro': (23, 56, 0), 'review': (25.5, 58, 12), 'discussion': (13.5, 30, 7)}  # medians of the 31 articles
    total = sum(len(s['flags']) for s in report['sections'].values()) + len(report['document'])
    print(f'Sections found: {", ".join(names[k] for k in report["sections"])} | prompts: {total}')
    for kind, sec in report['sections'].items():
        m = sec['metrics']
        pub = [f' (published {v})' for v in published[kind]] if kind in published else ['', '', '']
        print(f'\n[{names[kind]}] {m["words"]} words, {m["paragraphs"]} paragraphs | sentence median {m["sentence_median"]}, '
              f'>40 words {m["long_share"]}% | citations {m["cite_per_k"]}/1,000 words{pub[0]}, cited sentences {m["cited_share"]}%{pub[1]}, '
              f'narrative {m["narrative_share"]}%{pub[2]}, 3+ works {m["bundle3_share"]}% | sentences with numbers {m["number_share"]}% | '
              f'we {m["we_per_k"]}/1,000 | passive {m["passive_share"]}%')
        for f in sec['flags']:
            print(f'  ! {f}')
        for key in ('reviewer', 'signpost'):
            for e in sec['examples'][key][:5]:
                print(f'    {key}: {e}')
    a = report['argued']
    print(f'\n[Argued sections together] {a["words"]} words | sentence median {a["sentence_median"]} (published 26.5), '
          f'>40 words {a["long_share"]}% (14.6) | paragraph median {a["paragraph_median"]} words (130) | we {a["we_per_k"]}/1,000 (4.8) | '
          f'passive {a["passive_share"]}% (24) | abbreviations {a["abbr_per_k"]}/1,000 (15) | paragraphs opening with a connective '
          f'{a["connective_openings"]}% (21) | value-sentence paragraph endings {a["value_end_share"]}% (6)')
    for f in report['document']:
        print(f'  ! {f}')


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--draft', required=True, type=Path)
    ap.add_argument('--json', action='store_true')
    a = ap.parse_args()
    text = read(a.draft)
    if len(re.findall(r'[一-鿿]', text)) < len(re.findall(r'[A-Za-z]+', text)):
        report = check_en(text)
        print(json.dumps(report, ensure_ascii=False, indent=1)) if a.json else print_en(report)
        return
    report = check(text)
    if a.json:
        print(json.dumps(report, ensure_ascii=False, indent=1))
        return
    names = {'abstract': '摘要', 'intro': '引言', 'review': '文献综述与假设', 'method': '研究设计', 'results': '研究结果',
             'discussion': '讨论', 'conclusion': '结论与建议'}
    total = sum(len(s['flags']) for s in report['sections'].values()) + len(report['document'])
    print(f'Sections found: {", ".join(names[k] for k in report["sections"])} | prompts: {total}')
    for kind, sec in report['sections'].items():
        m = sec['metrics']
        print(f'\n[{names[kind]}] {m["chars"]} chars, {m["paragraphs"]} paragraphs | sentence median {m["sentence_median"]}, '
              f'>100: {m["long_share"]}% | citations {m["cite_per_k"]}/1,000, cited sentences {m["cited_share"]}%, '
              f'author-led {m["author_led_share"]}% | statistics {m["stats_per_k"]}/1,000, decimals {m["decimals_per_k"]}/1,000 | '
              f'paragraph-final value sentences {m["value_end_share"]}%')
        for f in sec['flags']:
            print(f'  ! {f}')
        for key in ('reviewer', 'signpost'):
            for e in sec['examples'][key][:5]:
                print(f'    {key}: {e}')
    if report['document']:
        print('\n[全文]')
        for f in report['document']:
            print(f'  ! {f}')


if __name__ == '__main__':
    main()
