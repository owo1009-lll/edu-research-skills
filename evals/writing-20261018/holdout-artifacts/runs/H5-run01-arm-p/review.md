# Substantive review and checking record

This is an AI self-review of the supplied-material writing exercise, not expert review or independent verification of the published review.

## Assessment of first.md

The draft answers the policy question and selects evidence around a coherent distinction: a positive homework-versus-none average does not identify an optimal duration. It keeps non-detected findings visible, reports the concepts interval correctly, attributes primary studies through Guo et al., and avoids invented timetable recommendations, causal mechanisms, sensitivity estimates, school-level counts and certainty grades. The original authors' primary-school arithmetic recommendation remains visible.

The main revision should deepen the reasoning rather than increase the amount of evidence:

1. **Explain the value of the intervention-focused synthesis.** The first paragraph says the review extends a correlational debate but gives little reason why this matters. Add the packet's distinction between chosen work and observed time: difficulty, prior attainment and effort can affect completion time. This clarifies the contribution without claiming that every included contrast is unbiased.
2. **Connect the seemingly different arithmetic-concepts findings.** The pooled concepts estimate concerns homework versus none; Koch's concepts finding concerns longer versus shorter work. The first draft reports both but leaves their relationship implicit. State their different comparison identities. Do not call the latter a refutation of the pooled result, or evidence of a universally beneficial increase in minutes.
3. **Make research priorities respond to the actual inference failures.** Connect content/time separation to designs varying amount within comparable tasks, the absent curve to wider duration contrasts, and the unclear four-month writing advantage to follow-up outcomes. Specify random assignment as a prospective response to confounding concerns. These are proposed designs, not assertions about unreported primary-study methods.
4. **Tighten the practical conclusion.** Replace the awkward phrase “a supplement to achievement.” Preserve the authors' primary-school arithmetic emphasis and make the final sentence prioritize defined outcomes and the persistence of gains. Do not transform the non-detected mathematics result into advice to remove mathematics homework.
5. **Remove optional mechanism discussion.** The practice/feedback account is explicitly speculative and therefore defensible, but it uses space without advancing the duration-policy argument. Removing it will allow the comparison-identity explanation to do more work. This is evidence selection, not denial of the review's theoretical framework.

## First-draft script results and decisions

All three supplied scripts were run with `python -X utf8`; every exit code was 0. Full outputs and command arrays are saved in `checks/`.

| Check | Output inspected | Finding and decision |
|---|---|---|
| Voice | first_voice.txt | One disclaimer cue: separate estimates do not establish domain differences. Retain the substance: the source reports no formal between-domain test. Two substantive-distinction cues are necessary comparison/interpretation statements. No stacked qualifiers, stray limitation cues, semantic-equivalence cues or unsupported numbers. |
| Voice: authorial presence | first_voice.txt | Zero first-person self-reference is appropriate because this is a secondary exercise. Do not add “we found” to match the published-article median. |
| Prose | first_prose.txt | No automatic prompts. The script counts 576 prose words; its tokenizer differs from whitespace counting. Lower citation density and all-narrative citations reflect one supplied review and explicit secondary attribution, not missing invented literature. Shorter sentences than corpus medians do not require expansion. |
| Consistency | first_consistency.txt | One term variant: “arithmetic concepts” and attributive “arithmetic-concepts.” Standardize to “arithmetic concepts” in final.md. No other reported findings. Abstract, sample-size and numbered-reference checks are structurally inapplicable to parts of this short author–year manuscript. |
| Independent count | first_word_count.json | 575 whitespace-delimited words in Discussion and Conclusion; 593 including notice and heading tokens before references. Both within 500–650. |

## Manual evidence checks on first.md

- The pooled g = 0.45 and interval [0.24, 0.66] describe homework versus none, not more versus less homework. They agree with the packet's rounded Figure 6 values.
- The concepts value is negative, −0.02, and its interval is [−0.22, 0.18]. It is not described as proof of no effect or equivalence.
- Koch's approximately 20–30 versus 10–15 minutes remains an arithmetic contrast; concepts and problem-solving results are distinguished.
- Dolean and Lervag's editing/spelling advantage is the writing-versus-mathematics-group short-term comparison, not a pure minute effect. Four-month differences are described as unclear, not equivalent or demonstrably zero.
- Primary-school application is the review authors' recommendation. The manuscript does not derive precise school-stage coverage from the inconsistent source.
- The source's heterogeneity, sensitivity, design-label and age-coverage questions are preserved in rationale.md; none was independently repaired or re-estimated.
- All empirical claims rest on H5-materials.md. The review DOI and reference metadata are supplied, not independently verified. No primary-study bibliography was invented.

## Cross-section consistency before revision

| Central proposition | Discussion | Conclusion | Revision decision |
|---|---|---|---|
| Homework versus none favors homework on average | Pooled estimate and CI | Considering homework as a supplement | Keep the conclusion conditional and align it with the authors' primary arithmetic recommendation |
| Optimal duration remains unresolved | Opening and duration paragraph | Explicitly unresolved | Retain; remove unnecessary repetition within the Discussion where possible |
| Content/outcome and retention matter | Duration findings and research proposals | Comparable task conditions and persistent gains | Strengthen the link between each proposal and its supporting result |

## Final verification

The single substantive revision is complete. After the first final-draft check, one local precision edit replaced “benefits and harms” with “lower and higher achievement,” keeping the interval interpretation confined to the measured outcome. The three checks were rerun on the delivered wording. The earlier final-check outputs are preserved as `final_before_wording_*`; the current `final_*` outputs describe the delivered file.

- **Length:** final.md contains 565 whitespace-delimited words in the Discussion and Conclusion, or 583 including the notice and heading tokens before references. The prose script reports 566 words using its own tokenizer. All counts satisfy the 500–650-word request.
- **Voice:** no unsupported-number or semantic-equivalence cues. The two substantive-distinction cues express the central comparison and interval interpretation; both were inspected and retained. One stacked-qualifier cue comes from two uses of “would” in a sentence with separate prospective research implications, not cumulative hedging of a finding. Retained. Zero self-reference is appropriate for the secondary writing exercise. The lower disclaimer count after a small subject change illustrates why these counts are not quality scores.
- **Prose:** no automatic prompts. The final discussion has five paragraphs and the conclusion one. The source constraint justifies the limited citation set; corpus medians were not used as targets.
- **Consistency:** zero reported findings, including the now-consistent “arithmetic concepts” term. All three final check commands returned exit code 0.
- **Manual inference check:** the homework-versus-none average, concepts interval, and two duration comparisons retain their original objects, directions and timing. No equivalence, optimum, between-domain superiority or pure minute effect is asserted. The final text explicitly distinguishes Koch's comparison from the pooled concepts comparison.
- **Advice check:** the primary-school arithmetic recommendation remains tied to the review authors' position. Reviewing assignments against intended skills is a reasoned curriculum action, not a claimed tested intervention. Randomization, comparable tasks, recording completion time and retention assessments are prospective research proposals supported by the identified gaps.
- **Cross-section check:** the conclusion preserves paper-and-pencil scope, the primary-school arithmetic focus and unresolved duration. Its amount/content/time research priority follows from the Discussion. It adds no new empirical finding or universal quota.
- **Source boundary:** the final citation is the supplied Guo et al. reference, with primary studies explicitly attributed through the review. No browsing, primary-paper assessment, reanalysis or new certainty rating was performed. Source reporting questions remain open in rationale.md.

The final artifact is suitable for the requested secondary writing exercise. Its empirical claims are checked against the supplied packet, not independently against the published full text or original studies.
