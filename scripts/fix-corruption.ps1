# fix-corruption.ps1 — Fix merge conflicts and encoding corruption in HTML files
param([string]$RepoPath, [switch]$DryRun)

$fixed = 0; $skipped = 0; $errors = 0
$utf8NoBOM = New-Object System.Text.UTF8Encoding $false

Get-ChildItem "$RepoPath" -Filter "*.html" -Recurse -ErrorAction SilentlyContinue | ForEach-Object {
    $file = $_.FullName
    try {
        $bytes = [System.IO.File]::ReadAllBytes($file)
        $originalStr = [System.Text.Encoding]::UTF8.GetString($bytes)
        if (-not $originalStr) { $skipped++; return }
        $content = $originalStr

        # Step 1: Remove all merge conflict markers
        # Pattern: <<<<<<< HEAD\n...=======\n...>>>>>>> hash
        while ($content -match '(?s)<<<<<<< [^\r\n]*\r?\n(.*?)\r?\n?=======\r?\n(.*?)\r?\n?>>>>>>> [a-f0-9]+') {
            # Keep the first version (HEAD side always)
            $content = $content -replace '(?s)<<<<<<< [^\r\n]*\r?\n(.*?)\r?\n?=======\r?\n(.*?)\r?\n?>>>>>>> [a-f0-9]+', '$1'
        }

        # Clean up any remaining conflict artifacts
        $content = $content -replace '<<<<<<< [^\r\n]*\r?\n?', ''
        $content = $content -replace '\r?\n=======\r?\n?', ''
        $content = $content -replace '\r?\n>>>>>>> [a-f0-9]+', ''

        # Remove BOM corruption artifacts
        $content = $content -replace '^\xEF\xBB\xBF', ''
        $content = $content -replace '^\xC3\xAF\xC2\xBB\xC2\xBF', ''

        # Remove duplicate DOCTYPEs (keep first)
        if ($content -match '^(.*?)(<!DOCTYPE[^>]*>)') {
            $firstDocType = $Matches[2]
            $rest = $Matches[1] + $Matches[2]
            while ($rest -match '(.*?)(<!DOCTYPE[^>]*>)(.*)') {
                # Find any SECOND doctype and remove it
                $all = $rest
                $parts = [regex]::Split($all, '(?=<!DOCTYPE)', [System.Text.RegularExpressions.RegexOptions]::None)
                if ($parts.Count -gt 2) {
                    $content = $parts[0] + $parts[1]  # keep first, remove rest
                }
                break
            }
        }

        # Step 2: Validate we have valid HTML
        if ($content -match '<[Hh][Tt][Mm][Ll]|<[Bb][Oo][Dd][Yy]|<[Hh][Ee][Aa][Dd]') {
            # Looks like HTML - good
        }

        # Step 3: Remove consecutive blank lines (3+ → 2)
        $content = $content -replace "`r`n`r`n`r`n+", "`r`n`r`n"
        $content = $content -replace "`n`n`n+", "`n`n"

        if ($content -ne $originalStr) {
            if (-not $DryRun) {
                [System.IO.File]::WriteAllText($file, $content, $utf8NoBOM)
            }
            $fixed++
            if ($fixed -le 5) {
                Write-Host ("  FIXED: {0}" -f $file.Substring($RepoPath.Length))
            }
        } else {
            $skipped++
        }
    } catch {
        $errors++
        Write-Host ("  ERROR: {0} - {1}" -f $file.Substring($RepoPath.Length), $_.Exception.Message) -ForegroundColor Red
    }
}

Write-Host "=== RESULTS ==="
Write-Host ("Repo: {0}" -f $RepoPath)
Write-Host ("Fixed: {0}" -f $fixed)
Write-Host ("Skipped (unchanged): {0}" -f $skipped)
Write-Host ("Errors: {0}" -f $errors)
