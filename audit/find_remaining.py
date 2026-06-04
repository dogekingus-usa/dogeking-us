#!/usr/bin/env python3
"""Find remaining issues"""
import os, re

SITE_ROOT = r"C:\content-sites\dogeking.us"
canonical = 'https://dogeking0.gumroad.com/l/dogeking-crypto-bundle'

all_html = set()
for root, dirs, fnames in os.walk(SITE_ROOT):
    if '.wrangler' in root: continue
    for f in fnames:
        if f.endswith('.html'):
            rel = os.path.relpath(os.path.join(root, f), SITE_ROOT).replace('\\', '/')
            all_html.add(rel)

print("=== REMAINING NON-CANONICAL GUMROAD ===")
for root, dirs, fnames in os.walk(SITE_ROOT):
    if '.wrangler' in root: continue
    for f in fnames:
        if not f.endswith('.html'): continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf-8', errors='replace') as fh:
            content = fh.read()
        rel = os.path.relpath(fp, SITE_ROOT).replace('\\', '/')
        for m in re.finditer(r'href=["\'](https?://[^"\']*gumroad[^"\']*)["\']', content, re.IGNORECASE):
            url = m.group(1)
            if url != canonical and '/affiliates' not in url and 'gumroad.com/library' not in url and 'gumroad.com/l/dogeking-crypto-bundle' not in url:
                print("  %s -> %s" % (rel, url[:120]))

print("\n=== BROKEN INTERNAL LINKS ===")
for root, dirs, fnames in os.walk(SITE_ROOT):
    if '.wrangler' in root: continue
    for f in fnames:
        if not f.endswith('.html'): continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf-8', errors='replace') as fh:
            content = fh.read()
        rel = os.path.relpath(fp, SITE_ROOT).replace('\\', '/')
        for m in re.finditer(r'href=["\'](/(?:articles/|blog/|short/)[^"\']*\.html)["\']', content, re.IGNORECASE):
            target = m.group(1).lstrip('/')
            if target not in all_html:
                print("  %s -> /%s" % (rel, target))
