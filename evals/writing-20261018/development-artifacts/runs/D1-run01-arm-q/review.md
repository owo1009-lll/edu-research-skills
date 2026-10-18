# AI self-review

This is an AI writing self-review against the supplied fictional materials, not expert peer review or independent validation of real data. The saved first draft precedes this review and the final revision.

## Overall judgment

The first draft answers the approved delayed-transfer question, preserves the authors' conditional teaching recommendation and separates the primary result from the positive secondary result. It has 901 whitespace-delimited words in its three manuscript sections, excluding the notice, headings and reference-card descriptions (925 including those descriptions). It is within the requested range. The two comparison cards perform distinct argumentative roles; neither becomes an invented real bibliographic source.

## Source and inference audit

| Item | Decision |
|---|---|
| Primary outcome | d = 0.08 and 95% CI [-0.07, 0.23] are attached to delayed conceptual transfer, favour retrieval and are described as unresolved. The interval is not used to assert no effect or equivalence. |
| Secondary outcome | d = 0.24 and 95% CI [0.09, 0.39] are attached to immediate conceptual transfer. The manuscript expressly states that the immediate?delayed difference was not tested, so it makes no decay or retention finding. |
| Randomisation and analysis | Classes, not pupils, were allocated within schools; 12 classes per condition, shared content/time and teacher explanation, class-unit analysis and school/baseline adjustment are preserved. No preregistration, blinding or additional analysis is invented. |
| Implementation | 81% refers to completing an attempt before example checking, not correct explanations, engagement, motivation or a measured mediator. |
| Experience | Reported ease is attributed to rereading and retains its status as a nonvalidated activity-experience item. It is not evidence of learning superiority. |
| Preparation | Medians are 10 and 6 minutes per lesson, correctly attached to retrieval and rereading. Their descriptive status is explicit; the recommendation does not claim cost-effectiveness. |
| Missingness | 480 enrolled and 456 completing both tests are distinguished. The equal count of 12 missing per condition does not imply ignorable missingness. |
| R1 | Supports only its own delayed factual-recall comparison in a single-session individually randomised university laboratory. No age moderation or direct effect-size conflict is inferred. |
| R2 | Supports a directionally similar immediate conceptual-performance pattern under teacher choice, with no delayed test. Effortful reconstruction remains a proposed, unmeasured explanation. |
| Recommendations | Conditional retention follows the immediate result and the stated educational aim, with preparation as a constraint. Delayed transfer remains the replacement criterion. Proposed future investigation is not presented as an implemented measure or completed analysis. |

## First-draft checker findings and dispositions

All three commands ran with `python -X utf8` and returned exit code 0. Command lines and full output are saved in the three `first-check_*.txt` files.

- `check_voice.py` found zero numbers absent from the source and no stacked hedges. Manual inspection additionally checked each number's outcome, timing, direction and descriptive/inferential identity, which the script cannot verify.
- It flagged two disclaimer-type sentences: the statement that the attempt record cannot identify a mechanism, and the statement that descriptive preparation medians cannot determine better value. The first repeats a boundary already conveyed by the absence of correctness/depth information; replace it with a substantive statement of what evidence a reconstruction explanation needs. The second guards a specific likely misreading and belongs alongside the cost-related recommendation; retain its substance.
- It identified the untested immediate?delayed difference as a substantive distinction. Retain the qualification where the temporal comparison is made. It also flagged the sentence rejecting equivalence because of the word ?equivalent?; this sentence rejects, rather than commits, the inference in question.
- The low self-mention rate is not a defect; adding pronouns would not strengthen the argument. The limitation-location statistic is a lexical diagnostic and misses attrition qualifications without its trigger words. Overall design boundaries already have a dedicated limitations unit. The mechanism qualification belongs near the process record.
- `check_prose.py` reported four citation-density prompts and claimed the Discussion cites no earlier study. These are detection limitations: it does not recognise the required [R1]/[R2] format as its standard citations. Manual inspection confirms two comparison-card citations in the Introduction and three in the Discussion. Do not invent references or alter the requested label system to satisfy the script.
- Sentence and paragraph lengths are below the published medians. This is a short, bounded three-section task; the paragraphs remain connected and perform distinct functions. No padding is warranted.
- `check_consistency.py` identified one term variant: ?immediate conceptual transfer? and ?immediate conceptual-transfer?. Normalise to the unhyphenated construct name. No precision, acronym or display issue was found. Its sample extractor reported no samples because the wording interrupts its fixed patterns, so the manual 480/456/12 check is necessary. Its numbered-reference check does not validate [R1]/[R2]; references were checked manually.

## One planned substantive revision

1. Replace the awkward ?under classroom allocation? phrase with a precise description of the unanswered class-randomised school comparison.
2. Use ?immediate conceptual transfer? consistently, including in noun phrases about the result or purpose.
3. Revise the process paragraph so the unmeasured mechanism issue advances the argument: a reconstruction explanation needs evidence about what pupils produce as well as participation.
4. Recast the example-checking recommendation positively. Since retrieval already included example checking and the subsequent teacher explanation, development work should examine pupils' explanations within that supported sequence. This is a proposed investigative focus, not a newly established intervention effect.

## Cross-section comparison before finalisation

The Introduction selects delayed transfer as the educational criterion without inventing a directional hypothesis. The Discussion retains the unresolved primary result, then interprets the secondary result for its own teaching purpose. The Conclusion makes the same conditional judgment without converting uncertainty into equivalence, failure or a time-moderation claim. General attrition and setting limits are concentrated in the Discussion's limitations unit; the specific interval, temporal and measurement restrictions stay with the claims they qualify.

The manuscript's educational contribution is a usable distinction between adopting an activity for a short-term lesson purpose and replacing a routine to achieve delayed transfer. It connects that distinction to the observed immediate result, uncertain delayed estimate, opportunity for reconstruction and preparation demand. It does not claim a new mechanism or general theory.

## Remaining limits

This is a closed teaching simulation with only the two supplied fictional comparison cards. The check scripts are heuristic and do not provide statistical reanalysis, external literature verification or expert review. No new analysis, measurement, empirical reference or network source was added. Final checks will be recorded below after the revision.

## Final verification completed

The final manuscript contains 910 whitespace-delimited words across the requested sections, excluding the teaching notice, headings and reference-card descriptions; including the reference-card descriptions gives 934 words. The prose checker's alphabetic-token count is 908, a different counting method. All counts are within 800?1,000.

All three final check commands returned exit code 0 with empty stderr; outputs are saved as `final-check_voice.txt`, `final-check_prose.txt` and `final-check_consistency.txt`. The final consistency check has zero findings, including zero term variants. The final voice check reports zero unsupported number strings, zero stacked hedges and zero limitation sentences outside the limitations unit. Its remaining disclaimer cue is the necessary interpretation of preparation medians. The equivalence cue explicitly rejects an equivalence claim; the temporal distinction explicitly states that declining benefit was not established. These are retained for substantive accuracy, not removed to improve a diagnostic rate.

The four final prose citation prompts remain consequences of the required [R1]/[R2] labels being outside the detector's supported format. Direct inspection confirms that all five manuscript citations point to the appropriate supplied card, with two in the Introduction and three in the Discussion. The short reference list identifies fictional cards only. Sample counts, signs, confidence bounds, intervention and follow-up timing, and preparation units were checked manually because the checker does not fully validate those relationships.

The complete final text was reread after the checks. The primary answer, interpretation of the immediate result, conditional recommendation and unresolved mechanism are consistent across sections. No further manuscript change followed this check. No statistical analysis, new measurement, network lookup, outside reference or expert review was performed.
