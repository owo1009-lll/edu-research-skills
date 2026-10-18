# Focused review — AI self-check

This is an AI review of the saved `first.md`, not independent expert review. Scope: the requested Introduction, Discussion and Conclusion against the supplied fictional evidence pack and relevant skill instructions. No statistical reanalysis was performed.

## Main judgement

The draft answers the primary delayed-transfer question before the secondary immediate result, retains the authors' educational position, and develops a substantive distinction among instructional opportunity, subjective experience and durable learning. It does not claim equivalence, effect decay, age moderation, a measured mechanism, or a cost-effectiveness result. The main revision should sharpen the conditional instructional recommendation and make the limits of the preparation records more precise.

## Findings and planned revision

| Location | Finding | Revision decision |
|---|---|---|
| Introduction paragraph 1 | The opening is grounded in the supplied decision problem, but “concerns whether the opportunity … when choosing a routine” is indirect. | State the delayed-transfer decision more directly and link the distinction to the replacement criterion. |
| Discussion opening | The primary estimate and interval are accurate. The explicit no-equivalence sentence prevents a foreseeable misreading and is not generic defensiveness. | Retain the interval and one equivalence explanation, without adding a second elsewhere. |
| Discussion immediate-outcome paragraph | The result is clearly secondary and the untested difference between time-specific effects is acknowledged. R1 and R2 are accurately distinguished, but the paragraph carries two comparisons. | Split the delayed-recall comparison into its own short paragraph and make the present study's specific evidential addition explicit. |
| Discussion reconstruction paragraph | Completion, quality, ease and learning are distinguished correctly. The R2 explanation remains a candidate. | Preserve the substantive distinction, condense the final abstract sentence, and state the instructional consequence positively. |
| Discussion implications | “Without an inferential comparison they do not rank … cost-effectiveness” could suggest that a significance test of preparation time would suffice for cost-effectiveness. | Report that preparation medians are descriptive and untested; separately state that preparation alone cannot establish cost-effectiveness. Link the conditional choice to the relevant outcome and preparation demand. |
| Discussion implications | The explicit denial of interchangeability repeats an inference already blocked by the first paragraph. | Remove this repeated negative sentence while keeping the short-term condition inside the affirmative recommendation. |
| Discussion final paragraph | Missingness and setting limits are grouped, but no named limitations unit is present for the checker. | Give the paragraph a “Limitations and scope” subheading; retain the substantive explanation of missingness. |
| Conclusion | The answer retains uncertainty and the authors' intended criterion. | Retain that judgement, reduce repetition of the mechanism distinction, and close with the specific purpose of subsequent work. |

## Cross-section semantic audit

| Claim | Introduction | Discussion | Conclusion | Verdict |
|---|---|---|---|---|
| Primary question | Delayed conceptual transfer after six-week routine | Unresolved superiority; d = 0.08, CI [-0.07, 0.23] | Unresolved advantage, with relevant benefit still included | Same question and answer; precision is not converted into “no effect” |
| Immediate finding | Secondary assessment nearer instruction | d = 0.24, CI [0.09, 0.39]; conditional short-term use | Conditional use for explicit short-term purpose | Secondary status and teaching purpose retained |
| Durability | Delayed outcome motivates the comparison | Difference between time-specific effects untested | No claim of retained or vanished benefit | No significance-versus-nonsignificance fallacy |
| Reconstruction | Attempt before checking example | 81% attempts; quality and mediation unmeasured | Opportunity is not treated as durable superiority | No observed mechanism claim |
| Practical choice | Intended learning determines decision | Delayed transfer for replacement; preparation considered for conditional use | Same outcome-specific priority | No recommendation based on equivalence or ease |

## Source and numerical audit

- Three schools with eight classes each; 12 classes per condition. Randomisation was at class level within schools. The draft does not invent individual allocation, sample power or preregistration.
- Common content, 15 scheduled minutes, and the same teacher explanation afterward are accurately described. It does not claim equal teacher preparation.
- Primary d = 0.08 and 95% CI [-0.07, 0.23] refer to conceptual transfer three weeks after the intervention and favour retrieval. They are not treated as a null effect or proof of equivalence.
- Secondary d = 0.24 and 95% CI [0.09, 0.39] refer to immediate conceptual transfer. There is no computed or tested contrast between the two estimates.
- 81% refers to scheduled retrieval activities in which an explanation was attempted, not to correct responses, pupils, fidelity across both arms, or productive reconstruction.
- Preparation medians are 10 minutes for retrieval and 6 for rereading, per lesson. No new test, total cost, ratio or economic ranking is introduced.
- 480 enrolled and 456 completing both tests are distinct denominators. Twelve missing per condition does not establish ignorable missingness.
- [R1] is used only for the university laboratory experiment's individually randomised comparison, delayed factual recall outcome and contextual differences. No age moderation, transfer measure or classroom implementation is attributed to it.
- [R2] is used only for the school comparison's immediate conceptual finding, teacher-selected conditions, absent delayed test and unmeasured effortful-reconstruction explanation.
- Both cards are explicitly fictional. No bibliography is fabricated and no outside reference supports a manuscript claim.

## Script results and adjudication

All three first-draft checks exited successfully; their complete outputs are saved in `checks/first-voice.txt`, `checks/first-prose.txt` and `checks/first-consistency.txt`.

1. **Voice:** one no-equivalence disclaimer cue; retained because it changes the interpretation of the primary interval. Two substantive-distinction cues concern retention and balanced missingness; both are accurate and necessary. One interchangeability semantic cue is a negated assertion, not a claim of equivalence, but its sentence can be cut as repetition. Zero stacked-hedge cues and zero unsupported-number cues. Low authorial self-mention is descriptive; a small use of “we” will clarify who found the immediate benefit, without chasing a rate.
2. **Prose:** four citation prompts arise because the checker does not recognise [R1]/[R2]. Manual inspection finds both cards in the Introduction and both in the Discussion, attached to supported claims. No real author–date or numbered bibliography will be added to satisfy that parser. Sentence and paragraph statistics are references, not quality targets; key estimates and intervals are retained because precision determines the practical answer.
3. **Consistency:** zero reported findings. The parser detected no sample-size statements and no numeric citations, so its clean result cannot replace the numerical and card audits above. CI is defined at first use. No abstract, tables or figures are requested.

First-draft length: 897 whitespace-delimited body words excluding the simulation notice and headings; 901 words with the accompanying lexical-count method. The prose script uses a different tokenisation and reports 895. Each count lies within the requested 800–1,000-word range.

## Remaining limitations

The supplied record is a closed fictional evidence set, so results are checked against it rather than against data, code or publications. The writing checks detect surface cues; interpretation has been reviewed directly against the supplied facts. No external validity, mediation, equivalence, time-contrast or economic analysis has been added. Final checks will be saved separately after the planned single revision.

## Final verification after revision

The single planned revision is saved in `final.md`. Its body contains 892 whitespace-delimited words, excluding the notice and headings; the lexical counter reports 896 and the prose script reports 890. The two supplied labels appear five times in the body: [R1] twice and [R2] three times. The simulation notice remains above the manuscript. All requested files are Markdown except the requested JSON load log and machine-readable verification record.

The three final check processes exited with code 0. Complete outputs are `checks/final-voice.txt`, `checks/final-prose.txt` and `checks/final-consistency.txt`; counts are in `checks/verification.json`.

- The voice checker now identifies two disclaimer cues: absence of equivalence support and the limits of attempt records. Each prevents a specific unsupported inference and stays beside the relevant finding. Its substantive cues concerning retention, age moderation and cost-effectiveness are accurate distinctions. The latter two also appear as “limitations outside the limitations unit”; they qualify their particular comparisons and therefore remain there. The actual limitations paragraph groups missing outcomes and setting scope, even though the checker's pattern-based limitation rate is 0%. No stacked-hedge, semantic-risk or unsupported-number cue remains.
- The same four citation prompts are parser limitations for [R1]/[R2], adjudicated by direct comparison with the cards. No citations are missing from the supplied evidence set. The lower sentence-length and self-mention rates are not treated as defects or mechanically altered.
- Consistency reports no findings. It still misses natural-language sample-size statements, so the manual source audit remains essential. “This study” and “the present study” both refer to the supplied experiment, not to either comparison card.

The final text retains the unresolved primary answer, a supported immediate benefit, and conditional recommendations without converting unmeasured processes or descriptive costs into findings. Completion is a writing-and-records judgement for this fictional exercise, not empirical validation or publication readiness.
