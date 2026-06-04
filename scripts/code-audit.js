const fs = require('fs');
const dir = 'C:/content-sites/dogeking.us';

console.log('=== ROOT FILE CHECK ===');
const rootFiles = fs.readdirSync(dir).filter(f => f.endsWith('.html'));
const keepRoot = ['index.html','404.html','about.html','checkout.html','contact.html','disclaimer.html','privacy.html','products.html','thank-you.html','all-articles.html','crypto-bundle.html'];
const extra = rootFiles.filter(f => !keepRoot.includes(f) && !f.includes('crown') && f !== 'dynamic-loader.js' && f !== 'subscription-worker.js' && f !== 'sales-cta-overlay.html' && !f.startsWith('.'));
const rootArticles = extra.filter(f => f.includes('-'));
console.log('Extra root .html files:', extra.length);
console.log('Root article duplicates:', rootArticles.length);

console.log('\n=== CORE CODE FILES ===');
['crown-design-system.css','dynamic-loader.js','articles-data.js','_redirects','_headers','functions/_middleware.js','wrangler.toml','feed.xml'].forEach(f => {
  const p = dir+'/'+f;
  console.log('  '+(fs.existsSync(p)?'OK':'MISSING')+':', f, fs.existsSync(p)?'('+fs.statSync(p).size+' bytes)':'');
});

console.log('\n=== HEADERS ===');
const h = fs.readFileSync(dir+'/_headers', 'utf8');
console.log('Cache-Control rules:', (h.match(/Cache-Control/g)||[]).length);
console.log('Security headers:', (h.match(/X-Frame-Options|Content-Security|X-Content-Type|Strict-Transport/g)||[]).length);

console.log('\n=== REDIRECTS ===');
const r = fs.readFileSync(dir+'/_redirects', 'utf8');
console.log('Total 301 rules:', (r.match(/301/g)||[]).length);
console.log('System→404 blocks:', (r.match(/\/404 301/g)||[]).length);

console.log('\n=== DATA FILE ===');
const d = fs.readFileSync(dir+'/articles-data.js', 'utf8');
const entries = (d.match(/\{title:/g)||[]).length;
console.log('Article entries:', entries);
console.log('Ends with ;', d.trimEnd().endsWith(';'));
console.log('Has trailing ]', d.trim().endsWith('];'));

console.log('\n=== JS SYNTAX ===');
try {
  require(dir+'/dynamic-loader.js');
  console.log('dynamic-loader.js: ✅ syntax OK');
} catch(e) {
  if (e instanceof SyntaxError) console.log('dynamic-loader.js: ❌', e.message);
  else console.log('dynamic-loader.js: ✅ syntax OK (runtime error expected)');
}

console.log('\n=== CSS SIZE ===');
const css = fs.readFileSync(dir+'/crown-design-system.css', 'utf8');
console.log('CSS size:', css.length, 'bytes,', css.split('\n').length, 'lines');

console.log('\n=== FILESYSTEM SIZE ===');
let totalSize = 0; let totalFiles = 0;
function walk(d) {
  fs.readdirSync(d).forEach(f => {
    const p = d+'/'+f;
    if (fs.statSync(p).isDirectory()) walk(p);
    else { totalSize += fs.statSync(p).size; totalFiles++; }
  });
}
walk(dir);
console.log('Total files:', totalFiles);
console.log('Total size:', (totalSize/1024/1024).toFixed(1), 'MB');
