"""Screen how statistics are reported in a manuscript (no recomputation).

    python check_reporting.py --draft 论文.docx|.md|.txt [--json]

Sentence-level checks: t, F and chi-square without degrees of freedom; tests without an effect size in the same
sentence; p printed as 0.000; p values without a test statistic; claims of significance with no statistic and no
table reference; indirect effects without a confidence interval; coefficients without SE or CI.
Document-level checks (reported only when the relevant analysis appears): SEM/CFA fit indices, CR/AVE and
discriminant validity, common-method bias for questionnaire data, assumption checks for t tests and ANOVA,
correction for multiple comparisons, missing data, software, sample-size justification, ethics and consent.
Every item is a prompt to read the passage; the script does not know whether a statistic is reported in a table.
"""
from pathlib import Path
import argparse
import json
import re
import sys

T_DF = r'(?<![A-Za-z])t\s*\(\s*\d+(?:\.\d+)?\s*\)\s*=\s*-?\d'
T_NO = r'(?<![A-Za-z(])t\s*=\s*-?\d'
F_DF = r'(?<![A-Za-z])F\s*\(\s*\d+\s*[,，]\s*\d+(?:\.\d+)?\s*\)\s*=\s*\d'
F_NO = r'(?<![A-Za-z(])F\s*=\s*\d'
CHI = r'(?:χ\s*2|χ²|chi-?square|卡方)'
CHI_DF = CHI + r'\s*\(\s*\d+|\bdf\s*=\s*\d'
EFFECT = r"(?:Cohen'?s?\s*d|\bd\s*=|\bg\s*=|η\s*[²2p]|eta|ω\s*²|\br\s*=|Cramér|Cramer|\bV\s*=|φ|phi|R\s*[²2]|效应量|odds ratio|\bOR\s*=)"
# an estimate with an interval counts as a reported statistic: d* = 0.04 [-0.15, 0.24], 调整差 0.05 分 [...]
STAT = (r'(?:\b[tFzZ]\s*[(=]|' + CHI + r'|\b[rR]\s*=|β|\b[Bb]\s*=|\bOR\s*=|\bU\s*=|\bH\s*\(|\bW\s*=|95%|CI|置信区间|'
        r'\b[dg]\*?\s*=|ICC|\[\s*-?\d*\.\d+\s*,\s*-?\d*\.\d+\s*\]|\bp\s*[<=>≤])')
DISPLAY = r'(?:表\s*\d|图\s*\d|Table\s*\d|Figure\s*\d|Fig\.\s*\d)'
SIG = r'(?:显著|significant(?:ly)?\b)'
NOT_SIG = r'(?:不显著|未达到显著|non-?significant|not\s+significant|无显著)'
# Chinese manuscripts write operators full-width (p＝0.03, F（2，495）) and minus as U+2212
FULLWIDTH = str.maketrans({'＝': '=', '＜': '<', '＞': '>', '（': '(', '）': ')', '−': '-', '＋': '+'})


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


def sentences(text):
    out = []
    for line in text.splitlines():
        if line.strip().startswith('|'):
            continue  # table rows are not prose
        out += [s.strip() for s in re.split(r'(?<=[。！？；])|(?<=[.!?;])\s+(?=[A-Z一-鿿])', line) if len(s.strip()) > 6]
    return out


def has(pattern, s):
    return re.search(pattern, s, re.I) is not None


def sentence_checks(sents):
    hits = []
    add = lambda kind, s: hits.append({'check': kind, 'sentence': s[:160]})
    for s in sents:
        if has(T_NO, s) and not has(T_DF, s):
            add('t without degrees of freedom', s)
        if has(F_NO, s) and not has(F_DF, s):
            add('F without degrees of freedom', s)
        if has(CHI + r'\s*=', s) and not has(CHI_DF, s) and not has(r'χ\s*[²2]\s*/\s*df|CMIN/DF', s):
            add('chi-square without degrees of freedom', s)
        if (has(T_DF, s) or has(F_DF, s) or has(T_NO, s) or has(F_NO, s) or has(CHI_DF, s)) and not has(EFFECT, s) \
                and not has(r'χ\s*[²2]\s*/\s*df|CFI|RMSEA', s):
            add('test without an effect size in the same sentence', s)
        if has(r'\bp\s*=\s*0?\.0+(?!\d*[1-9])', s):
            add('p printed as zero (write p < .001)', s)
        if has(r'\bp\s*[<=>≤]\s*0?\.\d', s) and not has(STAT.replace(r'|\bp\s*[<=>≤])', ')'), s) and not has(DISPLAY, s):
            add('p value without a test statistic or table reference', s)
        if has(SIG, s) and not has(NOT_SIG, s) and not has(STAT, s) and not has(DISPLAY, s) \
                and not has(r'(?:研究|文献|学者|studies|research|literature)', s):
            add('significance claimed without a statistic or table reference', s)
        if has(r'(?:间接效应|中介效应|indirect effect|mediat)', s) and has(r'(?:\d\.\d|β|\bb\s*=)', s) \
                and not has(r'(?:CI|置信区间|\[\s*-?\d?\.\d+\s*[,，]\s*-?\d?\.\d+\s*\]|bootstrap)', s):
            add('indirect effect without a (bootstrap) confidence interval', s)
        if has(r'(?:β|\b[Bb])\s*=\s*-?\d?\.\d', s) and not has(r'(?:\bSE\b|标准误|CI|置信区间|\[\s*-?\d?\.\d+\s*[,，])', s):
            add('coefficient without SE or CI in the same sentence', s)
    return hits


DOC = [
    ('sem', r'(?:结构方程|SEM\b|CFA|验证性因子|confirmatory factor|structural equation|\bCFI\b|RMSEA)',
     [('fit: chi-square and df', r'(?:χ\s*[²2]|chi-?square|CMIN)'), ('fit: CFI', r'\bCFI\b'), ('fit: TLI', r'\b(?:TLI|NNFI)\b'),
      ('fit: RMSEA', r'\bRMSEA\b'), ('fit: SRMR', r'\bSRMR\b'),
      ('composite reliability (CR)', r'(?:\bCR\b|组合信度|composite reliability)'),
      ('convergent validity (AVE)', r'(?:\bAVE\b|平均方差抽取|average variance extracted)'),
      ('discriminant validity (HTMT or Fornell–Larcker)', r'(?:HTMT|Fornell|区分效度|discriminant validity)')]),
    ('questionnaire', r'(?:问卷|量表|questionnaire|self-report|Likert|李克特)',
     [('common-method bias check', r'(?:共同方法|common[- ]method|Harman)'),
      ('reliability (α or ω)', r'(?:α|alpha|Cronbach|ω|omega|信度)')]),
    ('group comparison', r'(?:t\s*检验|方差分析|ANOVA|t-test|t test|\bt\s*\(|\bF\s*\()',
     [('assumption checks (normality, homogeneity, Welch)', r'(?:正态|方差齐|Levene|Welch|normality|homogeneity|Shapiro)')]),
    ('multiple comparisons', r'(?:事后|两两比较|多重比较|post[- ]hoc|pairwise)',
     [('correction method (Bonferroni, Holm, Tukey, FDR ...)', r'(?:Bonferroni|Holm|Tukey|Scheff|Games-Howell|FDR|Benjamini|校正|矫正)')]),
    ('any analysis', r'(?:\bp\s*[<=>≤]|显著|significant)',
     [('missing data handling', r'(?:缺失|missing|FIML|插补|imputation|listwise|删除)'),
      ('software', r'(?:SPSS|\bR\s*\(?\d|\bR\b 软件|lavaan|Mplus|AMOS|Stata|SmartPLS|fsQCA|JASP|Python|SAS)'),
      ('sample-size justification (power analysis or rule)', r'(?:G\*?Power|功效分析|统计检验力|power analysis|样本量估计|sample size (?:was )?(?:determined|calculated|justif))'),
      ('ethics approval or informed consent', r'(?:知情同意|伦理|informed consent|ethic|IRB)')]),
]


def document_checks(text):
    out = []
    for name, trigger, items in DOC:
        if re.search(trigger, text, re.I):
            missing = [label for label, pattern in items if not re.search(pattern, text, re.I)]
            if missing:
                out.append({'analysis': name, 'not_found': missing})
    if re.search(r'(?<![A-Za-z])LSD(?![A-Za-z])', text) and re.search(r'(?:事后|多重比较|post[- ]hoc)', text, re.I):
        out.append({'analysis': 'multiple comparisons', 'not_found': ['LSD does not correct for multiple comparisons']})
    return out


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--draft', required=True, type=Path)
    ap.add_argument('--json', action='store_true')
    a = ap.parse_args()
    text = read(a.draft).translate(FULLWIDTH)
    report = {'sentences': sentence_checks(sentences(text)), 'document': document_checks(text)}
    if a.json:
        print(json.dumps(report, ensure_ascii=False, indent=1))
        return
    print(f'Sentence-level prompts: {len(report["sentences"])}')
    for h in report['sentences']:
        print(f'  [{h["check"]}] {h["sentence"]}')
    print(f'\nNot found anywhere in the manuscript: {sum(len(d["not_found"]) for d in report["document"])}')
    for d in report['document']:
        print(f'  {d["analysis"]}: ' + '; '.join(d['not_found']))


if __name__ == '__main__':
    main()
