# English Q-C01 development comparison

**Completed experimental batch; project still in progress.** One study, two operations, two variants and two fresh runs per operation/variant. The candidate adds one positive example about explaining an actual comparison. It remains outside the runtime skill: local editorial preferences are encouraging, but they do not establish a consistent compression benefit or cross-study transfer.

- [Prospective design](design.md), [candidate passage](candidate-addition.md), [run configuration](run-config.json).
- [New-writing request](inputs/D-Q02/new-request.md), [compression request](inputs/D-Q02/revise-request.md), [source pack](inputs/D-Q02/source-pack.md), [actual published paragraph](inputs/D-Q02/original.md), [input freeze](input-freeze.json).
- [Outcome and semantic adjudication](adjudication.md), including direct comparisons, local fidelity concerns and the correction of blind reviewers' package-completeness inference.
- [New-writing blind review](reviews/new/review.md) and [compression blind review](reviews/revise/review.md); their JSON files retain all nine assessment dimensions and input hashes.
- [New-writing key](keys/new.json), [compression key](keys/revise.json), [artifact and resource hashes](archive-manifest.json), [record verification](record-verification.json).

Actual drafts, self-reviews, finals, notes, commands and checker outputs are under `runs/`. Anonymous manuscript bodies are under `blind/new/` and `blind/revise/`. Source material is public English scholarship; no user manuscript or Chinese-language writing task is included. The original paragraph is attributed and licensed CC BY 4.0; all rewritten passages are clearly identified as adaptations or secondary-writing demonstrations.

## Reproduce the setup

At source commit `cec4bc78fe9c240900e3c79a3097b1b96577d8fa`, use the existing [snapshot helper](../writing-20261018/snapshot.py) to create an external control. Use [prepare_variants.py](prepare_variants.py) to create a fresh candidate from that control and the recorded addition; it verifies that only one resource differs. The two manifests are under `snapshots/`.

Run each request in a fresh agent with no inherited history. Give it its specified variant's `skills/edu-writing/SKILL.md`, the operation's request and source pack, the original paragraph for compression, and a unique external output directory. Require the actual first draft, applicable checking/self-review/revision, final, separate rationale and input/resource hashes. Permit only these inputs, that snapshot and its own output directory; disallow browsing, other runs, installed skill copies and delegation. This is the wrapper used for all eight runs; the operation's prose request and word range are frozen, not adjusted between arms.

After all four runs for an operation finish, run [prepare_review.py](prepare_review.py) with `--root <experiment-root> --operation new` or `revise`. It removes only the separate attribution heading, normalizes line endings and randomly assigns A–D, recording exact keys and hashes. Ask a fresh reviewer to assess the supplied request, sources and anonymous bodies on the nine dimensions in `run-config.json`, distinguishing errors, ambiguities and optional preferences. Do not provide version labels, rationales or intended improvements. The observed reviewers were given body-only packages; their claims about missing supporting files are resolved against the actual runs in the adjudication.

Finally, [archive_results.py](archive_results.py) verifies frozen resources, inputs and body constraints, then archives the finished runs and reviews. `<EXPERIMENT_ROOT>` in archived process records substitutes for the local experiment path; the manifest records both byte hashes. Those archived helper scripts are execution records with placeholders, not portable runtime tools.

Exact hosted model settings and seeds are unavailable, so this reproduces materials and orchestration, not identical model sampling. One source study repeated eight ways is still one study. No human review, measured author-editing time, final held-out result or new runtime capability is claimed.
