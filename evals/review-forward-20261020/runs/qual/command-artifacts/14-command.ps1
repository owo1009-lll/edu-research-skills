$reviewDir = '<experiment>\runs\qual\edu_output\review\submission-review'
try {
    $readerProcess = Start-Process -FilePath (Join-Path $reviewDir 'qual_silence_审稿标注版.pdf') -WindowStyle Hidden -PassThru -ErrorAction Stop
    $readerResult = [ordered]@{ attempted = $true; launch_succeeded = $true; process_id = $readerProcess.Id; window_style = 'Hidden'; interactive_popup_inspection = 'Not performed; graphical interaction tools are unavailable in this run.' }
} catch {
    $readerResult = [ordered]@{ attempted = $true; launch_succeeded = $false; error = $_.Exception.Message; interactive_popup_inspection = 'Unavailable; PyMuPDF opening and rendered-page visual checks were performed separately.' }
}
$readerResult | ConvertTo-Json | Tee-Object -FilePath (Join-Path $reviewDir 'reader-launch.json')