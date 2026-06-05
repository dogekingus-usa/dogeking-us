// UNIVERSAL crown theme migration ” handles ALL template types
const fs = require('fs');
const path = require('path');

const dir = 'C:/content-sites/dogeking.us/articles';
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));

// System pages that don't need crown theme (separate templates)
const systemPages = ['404','about','checkout','contact','privacy','products','thank-you',
  'template','nav-component-enhanced','preview-card','cta-snippets','fetched-live',
  'ecosystem-section','sales-cta-overlay','sales-thank-you','dogeking-article-og-template',
  'affiliate','dynamic-loader'];

const CROWN_HEAD = 
  '<link rel="preconnect" href="https://fonts.googleapis.com">\n' +
  '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n' +
  '  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@400;600;700;800&display=swap">\n' +
  '  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@400;600;700;800&display=swap" rel="stylesheet" media="print" onload="this.media=\'all\'">\n' +
  '  <link rel="stylesheet" href="/crown-design-system.css">\n';

const NAV_BAR = 
  '<div class="nav-bar" style="background:rgba(10,10,26,0.95);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border-bottom:1px solid rgba(255,215,0,0.1);padding:10px 0;position:sticky;top:0;z-index:1000;box-shadow:0 2px 20px rgba(0,0,0,0.3);">' +
  '<div style="max-width:1200px;margin:0 auto;padding:0 20px;display:flex;justify-content:space-between;align-items:center;">' +
  '<a href="/" style="font-family:\'Playfair Display\',serif;font-size:1.3rem;font-weight:700;color:#FFD700;display:flex;align-items:center;gap:8px;text-decoration:none;letter-spacing:1px;">�œ˜ DogeKing</a>' +
  '<div style="display:flex;gap:2px;">' +
  '<a href="/" style="padding:6px 14px;border-radius:8px;color:#c0c0e0;font-size:0.85rem;text-decoration:none;transition:all 0.2s;">Home</a>' +
  '<a href="/all-articles.html" style="padding:6px 14px;border-radius:8px;color:#c0c0e0;font-size:0.85rem;text-decoration:none;transition:all 0.2s;">Articles</a>' +
  '<a href="/products.html" style="padding:6px 14px;border-radius:8px;color:#c0c0e0;font-size:0.85rem;text-decoration:none;transition:all 0.2s;">Products</a>' +
  '<a href="/crypto-bundle.html" style="padding:6px 14px;border-radius:8px;background:linear-gradient(135deg,#FFD700,#FF8C00);color:#0a0a1a;font-size:0.85rem;font-weight:600;text-decoration:none;transition:all 0.2s;margin-left:8px;">Get Bundle</a>' +
  '</div></div></div>';

const FOOTER = 
  '<footer style="background:#0a0a1a;border-top:1px solid rgba(255,255,255,0.05);padding:30px 0;margin-top:60px;">' +
  '<div style="max-width:1200px;margin:0 auto;padding:0 20px;text-align:center;">' +
  '<div style="display:flex;justify-content:center;gap:28px;flex-wrap:wrap;margin-bottom:16px;">' +
  '<a href="/privacy.html" style="color:#8080a0;font-size:0.85rem;text-decoration:none;transition:color 0.2s;">Privacy</a>' +
  '<a href="/contact.html" style="color:#8080a0;font-size:0.85rem;text-decoration:none;transition:color 0.2s;">Contact</a>' +
  '<a href="/disclaimer.html" style="color:#8080a0;font-size:0.85rem;text-decoration:none;transition:color 0.2s;">Disclaimer</a>' +
  '<a href="/feed.xml" style="color:#8080a0;font-size:0.85rem;text-decoration:none;transition:color 0.2s;">RSS Feed</a>' +
  '</div>' +
  '<div style="display:flex;justify-content:center;gap:20px;flex-wrap:wrap;margin-bottom:12px;">' +
  '<span style="color:#606080;font-size:0.8rem;">�œ˜ 333+ Free Crypto Guides</span>' +
  '<span style="color:#606080;font-size:0.8rem;">� 4.8/5 from 500+ Traders</span>' +
  '</div>' +
  '<p style="color:#404060;font-size:0.75rem;">© 2026 DogeKing.us ” Crypto Insights for the Bold. Not financial advice. DYOR.</p>' +
  '</div></footer>';

let migrated = 0;
let skipped = 0;

files.forEach(f => {
  const slug = f.replace('.html','');
  if (systemPages.includes(slug)) { skipped++; return; }
  
  const fp = path.join(dir, f);
  let html = fs.readFileSync(fp, 'utf8');
  if (html.charCodeAt(0) === 0xFEFF) html = html.slice(1);
  
  // Skip if already has crown theme
  if (html.includes('crown-design-system')) { skipped++; return; }
  
  let modified = false;
  
  // 1. Add crown CSS + fonts before </head>
  html = html.replace('</head>', '  ' + CROWN_HEAD + '</head>');
  modified = true;
  
  // 2. Add theme class to body
  if (html.includes('<body')) {
    html = html.replace('<body', '<body class="theme-dogeking"');
  } else {
    html = html.replace('<body>', '<body class="theme-dogeking">');
  }
  
  // 3. Add nav bar after <body>
  if (!html.includes('nav-bar')) {
    html = html.replace('<body class="theme-dogeking">', '<body class="theme-dogeking">\n' + NAV_BAR);
  }
  
  // 4. Add footer before </body>
  if (html.includes('</footer>') || html.includes('© 2026')) {
    // Replace existing footer with crown footer
    html = html.replace(/<footer[^>]*>[\s\S]*?<\/footer>/gi, FOOTER);
  } else if (!html.includes('DogeKing</div></div></footer>')) {
    html = html.replace('</body>', FOOTER + '\n</body>');
  }
  
  // 5. Remove dark mode toggles and old theme switchers
  html = html.replace(/<button[^>]*class="theme-toggle[^>]*>.*?<\/button>/gi, '');
  html = html.replace(/for="theme-toggle[^"]*"/gi, '');
  
  // 6. Fix any broken relative URLs for articles
  html = html.replace(/href="\/([^\/][^"]*\.html)"/g, (match, p1) => {
    if (p1.startsWith('articles/')) return match;
    if (p1 === 'index.html' || p1 === 'all-articles.html' || p1 === 'privacy.html' || 
        p1 === 'contact.html' || p1 === 'disclaimer.html' || p1 === 'products.html' ||
        p1 === 'crypto-bundle.html' || p1 === 'checkout.html' || p1 === 'thank-you.html' ||
        p1 === 'about.html') return match;
    return `href="/articles/${p1}"`;
  });
  
  // 7. Add social proof badge in content area
  if (html.includes('class="article-card"') && !html.includes('article-card-icon')) {
    // This is a listing page, not an article - skip content changes
  } else if (html.includes('<article') || html.includes('class="content"') && !html.includes('social-proof')) {
    html = html.replace(
      /(<div class="[^"]*content[^"]*"|class="post-content"|<article)/,
      '<div style="background:rgba(255,215,0,0.05);border:1px solid rgba(255,215,0,0.15);border-radius:12px;padding:16px 20px;margin-bottom:24px;display:flex;align-items:center;gap:12px;flex-wrap:wrap;">' +
      '<span style="font-size:1.2rem;">�œ˜</span>' +
      '<span style="font-size:0.85rem;color:#c0c0e0;">Part of <strong style="color:#FFD700;">333+ free crypto guides</strong> on DogeKing</span>' +
      '<a href="/crypto-bundle.html" style="margin-left:auto;padding:6px 16px;background:linear-gradient(135deg,#FFD700,#FF8C00);color:#0a0a1a;border-radius:8px;font-size:0.8rem;font-weight:600;text-decoration:none;white-space:nowrap;">Level Up �™</a>' +
      '</div>\n$1'
    );
  }
  
  fs.writeFileSync(fp, html, 'utf8');
  migrated++;
});

console.log(`�œŠ RESULTS:`);
console.log(`   Migrated to crown theme: ${migrated}`);
console.log(`   Skipped (already crown or system): ${skipped}`);
console.log(`   Total processed: ${migrated + skipped}`);
