# `edu-research` Skill

[中文说明](README.md)

Entry point for education research: routes a request to the right module, and handles topics, research questions, frameworks, design and sample size.

## What To Use It For

- Turn a topic into feasible research questions and a design
- Multi-step projects (analyze data, then write the paper)
- Locate manuscript, table, citation and presentation passages affected by updated materials
- When it is unclear which module to use

## Typical Requests

- "Propose feasible research questions and a design on generative AI and university students' self-regulated learning"
- "How large a sample does this quasi-experiment need?"
- "Write a paper from these data"
- "These are my confirmed results; check the Word manuscript and slides for old content without editing them"

## What You Need To Provide

- A topic or question; any literature, data or drafts you already have

## Outputs

- Candidate questions, framework, design and analysis plan, sample-size estimates; routing and hand-offs for multi-step work

## Runtime and Dependencies

- Routing needs no extra dependencies. Cross-format checks use this package's `requirements.txt` for DOCX, PPTX, PDF and XLSX reading; no R is required.

## Boundaries

- Does not invent recruitment, ethics approval, data or preregistration
- Update checks are Beta. The reader establishes semantic mappings; checks are read-only by default and disclose unreadable or unmapped content. Authorized synchronization creates new versions. See the [workflow](references/material-updates.md).

## Related Skills

- edu-analysis, edu-qual, edu-audit, edu-writing, edu-proposal, edu-review, edu-response, edu-ppt (research presentations and paper reading)

## Status

- Stable: used by the author on real research material; routing blind-tested on scenarios; four usage scenarios tried on synthetic data
