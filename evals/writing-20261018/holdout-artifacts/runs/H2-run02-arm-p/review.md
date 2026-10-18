# Substantive AI self-review

This is an AI self-check of the supplied passage, evidence packet and saved first draft, not independent peer review. The first draft and all three check outputs were inspected before preparing the final revision. No raw data, external literature or other runs were consulted.

## What the first draft preserves

The original position remains visible: institutions should sustain outreach, accommodate dietary and practical needs, and connect food, housing, financial and mental-health support. The draft retains first-generation and transfer students, disability, Black/African American identity and academic performance without interpreting those characteristics as individual diagnoses. The disability account is separate from the dining-restrictions account. The recipient who achieved three meals a day retains the friend's cooking assistance; another recipient's persistent academic stress remains visible. The 2020 pilot and 2022 formal launch remain in order, and the assistantship resolution is a commitment rather than an achieved result.

## Consequential revisions required

1. **Correct what the quantitative instrument measures.** Discussion paragraph 3 calls it “a financial measure.” The modified food-security instrument is not merely a financial-resources measure. Replace this with “the binary food-security classification,” and explain how classification and accounts answer different parts of the access question. This repairs the first draft's conceptual imprecision rather than claiming an error in the source.
2. **Make the evidential basis and contribution more explicit.** Add the survey timing, complete-response count and written-statement count. Describe the contribution as connecting who experienced insecurity with the practical difficulties of obtaining and preparing food. The first paragraph's “explain why … must” compresses evidence and institutional judgment too quickly. A more explicit link preserves the recommendation's strength.
3. **Distinguish classification from respondents' own labels.** Change “was reported by” before the prevalence figures to “were classified as having,” since the estimate comes from scoring. Name low/very low categories together and define the shortened “food insecurity” term once. Keep the table-specific undergraduate and graduate respondent scopes.
4. **Remove duplicated design qualification, not its substantive content.** Paragraph 2's directionality clause repeats the end-of-Discussion cross-sectional limitation. The academic-support implication remains grounded in the observed association. Discuss directionality once in the final limitations paragraph.
5. **Strengthen the chain from evidence to action.** The vouchers sentence should retain both familiarity and preparation knowledge. Continuing communication should be linked to changing finances, and service design should explicitly use feedback about fit. Keep concrete professional judgments with “should”; do not weaken every action simply because this is a cross-sectional study.
6. **Keep assistance benefits and their limits together.** Preserve the two contrasting assistance accounts, clarify that the claims are respondents' experiences, and retain the cross-campus comparison's specific uncertainty. Lower prevalence does not discriminate between effects of support, differences across populations/methods or selection into the survey.

## First-draft script outputs: decisions

| Output | Finding | Judgment and action |
|---|---|---|
| first_voice.txt | One disclaimer-type sentence: direction of the grade association | Move the work of that clause to the existing final limitations paragraph; preserve academic-support relevance. |
| first_voice.txt | Two substantive distinctions: service attribution and cross-sectional timing | Retain. Each blocks a likely, specific misinterpretation. The former belongs beside the cross-campus comparison; the latter belongs in the integrated limitations paragraph. |
| first_voice.txt | Two limitation sentences outside a recognized limitations unit; 0% inside | The user requests one Discussion, so the end-of-Discussion paragraph deliberately integrates limitations without a separate heading. The checker cannot identify that unit from headings. Do not add a heading merely to improve the metric. |
| first_voice.txt | No stacked hedges, semantic flags or unmatched numbers | Helpful screening only; not proof of accuracy. Manual numerical and claim checks are below. |
| first_voice.txt | Low self-mention relative to corpus | No change to mimic a median. An attributed secondary revision can use “this study” and respondent-specific descriptions without pretending to be the authors. |
| first_prose.txt | No prompts; 665 tokenized words; citation/sentence statistics supplied | The independent whitespace count is 664 words for Discussion plus Conclusion. Differences reflect tokenization. Do not add outside citations or inflate sentence length to match published medians. |
| first_consistency.txt | Food-security wording variants | “Low food security” is also a substring inside “low or very low food security.” It is not an unintended extra category. Explicit definition in the final draft will clarify the transition to “food insecurity.” |

## Manual numerical and source check

- 15.9% = the supplied undergraduate estimate (213/1,343), not the entire 2,116-response denominator. 16.5% = graduate estimate (125/759). Both retain respondent scope.
- Housing: OR 7.91, 95% CI [5.67, 11.07], concerns losing steady housing versus a steady home. It is not a risk ratio and is not labeled mutually adjusted or causal.
- The temporary/unstable housing OR and its imprecise interval are omitted together; no assertion of a precise dose-response gradient replaces them.
- Three meals a day is one recipient's account supported by both food service and a friend who cooked. It is not the program mean.
- The response rate is approximately 6%; conflicting invitation totals are not repaired. Pilot 2020, survey April 2021, policy commitment and formal launch 2022 are in sequence.
- The supplied accounts are survey statements, not interviews or independently recoded data. Narrative examples do not establish experience frequencies.
- Earlier-study claims are attributed to Hall et al.'s review; no secondary references are dressed up as firsthand reading.

## Visible-section consistency

Discussion and Conclusion both locate claims at the studied university. Both connect material pressures with practical food access. The Conclusion's coordinated-support recommendation is the same professional judgment developed in Discussion; it makes no claim of effects on grades, retention or prevalence. Neither the original abstract nor the rest of the original paper has been independently checked beyond the supplied packet.

## Final checks and disposition

The revised draft was run through all three supplied scripts using `python -X utf8`; all exited with code 0. The saved text outputs for both drafts were then reread in UTF-8. Final Discussion plus Conclusion: **678 words** by whitespace count, 685 by the runner's lexical count, and 680 by the prose checker's tokenizer; all are within 650–800. The attribution notice is outside that manuscript-body count; including it still leaves the document below 800 words before references.

- **Voice:** zero unmatched numbers, stacked hedges or semantic flags. The flagged sentence about what a binary classification cannot describe is a substantive distinction between methods. The service-attribution statement belongs with the comparison. The single-site/response-rate sentence belongs in the integrated limitations paragraph. The lack of a separate Limitations heading explains the checker's location metric; this is intentional under the requested structure.
- **Prose:** no prompts. Citation density is constrained by the single supplied source and acknowledged secondary review; there is no reason to add literature or imitate the corpus's sentence lengths. Zero conventional author self-mentions is acceptable for this explicitly attributed adaptation.
- **Consistency:** two terminology groups flagged. “Low food security” is a substring in the explicitly defined combined classification. “Written statements” names the 176 source items; “written accounts” describes their use in interpretation. Both refer to the same survey material and neither implies interviews. No figures, tables, numbered citations or acronym inconsistencies were reported.
- **Manual additions check:** 2,116 is the number of complete survey responses and 176 is the number of written statements, not a second interview sample. April 2021 is the data-collection month; 2020 and 2022 still refer to the appropriate pilot and subsequent policy/launch events.
- **Authorial position check:** the final draft retains direct institutional recommendations, not just a list of limitations. It preserves concrete support options, outreach across students' studies, practical food suitability, and coordination across services. No changes were made merely to improve script rates.

Residual uncertainty is source-bound: invitations are discrepant; the complete models, raw data and original secondary sources were not independently checked. These points are recorded in rationale.md and do not prevent completion of the supplied secondary-revision exercise.
