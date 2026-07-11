<#
.SYNOPSIS
    Bulk add nav + CTAs to DogeKing article pages per DK-NAV-CTA architecture.
    Run after website-architect verifies hub page changes.
.DESCRIPTION
    Phase 1: Add nav CTA button to articles that already have a nav
    Phase 2: Add nav to articles without any nav element
    Phase 3: Add inline CTAs after first H2 on article pages
    Phase 4: Add end-of-article CTA card before </body>
.NOTES
    Author: conversion-revenue-specialist (Cove)
    Arch: shared/architecture/DK-NAV-CTA.md
    Gumroad: https://dogeking0.gumroad.com/l/dogeking-crypto-bundle
#>

param(
    [ValidateSet("all","nav-only","cta-only","verify")]
    [string]$Mode = "all"
)

$repoRoot = "C:\Users\SAMPC\repos\dogeking-us"
$gumroadUrl = "https://dogeking0.gumroad.com/l/dogeking-crypto-bundle"
$navCtaHtml = '<a href="' + $gumroadUrl + '" class="nav-cta">Join the Pack 🐕</a>'

# Exclude non-article pages
$excludePages = @(
    "index.html", "products.html", "all-articles.html", "about.html", 
    "contact.html", "store.html", "404.html", "privacy.html",
    "articles-data.js", "generation_results.json"
)

# ============================================================
# PHASE 1: Add nav CTA to articles that already have a nav
# ============================================================
function Add-CtaToExistingNav {
    Write-Host "=== PHASE 1: Adding CTA to existing navs ===" -ForegroundColor Cyan
    
    $files = Get-ChildItem "$repoRoot" -Filter "*.html" | Where-Object { $_.Name -notin $excludePages }
    $modified = 0
    $skipped = 0
    
    foreach ($file in $files) {
        $content = Get-Content $file.FullName -Raw
        
        # Skip if already has nav-cta
        if ($content -match 'nav-cta|Join the Pack') {
            $skipped++
            continue
        }
        
        # Find nav-links div with closing </div>
        if ($content -match '<div class="nav-links"[^>]*>') {
            $navStart = $matches[0]
            $navSection = $content.Substring($content.IndexOf($navStart))
            
            # Find the closing </div> of nav-links
            if ($navSection -match '(.*?)</div>') {
                $navLinksHtml = $matches[1]
                $closingDiv = $matches[0]
                $original = $navStart + $navLinksHtml + '</div>'
                
                # Check if it already ends with an anchor
                if ($navLinksHtml -match '<a\s[^>]*>[^<]*</a>\s*$') {
                    # Add CTA before the closing </div>
                    $newNavContent = $navStart + $navLinksHtml + $navCtaHtml + '</div>'
                    $content = $content.Replace($original, $newNavContent)
                    Set-Content -Path $file.FullName -Value $content -NoNewline
                    $modified++
                    Write-Host "  [+] $($file.Name)"
                }
            }
        }
    }
    
    Write-Host "Phase 1 complete: $modified modified, $skipped already had CTA" -ForegroundColor Green
}

# ============================================================
# PHASE 2: Add basic nav to articles without any nav
# ============================================================
function Add-NavToArticles {
    Write-Host "=== PHASE 2: Adding nav to articles without one ===" -ForegroundColor Cyan
    
    $files = Get-ChildItem "$repoRoot" -Filter "*.html" | Where-Object { $_.Name -notin $excludePages }
    $modified = 0
    $skipped = 0
    
    $navHtml = @'
<nav>
<div class="container" style="display:flex;justify-content:space-between;align-items:center;padding:12px 20px;max-width:1200px;margin:0 auto;">
<a href="/" style="font-family:'Playfair Display',serif;font-size:1.3rem;font-weight:700;color:#f5f5ff;text-decoration:none;">👑 DogeKing</a>
<div class="nav-links" style="display:flex;gap:4px;align-items:center;">
<a href="/" style="color:#8080a0;padding:6px 12px;border-radius:6px;font-size:0.9rem;text-decoration:none;">Home</a>
<a href="/all-articles.html" style="color:#8080a0;padding:6px 12px;border-radius:6px;font-size:0.9rem;text-decoration:none;">Articles</a>
<a href="/products.html" style="color:#8080a0;padding:6px 12px;border-radius:6px;font-size:0.9rem;text-decoration:none;">Products</a>
<a href="/about.html" style="color:#8080a0;padding:6px 12px;border-radius:6px;font-size:0.9rem;text-decoration:none;">About</a>
<a href="' + $gumroadUrl + '" style="display:inline-flex;padding:8px 20px;border-radius:8px;background:#F7931A;color:#fff!important;font-weight:600;font-size:0.875rem;text-decoration:none;min-height:44px;align-items:center;justify-content:center;">Join the Pack 🐕</a>
</div>
</div>
</nav>

'@
    
    foreach ($file in $files) {
        $content = Get-Content $file.FullName -Raw
        
        # Skip if already has any nav
        if ($content -match '<nav[^>]*>') {
            $skipped++
            continue
        }
        
        # Insert nav after <body> tag
        if ($content -match '(.*?<body[^>]*>)(.*)') {
            $content = $matches[1] + "`n" + $navHtml + $matches[2]
            Set-Content -Path $file.FullName -Value $content -NoNewline
            $modified++
            Write-Host "  [+] $($file.Name)"
        }
    }
    
    Write-Host "Phase 2 complete: $modified navs added, $skipped already had nav" -ForegroundColor Green
}

# ============================================================
# PHASE 3: Add inline CTA after first H2
# ============================================================
function Add-InlineCtaAfterH2 {
    Write-Host "=== PHASE 3: Adding inline CTA after first H2 ===" -ForegroundColor Cyan
    
    $files = Get-ChildItem "$repoRoot" -Filter "*.html" | Where-Object { $_.Name -notin $excludePages }
    $modified = 0
    $skipped = 0
    
    $inlineCta = @'

<div class="info-box" style="background:#f0f8ff;border-left:4px solid #F7931A;padding:15px 20px;margin:25px 0;border-radius:0 8px 8px 0;">
<strong>🎯 Ready to stake SOL?</strong> The complete 15-page Solana Staking Guide covers wallet setup, staking pools, and passive income math. <a href="' + $gumroadUrl + '" style="color:#F7931A;font-weight:600;text-decoration:underline;">Get the guide →</a>
</div>

'@
    
    foreach ($file in $files) {
        $content = Get-Content $file.FullName -Raw
        
        # Skip if H2 CTA already added
        if ($content -match 'Ready to stake SOL|solana-staking-guide-cta') {
            $skipped++
            continue
        }
        
        # Find first regular H2 (not in TOC, not in table of contents)
        if ($content -match '<h2>(?![^<]*Table of Contents)([^<]*)</h2>') {
            $h2End = $content.IndexOf($matches[0]) + $matches[0].Length
            $content = $content.Substring(0, $h2End) + $inlineCta + $content.Substring($h2End)
            Set-Content -Path $file.FullName -Value $content -NoNewline
            $modified++
        }
    }
    
    Write-Host "Phase 3 complete: $modified inline CTAs added, $skipped already had" -ForegroundColor Green
}

# ============================================================
# PHASE 4: Add end-of-article CTA card
# ============================================================
function Add-EndOfArticleCta {
    Write-Host "=== PHASE 4: Adding end-of-article CTA card ===" -ForegroundColor Cyan
    
    $files = Get-ChildItem "$repoRoot" -Filter "*.html" | Where-Object { $_.Name -notin $excludePages }
    $modified = 0
    $skipped = 0
    
    $endCta = @'

<div class="cta-box" style="background:linear-gradient(135deg,#1a1a2e,#16213e);color:white;padding:35px;border-radius:12px;margin:45px 0;text-align:center;">
<h3 style="color:#F7931A;margin-top:0;font-size:1.5em;">📘 Solana Staking Guide</h3>
<p style="font-size:1em;opacity:0.9;">Complete 15-page guide to staking SOL for passive income. Wallet setup, staking pools, and real yield calculations included.</p>
<p style="font-size:0.9em;opacity:0.7;">Instant digital delivery · Lifetime access</p>
<a href="' + $gumroadUrl + '" style="display:inline-block;background:#F7931A;color:white;padding:14px 35px;text-decoration:none;border-radius:8px;font-weight:600;margin-top:15px;font-size:1.1em;transition:all 0.2s;">Buy Now →</a>
</div>

'@
    
    foreach ($file in $files) {
        $content = Get-Content $file.FullName -Raw
        
        # Skip if end CTA already added
        if ($content -match 'end-of-article-cta|solana-staking-guide-end') {
            $skipped++
            continue
        }
        
        # Insert before </body>
        if ($content -match '(.*)(</body>)') {
            $content = $matches[1] + $endCta + $matches[2]
            Set-Content -Path $file.FullName -Value $content -NoNewline
            $modified++
        }
    }
    
    Write-Host "Phase 4 complete: $modified end CTAs added, $skipped already had" -ForegroundColor Green
}

# ============================================================
# VERIFY: Check what was done
# ============================================================
function Verify-Changes {
    Write-Host "=== VERIFICATION ===" -ForegroundColor Cyan
    
    $total = (Get-ChildItem "$repoRoot" -Filter "*.html" | Where-Object { $_.Name -notin $excludePages }).Count
    $withNav = 0
    $withCta = 0
    $withInlineCta = 0
    $withEndCta = 0
    
    Get-ChildItem "$repoRoot" -Filter "*.html" | Where-Object { $_.Name -notin $excludePages } | ForEach-Object {
        $content = Get-Content $_.FullName -Raw
        if ($content -match '<nav') { $withNav++ }
        if ($content -match 'nav-cta|Join the Pack') { $withCta++ }
        if ($content -match 'Ready to stake SOL') { $withInlineCta++ }
        if ($content -match 'end-of-article-cta|solana-staking-guide-end') { $withEndCta++ }
    }
    
    Write-Host "Total article HTML files: $total"
    Write-Host "With nav: $withNav"
    Write-Host "With nav CTA: $withCta"
    Write-Host "With inline CTA: $withInlineCta"
    Write-Host "With end CTA: $withEndCta"
}

# ============================================================
# MAIN
# ============================================================
switch ($Mode) {
    "all" {
        Add-CtaToExistingNav
        Add-NavToArticles
        # Skip CTA injection - need to test on a subset first
        Write-Host "`nSkipping Phase 3-4 (inline/end CTAs). Run with -Mode cta-only after testing." -ForegroundColor Yellow
    }
    "nav-only" {
        Add-CtaToExistingNav
        Add-NavToArticles
    }
    "cta-only" {
        Add-InlineCtaAfterH2
        Add-EndOfArticleCta
    }
    "verify" {
        Verify-Changes
    }
}

Write-Host "`nDone. Run 'Verify-Changes' to check results." -ForegroundColor Green
