#!/usr/bin/env python3
"""Refined og:image scan - checks existence of every referenced image path.
Read-only. Distinguishes og:image from og:image:width/height.
"""
import os
import re
import collections

root = r'C:\content-sites\dogeking.us'
BASE = 'https://dogeking.us/'

def exists_rel(path):
    # path like 'og-images/foo.png' or 'assets/images/foo.jpg'
    p = os.path.join(root, path.replace('/', os.sep))
    return os.path.exists(p)

missing = []
by_target = collections.Counter()
ok_hist = collections.Counter()
og_image_refs = 0
files_with = 0

for dp, dn, fn in os.walk(root):
    if '.git' in dp:
        continue
    for f in fn:
        if not f.endswith('.html'):
            continue
        p = os.path.join(dp, f)
        with open(p, encoding='utf-8', errors='replace') as fh:
            t = fh.read()
        # only property="og:image" or name="twitter:image" (exact), skip width/height
        refs = re.findall(r'<meta[^>]+(?:property=["\']og:image["\']|name=["\']twitter:image["\'])[^>]*content=["\']([^"\']+)["\']', t)
        if refs:
            files_with += 1
        for r in refs:
            og_image_refs += 1
            u = r.strip()
            if u.startswith(BASE):
                rel = u[len(BASE):]
            elif u.startswith('/'):
                rel = u[1:]
            elif u.startswith('http'):
                missing.append((p, r, 'EXTERNAL'))
                continue
            else:
                rel = u
            rel = rel.split('#')[0].split('?')[0]
            by_target[rel] += 1
            if not exists_rel(rel):
                missing.append((p, r, rel))

print('files with og:image/twitter:image:', files_with, '| total image refs:', og_image_refs)
print('distinct targets:', len(by_target))
print()
print('=== TARGET EXISTENCE ===')
for tgt, c in sorted(by_target.items()):
    print('  %5d  %s  %s' % (c, 'OK  ' if exists_rel(tgt) else 'MISS', tgt))
print()
print('=== MISSING (would 404 / break social cards) ===')
for p, r, rel in missing[:60]:
    print('  %s -> %s' % (p.replace(root, ''), r))
print('TOTAL MISSING refs:', len(missing))
