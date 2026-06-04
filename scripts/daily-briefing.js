const fs = require('fs');
const dir = 'C:/content-sites/dogeking.us/articles';
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));

const dataFile = fs.readFileSync('C:/content-sites/dogeking.us/articles-data.js', 'utf8');
const artCount = (dataFile.match(/slug:/g) || []).length;
let crown = 0, author = 0, ld = 0, total = files.length;

files.forEach(f => {
  const c = fs.readFileSync(dir + '/' + f, 'utf8');
  if (c.includes('crown-design-system')) crown++;
  if (c.includes('Samuel Pason')) author++;
  if (c.includes('application/ld+json')) ld++;
});

const r = fs.readFileSync('C:/content-sites/dogeking.us/_redirects', 'utf8');
const redirects = (r.match(/301/g) || []).length;
const blocks = (r.match(/\/404 301/g) || []).length;

console.log('CURRENT METRICS:');
console.log('Articles in data file:', artCount);
console.log('HTML files on disk:', total);
console.log('Crown theme coverage:', crown + '/' + total);
console.log('Author bylines:', author + '/' + total);
console.log('JSON-LD coverage:', ld + '/' + total);
console.log('Total redirect rules:', redirects);
console.log('System files blocked:', blocks);

// Check for remaining issues
console.log('\nISSUES CHECK:');
let cssLeak = 0, brokenArrow = 0, badEmoji = 0;
files.forEach(f => {
  const c = fs.readFileSync(dir + '/' + f, 'utf8');
  const body = c.replace(/<style[^>]*>[\s\S]*?<\/style>/g, '').replace(/<head>[\s\S]*?<\/head>/g, '');
  if (body.match(/\* \{ margin|body \{ backgr|\{ margin: 0/)) cssLeak++;
  if (c.includes('Ã¢â€') || c.includes('Ã°Å¸')) badEmoji++;
});
console.log('CSS leak in content:', cssLeak > 0 ? cssLeak + ' FILES' : 'NONE CLEAN');
console.log('Corrupted emoji/arrows:', badEmoji > 0 ? badEmoji + ' FILES' : 'NONE CLEAN');

// Root file cleanup check
const rootFiles = fs.readdirSync('C:/content-sites/dogeking.us').filter(f => f.endsWith('.html'));
const keepRoot = ['index.html','404.html','about.html','checkout.html','contact.html','disclaimer.html','privacy.html','products.html','thank-you.html','all-articles.html','crypto-bundle.html'];
const extraRoot = rootFiles.filter(f => !keepRoot.includes(f) && f.includes('-'));
console.log('Extra root HTML files (duplicates):', extraRoot.length);

// Check homepage metrics
const index = fs.readFileSync('C:/content-sites/dogeking.us/index.html', 'utf8');
const artCountDisplay = index.match(/(\d+)\s*articles/i);
console.log('\nHOMEPAGE:');
console.log('Article count shown:', artCountDisplay ? artCountDisplay[0] : 'NOT FOUND');
console.log('Has Browse All button:', index.includes('Browse All'));
console.log('Has RSS link:', index.includes('feed.xml'));
console.log('Has static articles:', index.includes('article-card'));
console.log('Font optimization:', index.includes('media=\"print\"') && index.includes('rel=\"preload\"'));
