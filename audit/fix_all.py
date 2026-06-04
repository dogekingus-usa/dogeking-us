#!/usr/bin/env python3
"""Auto-fix script for dogeking.us - fix sitemap, OG tags, Gumroad links"""
import os, re

SITE_ROOT = r"C:\content-sites\dogeking.us"

def fix_file(filepath, actions_taken):
    """Apply fixes to one HTML file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        try:
            with open(filepath, 'r', encoding='latin-1') as f:
                content = f.read()
        except:
            return
    
    original = content
    rel = os.path.relpath(filepath, SITE_ROOT).replace('\\', '/')
    
    # Skip non-article, non-page files
    skip = ['template', 'nav-component', 'cta-snippets', 'preview-card', 'og-template', 
            'checklist', 'fetched-live', 'ecosystem-section', 'deployed-index', 'index-fixed']
    if any(x in rel for x in skip):
        return
    
    # === FIX 1: Standardize Gumroad links ===
    # Map of old short-link product IDs to canonical
    gumroad_replacements = {
        'https://dogeking0.gumroad.com/l/toifmun': 'https://dogeking0.gumroad.com/l/dogeking-crypto-bundle',
        'https://dogeking0.gumroad.com/l/ptfzf': 'https://dogeking0.gumroad.com/l/dogeking-crypto-bundle',
        'https://dogeking0.gumroad.com/l/emvsb': 'https://dogeking0.gumroad.com/l/dogeking-crypto-bundle',
        'https://dogeking0.gumroad.com/l/ycvsyd': 'https://dogeking0.gumroad.com/l/dogeking-crypto-bundle',
        'https://dogeking0.gumroad.com/l/hvvut': 'https://dogeking0.gumroad.com/l/dogeking-crypto-bundle',
        'https://dogeking0.gumroad.com/l/meme-coin-bundle': 'https://dogeking0.gumroad.com/l/dogeking-crypto-bundle',
        'https://dogeking0.gumroad.com/l/crypto-bundle': 'https://dogeking0.gumroad.com/l/dogeking-crypto-bundle',
        'https://dogeking.gumroad.com/l/dogeking-bundle': 'https://dogeking0.gumroad.com/l/dogeking-crypto-bundle',
        # Direct dogeking0.gumroad.com root links
        'https://dogeking0.gumroad.com"': 'https://dogeking0.gumroad.com/l/dogeking-crypto-bundle"',
    }
    
    for old_url, new_url in gumroad_replacements.items():
        if old_url in content:
            content = content.replace(old_url, new_url)
    
    # Also fix standalone gumroad links (not in href)
    content = re.sub(
        r'href="https://dogeking0\.gumroad(?!\.com/l/)',
        'href="https://dogeking0.gumroad.com/l/dogeking-crypto-bundle',
        content
    )
    
    # === FIX 2: Add OG tags, canonical, twitter:card ===
    # Only add if head exists and tags are missing
    head_match = re.search(r'<head>(.*?)</head>', content, re.DOTALL | re.IGNORECASE)
    if not head_match:
        return
    
    head_content = head_match.group(1)
    new_head = head_content
    
    # Get title for OG tags
    title_match = re.search(r'<title>(.*?)</title>', new_head, re.DOTALL | re.IGNORECASE)
    page_title = title_match.group(1).strip() if title_match else 'DogeKing'
    # Clean title for OG
    og_title = re.sub(r'\s*\|\s*DogeKing.*$', '', page_title).strip()
    if not og_title:
        og_title = 'DogeKing'
    
    # Get description
    desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\']', new_head, re.IGNORECASE)
    og_desc = desc_match.group(1).strip() if desc_match else 'DogeKing - The Meme Coin Royalty on Solana'
    
    # Build URL
    if rel.endswith('.html'):
        url_path = '/' + rel
    else:
        url_path = '/'
    canonical_url = 'https://dogeking.us' + url_path
    
    # Determine if this is a root page or article
    is_root = '/' not in rel.rstrip('.html')
    
    tags_to_add = []
    
    if not re.search(r'<meta\s+property=[\'"]og:title[\'"]', new_head, re.IGNORECASE):
        tags_to_add.append('  <meta property="og:title" content="%s">' % og_title)
    
    if not re.search(r'<meta\s+property=[\'"]og:description[\'"]', new_head, re.IGNORECASE):
        clean_desc = og_desc.replace('"', '&quot;')
        tags_to_add.append('  <meta property="og:description" content="%s">' % clean_desc)
    
    if not re.search(r'<meta\s+property=[\'"]og:image[\'"]', new_head, re.IGNORECASE):
        tags_to_add.append('  <meta property="og:image" content="https://dogeking.us/assets/crown-logo.svg">')
    
    if not re.search(r'<meta\s+property=[\'"]og:type[\'"]', new_head, re.IGNORECASE):
        tags_to_add.append('  <meta property="og:type" content="website">')
    
    if not re.search(r'<meta\s+property=[\'"]og:url[\'"]', new_head, re.IGNORECASE):
        tags_to_add.append('  <meta property="og:url" content="%s">' % canonical_url)
    
    if not re.search(r'<meta\s+name=[\'"]twitter:card[\'"]', new_head, re.IGNORECASE):
        tags_to_add.append('  <meta name="twitter:card" content="summary_large_image">')
    
    if not re.search(r'<link\s+rel=[\'"]canonical[\'"]', new_head, re.IGNORECASE):
        tags_to_add.append('  <link rel="canonical" href="%s">' % canonical_url)
    
    if not re.search(r'<meta\s+name=[\'"]twitter:title[\'"]', new_head, re.IGNORECASE):
        tags_to_add.append('  <meta name="twitter:title" content="%s">' % og_title)
    
    if not re.search(r'<meta\s+name=[\'"]twitter:description[\'"]', new_head, re.IGNORECASE):
        clean_desc = og_desc.replace('"', '&quot;')
        tags_to_add.append('  <meta name="twitter:description" content="%s">' % clean_desc)
    
    if not re.search(r'<meta\s+name=[\'"]twitter:image[\'"]', new_head, re.IGNORECASE):
        tags_to_add.append('  <meta name="twitter:image" content="https://dogeking.us/assets/crown-logo.svg">')
    
    if tags_to_add:
        # Insert after title or viewport meta, before style
        insert_point = None
        st_match = re.search(r'</title>', new_head)
        if st_match:
            insert_point = st_match.end()
        
        if insert_point:
            new_head = new_head[:insert_point] + '\n' + '\n'.join(tags_to_add) + new_head[insert_point:]
            content = content[:head_match.start(1)] + new_head + content[head_match.end(1):]
            actions_taken['seo_tags'] = actions_taken.get('seo_tags', 0) + len(tags_to_add)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def fix_sitemap():
    """Regenerate sitemap from actual files"""
    sitemap_path = os.path.join(SITE_ROOT, "sitemap.xml")
    
    # Get all actual HTML files
    files = []
    for root, dirs, fnames in os.walk(SITE_ROOT):
        if '.wrangler' in root:
            continue
        for f in fnames:
            if f.endswith('.html'):
                rel = os.path.relpath(os.path.join(root, f), SITE_ROOT).replace('\\', '/')
                files.append(rel)
    
    files.sort()
    
    # Priority map
    priority_map = {
        'index.html': 1.0,
        'all-articles.html': 0.9,
        'whitepaper.html': 0.8,
        'why-dogeking.html': 0.7,
        'about.html': 0.6,
        'contact.html': 0.5,
        'privacy.html': 0.3,
        'thank-you.html': 0.3,
    }
    
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    # Root URL first
    lines.append('  <url><loc>https://dogeking.us</loc><lastmod>2026-06-02</lastmod><changefreq>weekly</changefreq><priority>1.0</priority></url>')
    
    for f in files:
        if f == 'index.html':
            continue  # Already added as root
        # Skip junk files
        if f in ['deployed-index.html', 'index-fixed.html', 'ecosystem-section.html', 
                 'sales-cta-overlay.html', 'sales-thank-you.html']:
            continue
        if '/template' in f or '/nav-component' in f or '/og-template' in f:
            continue
        if f.startswith('articles/404') or f.startswith('articles/default') or f.startswith('articles/index'):
            continue
        if f.startswith('articles/checklist') or f.startswith('articles/cta-snippets') or f.startswith('articles/preview-card'):
            continue
        if f.startswith('articles/fetched-live'):
            continue
        
        url_path = 'https://dogeking.us/' + f
        
        priority = priority_map.get(f, 0.7)
        lines.append('  <url><loc>%s</loc><lastmod>2026-06-02</lastmod><changefreq>monthly</changefreq><priority>%s</priority></url>' % (url_path, priority))
    
    lines.append('</urlset>')
    
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    return len(files)

def main():
    print("=== DOGEKING.US AUTO-FIX ===\n")
    
    actions_taken = {'seo_tags': 0, 'gumroad_fixed': 0, 'files_modified': 0}
    
    # Fix all HTML files
    all_files = []
    for root, dirs, fnames in os.walk(SITE_ROOT):
        if '.wrangler' in root:
            continue
        for f in fnames:
            if f.endswith('.html'):
                all_files.append(os.path.join(root, f))
    
    print("Processing %d HTML files..." % len(all_files))
    for fp in all_files:
        if fix_file(fp, actions_taken):
            actions_taken['files_modified'] += 1
    
    # Fix sitemap
    sitemap_count = fix_sitemap()
    print("\nSitemap regenerated with %d URLs" % sitemap_count)
    
    print("\n=== RESULTS ===")
    print("Files modified: %d" % actions_taken['files_modified'])
    print("SEO tags added: %d" % actions_taken['seo_tags'])
    print("Sitemap URLs: %d" % sitemap_count)
    print("\nDone!")

if __name__ == '__main__':
    main()
