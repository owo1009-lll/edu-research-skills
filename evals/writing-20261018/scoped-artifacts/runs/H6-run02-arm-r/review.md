# Substantive AI self-review

This is an AI self-review of a new secondary-writing exercise, not an external expert review. The first draft was saved in full before the three skill checks were run. It contains 638 body words (661 including the exercise notice), excluding headings and references.

## Argument and educational contribution

The draft answers the intended question: the structured AI package improved immediate topic learning relative to an active-learning class. It does not transfer the claim to a whole course or to unrestricted chatbot use. The positive learning finding remains the organizing evidence; the single-item attitudes are not substituted for it. The distinction between an instructional package and generic tool access is supported by the actual design, including the authors' difficulty obtaining their sequence through prompting alone.

Two parts need more work. The Introduction's closing sentence, ?places the educational value ... at the center,? summarizes a value position without explaining exactly what the comparison adds. Replace it with the reason the active comparator matters: teachers were experienced and students already had opportunities for explanations and supported problem solving. The practical paragraph says teachers should ?try this approach,? but the decision is still underspecified. Identify a bounded pilot of selected initial-learning lessons, the required preparation, and the learning outcomes to examine before reallocating classroom time.

## Evidence and inference audit

| Location | Assessment of first draft | Revision decision |
|---|---|---|
| Introduction: earlier research | Properly attributes descriptions of unguided use to Kestin et al.'s review; no independently unread original is cited | Preserve the indirect scope; do not invent a literature consensus or a causal account of between-study differences |
| Introduction: design | Correctly identifies peer-group randomization, crossover, two weeks and common content | Make stepwise expert guidance explicit; keep the second topic and human support legible for non-specialists |
| Discussion: medians | 4.5 and 3.5 are correctly labeled post-test medians, in the correct conditions | Retain them; no score-count-as-person count, gain ratio or figure-mean conflation |
| Discussion: adjusted result | 0.63 is correctly a standardized regression coefficient; ?other measured differences? is vague | Name prior attainment and topic as examples of controls, without converting the coefficient to Cohen's d or asserting a magnitude benchmark |
| Discussion: mechanism | Accurate candidate explanations followed by package attribution limits | Remove redundant attribution wording around ?plausible ... authors suggest?; keep the home setting, introduction and peer interaction as unresolved alternative contributors |
| Discussion: time | Gives the measured 49-minute AI median and assumed 60-minute classroom allocation | State the educational implication more directly: timing merits investigation, while the two measures do not establish individual efficiency. Remove the less useful speculation about later study time |
| Discussion: practical use | Preserves the original authors' proposed initial-learning/classroom-collaboration arrangement | Make a pilot conditional on preparing the tested design and measuring immediate and delayed learning; keep the full combined arrangement explicitly untested |
| Discussion: overall limits | Outcomes, setting, cost and access are bounded correctly | Consolidate general limits; connect retained learning and complex synthesis to subsequent evaluation instead of generic caution |
| Conclusion | Answers the question, but ?credible classroom alternative? and the final teaching question partly repeat prior prose | End on the substantive decision: evaluate a specified instructional design and its place in the course, with the immediate-learning finding as the justified starting point |

## Cross-section reconciliation

- **Question to answer:** The Introduction asks about immediate topic learning; Discussion and Conclusion answer that same question. Neither section asserts that the tutor teaches more effectively across all outcomes.
- **Design to explanation:** The package comparison permits a learning-effect claim for the studied package. It does not identify feedback or pacing as proven causal mechanisms. The conclusion must not convert these candidates into an explanation.
- **Finding to action:** A positive randomized instructional comparison supports a bounded pilot. Reallocation of classroom time is still a proposed use, requiring evaluation of retention and more demanding learning.
- **Scope:** Two lessons, one course and immediate measurement are essential conditions, not optional disclaimers. They remain visible in the question/answer chain; full outcome and setting limits are discussed once.
- **Authorship:** Third-person reporting and the opening exercise notice are appropriate. The usual skill preference for authorial ?we? does not apply to presenting someone else's published study as a secondary exercise.

## First-draft script outputs inspected

All three commands used `python -X utf8`; each exited 0. Logs are `first_voice_check.txt`, `first_prose_check.txt`, and `first_consistency_check.txt`. An exit code records execution, not evidentiary validity.

**Voice:** No numeric tokens were absent from the materials; no semantic-equivalence/exclusive-mechanism flag appeared. Both hedge flags were read in context. ?Plausible ... authors suggest? combines appropriate uncertainty and source attribution, but can be shorter. ?Suggest a possible? can be reduced while preserving the time-measurement distinction. The mechanism limitation is correctly placed beside the result it qualifies. The script's 0% limitations-unit measure arises from having no separate limitations heading in a short selected-section exercise; the overall boundaries already occupy one paragraph. Zero self-mentions is appropriate to third-person secondary writing.

**Prose:** The Introduction's citation density (5.7/1,000) and cited-sentence share (11.1%) were flagged. There is only one allowed research source, so no citation quota will be pursued. The design paragraph does merit its own citation for clear local attribution. Narrative citations identify the one study being described and its review; they are not a listing of unrelated studies. The sentence median is 18 words; a non-specialist audience and short exercise justify direct sentences, but connected reasoning should be strengthened through the revisions above. The script detected no generic value-ending cues, which does not excuse the semantically weak introductory closing sentence identified manually.

**Consistency:** No findings. Manual checking additionally confirmed that both post-test values are medians, 0.63 is the adjusted standardized coefficient, and 49 versus 60 uses different measurement methods. No tests were recomputed, no interval was supplied, and no attitude-test discrepancy was silently resolved. Absence of a check finding does not verify these meanings.

## Revision plan

Revise once in full, retaining the core argument and main evidence. Improve the introductory comparison, precision of adjustment language, economy of mechanism/time qualifications and specificity of the teaching action. Preserve the positive learning claim. Keep all author queries, the unresolved attitude-test issue, the sample-count reconciliation and source-access notes in the work records. Then rerun and inspect all three checks on final.md.

## Final check reconciliation

The revised draft contains **621 body words**: Introduction 173, Discussion 384, Conclusion 64. Including the exercise notice gives 644 words, excluding section headings and references. Both counts meet the requested 600?750 range. The first and final versions were manually compared for research-question, population, condition, timing and outcome consistency.

All three final checks exited 0; their complete outputs were saved and inspected (`final_voice_check.txt`, `final_prose_check.txt`, `final_consistency_check.txt`).

| Final cue | Decision after reading the sentence |
|---|---|
| One disclaimer: differences across studies do not identify causal design components | Retain. The preceding sentence distinguishes implementations using a secondhand review; this sentence prevents an unsupported causal explanation of between-study differences. It is specific to that comparison and is not repeated as a generic warning. |
| One double-hedge cue: ?suggests a further question ... might be organized? | Retain. This is an explicitly prospective teaching question; the following sentences state exactly why the time evidence leaves individual efficiency unresolved. No already-demonstrated score difference is weakened. |
| Zero self-mentions | Retain third person. The study belongs to the named original authors. |
| No separately detected limitations unit | Appropriate to three requested sections and a 621-word exercise. Overall scope and outcome limits are together in Discussion paragraph 4; package/time issues are explained where they change interpretation. |
| Introduction cited-sentence share 22.2% | Retain. The design paragraph now has its own source citation, and the review is explicitly attributed. Adding repetitions to reach a corpus median would not add evidence. |
| No semantic, absent-number or consistency findings | Manually verified the meanings, not just their surface occurrence. These automatic results are not a substantive certification. |

The final revision strengthens the active comparator's relevance, names the adjusted estimate accurately, makes the bounded pilot and its preparation requirements concrete, and preserves the positive result. It does not claim a proven feedback/pacing mechanism, an individual time-efficiency effect, motivational improvement across all outcomes, cheap implementation or an effective whole-course integration. The two score medians and adjusted coefficient refer to the same immediate-learning comparison; no sample counts, p values, intervals or secondary attitude statistics were added. The conclusion remains aligned with the question and confines the established advantage to immediate topic learning.

No second full rewrite was performed. No change_log.md is required because this task is new writing from a factual packet, not revision of a supplied manuscript; the first-to-final changes are recorded in this review and in rationale.md.
