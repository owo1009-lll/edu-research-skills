# Independent final English writing validation

Status: six writing tasks and three independent manuscript assessments complete. See [actual outcomes, before/after examples and limitations](adjudication.md).

The user removed the illustrative corpus-size target on 20 October 2026. This evaluation tests the selected writing implementation, rather than extending the corpus to meet a quota. It is a final-version diagnostic, not a new baseline comparison or evidence of universal improvement.

## Frozen implementation and exposure

The [snapshot](snapshot.json) records 203 actual skill files from commit `a388aac65159ee5f0174adc80829ac878ce31c28`, with tree hash `895b0ddcda12fa21ff62fa0953afd5176654e12f126ffd3068e5e1719886f5cf`. Its purpose explicitly identifies independent final validation. No runtime changes are permitted during these runs.

The three English articles in [sources.json](sources.json) were selected after that freeze. Their DOI/title strings were searched in the existing `distill`, `evals`, and `skills` trees before adding these records; no prior use was found. This establishes non-use in this development record, not absence from a model's training data. The coordinator inspected source identity, licence, design and target passages while preparing inputs. The papers were not used to tune the frozen rules.

The studies cover a classroom quantitative comparison, a qualitative science-identity study, and a mixed-methods remote-laboratory study. The quantitative, qualitative and mixed labels describe these designs; three papers cannot represent every design or writing problem in those categories.

## Tasks and evidence boundaries

Each writer receives the same [request](request.md), the frozen skill and its own input directory. New writing uses introduction/design/findings extracts with the source abstract, discussion and conclusion withheld. Only after saving the new-writing final may the writer open the actual author passage and full article extraction for revision. Revision targets are authentic published passages, not model-generated surrogate drafts. Both tasks are English; none uses a private user manuscript.

The [preparation script](prepare_inputs.py) produces attributed extracts from the recorded PDF text and publisher HTML. It preserves page markers in PDF extracts and uses publisher paragraphs for revision targets. [Input hashes](inputs-manifest.json) make subsequent changes detectable. The three short revision targets are committed; long source extracts remain local and can be reconstructed from the public sources using the script. PDF text extraction can disturb tables, line breaks and reading order; evaluators must identify such uncertainties rather than silently repair reported evidence. [Acquisition metadata](acquisition.json) and publisher links support checking against the originals.

All three papers permit CC BY reuse. Original extracts retain attribution and licence links; generated prose is a secondary-writing adaptation. Source authors' citations do not establish that the cited papers were independently read.

## Assessment and records

Independent evaluators received anonymous manuscript outputs, the supplied evidence and, for revision, the actual original passage. They did not receive writer rationales, development hypotheses or implementation identity. The [assessment request](review-request.md) covers facts/author meaning, educational question, reasoning, theory/literature use, explanation/contribution, language, author voice, necessary qualification, and concrete remaining corrections. Mandatory corrections, optional preferences and verification issues are distinguished and tied to passages and sources. Word counts establish task scope only; keyword counts do not score prose quality.

Initial failures and self-corrections remain in `runs/`; assessments are in `judges/`. The coordinator checked the actual outputs and consequential source passages after independent assessment. All six finals met their tasks without an established mandatory correction; optional refinements and source-reporting questions remain. AI assessment is not human author validation. One run per study/task describes these outputs and does not estimate generation variability or editing-time savings.

The [run configuration](run-config.json) records available controls and extraction versions. The [publication manifest](publication-manifest.json) covers 95 archived artifacts: manuscript bytes are unchanged, while local paths in working records use documented aliases and 13 UTF-16 logs were transcoded to UTF-8. Reconstructed read logs are explicitly weaker than instrumented traces; malformed originals and repair notes are retained. Historical script cues were manually assessed, not treated as quality scores.

## Reproduction

1. Use the source commit and verify the skill hashes against `snapshot.json`.
2. Run `python evals/writing-final-20261020/prepare_inputs.py --cache <new-local-download-directory> --fetch` to download the public sources and reconstruct the evidence packs. Alternatively supply an existing cache containing `source.pdf`, `body.txt` and `publisher.html` per source ID and omit `--fetch`. The script refuses to replace a frozen file or manifest with different bytes. Publisher responses and PDF extraction versions may change; a mismatch requires investigation, not replacing the saved evidence. Dependencies are Beautiful Soup, PyMuPDF and requests, already used by the source-acquisition tooling.
3. Run each study in a fresh context, with only its inputs and the frozen runtime. Preserve actual read logs and task order.
4. Independently assess the anonymous outputs with their evidence. Generations are not expected to be byte-identical.

Run `python evals/writing-final-20261020/verify_artifacts.py` to check the archive, anonymous finals and reported loaded-file hashes. Add `--runtime` to compare the current skill tree with the tested freeze and `--inputs` after reconstructing the long source inputs. A later runtime may legitimately differ; that does not change the archived result. Input preparation and structural checks alone establish no writing-quality claim.
