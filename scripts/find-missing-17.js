const fs = require('fs');
const data = fs.readFileSync('C:/content-sites/dogeking.us/articles-data.js', 'utf8');
const slugMatches = data.match(/slug:\s*"([^"]+)"/g);
const slugsInData = new Set(slugMatches.map(s => s.match(/"([^"]+)"/)[1]));
const files = fs.readdirSync('C:/content-sites/dogeking.us/articles').filter(f => f.endsWith('.html')).map(f => f.replace('.html', ''));
const sys = ['404','about','checkout','contact','disclaimer','privacy','products','thank-you','all-articles','crypto-bundle','template','nav-component-enhanced','preview-card','cta-snippets','fetched-live','ecosystem-section','sales-cta-overlay','sales-thank-you','dogeking-article-og-template','affiliate','dynamic-loader'];
const missing = files.filter(f => !sys.includes(f) && !slugsInData.has(f));
console.log('Missing articles to add:', missing.length);
missing.forEach(s => { console.log(s); });
