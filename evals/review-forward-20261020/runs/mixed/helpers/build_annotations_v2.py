from pathlib import Path
from datetime import datetime, timezone
import json
out=Path.cwd()/'edu_output/review/mixed-review'
plan=json.loads((out/'annotations-v1.json').read_text(encoding='utf-8'))
plan['created_utc']=datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
comments={
'C1':'The abstract reports 52 students; Methods and Table 1 report 48 completed responses (24 + 24), with 48 as the usefulness denominator. This establishes an internal inconsistency, not which count is correct. Reconcile the counts against the study records, distinguishing any different populations or exclusions. Also describe the finding as 31 respondents rating the feedback useful; the excerpt provides no measured learning gains to support a broader benefit claim.',
'C2':'The excerpt does not provide the usefulness item, response options, or positive-rating rule. These details are needed to interpret the 31 favorable responses and relate perceived usefulness to interview accounts. Report them in the full Methods or instrument appendix, including treatment of any missing item responses. Their absence here does not establish that measurement procedures were omitted.',
'C3':'The interview prompts/timing, analytic approach, and supporting excerpts are not supplied, so the grounding of the six timing accounts and two later-use accounts cannot be assessed. In the full paper, provide these details and contextualized case evidence; clarify whether the two descriptions overlap and how exceptions were considered. This is an evidence gap in the excerpt, not a finding that analysis was not done.',
'C4':'This contradicts the preceding interview paragraph: even survey participation could not be determined, and the survey collected no linkage identifier. The Discussion also correctly says favorable respondents cannot be matched to timing accounts. Under the stated design, subgroup membership cannot be established. Align this sentence with that lack of linkage and integrate the survey pattern with interview accounts at the group or conceptual level.',
'C5':'Methods states that no learning-gain test was collected, and the interview paragraph limits its evidence to reported opportunities and uses. No statistical mechanism analysis is reported. These accounts cannot establish improved achievement or validate that mechanism. Instead, integrate favorable survey ratings with interview accounts of timing constraints and later use. The Discussion already makes this defensible distinction; its concrete scheduling recommendation can stand. See C4 for the separate linkage contradiction.'
}
for a in plan['annotations']:
    a['comment']=comments[a['id']]
(out/'annotations-v2.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'annotations':len(plan['annotations']),'words':sum(len(x.split()) for x in comments.values())},indent=2))
