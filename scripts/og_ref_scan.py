#!/usr/bin/env python3
"""Scan all og:image / twitter:image refs in dogeking.us deploy tree.
Read-only. Reports broken/missing targets by extension and file.
"""
import os
import re
import collections

root = r'C:\content-sites\dogeking.us'
broken = []
by_ext = collections.Counter()
total_refs = 0
files_with_refs = 0

for dp, dn, fn in os.walk(root):
    if '.git' in dp:
        continue
    for f in fn:
        if not f.endswith('.html'):
            continue
        p = os.path.join(dp, f)
        with open(p, encoding='utf-8', errors='replace') as fh:
            t = fh.read()
        refs = re.findall(r'(?:og:image|twitter:image)[^>]*content=["\']([^"\']+)["\']', t)
        if refs:
            files_with_refs += 1
        for r in refs:
            total_refs += 1
            m = re.search(r'og-images/([^"\']+)$', r)
            if m:
                target = m.group(1)
                ext = os.path.splitext(target)[1].lower()
                by_ext[ext] += 1
                if not os.path.exists(os.path.join(root, 'og-images', target)):
                    broken.append((p, r))
            else:
                broken.append((p, r + '  [NON-og-images PATH]'))

print('files with og/twitter:image:', files_with_refs, '| total refs:', total_refs)
print('by ext:', dict(by_ext))
print('BROKEN/MISSING refs:', len(broken))
for p, r in broken[:40]:
    print(' ', p.replace(root, ''), '->', r)
