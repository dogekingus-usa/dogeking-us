$ErrorActionPreference = 'Continue'
$wt = 'C:\Users\SAMPC\dogeking-us-astro'
$old = 'C:\Users\SAMPC\.openclaw\agents\website-architect\agent\dogeking-us-clone'
$bodiesDir = "$wt\src\bodies"
New-Item -ItemType Directory -Path $bodiesDir -Force | Out-Null
$utf8 = New-Object System.Text.UTF8Encoding($false)

$slugs = Get-ChildItem "$wt\src\pages" -File -Filter *.astro | ForEach-Object { $_.BaseName } | Sort-Object
$noBody = @()
$meta = @{}

foreach ($s in $slugs) {
  $srcFile = "$old\$s.html"
  $body = ''
  $h1text = ''
  if (Test-Path $srcFile) {
    $c = [System.IO.File]::ReadAllText($srcFile)
    $m = [regex]::Match($c, '<article[^>]*>([\s\S]*?)</article>')
    if ($m.Success) {
      $body = $m.Groups[1].Value
    } else {
      $start = $c.IndexOf('</nav>')
      if ($start -lt 0) { $start = $c.IndexOf('<body') }
      $end = $c.IndexOf('<footer')
      if ($end -lt 0) { $end = $c.IndexOf('</body>') }
      if ($start -ge 0 -and $end -gt $start) {
        $body = $c.Substring($start + 5, $end - $start - 5)
      }
    }
    if ($body) {
      $h1m = [regex]::Match($body, '<h1[^>]*>[\s\S]*?</h1>')
      if ($h1m.Success) { $h1text = $h1m.Value; $body = $body.Remove($h1m.Index, $h1m.Length) }
      $body = $body.Trim()
    }
  }
  if (-not $body) { $noBody += $s }
  [System.IO.File]::WriteAllBytes("$bodiesDir\$s.html", $utf8.GetBytes($body))
  $t = ''; $d = ''
  if (Test-Path $srcFile) {
    $c2 = [System.IO.File]::ReadAllText($srcFile)
    $t = [regex]::Match($c2, '<title>(.*?)</title>').Groups[1].Value.Trim()
    $d = [regex]::Match($c2, '<meta name="description" content="(.*?)">').Groups[1].Value
  }
  $meta[$s] = @{ title = $t; desc = $d; h1 = $h1text }
}

Write-Host "total slugs: $($slugs.Count)"
Write-Host "no-body slugs: $($noBody.Count)"
$noBody | ForEach-Object { Write-Host "  NO-BODY: $_" }
$meta | ConvertTo-Json -Depth 3 | Out-File "$wt\src\bodies\meta.json" -Encoding utf8
Write-Host "meta.json written"
