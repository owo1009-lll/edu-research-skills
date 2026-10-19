# English writing development checks

Status: six current-version diagnostic tasks on three studies and their independent manuscript reviews are complete; the larger evaluation remains in progress. These are development diagnostics, not final independent holdouts or evidence that a new method improves writing.

The full project baseline remains `684f5e435b76daf8d0109c9c6a93297542c59889`. The first diagnostics use the current released skill at `b89d3c5f414d26931fe0923a61ec53361018f8b3`, after the documented direct-conflict repairs. This is a different comparison point, not a replacement baseline. No new candidate writing methods have been loaded for these runs.

All sources, requests and manuscript outputs in this evaluation are English. Development notes may be Chinese. No private manuscript is used. M-N09, Q-N08 and L-N11 have already been read for method development; two operations on one paper remain one study, and none is a holdout.

| Task | Study | Operation | Purpose |
|---|---|---|---|
| D-M01-new | M-N09, one public mixed-methods study | New discussion from a source pack | Inspect what the existing skill does with observation patterns and interview accounts |
| D-M01-revise | The same M-N09 study | Compress an actual published paragraph | Inspect preservation of the author's argument, concepts, position and citations |
| D-Q01-new | Q-N08, one public quantitative study | New discussion from a source pack | Inspect interpretation across comparison levels and wellbeing outcomes |
| D-Q01-revise | The same Q-N08 study | Compress an actual published paragraph | Correct an unsupported inference while retaining the author's policy position |
| D-L01-new | L-N11, one public qualitative study | New discussion from a source pack | Interpret different accounts and conditions for collaboration |
| D-L01-revise | The same L-N11 study | Compress an actual published paragraph | Retain concepts, attributed judgments and practical conditions |

The source pack and requests are frozen before writing. The excerpt in the revision task is actual author prose, reproduced under the publisher's CC BY 4.0 licence with attribution; it is not a synthetic “original.” New discussion outputs are clearly recorded as secondary-writing demonstrations, not the writers' own empirical study.

An independent writing agent receives only the relevant request, raw task materials and frozen skill, not the distillation notes, suspected problems, candidate methods or intended answer. It records the files actually loaded. Different operations on one study remain one study; repeated runs will be labelled repeats, not extra contexts. Review results and negative findings will be retained. No human review or reduction in human editing time is claimed.

The hosted model, temperature and seed are not fully exposed or controllable in this environment. Agents inherit the session's default model; this is not a cross-model evaluation. Task constraints and skill bytes can be reproduced, but identical generations are not guaranteed. Writers do not browse, so the source package is the same evidence boundary for each run. Existing citations in the revision excerpt remain the original authors' citations, not independently verified sources.

The skill snapshot is recorded in [snapshots/current-01.json](snapshots/current-01.json), using the existing [snapshot utility](../writing-20261018/snapshot.py). The actual tree is copied outside the repository and its public manifest uses repository-relative paths. The published artifacts retain both original and published hashes in [publication-manifest.json](publication-manifest.json). Only local paths are replaced by documented aliases; one PowerShell checker output is transcoded from UTF-16 to UTF-8 without changing its text. Final manuscripts and frozen task inputs are byte-identical to the originals.

These current-version passes have no candidate arm. They can establish an observable issue or show that an existing capability needs no additional instruction. They cannot estimate an improvement from a new method. After diagnosing an actual issue, any narrowly scoped candidate comparison must use the same task materials, length constraints and recorded configuration, and must test the actual loaded combination. Wider coverage, targeted comparisons and final frozen-version independent review remain outstanding.

## Actual results and retained artifacts

| Operation | Final output | What happened | Limits |
|---|---|---|---|
| New discussion | [243 words, two paragraphs](runs/D-M01-new-run01-current/final.md) | Connected access to talk with how ideas are taken up; self-review removed an unsupported opposition and an unasked-for rejection of removing evaluation | One generation after local review; no candidate arm or transfer evidence |
| Published-paragraph compression | [138 words, one paragraph](runs/D-M01-revise-run01-current/final.md) | Preserved the argument, directive position and 12 citations; corrected an initial below-length candidate | The cited originals remain unverified; fidelity does not establish their claims' truth |

The [independent review](judges/diagnostic-01/assessment.md) covers all nine dimensions and establishes no mandatory new manuscript correction. Its [structured findings](judges/diagnostic-01/findings.json) retain optional improvements and unresolved evidence questions. [Developer adjudication](adjudication.md) checks those findings against actual outputs, delivery records and the failed drafts; it explains why this pass leads to no additional runtime rule.

The two `runs/` directories retain drafts, self-review, final, rationale, load manifests and actual script output. New-writing scripts checked its first draft; final length/structure checks and independent final review are recorded separately. Revision scripts checked its final. Script success is not a writing-quality verdict. [run-config.json](run-config.json) records conditions, permitted materials and scope; [input-freeze.json](input-freeze.json) identifies the exact requests and source bytes. The [label key](blind/key-diagnostic-01.json) maps anonymous finals to runs. X/Y were different operations, not randomized competing versions.

[Record verification](record-verification.json) reports the actual hash, link, snapshot and count checks. The four historical Chinese reading records were also compared with `b89d3c5` and remained unchanged. This verifies publication integrity and the language scope; it does not substitute for the substantive review or establish the paper's original facts.

The second batch adds [four actual outputs and developer adjudication](adjudication-02.md), with separate [quantitative](judges/diagnostic-02-Q/assessment.md) and [qualitative](judges/diagnostic-02-L/assessment.md) reviews. Neither review established a mandatory final-manuscript correction. All drafts, local reviews, explanations and failures remain under their `runs/` directories. The writers corrected substantive first-draft errors, length failures and encoding problems; the clean final reviews do not imply error-free first drafts. No runtime instruction was added on this evidence.

Its [configuration](run-config-02.json), [eight frozen inputs](input-freeze-02.json), [snapshot reuse check](snapshots/current-01-reuse-02.json), [64-artifact publication manifest](publication-manifest-02.json) and [verification](record-verification-02.json) extend the first batch without overwriting its records. Three writers checked first drafts with the skill scripts; qualitative compression used local semantic and format checks without those scripts. All four finals were independently reviewed. The same 203 snapshot files were verified against both the external frozen copy and the current repository before the runs.

## Reproducing the conditions

Obtain a clean checkout of source commit `b89d3c5f414d26931fe0923a61ec53361018f8b3`, then use the existing snapshot utility with new external output paths:

```powershell
python -X utf8 evals/writing-20261018/snapshot.py --source <checkout-at-b89d3c5> --out <new-external-snapshot> --manifest <new-manifest.json> --label current-01-reproduction
```

Compare its 203 file hashes and tree hash with the saved snapshot manifest. Give each fresh writer its corresponding frozen request, listed source files and the snapshot's `skills/edu-writing/SKILL.md`. Permit only relevant snapshot resources, prohibit browsing and other run/development records, and save outputs in an isolated folder. Do not supply the analyses, assessment or adjudication as writing instructions. The requests are the actual frozen task text; these reproduction instructions describe the orchestration conditions, not a verbatim transcript of the agent wrapper prompts.

For an independent review, supply one study's four frozen inputs and its two anonymous final manuscripts, but not the skills, writer notes or expected answer. Ask for the nine dimensions in `run-config.json` or `run-config-02.json`, distinguishing demonstrated errors, unresolved source checks and optional style choices. Judge each operation against its own request. Do not rank X against Y as rule versions. The second-batch keys are [Q](blind/key-diagnostic-02-Q.json) and [L](blind/key-diagnostic-02-L.json).

Aliases such as `@snapshot`, `@inputs` and `@runs` are publication placeholders. Resolve them to the reader's own directories before replaying recorded commands. The saved `run_checks.py` is an actual run artifact with aliased paths, not a ready-to-run general command. Identical model output is not guaranteed. No private or developer-only source path is required to obtain the public paper or reproduce the supplied task materials.
