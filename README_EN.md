# Education Research Skills

[中文说明](README.md)

Version **0.14.0**. Skills for education paper writing and revision, mock review, reviewer responses, recorded R analyses, qualitative analysis, statistical checks, proposals, research design and academic presentations. The Chinese [user manual](使用手册.md) explains material preparation and review responsibilities.

Mock review now returns the original DOCX or PDF with native highlights and comments, preserving prose and existing comments/revisions. No separate report or automatic rewrite by default. Public synthetic files and actual Word checks are in the [annotation evaluation](evals/review-annotations/README.md).

The [presentation evaluation](evals/edu-ppt-evaluation.md) records seven exercised scenarios, actual renders, independent AI trials and remaining limits. The [open-article example](skills/edu-ppt/examples/article-nbo/README.md) includes selection reasons, a runnable plan and attribution.

Version 0.14.0 adds scoped author preferences and user-triggered material-update checks. Preferences stay on the user side and support selective loading, pausing and deletion. Linked checks compare confirmed sources with manuscripts, tables, citations and native slides; they are read-only by default, with authorized updates saved as new versions. Both features are Beta. See the [complete synthetic example, independent trials and limits](evals/author-project-20261020/README.md).

Version 0.13.0 (2026-10-20) adds native DOCX/PDF review annotations and completes English quantitative, qualitative and mixed-methods writing distillation. It makes the mixed-methods route explicit, removes fixed paragraph endings, ordering and conclusion formulas, and preserves supported author judgments. Six final writing tasks on three held-out papers and native annotation checks are archived; extra rules without stable gains were withheld. See the [delivery and limits](distill/20261019/delivery.md), [final writing evaluation](evals/writing-final-20261020/README.md) and [annotation evaluation](evals/review-annotations/README.md). This version synchronization changes only release metadata and the root READMEs; historical evaluations retain their recorded frozen versions.

## Install

Run `python scripts/install.py --host codex` (or `claude`, `workbuddy`, `codebuddy`). Use `--action update` for installer-owned copies. Install every package listed in `skills/release.json`, including the shared support package. Python 3.9+ is required; statistical work also needs R.

## Presentations and Paper Reading

Use `$edu-ppt` or a natural request:

- “Turn my paper into a 15-minute lab-meeting presentation.”
- “Present my research progress, keeping incomplete work explicit.”
- “Explain this English paper in a Chinese editable deck.”
- “Find papers on infant socioemotional development and prepare a journal-club presentation.”
- “Only provide slide-by-slide content and speaker notes.”
- “Use this PowerPoint template.”

Own research has completed-paper, proposal and progress routes. Paper reading follows What, Why, How and Result, using supplied material or actual public literature searches. Content mode delivers complete copy, visual arrangements, notes, sources and timing. Finished mode adds editable PPTX, embedded notes and rendered previews. See [edu-ppt](skills/edu-ppt/README_EN.md).

## Dependencies and Verification

Presentation dependencies are in `skills/edu-ppt/requirements.txt`. The single generation engine is python-pptx; no additional model API key is required. Actual rendering needs Windows PowerPoint or LibreOffice plus pdftoppm. Source figures remain images; native text, tables, diagrams and data-backed charts remain editable.

From the repository root, install development dependencies with `python -m pip install -r requirements-dev.txt`, then run `python -X utf8 -m unittest discover tests`. Automated checks, AI review and author feedback have different scopes and are reported separately. The new presentation module is Beta. Writing repairs were tested on final frozen rules; observed improvements and remaining inference errors are documented in [evaluation records](evals/smoke-evaluation.md).

## Data and Attribution

Keep user material and generated work under the user's task directory, outside public skill files. Public examples are licensed or explicitly synthetic. Research ownership, source reading scope and limitations must remain visible. Software references and the adopted approach are recorded [here](skills/edu-ppt/references/open-source.md).
