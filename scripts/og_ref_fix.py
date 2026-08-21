#!/usr/bin/env python3
"""25-role overhaul cycle 2 - OG/Social Sharing integrity fix.
Remaps og:image / twitter:image refs that point to missing files
(or to HTML pages instead of images) onto existing images.

Rules:
  1. og-images/NAME.html -> og-images/NAME.png  (when PNG exists)
  2. any other missing/404 target -> og-images/default.png
  3. existing image targets are left untouched
Writes UTF-8 (no BOM). Reports per-file change counts.
"""
import os
import re

root = r'C:\content-sites\dogeking.us'
BASE = 'https://dogeking.us/'
DEFAULT = 'og-images/default.png'

META_RE = re.compile(
    r'(<meta[^>]+(?:property=["\']og:image["\']|name=["\']twitter:image["\'])[^>]*content=["\'])([^"\']+)(["\'])'
)

changed_files = 0
changed_refs = 0
skipped = 0
results = []

for dp, dn, fn in os.walk(root):
    if '.git' in dp or 'scripts' in dp:
        continue
    for f in fn:
        if not f.endswith('.html'):
            continue
        p = os.path.join(dp, f)
        with open(p, encoding='utf-8') as fh:
            text = fh.read()
        orig = text

        def repl(m):
            global changed_refs
            url = m.group(2).strip()
            if url.startswith('http') and not url.startswith(BASE):
                return m.group(0)
            rel = url[len(BASE):] if url.startswith(BASE) else url.lstrip('/')
            rel = rel.split('#')[0].split('?')[0]
            if not rel:
                return m.group(0)
            local = os.path.join(root, rel.replace('/', os.sep))
            if os.path.exists(local) and not rel.endswith('.html'):
                return m.group(0)
            # HTML page as image -> try PNG sibling
            if rel.endswith('.html') and rel.startswith('og-images/'):
                png = rel[:-5] + '.png'
                if os.path.exists(os.path.join(root, png.replace('/', os.sep))):
                    changed_refs += 1
                    return m.group(1) + BASE + png + m.group(3)
            # missing target -> default.png
            if not os.path.exists(local):
                changed_refs += 1
                return m.group(1) + BASE + DEFAULT + m.group(3)
            return m.group(0)

        text = META_RE.sub(repl, text)
        if text != orig:
            with open(p, 'w', encoding='utf-8', newline='') as fh:
                fh.write(text)
            changed_files += 1
            results.append((p.replace(root, ''), orig.count('og:image') + orig.count('twitter:image')))

print('changed files:', changed_files)
print('changed refs:', changed_refs)
for r in results[:10]:
    print('  ', r)
