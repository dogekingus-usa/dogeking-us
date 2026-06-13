#!/usr/bin/env python3
"""Add internal links and OG images to linkless and imageless articles."""

import os, re, random

BASE_DIR = r"C:\Users\SAMPC\.openclaw\content\dogeking.us"
ARTICLES_DIR = os.path.join(BASE_DIR, "articles")

# Build a list of all article titles and their URLs
articles = []
for root, dirs, files in os.walk(ARTICLES_DIR):
    for f in files:
        if not f.endswith('.html') or f == 'all-articles.html':
            continue
        fp = os.path.join(root, f)
        rel = os.path.relpath(fp, BASE_DIR).replace('\\', '/')
        with open(fp, 'r', encoding='utf-8', errors='replace') as fh:
            content = fh.read()
        
        title_match = re.search(r'<title>([^<]+)</title>', content, re.IGNORECASE)
        title = title_match.group(1).strip() if title_match else f.replace('.html', '').replace('-', ' ').title()
        # Clean title for display
        title = re.sub(r'\s*\|\s*Doge\s*King.*$', '', title).strip()
        title = re.sub(r'\s*[-–]\s*Doge.*$', '', title).strip()
        
        articles.append({
            'path': '/' + rel,
            'title': title,
            'fp': fp,
            'content': content,
            'has_links': len(re.findall(r'href=["\']/(?!http)[^"\']+\.html["\']', content)) > 0,
            'has_og_image': 'og:image' in content,
            'has_tldr': 'TL;DR' in content or 'Key Takeaways' in content or 'tl;dr' in content.lower(),
            'word_count': len(re.sub(r'<[^>]+>', ' ', content).split()),
        })

print(f"Total articles: {len(articles)}")

# Find linkless articles (genuine content, not templates)
linkless = [a for a in articles if not a['has_links'] and a['word_count'] > 100 and 'template' not in a['path'] and 'snippet' not in a['path'] and 'component' not in a['path'] and 'preview' not in a['path'] and 'default' not in a['path']]
print(f"Linkless content articles: {len(linkless)}")

# Find imageless articles (no og:image)
imageless = [a for a in articles if not a['has_og_image'] and a['word_count'] > 100 and 'template' not in a['path'] and 'snippet' not in a['path'] and 'component' not in a['path']]
print(f"Imageless content articles: {len(imageless)}")

# Find articles without TL;DR
no_tldr = [a for a in articles if not a['has_tldr'] and a['word_count'] > 500]
print(f"Articles without TL;DR: {len(no_tldr)}")

total_fixes = 0

# FIX 1: Add internal links to linkless articles
print("\n--- Adding internal links to linkless articles ---")
for article in linkless[:30]:  # Limit to 30 for this pass
    content = article['content']
    original = content
    
    # Find 2-3 related articles (by keyword overlap)
    article_words = set(re.findall(r'\b[a-z]{4,}\b', article['title'].lower()))
    scored = []
    for other in articles:
        if other['path'] == article['path']:
            continue
        other_words = set(re.findall(r'\b[a-z]{4,}\b', other['title'].lower()))
        overlap = len(article_words & other_words)
        if overlap > 0:
            scored.append((overlap, other))
    
    scored.sort(key=lambda x: -x[0])
    related = [s[1] for s in scored[:3] if s[0] > 0]
    
    if related:
        links_html = '\n\n<div class="related-articles">\n<h3>Related Articles</h3>\n<ul>\n'
        for r in related:
            clean_title = r['title']
            if len(clean_title) > 60:
                clean_title = clean_title[:57] + '...'
            links_html += f'<li><a href="{r["path"]}">{clean_title}</a></li>\n'
        links_html += '</ul>\n</div>\n'
        
        # Insert before </body> or at end
        if '</body>' in content:
            content = content.replace('</body>', links_html + '\n</body>', 1)
        else:
            content += '\n' + links_html
        
        with open(article['fp'], 'w', encoding='utf-8') as f:
            f.write(content)
        total_fixes += 1
        print(f"  + Links added: {article['path']}")

# FIX 2: Add OG image tag to imageless articles
print("\n--- Adding OG image tags to imageless articles ---")
for article in imageless[:80]:  # Limit
    content = article['content']
    original = content
    
    if 'og:image' in content:
        continue
    
    # Generate a meaningful OG image URL based on topic
    title_lower = article['title'].lower()
    image_slug = 'default'
    if 'meme' in title_lower:
        image_slug = 'meme-coin'
    elif 'solana' in title_lower:
        image_slug = 'solana'
    elif 'eth' in title_lower or 'ethereum' in title_lower:
        image_slug = 'ethereum'
    elif 'defi' in title_lower or 'yield' in title_lower:
        image_slug = 'defi'
    elif 'wallet' in title_lower or 'stake' in title_lower:
        image_slug = 'wallet'
    elif 'trade' in title_lower or 'exchange' in title_lower or 'buy' in title_lower:
        image_slug = 'trading'
    elif 'tax' in title_lower or 'security' in title_lower or 'safe' in title_lower:
        image_slug = 'security'
    elif 'guide' in title_lower or 'beginner' in title_lower:
        image_slug = 'guide'
    elif 'airdrop' in title_lower:
        image_slug = 'airdrop'
    elif 'nft' in title_lower:
        image_slug = 'nft'
    
    og_tag = f'\n<meta property="og:image" content="https://dogeking.us/images/og-{image_slug}.png">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n<meta property="og:type" content="article">'
    
    # Insert before </head>
    if '</head>' in content:
        content = content.replace('</head>', og_tag + '\n</head>', 1)
        with open(article['fp'], 'w', encoding='utf-8') as f:
            f.write(content)
        total_fixes += 1
        print(f"  + OG image: {article['path']}")

# FIX 3: Add TL;DR to articles over 500 words without one
print("\n--- Adding TL;DR summaries ---")
for article in no_tldr[:20]:  # Limit
    content = article['content']
    original = content
    
    # Extract first meaningful sentence
    text = re.sub(r'<[^>]+>', ' ', content)
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Find first 2 sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    key_points = []
    for s in sentences:
        s = s.strip()
        if len(s) > 30 and len(key_points) < 3:
            s_clean = s.replace('"', "'").strip()
            if len(s_clean) > 120:
                s_clean = s_clean[:117] + '...'
            key_points.append(s_clean)
    
    if key_points:
        tldr_html = '\n<div class="tldr-box" style="background:#f0f4ff;border:1px solid #cce;border-radius:8px;padding:16px;margin:20px 0">\n'
        tldr_html += '<strong style="color:#445;font-size:1.1em">📋 Key Takeaways</strong>\n<ul>\n'
        for kp in key_points:
            tldr_html += f'<li>{kp}</li>\n'
        tldr_html += '</ul>\n</div>\n'
        
        # Insert after <h1> or before first <p>
        h1_match = re.search(r'<h1[^>]*>.*?</h1>', content, re.DOTALL)
        if h1_match:
            content = content.replace(h1_match.group(0), h1_match.group(0) + tldr_html, 1)
        else:
            p_match = re.search(r'<p[^>]*>', content)
            if p_match:
                content = content.replace(p_match.group(0), tldr_html + '\n' + p_match.group(0), 1)
        
        with open(article['fp'], 'w', encoding='utf-8') as f:
            f.write(content)
        total_fixes += 1
        print(f"  + TL;DR: {article['path']}")

print(f"\nTotal fixes applied: {total_fixes}")
print("Done.")
