$ErrorActionPreference = 'Stop'
$wt = 'C:\Users\SAMPC\dogeking-us-astro'
$old = 'C:\Users\SAMPC\.openclaw\agents\website-architect\agent\dogeking-us-clone'
$bodiesDir = "$wt\src\bodies"
$utf8 = New-Object System.Text.UTF8Encoding($false)

# 1. Drop the 5 fabricated pages that don't exist on live (404)
$drop = @('ai-crypto-agents-explained-beginners-guide-2026','catfi-rugpull-south-korea-prosecution-solana-meme-coin-scam-2026','dk-solana-meme-coin-sniping-guide-2026','solana-meme-coins-2026-dogeking-guide','track-solana-whale-wallets-copy-smart-money-meme-coin-profits-2026')
foreach ($s in $drop) {
  foreach ($p in @("$wt\src\pages\$s.astro", "$bodiesDir\$s.html")) { if (Test-Path $p) { Remove-Item $p -Force; Write-Host "dropped: $s" } }
}

# 2. Fix cta-snippets body (exists on live, container is different)
$ctaFile = "$old\cta-snippets.html"
if (Test-Path $ctaFile) {
  $c = [System.IO.File]::ReadAllText($ctaFile)
  $start = $c.IndexOf('<body')
  $end = $c.IndexOf('<footer')
  if ($end -lt 0) { $end = $c.IndexOf('</body>') }
  if ($start -ge 0 -and $end -gt $start) {
    $body = $c.Substring($start, $end - $start)
    $h1m = [regex]::Match($body, '<h1[^>]*>[\s\S]*?</h1>')
    if ($h1m.Success) { $body = $body.Remove($h1m.Index, $h1m.Length) }
    [System.IO.File]::WriteAllBytes("$bodiesDir\cta-snippets.html", $utf8.GetBytes($body.Trim()))
    Write-Host "cta-snippets body extracted: $($body.Trim().Length) chars"
  }
}

# 3. Load meta (version-safe: works on PS 5.1 and 7+)
$rawMeta = Get-Content "$bodiesDir\meta.json" -Raw | ConvertFrom-Json
$meta = @{}
$rawMeta.PSObject.Properties | ForEach-Object { $meta[$_.Name] = $_.Value }

# 4. Regenerate every article .astro with full body via set:html
$slugs = Get-ChildItem "$wt\src\pages" -File -Filter *.astro | ForEach-Object { $_.BaseName } | Where-Object { $_ -ne 'index' }
$tpl = @'
---
import BaseLayout from '../layouts/BaseLayout.astro';
import CTA from '../components/CTA.astro';
import body from '../bodies/{SLUG}.html?raw';

const title = {TITLE_JSON};
const description = {DESC_JSON};
const canonical = 'https://dogeking.us/{SLUG}';
---

<BaseLayout title={title} description={description} canonical={canonical}>
  <article class="mx-auto max-w-4xl px-4 py-8">
    <Fragment set:html={body} />
    <div class="mt-12 text-center">
      <CTA href="/crypto-guide" text="Explore More Guides" variant="secondary" />
    </div>
  </article>
</BaseLayout>
'@

$count = 0
foreach ($s in $slugs) {
  $b = "$bodiesDir\$s.html"
  if (-not (Test-Path $b)) { Write-Host "SKIP (no body): $s"; continue }
  $title = ''
  $desc = ''
  if ($meta.ContainsKey($s)) { $title = $meta[$s].title; $desc = $meta[$s].desc }
  $titleJson = ($title | ConvertTo-Json -Compress)
  $descJson = ($desc | ConvertTo-Json -Compress)
  $out = $tpl.Replace('{SLUG}', $s).Replace('{TITLE_JSON}', $titleJson).Replace('{DESC_JSON}', $descJson)
  [System.IO.File]::WriteAllBytes("$wt\src\pages\$s.astro", $utf8.GetBytes($out))
  $count++
}
Write-Host "regenerated pages: $count"
Write-Host "total astro pages now: $((Get-ChildItem "$wt\src\pages" -File -Filter *.astro | Measure-Object).Count)"
