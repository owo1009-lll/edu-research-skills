# AI self-review of draft-01

This is an AI self-check of the supplied paragraph and source pack, not an expert review or a full-manuscript audit. It was written after preserving draft-01.md and running both skill checkers, and before writing draft-02.md.

## Actual checks

The first draft contains 129 body words in one paragraph by both whitespace and word-token counts. Attribution is excluded. Both checkers exited successfully. Their actual output and arguments are saved under checks/draft-01/.

check_voice.py found no disclaimer sentences, stacked hedges, semantic-check sentences or unsupported numbers. It marked the sentence beginning “Limited knowledge” as a limitation cue and reported rates outside its reference range for self-mention and placement of limitations. “Limited knowledge” is a proposed explanation, not a generic design disclaimer; it belongs beside this result. No self-mention or separate limitations section needs to be added to this short compression.

check_prose.py reported no prompts, seven sentences, a median sentence length of 18 words and one narrative citation. Its corpus rates are descriptive references; the draft should preserve the existing citation rather than add citations or change its voice to meet those rates.

The runner initially stopped before either checker because its word-count regex had an invalid character range. The regex was corrected, and the actual successful checker runs followed. Both attempts are retained in the command ledger. No prose draft was overwritten or reconstructed.

## Substantive review and revision decisions

1. **Preserve the original argument.** The first draft retains the discrepancy, knowledge explanation, responsibility explanation and request for further assessment research. It does not replace B068 with a summary of the study or introduce training-programme recommendations.
2. **Repair the training inference more fully.** The colon after “may contribute to this discrepancy” still makes absent training appear to substantiate measured knowledge deficits. Training attendance was not a direct knowledge measure. Remove this subsidiary inference from the compressed paragraph, retain knowledge as a possible explanation, and explain the omission separately.
3. **Make the responsibility explanation explicit.** “Potentially separating” is grammatically tied to teachers' reported behaviour without clearly distinguishing the authors' interpretation. Give the interview finding its own sentence, then state the proposed link between instructional provision and students' engagement as an interpretation.
4. **Preserve the missing correspondence accurately.** The issue is not that the explanation is wholly “untested,” which can sound broader than necessary. The displayed case data do not connect responsibility beliefs with individual implementation-quality ratings. State that specific gap without implying a lack of any relevant interview evidence.
5. **Clarify measurement coverage.** Replace “fewer basic elements” with five elements versus four. These worded counts occur in the supplied source and distinguish questionnaire coverage from the observation scale. Retain “typical practice” and “a selected lesson”; do not claim that measurement differences themselves caused the discrepancy.
6. **Keep a purposeful ending.** Retain a clear recommendation to examine knowledge and responsibility beliefs in assessment. Replace the slightly causal “shape” with “enter” so the research proposal does not imply an established process.

## Citation, attribution and boundaries

Hennessey and Dionigi (2013) must remain, with its existing role, but its original source was not independently checked. The adaptation is attributed to Adl-Amini, Völlinger and Eckart and marked as changed under the supplied CC BY 4.0 license. No correlation coefficient, new citation, student-learning claim, matched-score claim or whole-study conclusion is needed.

## Post-revision check, appended after draft-02

Draft-02 contains 121 body words in one paragraph by both counting methods. check_voice.py and check_prose.py both exited with code 0; their actual outputs are under checks/draft-02/. The prose checker reported no prompts. The voice checker again identified “Limited knowledge” as a limitation cue, with no stacked hedges, unsupported numbers or semantic-check sentences. The phrase identifies a candidate explanation, and the numerical comparison of five versus four elements was checked manually against the source pack. The six revision decisions above have been implemented; no further prose revision is necessary.
