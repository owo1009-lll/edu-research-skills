param([string]$InputDocx,[string]$OutputPdf)
$ErrorActionPreference = 'Stop'
$inputPath=(Resolve-Path -LiteralPath $InputDocx).Path
$outputPath=[System.IO.Path]::GetFullPath($OutputPdf)
if (Test-Path -LiteralPath $outputPath) { throw 'Output already exists.' }
$word=$null
$document=$null
try {
 $word=New-Object -ComObject Word.Application
 $word.Visible=$false
 $word.DisplayAlerts=0
 $document=$word.Documents.Open($inputPath,$false,$true)
 $document.ExportAsFixedFormat($outputPath,17,$false,0,0,1,1,7)
 Write-Output ('Rendered marked-up PDF: '+$outputPath)
} finally {
 if ($null -ne $document) { $document.Close(0); [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($document) }
 if ($null -ne $word) { $word.Quit(); [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($word) }
}
