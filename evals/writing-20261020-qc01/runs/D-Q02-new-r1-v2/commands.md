# Execution record

The detailed command arguments, stages, exit codes, and output filenames are in commands.jsonl. Resource paths and SHA-256 hashes are in loaded-resources.json; the two source inputs are recorded separately in input-hashes.json. All manuscript and note edits used apply_patch, with the argument plan saved before the first draft and the self-review saved before final.md.

The required first-draft commands executed against the specified snapshot were:

```powershell
python '<EXPERIMENT_ROOT>/variants/v2/skills/edu-writing/scripts/check_voice.py' --draft '<EXPERIMENT_ROOT>/runs/D-Q02-new-r1-v2/draft-01.md' --source '<EXPERIMENT_ROOT>/inputs/D-Q02/source-pack.md'
python '<EXPERIMENT_ROOT>/variants/v2/skills/edu-writing/scripts/check_prose.py' --draft '<EXPERIMENT_ROOT>/runs/D-Q02-new-r1-v2/draft-01.md'
python '<EXPERIMENT_ROOT>/runs/D-Q02-new-r1-v2/check_body_counts.py' '<EXPERIMENT_ROOT>/runs/D-Q02-new-r1-v2/draft-01.md'
```

These outputs were saved immediately. The following executed runner stages preserve the later checker subprocess arguments and raw stdout/stderr:

```powershell
python '<EXPERIMENT_ROOT>/runs/D-Q02-new-r1-v2/run_checks.py' first-draft-diagnostic
python '<EXPERIMENT_ROOT>/runs/D-Q02-new-r1-v2/run_checks.py' final-verification
```

The diagnostic stage replaced only the attribution heading in a separate copy so check_prose.py would identify the Discussion correctly. The final stage reran both required checkers after the substantive revision, kept both prose-classification outputs, and counted body and heading words separately. The runner also repaired the nested-array manifest representation described in self-review.md; the pre-repair manifest is retained. No checker stage or first draft was recreated after the revision.
