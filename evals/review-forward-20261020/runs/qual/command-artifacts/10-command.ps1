$runDir = '<experiment>\runs\qual'
$reviewDir = Join-Path $runDir 'edu_output\review\submission-review'
python -X utf8 (Join-Path $runDir 'executed-helpers\annotate_manuscript-frozen.py') apply '<experiment>\inputs-final\qual_silence.pdf' --plan (Join-Path $reviewDir 'annotations-v2.json') --output (Join-Path $reviewDir 'qual_silence_审稿标注版.pdf') | Tee-Object -FilePath (Join-Path $reviewDir 'apply-output.txt')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -X utf8 (Join-Path $runDir 'executed-helpers\annotate_manuscript-frozen.py') verify '<experiment>\inputs-final\qual_silence.pdf' (Join-Path $reviewDir 'qual_silence_审稿标注版.pdf') --plan (Join-Path $reviewDir 'annotations-v2.json') | Tee-Object -FilePath (Join-Path $reviewDir 'verify-output.txt')
exit $LASTEXITCODE