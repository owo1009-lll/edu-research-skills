# `edu-writing` Skill

[中文说明](README.md)

Writes or revises Chinese and English education papers from evidence, in a voice calibrated on published CSSCI and SSCI articles, preserving the author's argument in revisions.

## What To Use It For

- Write one part: abstract, introduction, literature review, methods, results, discussion, conclusions and implications
- Write a complete paper delivered as Word (three-line tables, figures, verified references)
- Revise or polish an existing manuscript
- Save, selectively apply and manage explicitly supported author preferences; keep project facts separate
- For a specified journal, verify editorial identities and search relevant journal, cross-journal editor and other necessary studies for evidence-based citation advice
- Check a whole manuscript for internal consistency and for writing conventions against published articles (27 CSSCI articles for Chinese, 50 SSCI articles for English)

## Typical Requests

- "Write a full paper for a Chinese educational technology journal"
- "Write the Discussion in English"
- "Revise the discussion but keep my argument and structure"
- "Remember my concept labels in English discussions; for this task, state the judgment before the evidence"
- "Check that numbers and terms are consistent throughout"
- "For AJET, find journal and editorial-team studies relevant to this abstract and integrate them into the introduction"

## What You Need To Provide

- Background, methods, results (or edu-analysis output) and references; the original manuscript for revisions

## Outputs

- Prose or a Word manuscript, figures and tables, a reference check table, a writing rationale table and the review record
- Journal searches also provide identity sources, actual reading scope and inclusion reasons; [public example](https://github.com/owo1009-lll/edu-research-skills/tree/main/evals/capability-20261013/journal)

## Runtime and Dependencies

- Python 3.9 or later; Word and figures need python-docx and matplotlib (`requirements.txt`); no R

## Boundaries

- Does not invent data, references or quotations; the AI review is a self-check, not expert review; Chinese references in CNKI are verified by the user
- Preferences stay on the user's side, support inspection, pausing, undoing additions and deletion, and do not turn inferred candidates into rewriting instructions. This new feature is Beta; see the [workflow](references/author-preferences.md).

## Related Skills

- edu-analysis and edu-qual (analysis first), edu-review (mock review before submission), edu-response (revisions)

## Status

- Stable: used by the author on real research material; voice and prose calibrated on 27 CSSCI and 50 SSCI published articles with same-materials before/after comparisons (Claude and Codex); full workflow tried on synthetic data
