# `edu-response` Skill

[中文说明](README.md)

Responds to journal peer review: splits comments, decides actions, revises the manuscript and delivers the response letter and a red-marked manuscript.

## What To Use It For

- Major and minor revisions, reject-and-resubmit
- 修改说明 for Chinese journals; response letters and cover letters for English journals
- Red-marked revised manuscripts

## Typical Requests

- "Revise the paper and write the 修改说明 from these reviews"
- "Write a point-by-point response to these reviewers"

## What You Need To Provide

- The reviews (editor's letter and reviewer comments) and the original manuscript; any revision ideas you have

## Outputs

- A comment list (comments.csv), the revised manuscript, a red-marked version, the response letter, a cover letter and items for the authors to complete

## Runtime and Dependencies

- Python 3.9 or later with python-docx; new analyses run in R through edu-analysis

## Boundaries

- Reports only changes actually made; new analyses must be run and new references verified; does not change the nature of a conclusion to please a reviewer

## Related Skills

- edu-writing (revision rules), edu-analysis (additional analyses), edu-review (pre-submission simulation)

## Status

- Stable: used by the author on real research material; check and redline scripts tested on seeded examples; full workflow tried on one set of synthetic reviews
