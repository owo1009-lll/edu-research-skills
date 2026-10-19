$runDir = '<experiment>\runs\qual'
New-Item -ItemType Directory -Path $runDir -Force | Out-Null
@'
# Initial plan (version 1)

1. Read the assigned request, frozen edu-review instructions, and only the supporting resources needed for this review.
2. Inspect the supplied manuscript and extract its text with recorded commands, preserving the original PDF.
3. Carry out the review workflow required by the frozen skill, grounded only in the supplied excerpt.
4. Produce the user-facing review deliverables, run available structural and visual opening/rendering checks, and preserve the evidence and limitations.
5. Record source/resource SHA-256 hashes, executed commands and outcomes, outputs, and the exact final response in the internal experimental receipt.
'@ | Set-Content -LiteralPath (Join-Path $runDir 'plan-v1.md') -Encoding utf8
Get-Content -LiteralPath '<experiment>\snapshot\skills\edu-review\SKILL.md' -Raw
Get-Content -LiteralPath '<experiment>\inputs-final\request.md' -Raw
Get-FileHash -Algorithm SHA256 -LiteralPath '<experiment>\snapshot\skills\edu-review\SKILL.md','<experiment>\inputs-final\request.md','<experiment>\inputs-final\qual_silence.pdf' | ConvertTo-Json