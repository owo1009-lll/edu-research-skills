# `edu-review` Skill

[中文说明](README.md)

Simulated peer review before submission: two or three independent reviewers give numbered concerns with resolution tests, synthesized into a revision list.

## What To Use It For

- Find what reviewers will criticize before you submit
- Check a grant application from a panel reviewer's view

## Typical Requests

- "Review this manuscript as a reviewer would and tell me where it may be rejected"
- "Simulate two external reviewers for this application"

## What You Need To Provide

- The manuscript or application; the target journal or fund if known

## Outputs

- Reviewer reports (major and minor concerns with locations, why they matter and resolution tests), a synthesis and a prioritized revision list

## Runtime and Dependencies

- Python 3.9 or later; uses the check scripts of edu-writing and edu-audit

## Boundaries

- Simulated by AI, not expert review; no acceptance probabilities; no guessing at author identity

## Related Skills

- edu-writing (revise from the list), edu-response (answer real reviews), edu-audit (reporting review)

## Status

- Beta: check script tested on seeded examples; full workflow tried on one synthetic manuscript with reviewers in separate sub-agents
