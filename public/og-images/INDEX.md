# DogeKing OG Image Templates — Index

**Last updated:** 2026-05-25 22:18 ICT
**Total templates:** 12 (1 default + 11 article-specific)
**Location:** /og-images/ (staged at workspace-main/content-sites/dogeking-us/og-images/)

## Template List

| # | Template | Article | Status |
|:-:|:---------|:--------|:------:|
| 1 | default.html | Generic fallback for all pages | ✅ COMPLETE |
| 2 | how-to-buy-dogeking.html | How to Buy DogeKing ($DKING) Step-by-Step Guide | ✅ COMPLETE |
| 3 | dogeking-tokenomics-explained.html | DogeKing Tokenomics Explained 2026 | ✅ COMPLETE |
| 4 | how-to-sell-dogeking.html | How to Sell DogeKing ($DKING) Complete Guide 2026 | ✅ COMPLETE |
| 5 | dogeking-roadmap-2026.html | DogeKing Roadmap 2026 — What's Next | ✅ COMPLETE |
| 6 | dogeking-vs-solana-meme-coins.html | DogeKing vs Other Solana Meme Coins Comparison | ✅ COMPLETE |
| 7 | dogeking-price-prediction.html | DogeKing Price Prediction 2026-2030 | ✅ COMPLETE |
| 8 | how-to-stake-dogeking.html | How to Stake DogeKing ($DKING) Guide 2026 | ✅ COMPLETE |
| 9 | dogeking-community-guide-join-the-kingdom.html | DogeKing Community Guide — Join the Kingdom | ✅ COMPLETE |
| 10 | dogeking-community-guide.html | DogeKing Community Guide — How to Join | ✅ COMPLETE |
| 11 | dogeking-community-guide-telegram-twitter-discord.html | DogeKing Community Guide — Telegram, Twitter & Discord | ✅ COMPLETE |
| 12 | dogeking-wallet-setup.html | DogeKing Wallet Setup Guide | ✅ COMPLETE |

## Usage

Each article's `<head>` references its OG template like:
```html
<meta property="og:image" content="https://dogeking.us/og-images/{template-name}.html">
```

These are served as HTML pages that social media platforms (Twitter/X, Facebook, LinkedIn, Discord) will render as 1200×630 preview cards.

## Notes

- Templates use the same design system: dark gradient background, gold crown accents, serif headings
- Each template shows article-specific content with visual data (stats, roadmaps, comparisons)
- All templates are 1200×630 HTML pages — no server-side rendering needed
- Screenshot at 1200×630 → PNG for production attachment (Commander task)
