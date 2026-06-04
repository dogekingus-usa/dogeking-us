const fs = require('fs');
const dataFile = 'C:/content-sites/dogeking.us/articles-data.js';
const articlesDir = 'C:/content-sites/dogeking.us/articles';

const data = fs.readFileSync(dataFile, 'utf8');
const slugRegex = /slug:\s*"([^"]+)"/g;
let m;
const slugsInData = [];
while ((m = slugRegex.exec(data)) !== null) {
  slugsInData.push(m[1]);
}

const filesOnDisk = new Set(fs.readdirSync(articlesDir).filter(f => f.endsWith('.html')).map(f => f.replace('.html', '')));

const missing = slugsInData.filter(slug => !filesOnDisk.has(slug));
const extra = [...filesOnDisk].filter(f => !slugsInData.includes(f) && !['404','about','checkout','contact','disclaimer','privacy','products','thank-you','all-articles','crypto-bundle','template','nav-component-enhanced','preview-card','cta-snippets','fetched-live','ecosystem-section','sales-cta-overlay','sales-thank-you','dogeking-article-og-template','affiliate','dynamic-loader'].includes(f));

console.log('Total slugs in data file:', slugsInData.length);
console.log('Total HTML files on disk:', filesOnDisk.size);
console.log('');
console.log('=== MISSING HTML FILES (data says exists but no file) ===');
console.log('Count:', missing.length);
missing.forEach(s => console.log('  ' + s));

console.log('');
console.log('=== EXTRA HTML FILES (file exists but not in data) ===');
console.log('Count:', extra.length);
extra.forEach(s => console.log('  ' + s));
