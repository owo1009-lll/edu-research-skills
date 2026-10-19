from pathlib import Path
from datetime import datetime, timezone
import json
base = Path.cwd()
out = base/'edu_output/review/mixed-review'
inv = json.loads((out/'anchors.json').read_text(encoding='utf-8'))
items = [
('C1','error','major',3,
 'Survey responses from 52 students showed that feedback was useful.',
 'The abstract reports 52 students, whereas Methods reports 48 completed responses and Table 1 lists 24 + 24 = 48, with 48 as the usefulness denominator. This establishes an internal inconsistency, not which count is correct. Reconcile the numbers against the study records and distinguish any different populations or exclusions consistently. Also describe this result as respondents rating the feedback useful: the excerpt reports 31 favorable ratings and no measured learning gains, so the current wording can imply a broader finding than the evidence supports.'),
('C2','verify','minor',5,
 'Thirty-one respondents rated the feedback useful.',
 'The supplied excerpt does not give the usefulness item, response options, or rule for classifying a response as favorable. These details are needed to interpret the 31 responses and the construct being compared with interview accounts. Report them in the full Methods or an accessible instrument appendix and confirm how missing item responses, if any, were handled. This is a reporting gap in the supplied material, not evidence that these procedures were omitted.'),
('C3','verify','major',15,
 'Six described receiving useful comments too close to the next submission deadline to revise their work.',
 'This timing account is central to the study\'s contribution, but the excerpt does not show how the interviews elicited these experiences or how the six timing accounts and two later-use accounts were derived. In the full paper, provide the relevant interview timing/prompts, analytic approach, and short contextualized excerpts or case evidence, clarifying whether the two descriptions are mutually exclusive and how exceptions were considered. Without those materials, the grounding and boundaries of this interpretation cannot be assessed; their absence here does not establish that analysis was not done.'),
('C4','error','major',16,
 'All interviewees belonged to the favorable-rating subgroup.',
 'This contradicts the preceding interview paragraph, which states that even survey participation could not be determined, and the survey paragraph, which states that no linkage identifier was collected. The Discussion also correctly says that the samples cannot identify which favorable respondents experienced timing constraints. On the stated design, subgroup membership cannot be established. Align this sentence with the documented lack of linkage and compare the survey pattern with interview accounts at the group or conceptual level; do not imply participant-level correspondence.'),
('C5','error','major',16,
 'Their accounts validate the statistical mechanism by which useful feedback improved achievement.',
 'The Methods explicitly states that no test of learning gains was collected, and the interview paragraph limits its evidence to reported opportunities and uses. No statistical mechanism analysis is reported in this excerpt. These accounts therefore cannot establish improved achievement or validate the claimed statistical mechanism. Replace this inference with an integration of what the two sources actually contribute: favorable survey ratings coexist at the study level with interview accounts of constrained timing and later use, distinguishing perceived value from an opportunity to act. The Discussion already makes this defensible distinction, and its practical scheduling recommendation need not be weakened on this account. See C4 for the separate linkage contradiction.')
]
plan = {'schema_version':1,'comment_language':'en','source_sha256':inv['source_sha256'],'created_utc':datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),'annotations':[]}
for aid,kind,severity,idx,quote,comment in items:
    unit=inv['units'][idx]
    assert unit['paragraph']==idx
    assert unit['text'].count(quote)==1,(aid,'anchor ambiguity')
    start=unit['text'].index(quote)
    anchor={k:unit[k] for k in ['part','paragraph','text_sha256']}
    anchor.update(start=start,end=start+len(quote),quote=quote)
    plan['annotations'].append({'id':aid,'kind':kind,'severity':severity,'comment':comment,'anchors':[anchor]})
(out/'annotations-v1.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'annotations':len(items),'created_utc':plan['created_utc'],'table_sum':24+24},indent=2))
