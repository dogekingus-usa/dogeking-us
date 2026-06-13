const fs = require('fs');
const d = fs.readFileSync('C:/content-sites/dogeking.us/articles-data.js', 'utf8');
const slugRegex = /slug:\s*"([^"]+)"/g;
const slugs = [];
let m;
while ((m = slugRegex.exec(d)) !== null) slugs.push(m[1]);

const files = new Set(
  fs.readdirSync('C:/content-sites/dogeking.us/articles')
    .filter(f => f.endsWith('.html'))
    .map(f => f.replace('.html', ''))
);

const sys = new Set([
  '404','about','checkout','contact','disclaimer','privacy','products',
  'thank-you','all-articles','crypto-bundle','template','nav-component-enhanced',
  'preview-card','cta-snippets','fetched-live','ecosystem-section',
  'sales-cta-overlay','sales-thank-you','dogeking-article-og-template',
  'affiliate','dynamic-loader'
]);

const missing = slugs.filter(s => !files.has(s));
console.log('Data entries with NO file:', missing.length);
missing.forEach(s => console.log('  ' + s));

const extra = [...files].filter(f => !sys.has(f) && !slugs.includes(f));
console.log('Files with NO data entry:', extra.length);
extra.forEach(s => console.log('  ' + s));
