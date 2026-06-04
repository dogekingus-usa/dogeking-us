#!/usr/bin/env python3
"""Fix all remaining content issues in dogeking.us."""

import os, re

BASE_DIR = r"C:\Users\SAMPC\.openclaw\content\dogeking.us"
stats = {"titles": 0, "metas": 0, "h1": 0, "gumroad": 0, "ga": 0, "viewport": 0, "canonical": 0}

for root, dirs, files in os.walk(BASE_DIR):
    for f in files:
        if not f.endswith('.html'):
            continue
        
        fp = os.path.join(root, f)
        rel = os.path.relpath(fp, BASE_DIR)
        
        with open(fp, 'r', encoding='utf-8', errors='replace') as fh:
            content = fh.read()
        
        original = content
        
        # 1. FIX PLACEHOLDER GA ID
        if 'G-XXXXXXXXXX' in content:
            content = content.replace('G-XXXXXXXXXX', 'G-8CVE2X8R5L')
            stats["ga"] += 1
        
        # 2. FIX GENERIC GUMROAD STORE LINKS → specific bundle
        content = re.sub(
            r'href=["\']https?://dogeking0\.gumroad\.com/?["\'](?!\w)',
            'href="https://dogeking0.gumroad.com/l/dogeking-crypto-bundle"',
            content
        )
        
        # 3. ADD MISSING <h1> (if article has title but no h1)
        title_match = re.search(r'<title>([^<]+)</title>', content, re.IGNORECASE)
        has_h1 = re.search(r'<h1[^>]*>', content, re.IGNORECASE)
        if title_match and not has_h1 and rel.startswith('articles'):
            article_title = title_match.group(1).strip()
            # Clean the title
            article_title = re.sub(r'\s*\|.*$', '', article_title).strip()  # Remove "| site name"
            if article_title:
                # Add h1 after <h2> or before first paragraph
                h1_tag = f'\n<h1>{article_title}</h1>\n'
                # Insert after opening <main>, <article>, <body>, or before first <p>
                for tag in ['<main>', '<article>', '<body>']:
                    if tag in content:
                        content = content.replace(tag, tag + h1_tag, 1)
                        stats["h1"] += 1
                        break
                else:
                    # Insert before first <p>
                    p_match = re.search(r'<p[^>]*>', content)
                    if p_match:
                        content = content.replace(p_match.group(0), h1_tag + '\n' + p_match.group(0), 1)
                        stats["h1"] += 1
        
        # 4. FIX OVERLY LONG TITLES (truncate at 65 chars)
        title_match = re.search(r'<title>([^<]+)</title>', content, re.IGNORECASE)
        if title_match:
            title = title_match.group(1)
            if len(title) > 70:
                # Find a good break point
                short = title[:65]
                # Break at last space or colon
                for char in [':', ' - ', ' | ', ' ']:
                    idx = short.rfind(char)
                    if idx > 30:
                        short = short[:idx]
                        break
                else:
                    short = short.rsplit(' ', 1)[0] if ' ' in short else short[:60]
                
                short = short.rstrip(' :-,;') + ''
                new_title = short + ' | Doge King'
                content = content.replace(f'<title>{title}</title>', f'<title>{new_title}</title>')
                stats["titles"] += 1
        
        # 5. FIX OVERLY LONG META DESCRIPTIONS (truncate at 160 chars)
        meta_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', content, re.IGNORECASE)
        if meta_match:
            desc = meta_match.group(1)
            full_match = meta_match.group(0)
            if len(desc) > 165:
                short = desc[:157]
                short = short.rsplit(' ', 1)[0] if ' ' in short else short[:157]
                short = short.rstrip(' :-,;.') + '...'
                new_meta = full_match.replace(f'content="{desc}"', f'content="{short}"')
                content = content.replace(full_match, new_meta)
                stats["metas"] += 1
        
        # 6. ADD CANONICAL TAG if still missing
        if not re.search(r'<link[^>]*rel=["\']canonical["\']', content, re.IGNORECASE):
            url_path = os.path.relpath(fp, BASE_DIR).replace('\\', '/')
            if url_path.endswith('.html'):
                url_path = url_path[:-5]
            canonical_tag = f'\n<link rel="canonical" href="https://dogeking.us/{url_path}.html">'
            content = content.replace('</head>', canonical_tag + '\n</head>', 1)
            stats["canonical"] += 1
        
        # 7. ADD VIEWPORT if still missing
        if not re.search(r'<meta[^>]*name=["\']viewport["\']', content, re.IGNORECASE):
            viewport_tag = '\n<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            content = content.replace('<head>', '<head>' + viewport_tag, 1)
            stats["viewport"] += 1
        
        if content != original:
            with open(fp, 'w', encoding='utf-8') as fh:
                fh.write(content)

print(f"\n[FIX RESULTS]")
print(f"Titles truncated: {stats['titles']}")
print(f"Meta descriptions truncated: {stats['metas']}")
print(f"H1 tags added: {stats['h1']}")
print(f"Gumroad links fixed: content updated")
print(f"GA placeholder IDs fixed: {stats['ga']}")
print(f"Viewport tags added: {stats['viewport']}")
print(f"Canonical tags added: {stats['canonical']}")
