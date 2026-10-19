# Record of PowerShell read commands actually executed before drafting.
# This record is not a script that was rerun. Initial default-encoding displays
# were garbled, so explicit UTF-8 reads followed. Large displays were truncated;
# smaller reads supplied the applicable instruction text. No external links opened.

# Execution 1
Get-Content -LiteralPath '<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\SKILL.md' -Raw
# Execution 2
Get-Content -LiteralPath '<EXPERIMENT_ROOT>\inputs\D-Q02\revise-request.md' -Raw
# Execution 3
Get-Content -LiteralPath '<EXPERIMENT_ROOT>\inputs\D-Q02\source-pack.md' -Raw
# Execution 4
Get-Content -LiteralPath '<EXPERIMENT_ROOT>\inputs\D-Q02\original.md' -Raw
# Execution 5
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Get-Content -LiteralPath '<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\SKILL.md' -Raw -Encoding UTF8
# Execution 6
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$paths = @('<EXPERIMENT_ROOT>\inputs\D-Q02\revise-request.md', '<EXPERIMENT_ROOT>\inputs\D-Q02\source-pack.md', '<EXPERIMENT_ROOT>\inputs\D-Q02\original.md')
foreach ($p in $paths) { Write-Output "FILE: $p"; Get-Content -LiteralPath $p -Raw -Encoding UTF8 }
# Execution 7
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$root = '<EXPERIMENT_ROOT>\variants\v1\skills'
$paths = @('edu-writing\references\foundation.md','edu-writing\references\argument.md','edu-writing\references\voice-en.md','edu-writing\references\quantitative-discussion.md','edu-writing\references\framing-results.md','edu-shared\references\integrity.md','edu-writing\scripts\check_voice.py','edu-writing\scripts\check_prose.py')
foreach ($p in $paths) { Write-Output "FILE: $p"; Get-Content -LiteralPath (Join-Path $root $p) -Raw -Encoding UTF8 }
# Execution 8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Get-Content -LiteralPath '<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\references\voice-en.md' -Raw -Encoding UTF8
Get-Content -LiteralPath '<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\references\quantitative-discussion.md' -Raw -Encoding UTF8
# Execution 9
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Get-Content -LiteralPath '<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\references\framing-results.md' -Raw -Encoding UTF8
Get-Content -LiteralPath '<EXPERIMENT_ROOT>\variants\v1\skills\edu-shared\references\integrity.md' -Raw -Encoding UTF8
# Execution 10
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Get-Content -LiteralPath '<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\scripts\check_voice.py' -Raw -Encoding UTF8
Get-Content -LiteralPath '<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\scripts\check_prose.py' -TotalCount 50 -Encoding UTF8
# Execution 11
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Get-Content -LiteralPath '<EXPERIMENT_ROOT>\variants\v1\skills\edu-shared\references\integrity.md' -Raw -Encoding UTF8
Get-Content -LiteralPath '<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\references\framing-results.md' -Encoding UTF8 | Select-Object -Skip 65
Select-String -LiteralPath '<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\scripts\check_prose.py','<EXPERIMENT_ROOT>\variants\v1\skills\edu-writing\scripts\check_voice.py' -Pattern '^import |^from |read_text|open\('
