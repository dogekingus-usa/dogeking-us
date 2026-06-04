#!/usr/bin/env python3
"""Verify fixes were applied correctly"""
import os, re

SITE_ROOT = r"C:\content-sites\dogeking.us"

# Check Gumroad links
bad = 0
total = 0
canonical = 'https://dogeking0.gumroad.com/l/dogeking-crypto-bundle'

# Check for broken internal links
broken_internal = 0
all_html = set()
for root, dirs, fnames in os.walk(SITE_ROOT):
    if '.wrangler' in root: continue
    for f in fnames:
        if f.endswith('.html'):
            rel = os.path.relpath(os.path.join(root, f), SITE_ROOT).replace('\\', '/')
            all_html.add(rel)

for root, dirs, fnames in os.walk(SITE_ROOT):
    if '.wrangler' in root: continue
    for f in fnames:
        if not f.endswith('.html'): continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf-8', errors='replace') as fh:
            content = fh.read()
        
        # Gumroad check
        for m in re.finditer(r'href=["\'](https?://[^"\']*gumroad[^"\']*)["\']', content, re.IGNORECASE):
            total += 1
            url = m.group(1)
            if url != canonical and '/affiliates' not in url and 'gumroad.com/library' not in url:
                bad += 1
        
        # Internal link check
        for m in re.finditer(r'href=["\'](/(?:articles/|blog/|short/)[^"\']*\.html)["\']', content, re.IGNORECASE):
            target = m.group(1).lstrip('/')
            if target not in all_html and target != '':
                broken_internal += 1

print("=== VERIFICATION ===")
print("Total Gumroad links:", total)
print("Non-canonical Gumroad links:", bad)
print("Broken internal links:", broken_internal)

# Check OG tags on a sample
sample_files = ['about.html', 'contact.html', 'ai-meme-coins-crypto-trend-2026.html', 'index.html']
print("\n=== OG TAG CHECK ===")
for f in sample_files:
    fp = os.path.join(SITE_ROOT, f)
    if os.path.exists(fp):
        with open(fp, 'r', encoding='utf-8') as fh:
            c = fh.read()
        has_og_title = bool(re.search(r'og:title', c))
        has_og_desc = bool(re.search(r'og:description', c))
        has_og_image = bool(re.search(r'og:image', c))
        has_twitter = bool(re.search(r'twitter:card', c))
        has_canonical = bool(re.search(r'rel=["\']canonical["\']', c))
        print("  %s: og:title=%s og:desc=%s og:image=%s twitter=%s canonical=%s" % (
            f, has_og_title, has_og_desc, has_og_image, has_twitter, has_canonical))

print("\nDone!")
