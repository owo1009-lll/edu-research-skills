# AI self-review of draft 01

This review was written after saving draft-01.md and running the supplied voice and prose checkers, and before writing the revised passage. It is an AI self-check, not expert review or independent verification of the published article.

## Scope and numerical checks

The body contains 409 whitespace-delimited words, excluding the attribution heading. The separate Unicode lexical count is also 409. The prose checker reports 410 using its own tokenisation; the explicit body count governs the requested length. The passage has four connected paragraphs and no internal subheadings. It attributes the study to its published authors and uses no first-person ownership.

The two, 30, four and 11 in the opening describe the source pack's consistent observation endpoints, not the survey sample or complete mixed-methods sample. The case paragraph refers to the two teachers with all four assessed elements and the contrasting cases. It does not substitute self-efficacy for implementation scores, invent a cross-source correlation, claim exact matching or claim measured learning gains. The distinction between instructional provision and student outcomes is preserved.

## Actual checker results and decisions

- The initial prose check classified the passage as an Introduction because it had only an attribution heading. Its raw output is retained. A generated checker input replaces only that heading with “Discussion”; the unchanged body has a recorded SHA-256. Both scripts were then rerun, and both normalized outputs are retained.
- The normalized voice check reports no unsupported numbers or semantic-check flags. These results do not establish semantic accuracy; the referents of the numerical claims were checked against the source pack above.
- The voice check flags the sentence beginning “Differences in teachers' knowledge or classroom circumstances...” for multiple qualifiers. The substantive issue is stronger than its hedge count: classroom circumstances are an unelaborated proposed explanation, and the source pack discusses limited knowledge specifically in relation to the self-report/observation difference. Remove this speculative sentence rather than imply that these factors explain the four-case contrast.
- The voice check flags the zero self-mention rate. Retain the absence of “we” and “our”: this is explicitly secondary writing.
- The normalized prose check flags low citation density and no earlier-study comparison. Retain the single-source scope required by the request. Do not add unread literature to meet corpus rates. An author–year reference to the source study in the body can make attribution easier to recognise without adding evidence.
- No sentence exceeded 40 words in the script's metrics. Readability is acceptable; there is no reason to lengthen sentences to approximate a published median.

## Substantive revision decisions

1. Preserve the central argument and the concrete counterexample: reaching academic goals can coexist with groups failing to work together. This shows why criteria for judging implementation matter to teacher education.
2. Replace “can shape what counts as a difficulty” with a description of the distinction displayed in the accounts. The first draft labels it as a suggestion, but the causal verb still makes a stronger claim than the cross-case evidence identifies.
3. Recast the third paragraph around the actual integration: observation scores guided selection of already-conducted interviews. The resulting comparison connects accounts to observed provision at the case level. It does not demonstrate that changing beliefs improves practice.
4. Consolidate the volunteer, selected-lesson and extreme-case boundaries in that paragraph. Retain the direct-coverage explanation next to the observation result because it changes what the result means.
5. Make the implication paragraph more specific about evaluating planning, responses to difficulty and cooperation. Preserve a justified recommendation to teacher educators while explicitly retaining the untested status of programme effects.
6. End with the substantive standard that follows from the argument, replacing the draft's more abstract final reference to “the specific understanding of implementation.”

## Source checks left unresolved

The exercise permits only the supplied pack. No underlying article, raw records, interview transcripts or cited originals have been opened or reanalysed. The partial-implementation count inconsistency, malformed correlation, unsuitable scale bound, matching description and unsupported resistance-to-change inference remain unresolved in the source pack. The revised passage will not depend on those claims. No external verification is represented as completed.

## Post-revision verification

Draft 02 implements the six decisions above in one substantive revision. Its body contains 392 whitespace-delimited words; the Unicode lexical count is also 392. The prose checker reports 393 under its tokenisation. The generated checker input preserves the revised body exactly and adds only a “Discussion” heading for section recognition.

Both supplied checkers completed successfully. The voice checker reports zero unsupported numbers, stacked qualifiers and semantic-check flags. It flags the sentence distinguishing a case comparison from evidence that changing understandings improves practice. Retain this sentence: it prevents a specific causal inference relevant to the subsequent recommendation. Its inclusion is preferable to optimizing a disclaimer rate. The zero self-mention rate remains appropriate for attributed secondary writing. The prose check retains one low-citation-density prompt; the supplied-source restriction continues to govern. No new evidence or prose change is warranted by those prompts.

Manual review confirms the correct observation denominator and endpoint counts, the four-element measurement scope, the observation-guided selection of interviews that had already occurred, and the distinction between case-specific accounts and tested intervention effects. The final file will be an exact copy of draft 02. No third draft or extra revision stage is claimed.
