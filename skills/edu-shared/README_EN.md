# `edu-shared` Skill

[中文说明](README.md)

Support package shared by the other edu-* skills; it does not handle tasks on its own.

## What To Use It For

- Provides the runner that executes R and records every analysis (`scripts/edu_runtime.py`)
- Provides the integrity rules shared by all modules (`references/integrity.md`)

## Typical Requests

- Not invoked directly; other modules read it through `../edu-shared/`

## What You Need To Provide

- Nothing

## Outputs

- provenance.json, run_status.json and sessionInfo.txt in each run folder

## Runtime and Dependencies

- Python 3.9 or later; R when analyses run

## Boundaries

- Must be installed in the same skills directory as the other edu-* skills

## Related Skills

- edu-analysis and edu-audit (runner); all modules (integrity rules)

## Status

- Stable: used by the author on real research material; tested together with the modules
