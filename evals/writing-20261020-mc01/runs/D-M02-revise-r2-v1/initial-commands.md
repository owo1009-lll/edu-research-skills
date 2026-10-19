# Initial commands

These shell commands were executed before the command recorder was created. Both initial reads completed successfully, but PowerShell's default decoding rendered non-ASCII characters incorrectly. The third command repeated the permitted reads with explicit UTF-8 decoding. No drafting stage occurred before these reads.

```powershell
Get-Content -LiteralPath '<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\SKILL.md' -Raw
```

```powershell
Get-Content -LiteralPath '<EXPERIMENT_ROOT>\inputs\D-M02\revise-request.md' -Raw; Get-Content -LiteralPath '<EXPERIMENT_ROOT>\inputs\D-M02\source-pack.md' -Raw; Get-Content -LiteralPath '<EXPERIMENT_ROOT>\inputs\D-M02\original.md' -Raw
```

```powershell
Get-Content -LiteralPath '<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\SKILL.md' -Raw -Encoding UTF8; Get-Content -LiteralPath '<EXPERIMENT_ROOT>\inputs\D-M02\revise-request.md' -Raw -Encoding UTF8; Get-Content -LiteralPath '<EXPERIMENT_ROOT>\inputs\D-M02\original.md' -Raw -Encoding UTF8; Get-Content -LiteralPath '<EXPERIMENT_ROOT>\inputs\D-M02\source-pack.md' -Raw -Encoding UTF8
```

Subsequent helper invocations and checker subprocesses are recorded in `executed-commands.json`. Prose and helper files are written using `apply_patch`; these edits are visible in the execution transcript.
