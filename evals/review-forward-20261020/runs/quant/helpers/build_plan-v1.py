from pathlib import Path
from datetime import datetime, timezone
import json

base = Path(__file__).resolve().parents[1] / 'edu_output' / 'review' / 'retrieval'
inventory = json.loads((base / 'anchors.json').read_text(encoding='utf-8'))
units = {(x['page'], x['line']): x for x in inventory['units']}

def anchor(page, line, quote):
    unit = units[(page, line)]
    assert unit['text'].count(quote) == 1, (page, line, quote)
    start = unit['text'].index(quote)
    return {'page': page, 'line': line, 'text_sha256': unit['text_sha256'], 'start': start, 'end': start + len(quote), 'quote': quote}

annotations = [
    {
        'id': 'C1', 'kind': 'error', 'severity': 'major',
        'comment': 'The inference of equal effectiveness does not follow from p = .12 or from a confidence interval spanning zero. The reported interval (-0.05 to 0.41) also includes a positive difference that the Discussion identifies as potentially educationally meaningful. Equivalence would require a justified equivalence margin and a corresponding analysis; neither is reported here. Align the abstract with the Discussion: for example, "The estimated between-condition difference was uncertain; the findings do not establish either superiority or equivalence." This concerns the interpretation, not proof that the numerical estimate is incorrect. See C2 for the model information needed to assess its uncertainty.',
        'anchors': [anchor(1, 5, 'The two approaches were'), anchor(1, 6, 'therefore equally effective.')]
    },
    {
        'id': 'C2', 'kind': 'verify', 'severity': 'major',
        'comment': 'Classes were randomized within schools, but this description does not specify how the analysis handled dependence among pupils in a class or the within-school allocation. A pupil-level regression is not inherently inappropriate; the model and inference must reflect the design. Report the model formula, treatment of school/block effects and class clustering, standard-error method, and degrees of freedom or small-sample adjustment used with only 12 randomized classes. If pupils were treated as independent for inference, reanalyse with a justified method that respects the allocation and update the estimate, interval and p value. Code/model output would allow verification; their absence here does not establish that the reported statistics are wrong. The final Discussion acknowledges this issue for a follow-up, but the current trial also needs it addressed.',
        'anchors': [anchor(1, 12, 'An ordinary individual-level regression was fitted, with pupil as the unit of analysis.')]
    },
    {
        'id': 'C3', 'kind': 'error', 'severity': 'major',
        'comment': 'A significant within-condition change (p = .02) and a nonsignificant change in the other condition (p = .21) do not establish that the changes differ between conditions. Those tests address separate null hypotheses. Base the comparative conclusion on the direct between-condition contrast, whose reported interval includes zero, rather than on the difference in significance labels. If a difference in change is an additional research question, estimate that contrast directly with inference reflecting class assignment. The present superiority statement also conflicts with both the abstract\'s equality claim (C1) and the Discussion\'s appropriate statement of uncertainty.',
        'anchors': [anchor(1, 17, 'This difference in statistical significance'), anchor(1, 18, 'establishes that retrieval practice outperformed usual review.')]
    },
    {
        'id': 'C4', 'kind': 'verify', 'severity': 'minor',
        'comment': 'Please define how this adjusted standardized contrast was calculated: the adjusted score contrast, standardizing SD, any small-sample correction, and the method used for its confidence interval and p value. The raw posttest means of 79 and 75 alone cannot verify or interpret this baseline-adjusted g. Reporting the test scale and an adjusted difference in score units with uncertainty would also help readers judge educational importance. This is a reporting/verification gap in the excerpt, not evidence of a numerical inconsistency; see C2 for the separate question of design-appropriate inference.',
        'anchors': [anchor(1, 5, 'g = 0.18, 95% CI [-0.05, 0.41], p = .12.')]
    },
    {
        'id': 'C5', 'kind': 'verify', 'severity': 'minor',
        'comment': 'The intended contrast between retrieval and review is clear, but equal subject content and an eight-week duration do not by themselves establish comparable exposure time. Specify the usual-review activity, planned time per activity, and whether implementation evidence confirms comparable time and feedback across conditions. If time was not measured or controlled, identify this as the intended design distinction rather than a demonstrated explanation of the outcome. This would make the contribution more interpretable without changing the Discussion\'s justified statement that the performance comparison remains uncertain.',
        'anchors': [anchor(2, 3, 'rather than simply increasing their exposure time.')]
    },
    {
        'id': 'C6', 'kind': 'verify', 'severity': 'minor',
        'comment': 'Please identify the treatment assignments and experience of the eight respondents, and what activity the seven favorable responses referred to. The Methods allocates only six classes to retrieval practice, whereas this questionnaire includes eight of 12 class teachers; it is therefore unclear how many responses describe actually delivering retrieval practice. This is not necessarily a contradiction, since control teachers may have observed or tried it, but that context is needed to interpret feasibility. Retain the useful restriction to respondents and the distinction from student motivation. The conditional recommendation to provide preparation time and suitable questions has an explicit implementation rationale and does not require a superiority claim.',
        'anchors': [anchor(2, 6, 'Eight of the 12 class teachers returned a short implementation questionnaire.')]
    }
]
plan = {'schema_version': 1, 'comment_language': 'en', 'source_sha256': inventory['source_sha256'], 'created_utc': datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z'), 'annotations': annotations}
(base / 'annotations-v1.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'annotations': len(annotations), 'errors': sum(x['kind'] == 'error' for x in annotations), 'verification_requests': sum(x['kind'] == 'verify' for x in annotations), 'plan': str(base / 'annotations-v1.json')}))
