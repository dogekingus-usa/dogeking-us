const fs = require('fs');
const data = fs.readFileSync('C:/content-sites/dogeking.us/articles-data.js', 'utf8');
const slugMatches = data.match(/slug:\s*"([^"]+)"/g);
const slugsInData = slugMatches.map(s => s.match(/"([^"]+)"/)[1]);
const files = new Set(fs.readdirSync('C:/content-sites/dogeking.us/articles').filter(f => f.endsWith('.html')).map(f => f.replace('.html', '')));
const sys = new Set(['404','about','checkout','contact','disclaimer','privacy','products','thank-you','all-articles','crypto-bundle','template','nav-component-enhanced','preview-card','cta-snippets','fetched-live','ecosystem-section','sales-cta-overlay','sales-thank-you','dogeking-article-og-template','affiliate','dynamic-loader']);

// Data entries with no corresponding file
const missingFiles = slugsInData.filter(s => !files.has(s));
console.log('Data entries with NO file:');
missingFiles.forEach(s => console.log('  ' + s));
console.log('Total:', missingFiles.length);

// Files with no data entry
const missingData = [...files].filter(f => !sys.has(f) && !slugsInData.includes(f));
console.log('\nFiles with NO data entry:');
missingData.forEach(s => console.log('  ' + s));
console.log('Total:', missingData.length);
