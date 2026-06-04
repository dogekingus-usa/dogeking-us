const fs = require('fs');
const path = require('path');
const dir = 'C:/content-sites/dogeking.us/articles';

const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));
let fixed = 0;

files.forEach(f => {
  const fp = path.join(dir, f);
  let html = fs.readFileSync(fp, 'utf8');
  if (html.charCodeAt(0) === 0xFEFF) html = html.slice(1);
  if (html.includes('crown-design-system')) return;
  
  html = html.replace('</head>',
    '  <link rel="preconnect" href="https://fonts.googleapis.com">\n' +
    '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n' +
    '  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@400;600;700;800&display=swap">\n' +
    '  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@400;600;700;800&display=swap" rel="stylesheet" media="print" onload="this.media=\'all\'">\n' +
    '  <link rel="stylesheet" href="/crown-design-system.css">\n' +
    '</head>'
  );
  if (!html.includes('theme-dogeking')) html = html.replace('<body', '<body class="theme-dogeking"');
  
  const nav = '<div class="nav-bar" style="background:rgba(10,10,26,0.95);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border-bottom:1px solid rgba(255,215,0,0.1);padding:10px 0;position:sticky;top:0;z-index:1000;box-shadow:0 2px 20px rgba(0,0,0,0.3);"><div style="max-width:1200px;margin:0 auto;padding:0 20px;display:flex;justify-content:space-between;align-items:center;"><a href="/" style="font-family:\'Playfair Display\',serif;font-size:1.3rem;font-weight:700;color:#FFD700;display:flex;align-items:center;gap:8px;text-decoration:none;letter-spacing:1px;">👑 DogeKing</a><div style="display:flex;gap:2px;"><a href="/" style="padding:6px 14px;border-radius:8px;color:#c0c0e0;font-size:0.85rem;text-decoration:none;">Home</a><a href="/all-articles.html" style="padding:6px 14px;border-radius:8px;color:#c0c0e0;font-size:0.85rem;text-decoration:none;">Articles</a><a href="/products.html" style="padding:6px 14px;border-radius:8px;color:#c0c0e0;font-size:0.85rem;text-decoration:none;">Products</a><a href="/crypto-bundle.html" style="padding:6px 14px;border-radius:8px;background:linear-gradient(135deg,#FFD700,#FF8C00);color:#0a0a1a;font-size:0.85rem;font-weight:600;text-decoration:none;margin-left:8px;">Get Bundle</a></div></div></div>';
  if (!html.includes('nav-bar')) html = html.replace('<body class="theme-dogeking">', '<body class="theme-dogeking">\n' + nav);
  
  const footer = '<footer style="background:#0a0a1a;border-top:1px solid rgba(255,255,255,0.05);padding:30px 0;margin-top:60px;"><div style="max-width:1200px;margin:0 auto;padding:0 20px;text-align:center;"><div style="display:flex;justify-content:center;gap:28px;flex-wrap:wrap;margin-bottom:16px;"><a href="/privacy.html" style="color:#8080a0;font-size:0.85rem;text-decoration:none;">Privacy</a><a href="/contact.html" style="color:#8080a0;font-size:0.85rem;text-decoration:none;">Contact</a><a href="/disclaimer.html" style="color:#8080a0;font-size:0.85rem;text-decoration:none;">Disclaimer</a><a href="/feed.xml" style="color:#8080a0;font-size:0.85rem;text-decoration:none;">RSS Feed</a></div><p style="color:#404060;font-size:0.75rem;">© 2026 DogeKing.us — Crypto Insights for the Bold. Not financial advice. DYOR.</p></div></footer>';
  html = html.replace('</body>', footer + '\n</body>');
  
  fs.writeFileSync(fp, html, 'utf8');
  fixed++;
});

console.log(fixed);
