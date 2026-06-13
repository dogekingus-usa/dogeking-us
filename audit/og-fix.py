#!/usr/bin/env python3
"""Re-add OG images ONLY to real content articles (not utility pages)."""

import os, re

ARTICLES_DIR = r"C:\Users\SAMPC\.openclaw\content\dogeking.us\articles"
UTILITY_KEYWORDS = ['404', 'about', 'contact', 'default', 'health', 'checklist', 'preview-card', 'thank-you', 
                    'crypto-bundle', 'template', 'nav-component', 'cta-snippets', 'og-template',
                    'portfolio', 'tools-comparison', 'fetched-live', 'disclaimer', 'privacy-policy',
                    'affiliate', 'lead-magnet', 'sales-cta', 'sales-thank', 'ecosystem-section',
                    'all-articles']

CATEGORY_IMAGES = {
    'meme': 'meme-coin', 'memecoin': 'meme-coin', 'doge': 'meme-coin', 'pepe': 'meme-coin',
    'bonk': 'meme-coin', 'wif': 'meme-coin', 'shib': 'meme-coin',
    'solana': 'solana', 'sol': 'solana',
    'eth': 'ethereum', 'ethereum': 'ethereum',
    'defi': 'defi', 'yield': 'defi', 'lend': 'defi',
    'wallet': 'wallet', 'stake': 'wallet',
    'trade': 'trading', 'exchange': 'trading', 'buy': 'trading', 'sell': 'trading',
    'tax': 'security', 'security': 'security', 'safe': 'security', 'scam': 'security', 'risk': 'security',
    'guide': 'guide', 'beginner': 'guide', 'intro': 'guide',
    'airdrop': 'airdrop',
    'nft': 'nft',
    'dogeking': 'dogeking', 'dking': 'dogeking', 'dk': 'dogeking',
    'price': 'trading', 'prediction': 'trading',
    'chart': 'trading', 'candle': 'trading',
    'portfolio': 'trading', 'invest': 'trading',
    'blockchain': 'solana', 'crypto': 'default',
}

fixed = 0
for root, dirs, files in os.walk(ARTICLES_DIR):
    for f in files:
        if not f.endswith('.html'):
            continue
        if any(kw in f.lower() for kw in UTILITY_KEYWORDS):
            continue
        
        fp = os.path.join(root, f)
        rel = os.path.relpath(fp, ARTICLES_DIR)
        
        with open(fp, 'r', encoding='utf-8', errors='replace') as fh:
            content = fh.read()
        
        if 'og:image' in content:
            continue  # Already has OG image
        
        original = content
        
        # Determine category from filename
        fname = f.lower()
        image_cat = 'default'
        for keyword, category in CATEGORY_IMAGES.items():
            if keyword in fname:
                image_cat = category
                break
        
        og_block = f'''
<meta property="og:image" content="https://dogeking.us/images/og-{image_cat}.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:type" content="article" />'''
        
        content = content.replace('</head>', og_block + '\n</head>', 1)
        
        with open(fp, 'w', encoding='utf-8') as fh:
            fh.write(content)
        fixed += 1
        
        if fixed <= 5:
            print(f"  OG: {rel} (category: {image_cat})")

print(f"\nOG images added to {fixed} real articles")
