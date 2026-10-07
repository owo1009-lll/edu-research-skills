# `edu-audit` Skill

[中文说明](README.md)

Checks statistics in papers or drafts: recompute values from data or tables, or review whether statistics are reported completely.

## What To Use It For

- Recompute counts, proportions and risk ratios from published tables
- Recompute means and SDs from participant-level data
- Review the statistical reporting in a results section before submission

## Typical Requests

- "Check the counts and risk ratios in Table 4 of this paper"
- "Is the statistical reporting in my results section complete?"

## What You Need To Provide

- The paper or draft; data or tables for recomputation

## Outputs

- A table of reported versus recomputed values and an audit report; a reporting review table (location, issue, suggested wording)

## Runtime and Dependencies

- Recomputation needs R (jsonlite); the reporting review needs only Python

## Boundaries

- Matching values do not prove the data are genuine; no adapters yet for regression or SEM recomputation; the reporting review gives prompts, and missing statistics must be computed from raw data

## Related Skills

- edu-analysis (compute missing statistics), edu-review (full pre-submission review)

## Status

- Beta: recomputation verified on a published paper; the reporting review is new and tested on seeded examples
