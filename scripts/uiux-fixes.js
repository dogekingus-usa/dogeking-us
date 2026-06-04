const fs = require('fs');
const dir = 'C:/content-sites/dogeking.us/articles';
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));

// UI/UX: Fix duplicate content issues, nav spacing, missing back-to-top
let fixedNav = 0, fixedFooter = 0, addedBackToTop = 0;

files.forEach(f => {
  const fp = dir + '/' + f;
  let c = fs.readFileSync(fp, 'utf8');
  if (c.charCodeAt(0) === 0xFEFF) c = c.slice(1);
  let mod = false;

  // Remove duplicate nav bars
  const navCount = (c.match(/class="nav-bar"/g) || []).length;
  if (navCount > 1) {
    // Keep only first nav-bar
    const parts = c.split(/<div class="nav-bar"[^>]*>[\s\S]*?<\/div>/);
    if (parts.length > 2) {
      c = parts.slice(0, 2).join(parts[1]) + parts.slice(2).join('');
      mod = true;
      fixedNav++;
    }
  }

  // Remove duplicate footers  
  const footerCount = (c.match(/<footer/g) || []).length;
  if (footerCount > 1) {
    // Keep only first footer
    const fParts = c.split(/<footer[\s\S]*?<\/footer>/);
    c = fParts.slice(0, 2).join(fParts[1]) + (fParts.slice(2).join('') || '');
    mod = true;
    fixedFooter++;
  }

  // Add back-to-top button on long pages
  if (c.length > 10000 && !c.includes('back-to-top') && !f.includes('404')) {
    const btt = '<div class="back-to-top" style="position:fixed;bottom:24px;right:24px;z-index:999;"><a href="#" style="display:flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:50%;background:linear-gradient(135deg,#FFD700,#FF8C00);color:#0a0a1a;text-decoration:none;font-size:1.2rem;box-shadow:0 4px 15px rgba(255,215,0,0.3);">\u2191</a></div>';
    c = c.replace('</body>', btt + '\n</body>');
    mod = true;
    addedBackToTop++;
  }

  if (mod) {
    fs.writeFileSync(fp, c, 'utf8');
  }
});

console.log('UI/UX fixes:');
console.log('  Duplicate navs removed:', fixedNav);
console.log('  Duplicate footers removed:', fixedFooter);
console.log('  Back-to-top added:', addedBackToTop);
