#!/usr/bin/env python3
"""Fix remaining issues: Gumroad short links, broken internal links, stale files"""
import os, re

SITE_ROOT = r"C:\content-sites\dogeking.us"
CANONICAL = 'https://dogeking0.gumroad.com/l/dogeking-crypto-bundle'

# Additional Gumroad replacements for short links still remaining
REPLACEMENTS = {
    'https://dogeking0.gumroad.com/l/ptfzf': CANONICAL,
    'https://dogeking0.gumroad.com/l/meme-coin-checklist': CANONICAL,
    'https://dogeking0.gumroad.com/l/crypto-secrets': CANONICAL,
    'https://dogeking0.gumroad.com/l/resume-kit': CANONICAL,
    'https://dogeking0.gumroad.com/l/crypto-starter-guide': CANONICAL,
    'https://dogeking0.gumroad.com/l/dogeking-bundle': CANONICAL,
    'https://dogeking0.gumroad.com/l/money-workbook': CANONICAL,
    'https://dogeking0.gumroad.com/l/crypto-portfolio-tracker': CANONICAL,
    'https://dogeking0.gumroad.com/l/life-os-system-23': CANONICAL,
    'https://dogeking0.gumroad.com/l/meme-coin-research-checklist': CANONICAL,
    # Fix plain gumroad root links
    'https://dogeking0.gumroad.com"': CANONICAL + '"',
    "https://dogeking0.gumroad.com'": CANONICAL + "'",
}

# Broken wave6/wave7 links - redirect by removing the wave prefix
BROKEN_LINK_FIXES = {
    '/articles/wave7/solana-dex-trading-guide-jupiter-exchange-2026.html': '/articles/solana-dex-trading-guide-jupiter-exchange-2026.html',
    '/articles/wave6/complete-solana-wallet-guide-meme-coins-2026.html': '/articles/complete-solana-wallet-guide-meme-coins-2026.html',
    '/articles/wave6/read-meme-coin-whitepaper-red-flags-green-flags-2026.html': '/articles/read-meme-coin-whitepaper-red-flags-green-flags-2026.html',
}

count = 0

for root, dirs, fnames in os.walk(SITE_ROOT):
    if '.wrangler' in root: continue
    for f in fnames:
        if not f.endswith('.html'): continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf-8', errors='replace') as fh:
            content = fh.read()
        
        orig = content
        
        # Fix remaining Gumroad links
        for old, new in REPLACEMENTS.items():
            if old in content:
                content = content.replace(old, new)
        
        # Fix broken internal links
        for old, new in BROKEN_LINK_FIXES.items():
            if old in content:
                content = content.replace(old, new)
        
        if content != orig:
            with open(fp, 'w', encoding='utf-8') as fh:
                fh.write(content)
            rel = os.path.relpath(fp, SITE_ROOT).replace('\\', '/')
            print("  Fixed: %s" % rel)
            count += 1

# Now fix _redirects to add redirects for wave6 and wave7
redirects_path = os.path.join(SITE_ROOT, '_redirects')
with open(redirects_path, 'r', encoding='utf-8') as f:
    redirects_content = f.read()

# Add wave redirects if not present
wave_redirects = """\n
# Wave article directories
/articles/wave6/* /articles/:splat 301
/articles/wave7/* /articles/:splat 301"""

if '/articles/wave6/' not in redirects_content:
    redirects_content += wave_redirects
    with open(redirects_path, 'w', encoding='utf-8') as f:
        f.write(redirects_content)
    print("  Added wave redirects to _redirects")

print("\nFixed %d files" % count)
print("Done!")
