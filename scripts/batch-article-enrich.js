const fs = require('fs');
const path = require('path');

const ARTICLES_DIR = 'C:/content-sites/dogeking.us/articles';
const DATA_FILE = 'C:/content-sites/dogeking.us/articles-data.js';
const SITE_URL = 'https://dogeking.us';
const AUTHOR_NAME = 'Samuel Pason';
const AUTHOR_URL = 'https://dogeking.us/about.html';

const dataJs = fs.readFileSync(DATA_FILE, 'utf8');
const match = dataJs.match(/const articles = (\[[\s\S]*?\]);/);
if (!match) { console.error('Could not parse articles-data.js'); process.exit(1); }

const raw = match[1];
let articles = [];

// Parse each article object from the JS literal format
const objRegex = /\{\s*title:\s*['"]([^'"]+?)['"]\s*,\s*slug:\s*['"]([^'"]+?)['"]\s*,\s*category:\s*['"]([^'"]+?)['"]\s*,\s*date:\s*['"]([^'"]+?)['"]\s*,\s*readTime:\s*['"]([^'"]+?)['"]\s*,\s*excerpt:\s*['"]([^'"]*?)['"]\s*/g;
let objMatch;
while ((objMatch = objRegex.exec(raw)) !== null) {
  articles.push({
    title: objMatch[1],
    slug: objMatch[2],
    category: objMatch[3],
    date: objMatch[4],
    readTime: objMatch[5],
    excerpt: objMatch[6] || ''
  });
}

if (articles.length === 0) {
  console.error('Regex parse failed');
  process.exit(1);
}

console.log(`Parsed ${articles.length} articles from data file`);

const articleMap = {};
articles.forEach(a => { if (a.slug) articleMap[a.slug] = a; });

const files = fs.readdirSync(ARTICLES_DIR).filter(f => f.endsWith('.html'));
console.log(`Found ${files.length} HTML files`);

let updated = 0;
let skippedHasLD = 0;
let skippedNoMeta = 0;
let errors = 0;

files.forEach((filename) => {
  const filePath = path.join(ARTICLES_DIR, filename);
  try {
    let html = fs.readFileSync(filePath, 'utf8');
    if (html.charCodeAt(0) === 0xFEFF) html = html.slice(1);
    
    const slug = filename.replace('.html', '');
    const meta = articleMap[slug] || null;
    
    if (!meta) { skippedNoMeta++; return; }
    if (html.includes('"@type":"Article"') || html.includes('application/ld+json')) { skippedHasLD++; return; }
    
    const title = (meta.title || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    const excerpt = (meta.excerpt || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;').replace(/>/g, '&gt;');
    const date = meta.date || '2026';
    const category = meta.category || 'crypto';
    const articleUrl = `${SITE_URL}/articles/${slug}.html`;
    
    const isNewTemplate = html.includes('theme-dogeking');
    const hasCanonical = html.includes('rel="canonical"');
    const hasGoogleFonts = html.includes('fonts.googleapis.com');
    
    // 1. Add canonical if missing
    if (!hasCanonical) html = html.replace('</head>', `\n<link rel="canonical" href="${articleUrl}">\n</head>`);
    
    // 2. Optimize Google Fonts
    if (hasGoogleFonts && !html.includes('media="print"')) {
      html = html.replace(
        /<link href="(https:\/\/fonts\.googleapis\.com\/css2\?[^"]+)" rel="stylesheet">/g,
        '<link rel="preload" as="style" href="$1">\n<link href="$1" rel="stylesheet" media="print" onload="this.media=\'all\'">\n<noscript><link href="$1" rel="stylesheet"></noscript>'
      );
    }
    
    // 3. Add JSON-LD
    const jsonld = `\n<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "${title}",
  "description": "${excerpt.substring(0, 200)}",
  "author": { "@type": "Person", "name": "${AUTHOR_NAME}", "url": "${AUTHOR_URL}" },
  "publisher": {
    "@type": "Organization",
    "name": "DogeKing",
    "logo": { "@type": "ImageObject", "url": "${SITE_URL}/assets/crown-logo.svg" }
  },
  "datePublished": "${date}",
  "dateModified": "${date}",
  "mainEntityOfPage": { "@type": "WebPage", "@id": "${articleUrl}" },
  "image": "${SITE_URL}/assets/og-image.svg",
  "articleSection": "${category}"
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "${SITE_URL}" },
    { "@type": "ListItem", "position": 2, "name": "Articles", "item": "${SITE_URL}/all-articles.html" },
    { "@type": "ListItem", "position": 3, "name": "${title.substring(0, 110)}", "item": "${articleUrl}" }
  ]
}
</script>`;
    html = html.replace('</head>', `${jsonld}\n</head>`);
    
    // 4. Author byline for new template articles
    if (isNewTemplate && html.includes('class="meta"') && !html.includes('Samuel Pason') && !html.includes('author-byline')) {
      html = html.replace(
        /(<div class="meta">[^<]*<\/div>)/,
        '$1\n<div class="author-byline" style="font-size:0.85rem;color:var(--text-muted);margin-top:8px;">By <a href="/about.html" style="color:var(--accent);">Samuel Pason</a> &middot; DogeKing Editor</div>'
      );
    }
    
    // 5. Add font-display swap to inline styles
    if (!html.includes('font-display: swap') && html.includes('<style>')) {
      html = html.replace('<style>', '<style>\nbody, h1, h2, h3, h4, h5, h6 { font-display: swap; }');
    }
    
    fs.writeFileSync(filePath, html, 'utf8');
    updated++;
  } catch(e) {
    console.error(`Error processing ${filename}: ${e.message}`);
    errors++;
  }
});

console.log(`\nResults: Updated=${updated}, Already had LD=${skippedHasLD}, No meta=${skippedNoMeta}, Errors=${errors}`);
