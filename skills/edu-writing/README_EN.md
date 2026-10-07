# `edu-writing` Skill

[中文说明](README.md)

Writes or revises Chinese and English education papers from evidence, in a voice calibrated on published CSSCI and SSCI articles, preserving the author's argument in revisions.

## What To Use It For

- Write one part: abstract, introduction, literature review, methods, results, discussion, conclusions and implications
- Write a complete paper delivered as Word (three-line tables, figures, verified references)
- Revise or polish an existing manuscript
- Check a whole manuscript for internal consistency and for writing conventions against published articles (27 CSSCI articles for Chinese, 50 SSCI articles for English)

## Typical Requests

- "Write a full paper for a Chinese educational technology journal"
- "Write the Discussion in English"
- "Revise the discussion but keep my argument and structure"
- "Check that numbers and terms are consistent throughout"

## What You Need To Provide

- Background, methods, results (or edu-analysis output) and references; the original manuscript for revisions

## Outputs

- Prose or a Word manuscript, figures and tables, a reference check table, a writing rationale table and the review record

## Runtime and Dependencies

- Python 3.9 or later; Word and figures need python-docx and matplotlib (`requirements.txt`); no R

## Boundaries

- Does not invent data, references or quotations; the AI review is a self-check, not expert review; Chinese references in CNKI are verified by the user

## Related Skills

- edu-analysis and edu-qual (analysis first), edu-review (mock review before submission), edu-response (revisions)

## Status

- Stable: used by the author on real research material; voice and prose calibrated on 27 CSSCI and 50 SSCI published articles with same-materials before/after comparisons (Claude and Codex); full workflow tried on synthetic data
