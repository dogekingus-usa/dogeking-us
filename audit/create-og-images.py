#!/usr/bin/env python3
"""Create placeholder OG image SVGs for social sharing."""
import os

img_dir = r"C:\content-sites\dogeking.us\images"
os.makedirs(img_dir, exist_ok=True)

categories = {
    "default": "Crypto Insights for the Bold",
    "meme-coin": "Meme Coin Trading Guides",
    "solana": "Solana Ecosystem Guides",
    "ethereum": "Ethereum & Layer 2 Guides",
    "defi": "DeFi & Yield Farming",
    "wallet": "Crypto Wallet Guides",
    "trading": "Trading Strategies",
    "security": "Security & Tax Guides",
    "guide": "Crypto Beginner Guides",
    "airdrop": "Airdrop Guides",
    "nft": "NFT & Gaming Guides",
    "dogeking": "Doge King Token Guides",
}

for cat, subtitle in categories.items():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1a0a2e"/>
      <stop offset="100%" stop-color="#0a0a1a"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="630" fill="url(#bg)"/>
  <rect x="80" y="80" width="1040" height="470" rx="20" fill="none" stroke="rgba(255,215,0,0.15)" stroke-width="2"/>
  <text x="600" y="260" font-family="Georgia, serif" font-size="80" font-weight="bold" fill="#FFD700" text-anchor="middle">Doge King</text>
  <text x="600" y="330" font-family="Arial, sans-serif" font-size="32" fill="#8080c0" text-anchor="middle">{subtitle}</text>
  <text x="600" y="480" font-family="Arial, sans-serif" font-size="20" fill="#505080" text-anchor="middle">dogeking.us</text>
  <circle cx="160" cy="160" r="40" fill="rgba(255,215,0,0.05)"/>
  <circle cx="1040" cy="160" r="40" fill="rgba(255,215,0,0.05)"/>
  <circle cx="160" cy="470" r="40" fill="rgba(255,215,0,0.05)"/>
  <circle cx="1040" cy="470" r="40" fill="rgba(255,215,0,0.05)"/>
</svg>'''
    
    fp = os.path.join(img_dir, f"og-{cat}.svg")
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"  Created: og-{cat}.svg")

print(f"\nDone — {len(categories)} OG images created in {img_dir}")
