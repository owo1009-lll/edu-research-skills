# Writing rationale and evidence record

## Scope and pre-draft argument

This is new synthesis writing: an English Discussion and short Conclusion, 500–650 words excluding references, for education researchers and curriculum specialists. It is a secondary writing exercise based exclusively on the supplied account of Guo et al. (2024). It is not a newly conducted review or an assessment of the primary studies. The request explicitly requires Markdown, so no Word conversion is needed.

**Educational question:** What can a review of homework interventions tell curriculum specialists deciding whether to assign homework and how long assignments should take?

**Evidence answer:** The homework-versus-none synthesis favors homework on average. Duration comparisons are sparse and do not establish a duration-response relation or optimal minutes. Outcome domains, follow-up timing and the distinction between time and content matter to interpretation.

**Central judgment:** The review advances policy reasoning by separating evidence for homework as a supplement from evidence for a daily duration rule. Its positive pooled estimate supports consideration of supplementary homework, while the unanswered duration question should guide research and constrain timetable prescriptions.

**Scope:** Teacher-assigned work outside school; all included homework was paper-and-pencil. Preserve the original authors' primary-school recommendation as their position, without inferring exact school-level coverage. The heterogeneous, mostly historical and methodologically vulnerable evidence does not establish universal K–12 or online-homework guidance.

## Evidence supporting and qualifying the judgment

Support: homework versus none, g = 0.45, 95% CI [0.24, 0.66]; positive arithmetic computation and problem-solving estimates; the original authors recommend primary-school supplementary homework. The review addresses assigned homework contrasts rather than relying only on correlations between time and achievement.

Qualification and competing evidence: arithmetic concepts g = −0.02, 95% CI [−0.22, 0.18]; no formal test of subdomain differences; Koch's narrow comparison and Dolean and Lervag's content/time contrasts cannot yield an optimum; short-term writing advantages were no longer clear at four months; no study received an overall low-risk rating; most evidence dates from 1939–1995; the final search was 5 November 2021; missing sources, omitted non-English databases and reporting inconsistencies constrain reach. These points enter the argument according to their inferential role rather than as a catalogue.

## Writing-unit evidence table, prepared before first.md

| Unit | Function and claim | Evidence/source location in H5-materials.md | Planned treatment and necessary conditions |
|---|---|---|---|
| Discussion opening | Answer the duration-policy question; distinguish assigning homework from increasing duration | Question and scope; B175/Figure 6; B187, B193–B194, B210–B211 | State the positive homework-versus-none estimate with its interval; identify duration as unresolved immediately |
| Discussion outcome paragraph | Specify what achievement means and resist an unsupported ranking of domains | B175/Figure 6 | Include computation, problem-solving and uncertain concepts; keep absence of a direct subdomain comparison beside these results |
| Discussion duration paragraph | Show why elapsed time, assigned content and retention need separation | Table 2; B184–B186; B152–B153 | Attribute primary studies to Guo et al.'s account; keep Koch's result narrow and Dolean and Lervag's subject allocation identifiable; retain the four-month condition |
| Discussion limitations paragraph | Explain strength and current reach of the synthesis | Table 2; B196–B213; source issues paragraph | Group overall risk, historical evidence and search limitations; no new certainty grade, heterogeneity value, sensitivity range or school-level count |
| Discussion research paragraph | Derive a study design from the unresolved contrast | B187, B193–B194; duration comparisons | Recommend controlled variation of amount with task content identifiable, measurement of actual time, and follow-up; recommendations are future designs, not established findings |
| Discussion practice paragraph | Connect positive supplementary-work findings to bounded curriculum action | Authors' conclusion, B196–B213; outcome and duration evidence | Preserve primary-school arithmetic focus as the authors' position; teachers specify intended learning and review outcomes; no recommended minutes |
| Conclusion | Answer whether the review justifies a homework-duration policy | Same central evidence as opening | Retain paper-and-pencil scope and unresolved duration; close on a specific research/policy priority without repeating every limitation |

## Terminology

| Preferred term | Meaning and use |
|---|---|
| homework | Teacher-assigned work completed outside school; no extracurricular teaching or guided in-school study |
| homework versus none | The pooled assigned-homework comparison; not a contrast between two durations |
| homework duration / time spent | Elapsed completion time; do not treat as interchangeable with task amount or subject allocation |
| amount | Assigned quantity of work; distinguish from observed completion time |
| arithmetic computation; arithmetic problem-solving; arithmetic concepts | Distinct achievement outcomes; retain the packet's labels |
| Hedges' g | Standardized mean difference, not a correlation; do not apply external effect-size thresholds |
| 95% CI | 95% confidence interval; no invented interval or equivalence margin |
| the review / Guo et al. (2024) | The published source; avoid first-person ownership of the underlying research |

## Source and citation boundary

Only H5-materials.md supplies research evidence. The full article URL and DOI are supplied bibliographic information, not evidence of an independent online verification. The packet compiler reports reading the full main text and inspecting figures; this writer has not read the full article, primary studies, raw data or protocol. Cite Guo et al. for the review and explicitly use secondary attribution for named primary studies. No separate primary-study references will be fabricated. The review's readiness/practice/feedback account may be used as a candidate explanation only; do not claim mediation was measured. No external literature comparison or numerical effect-size benchmark will be added.

## Author queries and unresolved checking questions

These are work-record queries for any later publication use, not blocking questions for this closed-material exercise.

1. Check the original source's conflicting design labels and age/grade coverage, including the grades 2–8 discussion claim versus high-school table entries. Do not silently resolve or reproduce exact school-level totals here.
2. Reconcile the pooled heterogeneity statistics and the B181 sensitivity range with Figure 8 before using them. They are omitted from the manuscript.
3. Determine whether an updated search exists beyond 5 November 2021 before using this 2024 review as current policy evidence. This task prohibits browsing, so currency is not independently assessed.
4. If a new manuscript needs a stronger causal or duration claim, obtain and assess the primary studies and protocol; the packet does not permit that assessment.

## Checks and revision record

Planned: run check_voice.py, check_prose.py and check_consistency.py on both first.md and final.md using python -X utf8. Inspect every output. Independently check word count, comparison identity, direction and intervals, secondary attribution, cross-section consistency, and all practice/research inferences. AI self-review only. Record substantive review and final checking decisions in review.md; add completed outcomes below after checks.

Completed: all three checks ran on first.md and final.md with exit code 0; all outputs were inspected. A local wording refinement after the first final check was followed by rerunning the three checks on the delivered final. Full commands, outputs and counts are in `checks/`. The first draft has 575 body words; the delivered final has 565 (583 including the exercise notice and heading tokens before references). Details and decisions are in review.md.

The revision strengthened the distinction between an assigned-work contrast and observed time, made the different arithmetic-concepts comparisons explicit, and tied research proposals to content/time separation and follow-up uncertainty. The optional practice/feedback explanation was omitted to give these evidence-grounded connections room. Terminology was standardized, and the conclusion retains the paper-and-pencil, primary-arithmetic and unresolved-duration conditions. The evidence table was checked against the final paragraph functions; no unsupported mechanism or new result was added.

No change_log.md is required because the user requested new synthesis writing, not revision of a supplied manuscript. The substantive changes from the required first draft to final are documented in review.md. The author queries above remain unresolved within the closed-material scope.
