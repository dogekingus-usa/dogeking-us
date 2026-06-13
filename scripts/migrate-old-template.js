// Migrate old segoe template articles to crown theme
const fs = require('fs');
const path = require('path');

const dir = 'C:/content-sites/dogeking.us/articles';
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));

const systemPages = ['404','about','checkout','contact','privacy','products','thank-you','all-articles',
  'crypto-bundle','template','nav-component-enhanced','preview-card','cta-snippets','fetched-live',
  'ecosystem-section','sales-cta-overlay','sales-thank-you','dogeking-article-og-template',
  'affiliate','dynamic-loader'];

let migrated = 0;
let alreadyCrown = 0;
let skipped = 0;

files.forEach(f => {
  const slug = f.replace('.html','');
  if (systemPages.includes(slug)) { skipped++; return; }
  
  const fp = path.join(dir, f);
  let html = fs.readFileSync(fp, 'utf8');
  if (html.charCodeAt(0) === 0xFEFF) html = html.slice(1);
  
  // Skip if already crown theme
  if (html.includes('theme-dogeking') || html.includes('crown-design-system')) { alreadyCrown++; return; }
  
  // Skip if not segoe template (other template type)
  if (!html.includes('Segoe UI')) { skipped++; return; }
  
  let modified = false;
  
  // 1. Add crown-design-system.css link (before </head>)
  if (!html.includes('crown-design-system')) {
    html = html.replace('</head>', 
      '  <link rel="preconnect" href="https://fonts.googleapis.com">\n' +
      '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n' +
      '  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@400;600;700;800&display=swap">\n' +
      '  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@400;600;700;800&display=swap" rel="stylesheet" media="print" onload="this.media=\'all\'">\n' +
      '  <link rel="stylesheet" href="/crown-design-system.css">\n' +
      '</head>'
    );
    modified = true;
  }
  
  // 2. Replace body inline style with crown classes
  if (html.includes('Segoe UI') && !html.includes('theme-dogeking')) {
    // Add class to body
    html = html.replace('<body>', '<body class="theme-dogeking">');
    
    // Replace the inline body style
    html = html.replace(
      /body\s*\{[^}]*font-family:\s*'Segoe UI'[^}]*\}/g,
      '/* body styled via crown-design-system.css */'
    );
    modified = true;
  }
  
  // 3. Fix container class to match crown
  if (html.includes('class="container"') && !html.includes('max-width: 1200px')) {
    html = html.replace(
      /\.container\s*\{[^}]*max-width:\s*780px[^}]*\}/g,
      '.article-container { max-width: 780px; margin: 0 auto; }'
    );
    html = html.replace(/class="container"/g, 'class="article-container"');
    modified = true;
  }
  
  if (modified) {
    // 4. Add a crown-style header bar at the top
    if (!html.includes('class="nav-bar"')) {
      const crownHeader = 
        '<div class="nav-bar" style="background:rgba(10,10,26,0.9);backdrop-filter:blur(20px);border-bottom:1px solid rgba(255,255,255,0.05);padding:12px 0;position:sticky;top:0;z-index:100;">' +
        '<div style="max-width:1200px;margin:0 auto;padding:0 20px;display:flex;justify-content:space-between;align-items:center;">' +
        '<a href="/" style="font-family:\'Playfair Display\',serif;font-size:1.4rem;font-weight:700;color:#f5f5ff;display:flex;align-items:center;gap:8px;text-decoration:none;">ðŸÅ“Ëœ DogeKing</a>' +
        '<div style="display:flex;gap:4px;">' +
        '<a href="/" style="padding:8px 16px;border-radius:8px;color:#8080a0;font-size:0.9rem;text-decoration:none;">Home</a>' +
        '<a href="/all-articles.html" style="padding:8px 16px;border-radius:8px;color:#8080a0;font-size:0.9rem;text-decoration:none;">Articles</a>' +
        '<a href="/products.html" style="padding:8px 16px;border-radius:8px;color:#8080a0;font-size:0.9rem;text-decoration:none;">Products</a>' +
        '</div></div></div>';
      html = html.replace('<body class="theme-dogeking">', '<body class="theme-dogeking">\n' + crownHeader);
      modified = true;
    }
    
    // 5. Add crown footer
    if (!html.includes('DogeKing</div></div>')) {
      const crownFooter = 
        '<footer style="background:#0a0a1a;border-top:1px solid rgba(255,255,255,0.05);padding:24px 0;margin-top:40px;text-align:center;">' +
        '<div style="max-width:1200px;margin:0 auto;padding:0 20px;">' +
        '<div style="display:flex;justify-content:center;gap:24px;flex-wrap:wrap;margin-bottom:12px;">' +
        '<a href="/privacy.html" style="color:#8080a0;font-size:0.85rem;text-decoration:none;">Privacy</a>' +
        '<a href="/contact.html" style="color:#8080a0;font-size:0.85rem;text-decoration:none;">Contact</a>' +
        '<a href="/disclaimer.html" style="color:#8080a0;font-size:0.85rem;text-decoration:none;">Disclaimer</a>' +
        '<a href="/feed.xml" style="color:#8080a0;font-size:0.85rem;text-decoration:none;">RSS Feed</a>' +
        '</div>' +
        '<p style="color:#606080;font-size:0.8rem;">Â© 2026 DogeKing. All rights reserved.</p>' +
        '</div></footer>';
      html = html.replace('</body>', crownFooter + '\n</body>');
      modified = true;
    }
    
    fs.writeFileSync(fp, html, 'utf8');
    migrated++;
  }
});

console.log(`Migrated to crown theme: ${migrated}`);
console.log(`Already crown: ${alreadyCrown}`);
console.log(`Skipped: ${skipped}`);
