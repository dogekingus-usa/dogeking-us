#!/usr/bin/env python3
"""Clean up: Remove OG image tags added to utility pages, keep only on real articles."""

import os, re

BASE_DIR = r"C:\Users\SAMPC\.openclaw\content\dogeking.us"
UTILITY_PAGES = ['404', 'about', 'contact', 'default', 'health', 'checklist', 'preview-card', 'thank-you', 
                 'crypto-bundle', 'template', 'nav-component', 'cta-snippets', 'og-template',
                 'portfolio', 'tools-comparison', 'fetched-live', 'disclaimer', 'privacy-policy',
                 'affiliate', 'lead-magnet', 'sales-cta', 'sales-thank', 'ecosystem-section']

removed_count = 0
for root, dirs, files in os.walk(BASE_DIR):
    for f in files:
        if not f.endswith('.html'):
            continue
        
        fp = os.path.join(root, f)
        rel = os.path.relpath(fp, BASE_DIR)
        
        # Check if this is a utility page
        is_utility = any(part in rel.lower() for part in UTILITY_PAGES)
        
        with open(fp, 'r', encoding='utf-8', errors='replace') as fh:
            content = fh.read()
        
        original = content
        
        # Remove og:image tags (both the ones I added and any existing)
        content = re.sub(r'\n\s*<meta[^>]*property=["\']og:image["\'][^>]*>', '', content, flags=re.IGNORECASE)
        content = re.sub(r'\n\s*<meta[^>]*property=["\']og:image:width["\'][^>]*>', '', content, flags=re.IGNORECASE)
        content = re.sub(r'\n\s*<meta[^>]*property=["\']og:image:height["\'][^>]*>', '', content, flags=re.IGNORECASE)
        
        if content != original:
            with open(fp, 'w', encoding='utf-8') as fh:
                fh.write(content)
            removed_count += 1
            if removed_count <= 5:
                print(f"  Cleaned: {rel}")

print(f"\nCleaned {removed_count} files (removed og:image tags)")
