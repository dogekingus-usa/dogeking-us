#!/usr/bin/env python3
"""Comprehensive content audit for dogeking.us — checks every file for issues."""

import os, re, sys
from collections import defaultdict

BASE_DIR = r"C:\Users\SAMPC\.openclaw\content\dogeking.us"
ARTICLES_DIR = os.path.join(BASE_DIR, "articles")
RESULTS_DIR = r"C:\content-sites\dogeking.us\audit"

os.makedirs(RESULTS_DIR, exist_ok=True)

ISSUES = defaultdict(list)
FILES_CHECKED = 0

def log_issue(file, severity, category, desc):
    ISSUES[severity].append(f"{file} | {category} | {desc}")

def check_file(filepath):
    global FILES_CHECKED
    FILES_CHECKED += 1
    rel = os.path.relpath(filepath, BASE_DIR)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(filepath, 'r', encoding='latin-1') as f:
                content = f.read()
            log_issue(rel, "HIGH", "ENCODING", "Not valid UTF-8 — read with latin-1")
        except:
            log_issue(rel, "CRITICAL", "ENCODING", "Could not read file at all")
            return

    # Skip all-articles.html — it's a listing page, not an article
    if rel.endswith("all-articles.html"):
        return

    # 1. TITLE CHECK
    title_match = re.search(r'<title>([^<]*)</title>', content, re.IGNORECASE)
    if not title_match:
        log_issue(rel, "CRITICAL", "TITLE", "Missing <title> tag")
    else:
        title = title_match.group(1).strip()
        if not title:
            log_issue(rel, "CRITICAL", "TITLE", "<title> tag is empty")
        elif len(title) < 10:
            log_issue(rel, "MEDIUM", "TITLE", f"Title too short ({len(title)} chars): '{title}'")
        elif len(title) > 70:
            log_issue(rel, "MEDIUM", "TITLE", f"Title too long ({len(title)} chars): '{title[:60]}...'")

    # 2. META DESCRIPTION CHECK
    meta_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', content, re.IGNORECASE)
    if not meta_match:
        log_issue(rel, "CRITICAL", "META", "Missing meta description tag")
    else:
        desc = meta_match.group(1).strip()
        if not desc:
            log_issue(rel, "HIGH", "META", "Meta description is empty")
        elif len(desc) < 50:
            log_issue(rel, "MEDIUM", "META", f"Meta description too short ({len(desc)} chars)")
        elif len(desc) > 165:
            log_issue(rel, "LOW", "META", f"Meta description too long ({len(desc)} chars)")

    # 3. BRAND CONSISTENCY CHECK
    brand_variants = []
    if re.search(r'\bDogeKing\b(?!\s)', content): brand_variants.append("DogeKing (one word)")
    if re.search(r'\bdogeking\b', content, re.IGNORECASE) and not re.search(r'\bDoge King\b', content):
        if "DogeKing" not in str(brand_variants):
            brand_variants.append("dogeking (lowercase)")
    if re.search(r'\bDogeking\b', content): brand_variants.append("Dogeking (capital D, lowercase k)")
    
    if brand_variants:
        log_issue(rel, "HIGH", "BRAND", f"Inconsistent brand: {', '.join(brand_variants)}")

    # 4. CANONICAL TAG CHECK
    canonical_match = re.search(r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']*)["\']', content, re.IGNORECASE)
    if not canonical_match:
        log_issue(rel, "HIGH", "CANONICAL", "Missing canonical tag")

    # 5. H1 CHECK
    h1_matches = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE)
    if len(h1_matches) == 0:
        log_issue(rel, "HIGH", "H1", "Missing <h1> tag")
    elif len(h1_matches) > 1:
        log_issue(rel, "MEDIUM", "H1", f"Multiple <h1> tags ({len(h1_matches)})")

    # 6. BROKEN INTERNAL LINKS CHECK
    # Extract all href="#" links
    internal_links = re.findall(r'href=["\']([^"\']+)["\']', content)
    hash_links = [l for l in internal_links if l.startswith('#') and len(l) > 1]
    if hash_links:
        for link in hash_links:
            anchor = link[1:]  # remove #
            # Check if anchor exists in the file
            if not re.search(r'id=["\']' + re.escape(anchor) + r'["\']', content) and \
               not re.search(r'name=["\']' + re.escape(anchor) + r'["\']', content):
                log_issue(rel, "MEDIUM", "BROKEN_LINK", f"Anchor '{link}' has no matching element in page")

    # 7. WORD COUNT
    # Extract text content (rough)
    text = re.sub(r'<[^>]+>', ' ', content)
    text = re.sub(r'\s+', ' ', text).strip()
    word_count = len(text.split())
    
    if word_count < 300 and not rel.startswith('articles') and not rel.startswith('blog'):
        log_issue(rel, "LOW", "WORD_COUNT", f"Short page ({word_count} words) — may be a redirect/placeholder")
    elif word_count < 300:
        log_issue(rel, "HIGH", "WORD_COUNT", f"Article too thin ({word_count} words) — needs expansion")
    elif word_count < 700:
        log_issue(rel, "MEDIUM", "WORD_COUNT", f"Article below optimal length ({word_count} words)")

    # 8. ENCODING ISSUES
    if '\ufffd' in content or '?' in content:
        # Check for actual encoding problems
        bad_chars = len(re.findall(r'[\ufffd\u2013\u2014\u2018\u2019\u201c\u201d\u2026\u00a0]', content))
        if bad_chars > 5:
            log_issue(rel, "HIGH", "ENCODING", f"Found {bad_chars} special character issues (bad UTF-8)")

    # 9. GUMROAD LINKS CHECK
    gumroad_links = re.findall(r'href=["\'](https?://[^"\']*gumroad[^"\']*)["\']', content, re.IGNORECASE)
    generic_store = [l for l in gumroad_links if l.rstrip('/') == 'https://dogeking0.gumroad.com']
    if generic_store:
        log_issue(rel, "HIGH", "GUMROAD", f"Generic store link (should point to specific product): {generic_store[0]}")

    # 10. CHECK FOR OLD GA ID
    if 'G-XXXXXXXXXX' in content:
        log_issue(rel, "HIGH", "OLD_GA", "Still has placeholder GA tracking ID G-XXXXXXXXXX")

    # 11. RESPONSIVE VIEWPORT CHECK
    if not re.search(r'<meta[^>]*name=["\']viewport["\']', content, re.IGNORECASE):
        log_issue(rel, "HIGH", "VIEWPORT", "Missing viewport meta tag (not mobile-responsive)")

# Walk all HTML files
for root, dirs, files in os.walk(BASE_DIR):
    for f in files:
        if f.endswith('.html'):
            check_file(os.path.join(root, f))

# WRITE REPORT
report_path = os.path.join(RESULTS_DIR, "content-audit-report.md")
with open(report_path, 'w', encoding='utf-8') as r:
    r.write("# DogeKing.us — Full Content Audit Report\n")
    r.write(f"**Generated:** 2026-06-02 08:15 ICT\n")
    r.write(f"**Files checked:** {FILES_CHECKED}\n\n")
    
    for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        issues = ISSUES.get(severity, [])
        r.write(f"## {severity} — {len(issues)} issues\n\n")
        r.write(f"| File | Category | Description |\n")
        r.write(f"|------|----------|-------------|\n")
        for issue in issues:
            parts = issue.split(" | ", 2)
            if len(parts) == 3:
                r.write(f"| {parts[0]} | {parts[1]} | {parts[2]} |\n")
        r.write("\n")
    
    # Summary
    total = sum(len(v) for v in ISSUES.values())
    r.write(f"## Summary\n\n")
    r.write(f"- **Total issues found:** {total}\n")
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        r.write(f"- **{sev}:** {len(ISSUES.get(sev, []))}\n")
    r.write(f"\n*Auto-generated by Growth Commander audit script*\n")

print("\n[OK] Audit complete!")
print(f"Files checked: {FILES_CHECKED}")
for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
    print(f"  {sev}: {len(ISSUES.get(sev, []))} issues")
print(f"\nFull report: {report_path}")
