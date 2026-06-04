#!/usr/bin/env python3
"""Auto-fix common issues in dogeking.us content files."""

import os, re

BASE_DIR = r"C:\Users\SAMPC\.openclaw\content\dogeking.us"
FIXED = {"meta": 0, "canonical": 0, "brand": 0, "encoding": 0, "viewport": 0}

def make_slug(filepath, base_dir):
    """Create URL slug from file path."""
    rel = os.path.relpath(filepath, base_dir).replace('\\', '/')
    name = os.path.splitext(rel)[0]
    return name

def derive_title_from_slug(slug):
    """Derive a human-readable title from URL slug."""
    name = os.path.basename(slug).replace('-', ' ').title()
    # Fix common patterns
    name = name.replace(' And ', ' and ').replace(' For ', ' for ')
    name = name.replace(' Of ', ' of ').replace(' In ', ' in ')
    name = name.replace(' The ', ' the ').replace(' To ', ' to ')
    name = name.replace(' Is ', ' is ').replace(' A ', ' a ')
    name = name.replace(' Vs ', ' vs ')
    # Capitalize first letter
    if name:
        name = name[0].upper() + name[1:]
    return name

def fix_file(filepath):
    global FIXED
    rel = os.path.relpath(filepath, BASE_DIR)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        try:
            with open(filepath, 'r', encoding='latin-1') as f:
                content = f.read()
            FIXED["encoding"] += 1
        except:
            return False

    original = content
    slug = make_slug(filepath, BASE_DIR)
    is_article = slug.startswith('articles/') or slug.startswith('blog/')
    
    # Get existing title for meta description generation
    existing_title = ""
    title_match = re.search(r'<title>([^<]*)</title>', content, re.IGNORECASE)
    if title_match:
        existing_title = title_match.group(1).strip()
    
    # 1. ADD META DESCRIPTION if missing
    meta_pattern = r'<meta[^>]*name=["\']description["\'][^>]*>'
    if not re.search(meta_pattern, content, re.IGNORECASE):
        # Generate description from title or slug
        if existing_title:
            desc = existing_title
        else:
            desc = derive_title_from_slug(slug)
        
        # Clean description
        desc = re.sub(r'<[^>]+>', '', desc)
        desc = desc.strip()
        
        # Truncate to reasonable length
        if len(desc) > 155:
            desc = desc[:152] + "..."
        
        # Add meta description after charset or title
        meta_insert = f'\n<meta name="description" content="{desc}">'
        
        # Try to insert after charset meta, or after <title>, or after <head>
        charset_match = re.search(r'(<meta[^>]*charset[^>]*>)', content, re.IGNORECASE)
        if charset_match:
            content = content.replace(charset_match.group(1), charset_match.group(1) + meta_insert, 1)
        elif title_match:
            content = content.replace(title_match.group(0), title_match.group(0) + meta_insert, 1)
        else:
            content = content.replace('<head>', '<head>' + meta_insert, 1)
        
        FIXED["meta"] += 1

    # 2. ADD CANONICAL TAG if missing
    canonical_pattern = r'<link[^>]*rel=["\']canonical["\']'
    if not re.search(canonical_pattern, content, re.IGNORECASE):
        url_path = make_slug(filepath, BASE_DIR).replace('\\', '/')
        canonical_tag = f'\n<link rel="canonical" href="https://dogeking.us/{url_path}.html">'
        
        # Insert before </head>
        content = content.replace('</head>', canonical_tag + '\n</head>', 1)
        FIXED["canonical"] += 1

    # 3. FIX BRAND INCONSISTENCY — standardize to "Doge King"
    # But only for the display text, not URLs or code
    # Replace "DogeKing" (one word) with "Doge King" (two words) in display text
    # Be careful not to break URLs, class names, or IDs
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        # Only fix display text — skip code/attributes
        if 'href=' in line or 'src=' in line or 'class=' in line or 'id=' in line or 'action=' in line:
            new_lines.append(line)
        else:
            # Replace "DogeKing" with "Doge King" in text content
            line = re.sub(r'(?<![a-zA-Z])DogeKing(?![a-zA-Z])', 'Doge King', line)
            new_lines.append(line)
    content = '\n'.join(new_lines)
    
    # Don't count brand fix since it's often in the original
    # We'll count if we actually changed something
    if content != original:
        # Check if it was a brand change vs other changes
        pass

    # 4. FIX ENCODING ISSUES — smart quotes and special chars
    content = content.replace('\u2013', '-').replace('\u2014', '-')
    content = content.replace('\u2018', "'").replace('\u2019', "'")
    content = content.replace('\u201c', '"').replace('\u201d', '"')
    content = content.replace('\u2026', '...')
    
    # 5. ADD VIEWPORT if missing
    if not re.search(r'<meta[^>]*name=["\']viewport["\']', content, re.IGNORECASE):
        viewport_tag = '\n<meta name="viewport" content="width=device-width, initial-scale=1.0">'
        content = content.replace('<head>', '<head>' + viewport_tag, 1)
        FIXED["viewport"] += 1

    # Write if changed
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Walk all HTML files
fixed_count = 0
total = 0
for root, dirs, files in os.walk(BASE_DIR):
    for f in files:
        if f.endswith('.html'):
            total += 1
            if fix_file(os.path.join(root, f)):
                fixed_count += 1

print(f"\n[RESULTS]")
print(f"Files checked: {total}")
print(f"Files modified: {fixed_count}")
print(f"Meta descriptions added: {FIXED['meta']}")
print(f"Canonical tags added: {FIXED['canonical']}")
print(f"Viewport tags added: {FIXED['viewport']}")
print(f"Encoding fixes: {FIXED['encoding']}")
