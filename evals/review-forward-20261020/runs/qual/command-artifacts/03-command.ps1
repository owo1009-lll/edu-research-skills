$runDir = '<experiment>\runs\qual'
$reviewDir = Join-Path $runDir 'edu_output\review\submission-review'
New-Item -ItemType Directory -Path $reviewDir -Force | Out-Null
@'
# Plan version 2

The frozen skill specifies one annotated copy of the original PDF as the user deliverable. The review will use English native PDF highlight comments, with author AI 模拟审稿. Red marks require a verified error or contradiction; blue marks identify information that needs verification; yellow marks identify argument or expression improvements. No separate review report or rewritten manuscript will be delivered.

1. Build a line-level PDF inventory with the frozen annotation helper and read the full excerpt.
2. Review qualitative claims against the draft's own scenes, quotations, methods, case differences, and limitations, without external research or unsupported assumptions about missing materials.
3. Preserve a versioned internal annotation plan, generate the annotated PDF, and run the helper's verification.
4. Open and render the output with available local PDF tools; inspect each page and comment content. Report any limit on interactive reader checks separately from structural or rendered-page checks.
5. Preserve helper versions, outputs, hashes, commands, and final response as internal run records.
'@ | Set-Content -LiteralPath (Join-Path $runDir 'plan-v2.md') -Encoding utf8
Get-Content -LiteralPath '<experiment>\snapshot\skills\edu-review\requirements.txt' -Encoding UTF8 -Raw
Get-Content -LiteralPath '<experiment>\snapshot\skills\edu-review\scripts\annotate_manuscript.py' -Encoding UTF8 -TotalCount 100
Get-FileHash -Algorithm SHA256 -LiteralPath '<experiment>\snapshot\skills\edu-review\requirements.txt','<experiment>\snapshot\skills\edu-review\scripts\annotate_manuscript.py' | ConvertTo-Json
python -X utf8 '<experiment>\snapshot\skills\edu-review\scripts\annotate_manuscript.py' inventory '<experiment>\inputs-final\qual_silence.pdf' --output (Join-Path $reviewDir 'anchors.json')