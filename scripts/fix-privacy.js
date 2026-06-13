const fs = require('fs');
let html = fs.readFileSync('C:/content-sites/dogeking.us/articles/privacy.html', 'utf8');
if (html.charCodeAt(0) === 0xFEFF) html = html.slice(1);
html = html.replace(
  /<footer style="background:#0a0a1a;border-top:1px solid rgba\(255,255,255,0\.05\);padding:30px 0;margin-top:60px;">[\s\S]*?<\/footer>\s*/,
  ''
);
fs.writeFileSync('C:/content-sites/dogeking.us/articles/privacy.html', html, 'utf8');
console.log('Fixed privacy footer');
