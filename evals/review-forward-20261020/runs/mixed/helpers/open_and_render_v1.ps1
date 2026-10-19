param([string]$InputDocx,[string]$OutputDir)
$ErrorActionPreference = 'Stop'
$inputPath = (Resolve-Path -LiteralPath $InputDocx).Path
$out = (Resolve-Path -LiteralPath $OutputDir).Path
$word = $null
$document = $null
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $document = $word.Documents.Open($inputPath, $false, $true)
    $comments = @()
    foreach ($comment in $document.Comments) {
        $comments += [pscustomobject]@{Index=$comment.Index;Author=$comment.Author;Scope=$comment.Scope.Text;Text=$comment.Range.Text;Start=$comment.Scope.Start;End=$comment.Scope.End;Page=$comment.Scope.Information(3)}
    }
    $report = [pscustomobject]@{Application=$word.Name;Version=$word.Version;ReadOnly=$document.ReadOnly;CommentCount=$document.Comments.Count;RevisionCount=$document.Revisions.Count;Tables=$document.Tables.Count;InlineShapes=$document.InlineShapes.Count;Comments=$comments}
    $report | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $out 'word-opening-check.json') -Encoding UTF8
    $document.ExportAsFixedFormat((Join-Path $out 'annotated-body-preview.pdf'),17)
    $document.ExportAsFixedFormat((Join-Path $out 'annotated-markup-preview.pdf'),17,$false,0,0,1,1,7)
    $report | ConvertTo-Json -Depth 6
} finally {
    if ($null -ne $document) { $document.Close(0); [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($document) }
    if ($null -ne $word) { $word.Quit(); [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($word) }
}
