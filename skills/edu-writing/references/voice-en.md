# English voice for SSCI education journals

This file covers stance at the level of language: where to state, where to qualify, and how to express a position. How the argument is ordered, how qualifications are classified and what each kind of claim needs are in [argument](argument.md) (written in Chinese, with English examples). How statistical results are interpreted is in [framing-results](framing-results.md).

The figures below come from stance coding of 15 empirical articles (2024–2025: Computers & Education, BJET, ETR&D, IJETHE, Education and Information Technologies, Teaching and Teacher Education, Learning and Instruction, IJME, Music Education Research; analysis in `distill/results/`). [prose-en](prose-en.md) describes paragraph and sentence habits in 50 articles. Both describe how published papers usually write. Use them as references, not as quality targets.

## Findings: state what the evidence supports

Restate results as plain declaratives with the statistic or theme: "Teacher support predicted engagement (β = .41, p < .001)", "Participants most often described…". In the corpus 86% of finding statements carry no hedge.

- **Match the verb to the design.** Experiments may say *improved* or *increased*. Surveys and correlational designs, including path models, say *predicted*, *was associated with* or *was related to*. In the abstract and implications too, cross-sectional findings do not *add to*, *drive* or *build* anything.
- **Keep the conditions that define a claim inside it.** Sample scope, covariates, the exploratory status of an analysis and the timing of measurement belong in the sentence: "With prior achievement controlled, …", "In an exploratory analysis, …". Do not move them to the end of the paper.
- **Plain is not absolute.** A non-significant direct path next to a significant indirect one gives "the indirect association was significant; the direct estimate did not reach statistical significance", not "only through self-efficacy" or "there was no direct association". See [framing-results](framing-results.md) §5 for the evidence needed for each claim.
- **Name what each method shows.**
  - NCA identifies necessity in degree.
  - The fsQCA necessity test asks about necessity in kind.
  - One sufficient configuration is one route to the outcome, not the only route.

## Explanations: qualify them accurately

When you propose why a result occurred, qualify the reason by the strength of its support: "One possible explanation is that…", "This may partly reflect…". In the corpus 69% of the authors' own explanations are qualified, against 16% of findings.
- "May partly reflect" is accurate when the evidence partly supports an explanation. It is not defensive.
- Make the comparison specific: which claim, population, operation, measure and time point align? State supported agreement directly. Different significance labels do not establish a conflict, and a design difference does not itself explain a discrepancy. Give a possible reason only when the materials support it; otherwise keep the disagreement unresolved.

## Qualifications and limitations: classify them

Handle qualifications by the four types in [argument](argument.md) §4:
- **Repeated generic disclaimers:** merge or delete.
- **Conditions that define a claim:** keep in the claim.
- **Overall design limitations:** discuss together in the limitations unit.
- **A specific problem that changes how one result reads**, such as low reliability of one scale: say it briefly where that result is discussed.

A sentence such as "this does not show / cannot establish" appears a median of 0 times in a typical discussion body. Write one only when a reader is likely to draw a specific wrong inference, and follow it with an explanation or an alternative reading.

A distinction that makes a substantive point is an argument, not a disclaimer: "Access to a tool is not the same as productive engagement with it."

## Null and unexpected results

State a non-significant or contrary result and what its estimate and precision leave open. Explain a supported pattern or compare candidate explanations when the materials permit; do not invent a reason to complete a paragraph. In the corpus, 13 of 15 papers offered reasons and none treated a null result only as a limitation. This is an observation, not an explanation quota. A non-significant result does not by itself mean equivalence, interchangeability, no effect or an identified boundary condition (see [framing-results](framing-results.md) §4).

## Taking a position

A position comes from clear claims and grounded choices, not from intensifiers.
- **One question carried through.** Pose it in the Introduction, answer it point by point in the Discussion, and answer it in the first sentence of the conclusion. This holds when the main outcome is null too.
- **Competing explanations.** When the evidence distinguishes them, choose and give the reason: "If X, we would have expected Y; we observed Z." Otherwise state what remains unresolved. Explain any supported common pattern or process; if the materials provide none, keep the unresolved answer concise.
- **Relation to prior knowledge.** Say what the study refines, adds to or changes, and name representative studies. Write "contradicts" or "revises" only for comparable outcomes and populations; otherwise write "extends" or "adds to".
- **Conclusions as claims.** State what the study adds to the educational question, including an unresolved answer when warranted. Preserve the author's supported conceptual frame. Define "complement" according to its intended meaning: functional roles, resource coordination or statistical interaction need different evidence (see [foundation](foundation.md) §1).
- **Implications as trade-offs.** Say what to prioritise, what not to do and under which conditions ([argument](argument.md) §8).
- **End with weight.** The last sentence states the central judgement or the most specific next step.

Limits:
- The abstract, Discussion and conclusion word each result the same way. A result described as imprecise in the Discussion does not become "did not act as a separate route" in the conclusion.
- Do not present an unmeasured factor as an observed mechanism or an untested measure as an established intervention effect. A recommendation may also draw on verified literature or explicit professional or normative premises; explain those grounds and the conditions for action rather than attributing them to this study's findings.
- Explanations do not rest on facts outside the materials.
- Calibrate recommendations to their grounds, conditions and consequences. A cross-sectional association does not establish an intervention effect; it does not automatically invalidate a supported professional or normative judgement. Preserve a justified *should* rather than replacing it with *could* by default ([argument](argument.md) §8).

## Contribution and implications

Explain the specific advance: what the study adds to an educational question or changes in an existing account. The contribution categories in [argument](argument.md) §2 support internal judgement; they need not appear as labels in the manuscript. Briefly revisit the contribution where a section has a distinct purpose, without repeating its full justification. "The results fit theory X" or "the mediation was significant" is not by itself a theoretical contribution.

For each implication, explain its grounds, practical meaning, conditions and proposed action. Identify whether those grounds are this study's findings, verified literature or explicit professional or normative premises. Separate measures the study tested from applications inferred from associations. The number of implications follows the evidence. Concrete examples come only from the study's materials, or are general practices without invented durations, counts or proportions.

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
