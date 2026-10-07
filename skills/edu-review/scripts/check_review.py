"""Check simulated reviewer reports and their synthesis for the required structure.

    python check_review.py --reports R1.md R2.md [R3.md] --synthesis synthesis.md [--json]

Checks: every major concern (R1-M1) has the fields blocking (是/否, Yes/No), axis, claim location, evidence
location, concern, why it matters and resolution test (Chinese or English field names), and its evidence field names a
location; every minor concern (R1-m1) has a location and an issue; concern ids are unique; ids cited in the synthesis
exist and every major concern appears in it; the synthesis says it is simulated; nothing predicts acceptance (a
sentence that says no prediction is made is fine).
"""
from pathlib import Path
import argparse
import json
import re
import sys

FIELDS = {
    'blocking': r'(?:是否阻断|Blocking)',
    'axis': r'(?:维度|Axis)',
    'claim': r'(?:论断位置|Claim)',
    'evidence': r'(?:证据位置|Evidence)',
    'concern': r'(?:问题|Concern)',
    'why': r'(?:为什么重要|Why it matters)',
    'resolution': r'(?:怎样算解决|Resolution test)',
}
MINOR_FIELDS = {'location': r'(?:位置|Location)', 'issue': r'(?:问题与建议|问题|Issue)'}
LOCATION = (r'(?:第\s*\d+\s*[页行段]|第[一二三四五六七八九十\d]+\s*(?:部分|节|段|章)|[（(][一二三四五六七八九十]+[）)]|[表图]\s*\d+|'
            r'(?<![\d.])\d+(?:\.\d+)+\s*节?|(?<![\d.])\d+\s*节|'  # numbered sections: 3.7, 3.7节, 4节
            r'摘要|引言|问题提出|文献综述|研究设计|研究方法|研究结果|讨论|结论|参考文献|附录|选题依据|研究内容|创新之处|研究基础|'
            r'标题|题目|关键词|声明|致谢|'
            r'\bpages?\s*\d+|\blines?\s*\d+|\bSection\s*\d|\bTable\s*\d|\bFigure\s*\d|\bAbstract|\bIntroduction|\bMethods?\b|'
            r'\bResults\b|\bDiscussion|\bConclusions?\b|\bparagraph)')
PROBABILITY = r'(?:录用概率|录用可能性为|接受概率|\d+\s*%\s*的?(?:可能|概率)(?:被)?录用|acceptance (?:probability|chance)|chance of (?:acceptance|being accepted)|likelihood of acceptance)'
NEGATED = r'(?:不预测|不估计|不给出|不提供|不做|不对|无法预测|并非|not (?:predict|estimate|give)|\bno\b|does not|without)'
ID = r'R\d+-[Mm]\d+'


def concerns(text):
    marks = [(m.start(), m.group(0)) for m in re.finditer(rf'^#+\s*({ID})\b', text, re.M)]
    marks = [(s, re.search(ID, h).group(0)) for s, h in marks]
    out = []
    for i, (start, cid) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(text)
        body = text.find('\n', start) + 1 or end
        nxt = re.search(r'^#{1,2}\s', text[body:end], re.M)  # a higher-level heading ends the concern
        out.append((cid, text[start:body + nxt.start()] if nxt else text[start:end]))
    return out


def field_value(block, pattern):
    """Value of a '- 字段：值' line, plus indented or numbered continuation lines below it. An empty field stays
    empty instead of taking the next field's line."""
    m = re.search(rf'^[ \t]*[-*]?[ \t]*(?:\*\*)?{pattern}(?:\*\*)?[^：:\n]*[：:][ \t]*(.*)$', block, re.I | re.M)
    if not m:
        return None
    value = [m.group(1)]
    for line in block[m.end():].split('\n')[1:]:
        if re.match(r'^(?:[ \t]+\S|\d+[.、)）])', line):
            value.append(line.strip())
        elif line.strip():
            break
    return ' '.join(value).strip().strip('*').strip()


def probability_claims(text):
    """Acceptance predictions, skipping sentences that say no prediction is made."""
    out = []
    for m in re.finditer(PROBABILITY, text, re.I):
        start = max(text.rfind('。', 0, m.start()), text.rfind('. ', 0, m.start()), text.rfind('\n', 0, m.start())) + 1
        if not re.search(NEGATED, text[start:m.start()], re.I):
            out.append(m.group(0))
    return out


def check(reports, synthesis):
    issues, ids = [], []
    for path, text in reports:
        found = concerns(text)
        if not found:
            issues.append(f'{path}: no numbered concerns (R1-M1, R1-m1) found')
        for cid, block in found:
            if cid in ids:
                issues.append(f'{cid}: id used more than once')
            ids.append(cid)
            major = re.search(r'-M\d', cid) is not None
            for name, pattern in (FIELDS if major else MINOR_FIELDS).items():
                value = field_value(block, pattern)
                if not value or value in ('……', '...', '…'):
                    issues.append(f'{cid}: missing field {name}')
            if major:
                blocking = field_value(block, FIELDS['blocking']) or ''
                if blocking and not re.match(r'(?:是|否|yes\b|no\b)', blocking, re.I):
                    issues.append(f'{cid}: blocking should be 是/否 (Yes/No), got "{blocking[:20]}"')
                ev = field_value(block, FIELDS['evidence']) or ''
                if re.search(r'(?:见|see).{0,6}(?:问题|concern)', ev, re.I):
                    ev += ' ' + (field_value(block, FIELDS['concern']) or '')  # locations listed in the concern field
                if ev and not re.search(LOCATION, ev, re.I):
                    issues.append(f'{cid}: evidence field names no location: "{ev[:50]}"')
        for claim in probability_claims(text):
            issues.append(f'{path}: acceptance-probability claim "{claim}"')
    if synthesis is not None:
        path, text = synthesis
        cited = set(re.findall(ID, text))
        for cid in sorted(cited - set(ids)):
            issues.append(f'{path}: cites {cid}, which is not in any report')
        for cid in [i for i in ids if re.search(r'-M\d', i) and i not in cited]:
            issues.append(f'{path}: major concern {cid} does not appear in the synthesis')
        if not re.search(r'(?:模拟|simulat)', text, re.I):
            issues.append(f'{path}: does not say the review is simulated')
        for claim in probability_claims(text):
            issues.append(f'{path}: acceptance-probability claim "{claim}"')
    majors = sum(bool(re.search(r'-M\d', i)) for i in ids)
    return {'concerns': len(ids), 'major': majors, 'minor': len(ids) - majors, 'issues': issues}


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--reports', required=True, nargs='+', type=Path)
    ap.add_argument('--synthesis', type=Path)
    ap.add_argument('--json', action='store_true')
    a = ap.parse_args()
    reports = [(p.name, p.read_text(encoding='utf-8')) for p in a.reports]
    synthesis = (a.synthesis.name, a.synthesis.read_text(encoding='utf-8')) if a.synthesis else None
    result = check(reports, synthesis)
    if a.json:
        print(json.dumps(result, ensure_ascii=False, indent=1))
        return
    print(f'Concerns: {result["concerns"]} (major {result["major"]}, minor {result["minor"]}) | issues: {len(result["issues"])}')
    for i in result['issues']:
        print('  ' + i)
    if result['issues']:
        sys.exit(1)


if __name__ == '__main__':
    main()
