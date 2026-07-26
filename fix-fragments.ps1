$repo = "C:\Users\SAMPC\.openclaw\workspace-website-architect\dogeking-us-clone"
Set-Location $repo
$files = @("cta-snippets.html","extracted-sections.html","nav-component-enhanced.html")
$nl = "`r`n"
foreach ($f in $files) {
    $c = Get-Content -Path $f -Raw
    # Strip leading head blocks (one or more)
    $c = $c -replace '^(<head>\s*<meta charset="UTF-8">\s*<meta name="viewport" content="width=device-width, initial-scale=1.0">\s*</head>\s*)+', ''
    # Add exactly one correct header
    $h = "<head>$nl  <meta charset=""UTF-8"">$nl  <meta name=""viewport"" content=""width=device-width, initial-scale=1.0"">$nl</head>$nl"
    $c = $h + $c
    Set-Content -Path $f -Value $c -NoNewline
    Write-Output "Fixed: $f"
}
