$helperPath = '<experiment>\snapshot\skills\edu-review\scripts\annotate_manuscript.py'
rg -n '^(def .*pdf|def main|def inventory|def apply|def verify)|import ' $helperPath
Get-Content -LiteralPath $helperPath -Encoding UTF8 | Select-Object -Last 270