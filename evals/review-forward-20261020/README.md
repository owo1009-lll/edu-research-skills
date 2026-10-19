# English manuscript review: independent forward tasks

Three fresh agents used the frozen `edu-review` skill to review newly composed public English excerpts. Each returned one annotated original, with no rewritten manuscript or separate reviewer report. These are synthetic behavior fixtures, not papers in the expert-distillation corpus or evidence about actual participants.

| Task | Source | Actual user deliverable | Observed review |
|---|---|---|---|
| Quantitative classroom trial | [PDF](inputs-final/quant_retrieval.pdf) | [Annotated PDF](runs/quant/edu_output/review/retrieval/quant_retrieval_审稿标注版.pdf) | Two red inference errors and four blue verification requests. Preserved primary uncertainty and the justified preparation-time recommendation. |
| Qualitative case comparison | [PDF](inputs-final/qual_silence.pdf) | [Annotated PDF](runs/qual/edu_output/review/submission-review/qual_silence_审稿标注版.pdf) | One red paragraph contradicting the cases and two blue methods requests. Retained heterogeneous silence, relational interpretation and the leadership recommendation. |
| Mixed-methods feedback study | [DOCX](inputs-final/mixed_feedback.docx) | [Annotated DOCX](runs/mixed/edu_output/review/mixed-review/final/mixed_feedback_审稿标注版.docx) | Three red contradictions and two blue evidence/reporting requests. Retained value versus opportunity and the scheduling recommendation. |

The comment counts describe these actual outputs; they are not quotas or a quality score. All new substantive comments and their type/severity labels are English. The author identifier remains `AI 模拟审稿` as explicitly required. The Chinese Word interface labels visible in previews are application chrome, not Chinese manuscript content.

## Why the runtime changed

The skill required comments to follow the manuscript language, but the generator always prefixed them with Chinese type and severity labels. Tests of actual DOCX and PDF comments reproduced this conflict; an unknown language was also accepted. The preserved [before log](checks/before-language-fix.txt) contains three failing subcases. The small patch adds an explicit `comment_language` field for `en`/`zh`, updates automatic labels and rejects unsupported values. Omitted language retains historical-plan compatibility. It does not translate comment bodies or change review criteria.

The [after log](checks/after-language-fix.txt) records all 37 review test methods passing, including native English output and legacy preservation cases. Those software checks are separate from the three fresh-agent behavior tasks here. No writing, PPT, statistics or journal-search implementation changed in this patch.

## Frozen inputs and task conditions

The [snapshot manifest](snapshot.json) records 203 actual skill files, source HEAD `963cdf4a40d1b07690c1809208916d4a207fe3ba` and the two dirty skill paths at freeze time. The actual tested tree is `bb4e73cc22eaca30de7aa9de7e56d2bd9c1eca0b0b4a413e2e34447b945d5789`. This is a freeze of edited bytes, not a claim that the source HEAD already included the patch. The seven resources reported read or executed across the tasks are preserved verbatim under [snapshot](snapshot/); the full manifest lets readers verify the published runtime tree.

All tasks received the same [request](inputs-final/request.md), one raw source and the frozen skill path. No output-format hint or intended diagnosis was supplied. Each fresh agent had no parent history and was restricted to its assigned manuscript, request, snapshot and own run directory. No web research, private materials or sibling results were available. The actual initial messages are preserved for [quantitative](runs/quant/task-message.txt), [qualitative](runs/qual/task-message.txt) and [mixed](runs/mixed/task-messages.txt). The mixed wrapper's contradictory last instruction was immediately corrected from “do not read or alter” to “do not alter”; the exact correction and later Word-status exchange are retained. No substantive review answer was supplied.

Agents inherited the same model family and configuration, with no model override. These are independent task contexts, not independent model families or human reviews. One run per research type cannot estimate run-to-run reliability. Inputs were generated with [create_inputs.py](create_inputs.py); the exact files used, including existing comments and tracked changes, are archived in [inputs-final](inputs-final/). Earlier untested drafting of the fixture is not an experimental arm.

## Inspection and limitations

The developer read all final comments against the supplied excerpts and inspected all six annotated manuscript pages, plus both Word comment-balloon pages. Anchors correspond to the identified problems; the Word table, figure, existing author comment and two tracked changes remain. Original PDF notes and content streams remain. The agents also inspected original-page previews, and the frozen verifier passed for all three outputs.

The Word task encountered a stalled first COM export. The document had opened and native comment ranges had been checked. An isolated export using the frozen renderer succeeded. Its first markup preview clipped the final long comment; the agent shortened comments within the same run, generated a second plan and checked all full final comments. Both plans, unsuccessful attempts, helper versions and previews are preserved. Final body highlights and comment-balloon previews are separate views; Word's balloon view can display author colors instead of the native body highlight colors.

The two PDF tasks opened and rendered both pages, and native comment text was read back. Launching the desktop reader succeeded, but interactive popup display was not visually inspected. This limitation is retained in both final receipts; rendering is not a claim of full GUI testing.

The review comments distinguish demonstrated contradictions from missing evidence. The quantitative trial's cluster handling is a verification request, not a declaration that unseen statistics are wrong. The qualitative review does not require statistical generalization or impose a saturation rule. The mixed review identifies impossible individual linkage without removing a defensible conceptual integration. No reviewer claimed to verify omitted literature, raw data or journal-specific requirements. The comments are sometimes long; this test does not establish minimum author effort or superiority over another version.

## Reproduction and records

With the repository review dependencies installed, run from the repository root:

```powershell
python -X utf8 evals/review-forward-20261020/verify_artifacts.py --runtime
```

This checks archived hashes, the full tested runtime tree, exact frozen resources and all actual native outputs against their plans. On a later changed runtime, omit `--runtime` to validate the archived experiment. To generate a fresh annotation copy, call the frozen `annotate_manuscript.py apply` with one archived source and its final plan, choosing a new output path; do not overwrite the archived output. DOCX rendering additionally requires desktop Word; the exact renderer is included among frozen resources. Generating annotations or passing this verifier is not visual acceptance.

[Archive manifest](archive-manifest.json) records original and published hashes. Only local experiment/repository root prefixes in text records were replaced with `<experiment>`/`<repository>`; use a reader-chosen path when replaying historical commands. Documents, plans, source hashes, failed logs, helper code and substantive text are otherwise retained. Hash values inside historical records describe original bytes; the archive manifest gives the corresponding published bytes. Recorded reads are agent-reported and hash-checked, not an instrumented access trace. The three `run-record.json` files and exact `final-response.md` receipts are under [runs](runs/). They distinguish internal experimental logs from user deliverables.

These results support the default annotated-original behavior on three English excerpts and the language-label fix. They do not complete the broader English literature distillation or the final independent writing evaluation.
