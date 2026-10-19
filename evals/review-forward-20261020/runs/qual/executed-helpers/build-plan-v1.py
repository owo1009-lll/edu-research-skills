from pathlib import Path
import json
from datetime import datetime, timezone
import fitz

root = Path(__file__).resolve().parents[1]
review = root / 'edu_output' / 'review' / 'submission-review'
source = Path(r'<experiment>\inputs-final\qual_silence.pdf')
inventory = json.loads((review / 'anchors.json').read_text(encoding='utf-8'))
units = {(u['page'], u['line']): u for u in inventory['units']}

def anchor(page, line, quote):
    unit = units[(page, line)]
    assert unit['text'].count(quote) == 1, (page, line, quote)
    start = unit['text'].index(quote)
    return {'page': page, 'line': line, 'text_sha256': unit['text_sha256'],
            'start': start, 'end': start + len(quote), 'quote': quote}

plan = {
    'schema_version': 1,
    'comment_language': 'en',
    'source_sha256': inventory['source_sha256'],
    'created_utc': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    'annotations': [
        {
            'id': 'C1', 'kind': 'verify', 'severity': 'major',
            'comment': "Recruitment and access are explicitly unreported in this excerpt. In the full methods, explain how the three programs and nine teachers were selected, who invited participation, the basis for inclusion, and the researcher's role and relationship to the teams. These details matter here because access through managers or existing relationships could shape whose accounts are available and how concerns about speaking are expressed. Report the actual arrangements and any relevant reflexive considerations; the omission in this excerpt does not establish that recruitment or access procedures were inadequate.",
            'anchors': [
                anchor(1, 6, 'The supplied excerpt does not describe how'),
                anchor(1, 7, 'the nine teachers were recruited or how the researcher entered the teams.')
            ]
        },
        {
            'id': 'C2', 'kind': 'verify', 'severity': 'major',
            'comment': "This provides the focus of comparison but not enough of the analytic process to assess how the interpretation was developed. In the full methods, explain what counted as an episode or case, how interview accounts were compared with meeting records, how these two illustrative cases relate to the wider material, and how discrepant accounts or alternative interpretations were considered. Clarify which sources support the email, later agenda and partial adoption in Marta's sequence, and the limits of the record supporting the absence of a later proposal from Amir. Distinguish participants' stated intentions from the researcher's interpretation. These are reporting details to verify from the actual study records, not a requirement to add frequency counts, statistical tests or a particular coding-agreement metric.",
            'anchors': [
                anchor(1, 4, 'Analysis compared how speaking,'),
                anchor(1, 5, units[(1, 5)]['text']),
                anchor(1, 6, 'accounts were considered alongside the meeting records.')
            ]
        },
        {
            'id': 'C3', 'kind': 'error', 'severity': 'major',
            'comment': "The universal conclusion conflicts with the distinction developed in the findings (p. 1, Marta and Amir) and the preceding paragraph here. Marta describes waiting before an alternative intervention; Amir describes concern about the manager's reaction, without a stated intention to resist or a documented planned alternative intervention. These accounts do not support classifying every silence as deliberate resistance or claiming that all silent teachers intended to intervene. The same paragraph also asserts equal influence: the excerpt traces partial adoption of Marta's proposal but provides no comparison with frequent speakers that establishes equality. Remove or reformulate these claims around the distinction the cases actually support, for example: 'The cases distinguish waiting as part of an intervention from silence under anticipated sanction.' The preceding interpretation of heterogeneous silence and the following recommendation about responsive routes for contributions can be retained. This is an internal evidence-to-conclusion problem, not a consequence of lacking statistical tests.",
            'anchors': [anchor(2, line, units[(2, line)]['text']) for line in (5, 6, 7)]
        }
    ]
}
(review / 'annotations-v1.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding='utf-8')
with fitz.open(source) as doc:
    extracted = '\n\n'.join(f'PAGE {i+1}\n{page.get_text()}' for i, page in enumerate(doc))
    (review / 'source-extracted.txt').write_text(extracted, encoding='utf-8')
    for i, page in enumerate(doc):
        page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5), annots=True).save(review / 'previews' / f'source-page-{i+1}.png')
    print(json.dumps({'source_opened_with': 'PyMuPDF', 'pages': len(doc), 'rendered_pages': len(doc),
                      'annotations_planned': len(plan['annotations']), 'plan': str(review / 'annotations-v1.json')}, indent=2))
