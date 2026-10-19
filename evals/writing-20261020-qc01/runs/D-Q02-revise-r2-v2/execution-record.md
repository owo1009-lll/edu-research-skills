# Execution record

All prose stages were created with apply_patch in the assigned output directory. The recorded sequence is: skill and input reads; applicable support reads; pre-draft rationale and draft 1; actual first-draft checks; AI self-review; draft 2; actual revision checks; final delivery and separate change/source note. No stage was generated retrospectively to fill a missing draft or review.

The first PowerShell read used Get-Content -Raw without an explicit encoding and displayed UTF-8 characters incorrectly. The skill and inputs were read again with UTF-8; all saved files use UTF-8. Large support/script displays were truncated by the output limits. voice-en.md was re-read in full, and script imports and file reads were inspected with rg. No output text was reconstructed from checker results: their stdout and stderr bytes are saved directly.

Executed checker launcher commands:

```powershell
$env:PYTHONIOENCODING = 'utf-8'
python '<EXPERIMENT_ROOT>\runs\D-Q02-revise-r2-v2\run-checks.py' draft-1
```

```powershell
$env:PYTHONIOENCODING = 'utf-8'
python '<EXPERIMENT_ROOT>\runs\D-Q02-revise-r2-v2\run-checks.py' draft-2
```

The exact Python executable, script path, arguments, working directory, timestamps, return code, and output paths for each of the four actual checker subprocesses are in executed-commands.jsonl. The helper's SHA-256 is included in loaded-resources.json. It is an output-local logging helper, not a replacement checker.

The checkers import only Python standard-library modules for these Markdown inputs. Corpus reference values are embedded in their scripts; no corpus articles, external benchmark files, installed skill copies, other runs, or repository files were read. The task's explicit no-browsing restriction was followed. No other agents were spawned.
