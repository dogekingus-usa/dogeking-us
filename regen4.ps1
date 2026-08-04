$ErrorActionPreference = 'Stop'
$wt = 'C:\Users\SAMPC\dogeking-us-astro'
$bodiesDir = "$wt\src\bodies"
$utf8 = New-Object System.Text.UTF8Encoding($false)

# Load meta.json
$rawMeta = Get-Content "$bodiesDir\meta.json" -Raw | ConvertFrom-Json
$meta = @{}
$rawMeta.PSObject.Properties | ForEach-Object { $meta[$_.Name] = $_.Value }

# HTML-decode helper (converts &mdash; &ndash; &amp; &rsquo; etc. to real chars)
function HtmlDecode([string]$s) {
  if ([string]::IsNullOrEmpty($s)) { return '' }
  return [System.Net.WebUtility]::HtmlDecode($s)
}

# New page template WITH JSON-LD Article schema
$tpl = @'
---
import BaseLayout from '../layouts/BaseLayout.astro';
import CTA from '../components/CTA.astro';
import body from '../bodies/{SLUG}.html?raw';

const title = {TITLE_JSON};
const description = {DESC_JSON};
const canonical = 'https://dogeking.us/{SLUG}';
const jsonLd = {
  '@context': 'https://schema.org',
  '@type': 'Article',
  headline: title,
  description: description,
  url: canonical,
  mainEntityOfPage: { '@type': 'WebPage', '@id': canonical },
  publisher: { '@type': 'Organization', name: 'DogeKing.us' },
};
---

<BaseLayout title={title} description={description} canonical={canonical}>
  <script type="application/ld+json" set:html={JSON.stringify(jsonLd)} />
  <article class="mx-auto max-w-4xl px-4 py-8">
    <Fragment set:html={body} />
    <div class="mt-12 text-center">
      <CTA href="/crypto-guide" text="Explore More Guides" variant="secondary" />
    </div>
  </article>
</BaseLayout>
'@

$count = 0
$skipped = @()
foreach ($s in (Get-ChildItem "$wt\src\pages" -File -Filter *.astro | ForEach-Object { $_.BaseName } | Where-Object { $_ -ne 'index' })) {
  $b = "$bodiesDir\$s.html"
  if (-not (Test-Path $b)) { $skipped += $s; continue }
  $title = ''; $desc = ''
  if ($meta.ContainsKey($s)) { $title = HtmlDecode $meta[$s].title; $desc = HtmlDecode $meta[$s].desc }
  $out = $tpl.Replace('{SLUG}', $s).Replace('{TITLE_JSON}', ($title | ConvertTo-Json -Compress)).Replace('{DESC_JSON}', ($desc | ConvertTo-Json -Compress))
  [System.IO.File]::WriteAllBytes("$wt\src\pages\$s.astro", $utf8.GetBytes($out))
  $count++
}
Write-Host "regenerated pages with decoded titles: $count"
Write-Host "skipped (no body): $($skipped.Count)"
$skipped | ForEach-Object { Write-Host "  $_" }

# Also regenerate index + cta-snippets with decoded titles
foreach ($extra in @('index','cta-snippets')) {
  $s = $extra
  $b = "$bodiesDir\$s.html"
  if (Test-Path $b) {
    $title = ''; $desc = ''
    if ($meta.ContainsKey($s)) { $title = HtmlDecode $meta[$s].title; $desc = HtmlDecode $meta[$s].desc }
    if ($s -eq 'index') { $title = 'DogeKing — Meme Coin Trading Guides'; $desc = 'Your ultimate guide to meme coin trading on Solana. Guides, tips, and market analysis for DogeKing and Solana meme coins.' }
    if ($s -eq 'cta-snippets') { $title = 'CTA Snippets'; $desc = 'Reusable CTA snippets for DogeKing articles.' }
    $out = $tpl.Replace('{SLUG}', $s).Replace('{TITLE_JSON}', ($title | ConvertTo-Json -Compress)).Replace('{DESC_JSON}', ($desc | ConvertTo-Json -Compress))
    [System.IO.File]::WriteAllBytes("$wt\src\pages\$s.astro", $utf8.GetBytes($out))
    Write-Host "regenerated: $s.astro"
  }
}
Write-Host "done"
