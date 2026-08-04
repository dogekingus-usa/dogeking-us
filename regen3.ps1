$ErrorActionPreference = 'Continue'
$wt = 'C:\Users\SAMPC\dogeking-us-astro'
$old = 'C:\Users\SAMPC\.openclaw\agents\website-architect\agent\dogeking-us-clone'
$bodiesDir = "$wt\src\bodies"
$utf8 = New-Object System.Text.UTF8Encoding($false)

function Get-ContentRegion($html) {
  # article tag first, else between </nav> and <footer>, else whole body
  $m = [regex]::Match($html, '<article[^>]*>([\s\S]*?)</article>')
  if ($m.Success) { return $m.Groups[1].Value.Trim() }
  $start = $html.IndexOf('</nav>')
  if ($start -lt 0) { $start = $html.IndexOf('<body') }
  $end = $html.IndexOf('<footer')
  if ($end -lt 0) { $end = $html.IndexOf('</body>') }
  if ($start -ge 0 -and $end -gt $start) {
    $seg = $html.Substring($start + 5, $end - $start - 5)
    # strip first h1 (title rendered by layout)
    $h1m = [regex]::Match($seg, '<h1[^>]*>[\s\S]*?</h1>')
    if ($h1m.Success) { $seg = $seg.Remove($h1m.Index, $h1m.Length) }
    return $seg.Trim()
  }
  # last resort: strip head
  $b = [regex]::Match($html, '<body[^>]*>([\s\S]*)</body>')
  if ($b.Success) { return $b.Groups[1].Value.Trim() }
  return $html.Trim()
}

# 1. Fix cta-snippets body (snippet library page, no nav/footer)
$c = [System.IO.File]::ReadAllText("$old\cta-snippets.html")
$bodyCta = Get-ContentRegion $c
[System.IO.File]::WriteAllBytes("$bodiesDir\cta-snippets.html", $utf8.GetBytes($bodyCta))
Write-Host "cta-snippets body: $($bodyCta.Length) chars"

# 2. Fix how-to-stake-dogeking body
$h = [System.IO.File]::ReadAllText("$old\how-to-stake-dogeking.html")
$bodyH = Get-ContentRegion $h
[System.IO.File]::WriteAllBytes("$bodiesDir\how-to-stake-dogeking.html", $utf8.GetBytes($bodyH))
Write-Host "how-to-stake-dogeking body: $($bodyH.Length) chars"

# 3. Extract index (homepage) body from clone
$ix = [System.IO.File]::ReadAllText("$old\index.html")
$bodyIx = Get-ContentRegion $ix
[System.IO.File]::WriteAllBytes("$bodiesDir\index.html", $utf8.GetBytes($bodyIx))
Write-Host "index body: $($bodyIx.Length) chars"

# 4. Extract about body if not already
if (-not (Test-Path "$bodiesDir\about.html")) {
  $ab = [System.IO.File]::ReadAllText("$old\about.html")
  $bodyAb = Get-ContentRegion $ab
  [System.IO.File]::WriteAllBytes("$bodiesDir\about.html", $utf8.GetBytes($bodyAb))
  Write-Host "about body: $($bodyAb.Length) chars"
}

# 5. Regenerate index.astro + cta-snippets.astro with real content
function Write-Page($slug, $title, $desc) {
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
  $out = $tpl.Replace('{SLUG}', $slug).Replace('{TITLE_JSON}', ($title | ConvertTo-Json -Compress)).Replace('{DESC_JSON}', ($desc | ConvertTo-Json -Compress))
  [System.IO.File]::WriteAllBytes("$wt\src\pages\$slug.astro", $utf8.GetBytes($out))
  Write-Host "page written: $slug.astro"
}

$metaRaw = Get-Content "$bodiesDir\meta.json" -Raw | ConvertFrom-Json
$meta = @{}
$metaRaw.PSObject.Properties | ForEach-Object { $meta[$_.Name] = $_.Value }

Write-Page 'index' 'DogeKing — Meme Coin Trading Guides' 'Your ultimate guide to meme coin trading on Solana. Guides, tips, and market analysis for DogeKing and Solana meme coins.'
Write-Page 'cta-snippets' 'CTA Snippets' 'Reusable CTA snippets for DogeKing articles.'

# 6. Remove debug/junk files from public/ (never deploy)
$junk = @('curr-head.html','extracted-sections.html','fetched-live.html','live-html.html','nav-component-enhanced.html','orig-base.html','orig-index.html','preview-card.html','rebuild.html','dogeking-article-og-template.html')
foreach ($j in $junk) { $p = "$wt\public\$j"; if (Test-Path $p) { Remove-Item $p -Force; Write-Host "public junk removed: $j" } }

# 7. Remove public/*.html that collide with astro pages (astro generates them)
$astroSlugs = Get-ChildItem "$wt\src\pages" -File -Filter *.astro | ForEach-Object { $_.BaseName }
foreach ($f in Get-ChildItem "$wt\public" -File -Filter *.html) {
  if ($astroSlugs -contains $f.BaseName) { Remove-Item $f.FullName -Force; Write-Host "public collision removed: $($f.Name)" }
}

Write-Host "=== remaining public/ ==="
Get-ChildItem "$wt\public" -File | Select-Object -ExpandProperty Name
