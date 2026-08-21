#!/usr/bin/env python3
"""Refresh sitemap.xml lastmod dates from actual file mtimes.
Maps each <loc> to its local file, sets <lastmod> to file mtime (UTC).
Unresolvable URLs keep their existing lastmod and are reported.
"""
import os
import re
from datetime import datetime, timezone

root = r'C:\content-sites\dogeking.us'
sitemap = os.path.join(root, 'sitemap.xml')
BASE = 'https://dogeking.us/'

with open(sitemap, encoding='utf-8') as fh:
    text = fh.read()

URL_RE = re.compile(r'<url>(.*?)</url>', re.DOTALL)
LOC_RE = re.compile(r'<loc>(.*?)</loc>')
MOD_RE = re.compile(r'<lastmod>[^<]*</lastmod>')

total = 0
updated = 0
unresolved = []

def resolve(rel):
    rel = rel.rstrip('/')
    if not rel:
        return 'index.html'
    for cand in (rel + '.html', os.path.join(rel, 'index.html')):
        p = os.path.join(root, cand.replace('/', os.sep))
        if os.path.exists(p):
            return cand
    return None

def fmt(mtime):
    dt = datetime.fromtimestamp(mtime, tz=timezone.utc)
    return dt.strftime('%Y-%m-%dT%H:%M:%S+00:00Z')

def repl_block(m):
    global total, updated
    block = m.group(0)
    lm = LOC_RE.search(block)
    if not lm:
        return block
    total += 1
    loc = lm.group(1)
    if not loc.startswith(BASE):
        unresolved.append((loc, 'not-dogeking'))
        return block
    rel = resolve(loc[len(BASE):])
    if rel is None:
        unresolved.append((loc, 'no-file'))
        return block
    fpath = os.path.join(root, rel.replace('/', os.sep))
    mtime = os.path.getmtime(fpath)
    new = '<lastmod>' + fmt(mtime) + '</lastmod>'
    if MOD_RE.search(block):
        block = MOD_RE.sub(new, block, count=1)
        updated += 1
    return block

new_text = URL_RE.sub(repl_block, text)

with open(sitemap, 'w', encoding='utf-8', newline='') as fh:
    fh.write(new_text)

print('url blocks:', total)
print('lastmod updated:', updated)
print('unresolved:', len(unresolved))
for u in unresolved[:15]:
    print('  ', u)
