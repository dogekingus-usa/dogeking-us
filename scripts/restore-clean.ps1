# restore-clean.ps1 — Restore HTML files from clean commit c1c4b6b (before corruption)
param([string]$RepoPath, [switch]$DryRun)

$cleanCommit = "c1c4b6b"
$utf8NoBOM = New-Object System.Text.UTF8Encoding $false
$restored = 0; $skipped = 0; $errors = 0

# Get list of HTML files in the clean commit
$cleanFiles = git -C $RepoPath ls-tree -r --name-only $cleanCommit 2>&1 | Where-Object { $_ -match '\.html$' }

foreach ($relPath in $cleanFiles) {
    $fullPath = Join-Path $RepoPath $relPath
    try {
        # Get clean content from git
        $cleanContent = git -C $RepoPath show "$cleanCommit`:$relPath" --no-color 2>&1
        if (-not $cleanContent -or $cleanContent -match "^fatal:" ) { $skipped++; continue }

        # Get current content
        if (Test-Path $fullPath) {
            $currentContent = [System.IO.File]::ReadAllBytes($fullPath)
            $currentStr = [System.Text.Encoding]::UTF8.GetString($currentContent)

            # Skip if already clean (no merge conflicts, no mojibake)
            if ($currentStr -notmatch "<<<<<<<" -and $currentStr -notmatch "[Ã-ÿ]{2,}" -and $currentStr -notmatch "\uFFFD") {
                $skipped++; continue
            }
        }

        # Write clean version
        if (-not $DryRun) {
            [System.IO.File]::WriteAllText($fullPath, $cleanContent, $utf8NoBOM)
        }
        $restored++
        if ($restored -le 10) { Write-Host ("  RESTORED: {0}" -f $relPath) }
    } catch {
        $errors++
        Write-Host ("  ERROR: {0} - {1}" -f $relPath, $_.Exception.Message) -ForegroundColor Red
    }
}

Write-Host "=== RESULTS ==="
Write-Host ("Repo: {0}" -f $RepoPath)
Write-Host ("Restored from clean commit: {0}" -f $restored)
Write-Host ("Skipped (already clean): {0}" -f $skipped)
Write-Host ("Errors: {0}" -f $errors)
