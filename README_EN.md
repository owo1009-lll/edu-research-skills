# Education Research Skills

[中文说明](README.md)

Version **0.12.0**. Skills for education paper writing and revision, mock review, reviewer responses, recorded R analyses, qualitative analysis, statistical checks, proposals, research design and academic presentations. The Chinese [user manual](使用手册.md) explains material preparation and review responsibilities.

Mock review now returns the original DOCX or PDF with native highlights and comments, preserving prose and existing comments/revisions. No separate report or automatic rewrite by default. Public synthetic files and actual Word checks are in the [annotation evaluation](evals/review-annotations/README.md).

The [presentation evaluation](evals/edu-ppt-evaluation.md) records seven exercised scenarios, actual renders, independent AI trials and remaining limits. The [open-article example](skills/edu-ppt/examples/article-nbo/README.md) includes selection reasons, a runnable plan and attribution.

Version 0.12.0 adds per-point chart-label and interval-row checks, plus target-journal and editorial-team literature discovery. A new writing card was withheld after mixed blinded comparisons; mechanical introduction quotas were removed, and an optional evidence-sequencing method was retained for article presentations. Complete outputs, source records and rendered previews are in the [evaluation](evals/capability-20261013/README.md).

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

Run `python -X utf8 -m unittest discover tests`. Automated checks, AI review and author feedback have different scopes and are reported separately. The new presentation module is Beta. Writing repairs were tested on final frozen rules; observed improvements and remaining inference errors are documented in [evaluation records](evals/smoke-evaluation.md).

## Data and Attribution

Keep user material and generated work under the user's task directory, outside public skill files. Public examples are licensed or explicitly synthetic. Research ownership, source reading scope and limitations must remain visible. Software references and the adopted approach are recorded [here](skills/edu-ppt/references/open-source.md).
