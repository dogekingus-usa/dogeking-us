const fs = require('fs');
const dir = 'C:/content-sites/dogeking.us/articles';

// Only remove sticky bar from pages that have their OWN site-nav
const pages = ['about','checkout','disclaimer','products','thank-you','all-articles','crypto-bundle','404'];

pages.forEach(slug => {
  const fp = dir + '/' + slug + '.html';
  if (!fs.existsSync(fp)) return;
  
  let html = fs.readFileSync(fp, 'utf8');
  if (html.charCodeAt(0) === 0xFEFF) html = html.slice(1);
  
  // Only remove if this page has its own site-nav
  if (!html.includes('site-nav') && !html.includes('nav-inner')) {
    console.log('Skipped (no site-nav): ' + slug);
    return;
  }
  
  // Remove the sticky nav-bar (added by migration script)
  html = html.replace(
    /<div class="nav-bar"[^>]*>[\s\S]*?<\/div>\s*\n*/,
    ''
  );
  
  // Remove duplicate footer (from migration script)
  html = html.replace(
    /<footer style="background:#0a0a1a;border-top:1px solid rgba\(255,255,255,0\.05\);padding:30px 0;margin-top:60px;">[\s\S]*?<\/footer>\s*\n*/,
    ''
  );
  
  fs.writeFileSync(fp, html, 'utf8');
  console.log('Fixed: ' + slug);
});

console.log('\nDone.');
