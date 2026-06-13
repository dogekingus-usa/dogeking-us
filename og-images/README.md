# DogeKing Social Preview Images (OG Images)

## Strategy
Since we cannot generate actual PNG/JPEG images via shell/exec, we use two approaches:

### Approach 1: Dynamic OG Image Page (Recommended)
Create a dedicated `/og-image.html` page that accepts URL parameters and renders a styled social preview card.
Articles reference this page via OG meta tags using `og:image` pointing to the page URL.

### Approach 2: Static SVG placeholder
Inline SVG-based OG image references for fallback.

---

## OG Image Meta Tag Template

Add this to every article's `<head>` section:

```html
<!-- Open Graph -->
<meta property="og:title" content="ARTICLE_TITLE | DogeKing" />
<meta property="og:description" content="ARTICLE_DESCRIPTION" />
<meta property="og:image" content="https://dogeking.us/og-images/preview-card.html?title=ARTICLE_TITLE&cat=CATEGORY" />
<meta property="og:url" content="https://dogeking.us/ARTICLE_FILENAME" />
<meta property="og:type" content="article" />
<meta property="og:site_name" content="DogeKing.us" />

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="ARTICLE_TITLE | DogeKing" />
<meta name="twitter:description" content="ARTICLE_DESCRIPTION" />
<meta name="twitter:image" content="https://dogeking.us/og-images/preview-card.html?title=ARTICLE_TITLE&cat=CATEGORY" />
```

## Implementation Status
- [x] OG image concept defined
- [x] OG meta tags added to all new DogeKing articles
- [ ] Deploy preview-card.html to Cloudflare Pages
- [ ] Update all existing 119 files with OG tags (bulk job needed)
