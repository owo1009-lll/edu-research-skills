# Preparatory command record

The following commands were actually executed before or outside the audit helper. They are recorded from this run's tool calls. They do not represent recreated drafting stages. The initial `Get-Content` calls used the shell's default decoding and produced mojibake in the tool display; all three files were then read again as UTF-8 through `audit.py`, which recorded their hashes. All saved prose uses UTF-8.

```powershell
Get-Content -LiteralPath '<EXPERIMENT_ROOT>\inputs\D-M02\new-request.md' -Raw
Get-Content -LiteralPath '<EXPERIMENT_ROOT>\inputs\D-M02\source-pack.md' -Raw
Get-Content -LiteralPath '<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\SKILL.md' -Raw
New-Item -ItemType Directory -Path '<EXPERIMENT_ROOT>\runs\D-M02-new-r2-v1' -Force | Out-Null
rg -n '^(from|import)|read_text|read_bytes|open\(' '<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\scripts\check_prose.py' '<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\scripts\check_voice.py'
```

`executed-commands.json` records each audit-helper invocation and each checker subprocess argument vector. Every invocation used `python` followed by the displayed audit-helper path and arguments. Checker logs include the real command arguments, exit code, stdout, and stderr. Prose and the audit helper were written with `apply_patch`; the tool-call history retains the exact patches. The original first draft was saved before checker execution and AI self-review; the second draft was saved afterward. Diagnostic copies replace only the attribution heading with `# Discussion` so the scripts inspect the intended section. They are not additional prose revisions.

`loaded-resources.json` records supplied skill and support resources read or executed, including repeated execution entries. The task-created audit helper is also recorded at its final executable version. `task-input-hashes.json` records the two inputs separately. No additional package-local resources are imported by the checker scripts; their remaining imports are Python standard-library modules.
