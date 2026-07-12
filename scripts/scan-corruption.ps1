param([string]$RepoPath)

$corrupted = 0
$total = 0
$samples = @()

Get-ChildItem $RepoPath -Filter "*.html" -Recurse -ErrorAction SilentlyContinue | ForEach-Object {
    $total++
    try {
        $content = Get-Content $_.FullName -Raw -Encoding UTF8 -ErrorAction Stop
        # Check for known mojibake patterns: Ã character sequences indicate double-encoding
        if ($content -match "[Ã-ÿ]{2,}") {
            $corrupted++
            if ($samples.Count -lt 5) { $samples += $_.FullName.Replace($RepoPath, "") }
        }
    } catch {
        # skip binary/non-UTF8 files
    }
}

Write-Host "=== SCAN RESULT ==="
Write-Host "Repo: $RepoPath"
Write-Host "Total HTML files: $total"
Write-Host "Corrupted: $corrupted"
Write-Host ""
Write-Host "Sample corrupted files:"
$samples | ForEach-Object { Write-Host "  $_" }
