# Q-C01: one English comparison example, tested on a different study

Status at design freeze: prospective development comparison. Project baseline remains `684f5e435b76daf8d0109c9c6a93297542c59889`; the immediate control is the runtime skill at `cec4bc78fe9c240900e3c79a3097b1b96577d8fa`. The earlier current-01 diagnostics found no mandatory new final-manuscript correction. This experiment therefore tests possible transfer and useful clarification, not a claim that current writing is generally defective.

## Narrow intervention and rationale

Q-C01 concerns explaining what a comparison means for the research question. Earlier development text sometimes turned internal cautions into an unprompted rebuttal; current reviewed finals already preserved important comparisons and substantive judgments. The remaining empirical question is whether a short positive example can improve explanation on a demanding, different comparison without adding a tutorial, defensive ending or redundant length.

The candidate appends [one passage](candidate-addition.md) to `references/quantitative-discussion.md`. It adds a concise, original example based on the common-review design in Rohrer et al. (Q-N12), with an explanation of why its sentences matter. It changes no other resource, routing, checker or delivery requirement. The transfer study is Marsh et al. (Q-N05), about longitudinal model comparisons, not the study used in the example. No distillation notes or expected output are given to writers.

This is one intervention, not a package combining all proposed writing methods. It stays in external snapshots until outcomes justify a decision. A positive result on this one development study would still require testing on other materials before any broad adoption claim.

## Tasks and runs

- One unique English development study; two operations: a new 450–550-word discussion passage and a 140–170-word compression of an actual published paragraph.
- Two fresh runs per operation per arm: eight outputs in total. Repetitions assess generation variation; they are not eight independent studies.
- Each run receives the same operation-specific request and source bytes, its isolated skill snapshot, and an isolated output directory. A fresh agent has no inherited discussion history.
- Writers follow the skill's applicable drafting and self-review workflow. They save all actual drafts, self-review, final text, separate rationale and executed-check outputs. Do not manufacture missing stages after the fact. They record loaded/executed resource paths and hashes.
- No browsing, other runs, source-development notes, candidate design records or review conclusions are allowed. Only English manuscript outputs are in scope. No target journal, Word output or external application write is requested.
- Model family and reasoning configuration are inherited consistently from the parent. Hosted model identifier, sampling temperature and seed are not exposed. This is not a cross-model or human evaluation.

## Evaluation fixed before runs

Fresh reviewers see the frozen task, source pack, original paragraph when relevant and anonymous final manuscripts. They do not see skills, version labels, writer rationales or other reviews. Judge all nine dimensions requested for the project: factual/author fidelity; problem and central judgment; reasoning/evidence; theory/literature; explanation/contribution; natural, specific prose; author voice; necessary qualification and repeated disclaimers; concrete author corrections.

Ask whether the different comparisons and their substantive consequence are actually easier to understand, whether the author's complementarity and practical position survive, and whether a proposed improvement requires author correction elsewhere. These are semantic judgments, not keyword or sentence-length scores. Word counts check task compliance only. Prefer specific manuscript passages to a global numerical score.

Review the two operations separately and inspect repeat consistency. A local improvement with regressions in fidelity or author meaning does not justify adoption. Optional preferences do not become mandatory errors. If the control already achieves the purpose, or candidate gains are inconsistent or only make the text longer, keep the candidate out of runtime. Preserve null and negative outcomes and resolve reviewer reservations against the actual inputs and outputs.

## Reproduction and limits

At the stated source commit, use `../writing-20261018/snapshot.py` to create a new external control snapshot and manifest. Then run `prepare_variants.py --control <control> --control-manifest <manifest> --out <new-candidate> --manifest <new-candidate-manifest>`. Verify the recorded tree hashes and one-file difference. Task files under `inputs/D-Q02/` provide the exact public inputs; the source is CC BY 4.0 and private manuscripts are excluded.

Inputs, snapshots, actual run records and blind keys will be preserved with the results. Record integrity verifies what was compared; it does not establish writing quality or the original article's statistical correctness. Neither this experiment nor the current corpus completes the requested coverage or final frozen-version independent review.
