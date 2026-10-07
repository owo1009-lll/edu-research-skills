# English voice for SSCI education journals

Calibrated on 15 empirical articles (2024–2025) from Computers & Education, BJET, ETR&D, IJETHE, Education and Information Technologies, Teaching and Teacher Education, Learning and Instruction, IJME and Music Education Research. Figures below are medians across those papers; the analysis is in `distill/results/` of the project repository.

This file covers stance. How paragraphs, citations and sentences are built is in [prose-en](prose-en.md), calibrated on 50 articles (35 from top-tier journals; 22 quantitative, 15 qualitative, 13 mixed); read both.

Published authors are not less cautious than a careful draft. They put the caution in different places: findings are stated plainly, the authors' own explanations carry the hedges, and design limits are gathered in one limitations unit that turns into future work.

## Findings: state them

Restate results as plain declaratives with the statistic or theme: "Teacher support predicted engagement (β = .41, p < .001)", "Participants most often described…". In the corpus 86% of finding statements carry no hedge. When a finding is weak (marginal p, small subgroup, exploratory analysis), one reporting verb is enough: "The data suggest…". Do not stack modals on a result.

Direct is not causal. Match the verb to the design: experiments may say *improved* or *increased*; surveys and correlational designs say *predicted*, *was associated with*, *was related to*. Choosing the right verb replaces any later "this does not prove causation" sentence. In the abstract and implications too, cross-sectional findings do not *add to*, *drive* or *build* anything.

Plain is not absolute. Write *only*, *solely* or *fully* only when the estimates show it.
- **Non-significant direct path.** When the direct path is not significant but the indirect one is, write "was related to engagement through self-efficacy; the direct path was not significant", not "only through self-efficacy". This matters most when the direct estimate is not smaller than the indirect one; mention power there.
- **Name what each method shows.**
  - NCA identifies necessity in degree (bottlenecks at given outcome levels).
  - The fsQCA necessity test asks about necessity in kind.
  - One sufficient configuration is one route to the outcome, not the only route.
- **Keep the same strength everywhere.** A finding is worded the same way in the abstract, the discussion and the conclusion.

## Explanations: carry the uncertainty here

When you propose why a result occurred, hedge the reason, not the result: "One possible explanation is that…", "This may reflect…", "…may be attributed to…". In the corpus 69% of the authors' own explanations are hedged against 16% of findings. Agreement with prior work is stated without hedges, usually with parenthetical citations: "This is consistent with studies of [population] (Lee & Kim, 2023; …)". When a result contradicts prior work, name the difference in sample, setting or measure that could account for it.

## Null and unexpected results: report, then explain

State a non-significant or contrary result directly, mark it as noteworthy ("Contrary to H2…", "Interestingly…"), offer one or two reasons with *may*, and name the design that could separate them. 13 of 15 papers do this; none treats a null result only as a limitation.

## Disclaimers: rare, specific, and followed by something

A sentence of the form "this does not show / cannot establish / should not be interpreted as" appears 0 times in the discussion body of a typical paper (corpus total: 9 sentences, 1.2% of body sentences). When one is genuinely needed, it targets one named inference and is immediately followed by an explanation, an alternative reading or a next step. Never end a paragraph on a disclaimer, and never attach one to every finding.

## Contribution and implications

Claim the contribution explicitly, in the discussion opening or the conclusion: "This study adds to research on [topic] by showing [finding] in [context]." All 15 papers do so. Implications name the actor, the action and the finding behind it: "Because [finding], teacher educators should…". Use *should*, *can* or *need to*. Write them as prose paragraphs, not numbered lists (28 of 31 articles; see [prose-en](prose-en.md)). Take concrete examples only from the study's own materials, or state them as general practices without parameters; never add durations, counts or proportions that the materials do not give.

## Limitations: one unit, turned into future work

Gather limitations in one subsection or the final discussion paragraph (46 of 50 articles; median 4 distinct limitations, 2 in qualitative papers). State each limit once, say what it means for the claim, and turn it into a design: "Because the data are cross-sectional, the direction of the effect remains open; a longitudinal design could test whether…". Answer a limit with a mitigating fact when one exists. Close the paper on the conclusion or contribution, not on limitations (11 of 15 papers).

## Authorial presence

Write as the authors: "we found", "our findings", "this study". The corpus uses about 11 such self-mentions per 1,000 words of discussion, counting "this study"; *we/our/us* alone run at about 6 per 1,000 words of discussion and 5 across the argued sections (see [prose-en](prose-en.md)). An impersonal draft with none reads as detached from its own results.

## Check

Run `scripts/check_voice.py --draft <file> --source <materials or results>` on any discussion or full manuscript. It lists every disclaimer sentence, stacked hedges, limitation sentences that sit outside the limitations unit and numbers or durations that do not occur in the sources, and compares the rates with the corpus range.
