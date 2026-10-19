# Reproducing the M-C01 comparison

This directory contains public inputs and source links; no private manuscript is needed. The cached full article is not redistributed. `inputs/D-M02/original.md` reproduces one licensed paragraph, with the preparation defect documented separately in [input-context-correction.md](input-context-correction.md).

The project baseline is `684f5e435b76daf8d0109c9c6a93297542c59889`. The immediate control source for this batch is `a54bb86d4d9727acba4cb5f00165472ec78f65a0`. Freeze that checkout's `skills` directory with [snapshot.py](../writing-20261018/snapshot.py). Use a new directory outside the checkout for each reproduction; do not overwrite this archive or the recorded snapshots.

The two frozen trees contain 203 files each:

- Control tree SHA-256: `2ac357f06b434ea2d36bf021e70ea3371dea47c5cfb90ed053164c440f04c147`.
- Candidate tree SHA-256: `753ca010e482348d15c02e47196ed8d33cc25cd2c463cbfccd4d0325beb4d9da`.

The per-file definitions and hashes are in [control.json](snapshots/control.json) and [candidate.json](snapshots/candidate.json). The candidate changes only `skills/edu-writing/references/analysis-bridge.md`, appending [candidate-addition.md](candidate-addition.md). It is not installed in the runtime skill.

Use [prepare_variants.py](../writing-20261020-qc01/prepare_variants.py) with the control directory/manifest, a new candidate directory/manifest, and these options:

```text
--target skills/edu-writing/references/analysis-bridge.md
--addition evals/writing-20261020-mc01/candidate-addition.md
--label mc01-example-only
```

Copy the four `inputs/D-M02` files byte-for-byte into the new experiment's `inputs/D-M02` directory. Verify against [input-freeze.json](input-freeze.json). Run the eight cells in [run-config.json](run-config.json), using the [writer wrapper](writer-wrapper.md), separate output folders and fresh histories. The new-writing range is 350–450 words; compression is 120–145. Each arm has two repetitions of each operation on the same study. Hosted model settings were not exposed, so the records support procedural reproduction rather than deterministic regeneration.

Once writers finish, run [prepare_review.py](../writing-20261020-qc01/prepare_review.py) separately with `--operation new` and `--operation revise`, each with `--case D-M02` and the experiment's `--root`. It randomly assigns A–D within each operation and saves the key separately. Copy [review-brief.md](review-brief.md) into each blind folder. Use two fresh reviewers, each restricted to its blind folder and own output. Give neither reviewer the key or candidate addition. The new review reads seven files; the compression review reads eight, including the original. Both preserve review.md, review.json and input-hashes.json.

The body extractor accepts either an initial title/attribution heading or a separate final Attribution section. This accommodates actual valid deliveries without editing their final files. It removes only those wrappers and normalizes line endings in the anonymous copy; the original and anonymous hashes are retained. Eight prior Q-C01 bodies and all four M-C01 new-writing bodies were checked to retain the same anonymous hashes after this helper extension. Unexpected internal body headings are rejected.

For a new result archive, copy its own snapshot manifests, input freeze, run configuration and input files into an empty archive directory. Run [archive_results.py](../writing-20261020-qc01/archive_results.py) with the experiment's `--root`, that archive's `--out`, and:

```text
--case D-M02 --new-words 350 450 --revise-words 120 145
```

The helper verifies frozen files, reported loaded-resource hashes, all required input hash records, body length/language, one-paragraph compression and anonymous-copy correspondence. It preserves actual drafts, reviews and checker outputs. Only the local experiment-root prefix is replaced with `<EXPERIMENT_ROOT>` in published text, with both hashes recorded. Copied run-specific helper scripts are historical records with aliased paths, not portable reproduction entrypoints.

For this original batch, archiving first stopped because a writer's audit.py had an earlier execution digest whose file version was no longer retained. The final archive call additionally used `--historical-helper-gaps evals/writing-20261020-mc01/historical-helper-gaps.json`. That exact documented gap is reported as unverified, not passed; all other reported resources and every frozen skill/input remain strictly checked. Do not reuse this gap file for a new experiment whose records differ. The default remains to stop at a mismatch, and declared gaps cannot apply to frozen instructions, task inputs or manuscripts.

Review writing quality and evidence correspondence separately from these integrity checks. Preserve failures and do not regenerate a manuscript merely because a reviewer prefers another. Use the actual review, source pack and original to adjudicate any disagreement. No score total or number of passed scripts determines adoption.
