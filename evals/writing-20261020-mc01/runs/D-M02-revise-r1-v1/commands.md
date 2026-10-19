# Executed commands

The read commands below are recorded from the actual tool calls. The first four used PowerShell’s default decoding; the files were then reread explicitly as UTF-8. One large output was truncated, so the relevant support texts were reread in smaller batches. All reads remained within the permitted task inputs and skill snapshot.

```powershell
Get-Content -Raw -LiteralPath '<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\SKILL.md'
Get-Content -Raw -LiteralPath '<EXPERIMENT_ROOT>\inputs\D-M02\revise-request.md'
Get-Content -Raw -LiteralPath '<EXPERIMENT_ROOT>\inputs\D-M02\source-pack.md'
Get-Content -Raw -LiteralPath '<EXPERIMENT_ROOT>\inputs\D-M02\original.md'
Get-Content -Raw -Encoding UTF8 -LiteralPath '<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\SKILL.md'
Get-Content -Raw -Encoding UTF8 -LiteralPath '<EXPERIMENT_ROOT>\inputs\D-M02\revise-request.md'
Get-Content -Raw -Encoding UTF8 -LiteralPath '<EXPERIMENT_ROOT>\inputs\D-M02\source-pack.md'
Get-Content -Raw -Encoding UTF8 -LiteralPath '<EXPERIMENT_ROOT>\inputs\D-M02\original.md'
Get-Content -Raw -Encoding UTF8 -LiteralPath '<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\references\foundation.md'
Get-Content -Raw -Encoding UTF8 -LiteralPath '<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\references\argument.md'
Get-Content -Raw -Encoding UTF8 -LiteralPath '<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\references\voice-en.md'
Get-Content -Raw -Encoding UTF8 -LiteralPath '<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\references\quantitative-discussion.md'
Get-Content -Raw -Encoding UTF8 -LiteralPath '<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\scripts\check_voice.py'
Get-Content -Raw -Encoding UTF8 -LiteralPath '<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\scripts\check_prose.py'
Get-Content -Raw -Encoding UTF8 -LiteralPath '<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\references\foundation.md'
Get-Content -Raw -Encoding UTF8 -LiteralPath '<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\references\argument.md'
Get-Content -Raw -Encoding UTF8 -LiteralPath '<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\references\voice-en.md'
Get-Content -Raw -Encoding UTF8 -LiteralPath '<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\references\quantitative-discussion.md'
Get-Content -Raw -Encoding UTF8 -LiteralPath '<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\references\analysis-bridge.md'
Get-Content -Raw -Encoding UTF8 -LiteralPath '<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\references\qualitative-narrative.md'
Get-Content -Raw -Encoding UTF8 -LiteralPath '<EXPERIMENT_ROOT>\variants\v1\skills\edu-shared\references\integrity.md'
rg -n '^(import|from)|read_text|open\(|Path\(|__file__|\.json|\.md' '<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\scripts\check_voice.py' '<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\scripts\check_prose.py'
Get-Content -Raw -Encoding UTF8 -LiteralPath '<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\references\framing-results.md'
```

Draft and note files were written with `apply_patch`. Checker execution is performed by `audit_run.py`; the exact child-process argument lists, timestamps, script hashes, exit codes, and raw output filenames are stored in `executed-commands.jsonl` and the stage validation JSON files. No checker output is synthesized.

```powershell
python '<EXPERIMENT_ROOT>\runs\D-M02-revise-r1-v1\audit_run.py' first-draft
```

```powershell
python -X utf8 '<EXPERIMENT_ROOT>\runs\D-M02-revise-r1-v1\audit_run.py' second-draft
python -X utf8 '<EXPERIMENT_ROOT>\runs\D-M02-revise-r1-v1\audit_run.py' third-draft
```

```powershell
python -X utf8 '<EXPERIMENT_ROOT>\runs\D-M02-revise-r1-v1\finalize.py'
```

`audit_run.py` computes SHA-256 hashes directly from the permitted input and resource files and saves exact checker output. `finalize.py` checks only this run’s outputs, verifies that saved drafts are unchanged since checking, and records the final word count and UTF-8 checks. Both local support scripts are included with their hashes in the resource manifest.

