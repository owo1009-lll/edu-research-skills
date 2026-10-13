# English voice for SSCI education journals

This file covers stance at the level of language: where to state, where to qualify, and how to express a position. How the argument is ordered, how qualifications are classified and what each kind of claim needs are in [argument](argument.md) (written in Chinese, with English examples). How statistical results are interpreted is in [framing-results](framing-results.md).

The figures below come from stance coding of 15 empirical articles (2024–2025: Computers & Education, BJET, ETR&D, IJETHE, Education and Information Technologies, Teaching and Teacher Education, Learning and Instruction, IJME, Music Education Research; analysis in `distill/results/`). [prose-en](prose-en.md) describes paragraph and sentence habits in 50 articles. Both describe how published papers usually write. Use them as references, not as quality targets.

## Findings: state what the evidence supports

Restate results as plain declaratives with the statistic or theme: "Teacher support predicted engagement (β = .41, p < .001)", "Participants most often described…". In the corpus 86% of finding statements carry no hedge.

- **Match the verb to the design.** Experiments may say *improved* or *increased*. Surveys and correlational designs, including path models, say *predicted*, *was associated with* or *was related to*. In the abstract and implications too, cross-sectional findings do not *add to*, *drive* or *build* anything.
- **Keep the conditions that define a claim inside it.** Sample scope, covariates, the exploratory status of an analysis and the timing of measurement belong in the sentence: "With prior achievement controlled, …", "In an exploratory analysis, …". Do not move them to the end of the paper.
- **Plain is not absolute.** Write *only*, *solely* or *fully* only when the estimates show it. A non-significant direct path next to a significant indirect one gives "the indirect association was significant; the direct association was not", not "only through self-efficacy". See [framing-results](framing-results.md) §5.
- **Name what each method shows.**
  - NCA identifies necessity in degree.
  - The fsQCA necessity test asks about necessity in kind.
  - One sufficient configuration is one route to the outcome, not the only route.

## Explanations: qualify them accurately

When you propose why a result occurred, qualify the reason by the strength of its support: "One possible explanation is that…", "This may partly reflect…". In the corpus 69% of the authors' own explanations are qualified, against 16% of findings.
- "May partly reflect" is accurate when the evidence partly supports an explanation. It is not defensive.
- Agreement with prior work is stated without qualifiers: "This is consistent with studies of [population] (Lee & Kim, 2023; …)".
- When a result contradicts prior work, name the difference in sample, setting or measure that could account for it.

## Qualifications and limitations: classify them

Handle qualifications by the four types in [argument](argument.md) §4:
- **Repeated generic disclaimers:** merge or delete.
- **Conditions that define a claim:** keep in the claim.
- **Overall design limitations:** discuss together in the limitations unit.
- **A specific problem that changes how one result reads**, such as low reliability of one scale: say it briefly where that result is discussed.

A sentence such as "this does not show / cannot establish" appears a median of 0 times in a typical discussion body. Write one only when a reader is likely to draw a specific wrong inference, and follow it with an explanation or an alternative reading.

A distinction that makes a substantive point is an argument, not a disclaimer: "Access to a tool is not the same as productive engagement with it."

## Null and unexpected results

State a non-significant or contrary result directly ("Contrary to H2…"), offer reasons, and say what design could separate them. 13 of 15 papers do this; none treats a null result only as a limitation. A non-significant result does not by itself mean equivalence, interchangeability, no effect or an identified boundary condition (see [framing-results](framing-results.md) §4).

## Taking a position

A position comes from clear claims and grounded choices, not from intensifiers.
- **One question carried through.** Pose it in the Introduction, answer it point by point in the Discussion, and answer it in the first sentence of the conclusion. This holds when the main outcome is null too.
- **Competing explanations.** When the evidence distinguishes them, choose and give the reason: "If X, we would have expected Y; we observed Z." When it does not, do not force a choice. Say what each account implies, what design would separate them, and what has been learned either way.
- **Relation to prior knowledge.** Say what the study refines, adds to or changes, and name representative studies. Write "contradicts" or "revises" only for comparable outcomes and populations; otherwise write "extends" or "adds to".
- **Conclusions as claims.** Give propositions a reader could cite or dispute, not a restatement of the Results. A short label for the central finding can help if it is accurate; "complement", for instance, implies a tested interaction.
- **Implications as trade-offs.** Say what to prioritise, what not to do and under which conditions ([argument](argument.md) §8).
- **End with weight.** The last sentence states the central judgement or the most specific next step.

Limits:
- The abstract, Discussion and conclusion word each result the same way. A result described as imprecise in the Discussion does not become "did not act as a separate route" in the conclusion.
- Factors the study did not manipulate or measure can appear in the Discussion as candidate explanations, but not as conclusions or as the basis for recommendations.
- Explanations do not rest on facts outside the materials.
- Implications are only as strong as the design allows. From a single-site, cross-sectional study, write "this does not justify …"; do not make claims about class sizes, teaching hours or budgets.

## Contribution and implications

State the contribution once and say what kind it is: a new finding, a conceptual distinction, a deeper explanation, an important counter-example, a condition of application or a practical trade-off ([argument](argument.md) §2). "The results fit theory X" or "the mediation was significant" is not by itself a theoretical contribution.

For each implication, give the finding, its practical meaning, the conditions it needs and the action. Separate measures the study tested from applications inferred from associations. The number of implications follows the evidence. Concrete examples come only from the study's materials, or are general practices without invented durations, counts or proportions.

## Limitations

Discuss overall design limitations together, say which inference each one limits, and turn it into a design for future work: "Because the data are cross-sectional, the direction of the association remains open; a longitudinal design could test whether…". Answer a limitation with a mitigating fact when one exists. Close the paper on the conclusion or contribution, not on limitations.

## Authorial presence

Write as the authors: "we found", "our findings", "this study". The corpus uses about 11 such self-mentions per 1,000 words of discussion, counting "this study".

## Check

Run `scripts/check_voice.py --draft <file> --source <materials or results>`. It lists cues for a human to judge:
- disclaimer-type sentences and stacked qualifiers;
- limitation sentences outside the limitations unit;
- sentences that need a semantic check (a null result possibly turned into equivalence, an exclusive mechanism or a free choice);
- numbers that do not occur in the sources.

Decide each one. Conditions that define a claim and accurate qualifications stay.
