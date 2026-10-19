$ErrorActionPreference = 'Stop'
$word = [Runtime.InteropServices.Marshal]::GetActiveObject('Word.Application')
$document = $word.Documents.Item('mixed_feedback_审稿标注版.docx')
$expected = (Resolve-Path -LiteralPath '.\edu_output\review\mixed-review\mixed_feedback_审稿标注版.docx').Path
if ($document.FullName -ne $expected) { throw 'Unexpected active manuscript path.' }
$outputPath = Join-Path (Get-Location).Path 'edu_output\review\mixed-review\annotated-body-retry-preview.pdf'
$document.ActiveWindow.View.ShowRevisionsAndComments = $false
$document.ExportAsFixedFormat($outputPath, 17)
Write-Output ('Rendered PDF: ' + $outputPath)
[void][Runtime.InteropServices.Marshal]::ReleaseComObject($document)
[void][Runtime.InteropServices.Marshal]::ReleaseComObject($word)
