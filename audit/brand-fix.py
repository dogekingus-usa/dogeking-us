#!/usr/bin/env python3
"""Fix brand consistency: Replace "DogeKing" with "Doge King" in visible text only."""

import os, re

BASE_DIR = r"C:\Users\SAMPC\.openclaw\content\dogeking.us"
fixed_count = 0

for root, dirs, files in os.walk(BASE_DIR):
    for f in files:
        if not f.endswith('.html'):
            continue
        
        fp = os.path.join(root, f)
        
        with open(fp, 'r', encoding='utf-8', errors='replace') as fh:
            content = fh.read()
        
        original = content
        rel = os.path.relpath(fp, BASE_DIR)
        
        # Only fix visible text content — between HTML tags
        # Replace "DogeKing" → "Doge King" ONLY when it's visible text, not in attributes
        def fix_visible_text(match):
            full_tag = match.group(0)
            tag_content = match.group(1)
            # Fix brand in visible text
            fixed = re.sub(r'(?<![\/\w])DogeKing(?![\/\w])', 'Doge King', tag_content)
            fixed = re.sub(r'(?<![\/\w])Dogeking(?![\/\w])', 'Doge King', fixed)
            fixed = re.sub(r'(?<![\/\w])dogeking(?![\/\w])', 'Doge King', fixed, flags=re.IGNORECASE)
            if fixed != tag_content:
                return full_tag.replace(tag_content, fixed)
            return full_tag
        
        # Match content between HTML tags (outside of angle brackets)
        content = re.sub(r'>([^<]+)<', fix_visible_text, content)
        
        if content != original:
            with open(fp, 'w', encoding='utf-8') as fh:
                fh.write(content)
            fixed_count += 1
            if fixed_count <= 5:
                print(f"  Fixed: {rel}")

print(f"\nFiles with brand fixes: {fixed_count}")
