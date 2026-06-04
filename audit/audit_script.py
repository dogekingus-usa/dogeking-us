#!/usr/bin/env python3
"""Dogeking.us full site audit script"""
import os, re, sys
from collections import defaultdict

SITE_ROOT = r"C:\content-sites\dogeking.us"

def get_all_html_files():
    files = []
    for root, dirs, fnames in os.walk(SITE_ROOT):
        if '.wrangler' in root:
            continue
        for f in fnames:
            if f.endswith('.html'):
                rel = os.path.relpath(os.path.join(root, f), SITE_ROOT)
                files.append(rel.replace('\\', '/'))
    return sorted(files)

def extract_links(content):
    links = []
    for m in re.finditer(r'href=[\'"]([^\'"]+)[\'"]', content, re.IGNORECASE):
        links.append(m.group(1))
    for m in re.finditer(r'src=[\'"]([^\'"]+)[\'"]', content, re.IGNORECASE):
        links.append(m.group(1))
    return links

def check_brand(content, filename):
    issues = []
    patterns = [
        (r'\bDoge King\b(?!\.us)', 'Doge King (space) -> DogeKing'),
        (r'\bdoge king\b', 'lowercase doge king -> DogeKing'),
        (r'\bDOGE KING\b', 'DOGE KING all caps -> DogeKing'),
    ]
    for pattern, msg in patterns:
        for m in re.finditer(pattern, content):
            # Get context
            start = max(0, m.start()-30)
            end = min(len(content), m.end()+30)
            context = content[start:end].replace('\n', ' ').strip()
            issues.append((filename, msg, context))
    return issues

def check_seo_tags(content, filename):
    issues = []
    checks = {
        'title': r'<title>',
        'description': r'<meta\s+name=[\'"]description[\'"]',
        'og:title': r'<meta\s+property=[\'"]og:title[\'"]',
        'og:description': r'<meta\s+property=[\'"]og:description[\'"]',
        'og:image': r'<meta\s+property=[\'"]og:image[\'"]',
        'twitter:card': r'<meta\s+name=[\'"]twitter:card[\'"]',
        'viewport': r'<meta\s+name=[\'"]viewport[\'"]',
        'canonical': r'<link\s+rel=[\'"]canonical[\'"]',
    }
    for tag, pattern in checks.items():
        if not re.search(pattern, content, re.IGNORECASE):
            issues.append((filename, tag))
    return issues

def check_gumroad(content, filename):
    issues = []
    expected = "https://dogeking0.gumroad.com/l/dogeking-crypto-bundle"
    for m in re.finditer(r'href=[\'"](https?://[^\'"]*gumroad[^\'"]*)[\'"]', content, re.IGNORECASE):
        url = m.group(1)
        if url != expected:
            issues.append((filename, url))
    return issues

def count_article_type(filename):
    """Categorize article"""
    if filename.startswith('articles/wave5/'):
        return 'wave5'
    elif filename.startswith('articles/'):
        return 'article'
    elif filename.startswith('blog/'):
        return 'blog'
    elif filename.startswith('short/'):
        return 'short'
    else:
        return 'root'

def main():
    all_files = get_all_html_files()
    print("=== TOTAL HTML FILES: %d ===\n" % len(all_files))
    
    # Categorize
    cats = defaultdict(list)
    for f in all_files:
        t = count_article_type(f)
        cats[t].append(f)
    for t, flist in sorted(cats.items()):
        print("  %s: %d" % (t, len(flist)))
    
    # Read sitemap
    sitemap_path = os.path.join(SITE_ROOT, "sitemap.xml")
    sitemap_urls = set()
    if os.path.exists(sitemap_path):
        with open(sitemap_path, 'r', encoding='utf-8') as f:
            sitemap_content = f.read()
        for m in re.finditer(r'<loc>https://dogeking\.us/([^<]+)</loc>', sitemap_content):
            sitemap_urls.add(m.group(1))
    
    print("\nSitemap URLs: %d" % len(sitemap_urls))
    
    # Files not in sitemap
    sitemap_paths = set()
    for u in sitemap_urls:
        if u == '' or u == '/':
            sitemap_paths.add('index.html')
        else:
            sitemap_paths.add(u.lstrip('/'))
    
    files_not_in_sitemap = [f for f in all_files if f not in sitemap_paths]
    if files_not_in_sitemap:
        print("\n!! FILES NOT IN SITEMAP (%d):" % len(files_not_in_sitemap))
        for f in files_not_in_sitemap:
            print("  - %s" % f)
    
    sitemap_not_in_files = [u for u in sitemap_paths if u not in all_files and u != '']
    if sitemap_not_in_files:
        print("\n!! SITEMAP URLS WITH NO FILE (%d):" % len(sitemap_not_in_files))
        for u in sitemap_not_in_files:
            print("  - %s" % u)
    
    brand_issues = []
    seo_issues = []
    gumroad_issues = []
    external_links = defaultdict(list)
    
    skip_seo_for = ['template', 'nav-component', 'cta-snippets', 'preview-card', 'og-template', 'checklist', 'checkout', 'ecosystem-section', 'fetched-live', 'deployed-index', 'index-fixed']
    
    for f in all_files:
        filepath = os.path.join(SITE_ROOT, f)
        try:
            with open(filepath, 'r', encoding='utf-8') as fp:
                content = fp.read()
        except:
            try:
                with open(filepath, 'r', encoding='latin-1') as fp:
                    content = fp.read()
            except:
                print("  CANNOT READ: %s" % f)
                continue
        
        brand_issues.extend(check_brand(content, f))
        
        skip = any(x in f for x in skip_seo_for)
        if not skip:
            seo_issues.extend(check_seo_tags(content, f))
        
        gumroad_issues.extend(check_gumroad(content, f))
        
        links = extract_links(content)
        for link in links:
            if link.startswith('http') and 'dogeking.us' not in link and 'dogeking0.gumroad.com' not in link:
                if not any(x in link for x in ['fonts.googleapis.com', 'fonts.gstatic.com', 'googletagmanager.com', 'unpkg.com', 'cdnjs.cloudflare.com']):
                    external_links[link].append(f)
    
    print("\n=== BRAND INCONSISTENCIES: %d ===" % len(brand_issues))
    brand_by_type = defaultdict(list)
    for f, msg, ctx in brand_issues:
        brand_by_type[msg].append((f, ctx))
    for msg, items in sorted(brand_by_type.items(), key=lambda x: -len(x[1])):
        print("  [%s] %d occurrences" % (msg, len(items)))
        for f, ctx in items[:5]:
            print("    %s: ...%s..." % (f, ctx[:80]))
    
    print("\n=== SEO ISSUES (missing tags): %d ===" % len(seo_issues))
    seo_count = defaultdict(int)
    for f, tag in seo_issues:
        seo_count[tag] += 1
    for tag, count in sorted(seo_count.items(), key=lambda x: -x[1]):
        print("  Missing %s: %d" % (tag, count))
    # Show files missing most
    files_missing_seo = defaultdict(list)
    for f, tag in seo_issues:
        files_missing_seo[f].append(tag)
    if files_missing_seo:
        worst_files = sorted(files_missing_seo.items(), key=lambda x: -len(x[1]))[:10]
        print("\n  Worst files:")
        for f, tags in worst_files:
            print("    %s: missing %s" % (f, ', '.join(tags)))
    
    print("\n=== GUMROAD ISSUES: %d ===" % len(gumroad_issues))
    for f, url in gumroad_issues:
        print("  %s: %s" % (f, url))
    
    print("\n=== EXTERNAL LINKS (%d) ===" % len(external_links))
    for url, files in sorted(external_links.items()):
        print("  %s" % url)
        for f in files[:2]:
            print("    - %s" % f)
    
    print("\n" + "="*50)
    print("SUMMARY:")
    print("  Total HTML files: %d" % len(all_files))
    print("  Files not in sitemap: %d" % len(files_not_in_sitemap))
    print("  Sitemap URLs missing files: %d" % len(sitemap_not_in_files))
    print("  Brand issues: %d" % len(brand_issues))
    print("  SEO issues (missing tags): %d" % len(seo_issues))
    print("  Gumroad issues: %d" % len(gumroad_issues))
    print("  External links: %d" % len(external_links))
    print("="*50)

if __name__ == '__main__':
    main()
