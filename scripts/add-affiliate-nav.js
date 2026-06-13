const fs = require('fs');
let c = fs.readFileSync('C:/content-sites/dogeking.us/index.html', 'utf8');

// Add Affiliate link to nav
const navLink = '<a href="/affiliate.html" style="padding:6px 14px;border-radius:8px;color:#c0c0e0;font-size:0.85rem;text-decoration:none;transition:all 0.2s;">Affiliate</a>';

// Check if affiliate link already exists
if (!c.includes('affiliate.html')) {
  // Add before the "Get Bundle" button
  c = c.replace('Get Bundle</a>', navLink + 'Get Bundle</a>');
  fs.writeFileSync('C:/content-sites/dogeking.us/index.html', c, 'utf8');
  console.log('Affiliate link added to nav');
} else {
  console.log('Affiliate link already exists');
}

// Also add to all articles nav bars  
const articlesDir = 'C:/content-sites/dogeking.us/articles';
const files = fs.readdirSync(articlesDir).filter(f => f.endsWith('.html') && !f.includes('404'));
let count = 0;
files.forEach(f => {
  let ac = fs.readFileSync(articlesDir + '/' + f, 'utf8');
  if (ac.charCodeAt(0) === 0xFEFF) ac = ac.slice(1);
  if (ac.includes('Get Bundle') && !ac.includes('affiliate.html') && ac.includes('nav-bar')) {
    ac = ac.replace('Get Bundle</a>', 'Affiliate</a><a href="/crypto-bundle.html" style="padding:6px 14px;border-radius:8px;background:linear-gradient(135deg,#FFD700,#FF8C00);color:#0a0a1a;font-size:0.85rem;font-weight:600;text-decoration:none;margin-left:8px;">Get Bundle</a>');
    // Wait, that's wrong. Let me carefully add the affiliate link
    ac = ac.replace(
      '<a href="/crypto-bundle.html" style="padding:6px 14px;border-radius:8px;background:linear-gradient(135deg,#FFD700,#FF8C00);color:#0a0a1a;font-size:0.85rem;font-weight:600;text-decoration:none;margin-left:8px;">Get Bundle</a>',
      '<a href="/affiliate.html" style="padding:6px 14px;border-radius:8px;color:#c0c0e0;font-size:0.85rem;text-decoration:none;">Affiliate</a><a href="/crypto-bundle.html" style="padding:6px 14px;border-radius:8px;background:linear-gradient(135deg,#FFD700,#FF8C00);color:#0a0a1a;font-size:0.85rem;font-weight:600;text-decoration:none;margin-left:8px;">Get Bundle</a>'
    );
    fs.writeFileSync(articlesDir + '/' + f, ac, 'utf8');
    count++;
  }
});
console.log('Affiliate links added to ' + count + ' article navs');
