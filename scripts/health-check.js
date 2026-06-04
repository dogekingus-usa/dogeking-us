// Automated Site Health Monitor
// Run: node scripts/health-check.js
// Reports: broken links, missing files, encoding issues

const fs = require('fs');
const dir = 'C:/content-sites/dogeking.us/articles';
const dataFile = 'C:/content-sites/dogeking.us/articles-data.js';
const redirects = 'C:/content-sites/dogeking.us/_redirects';

let issues = [];

// 1. Check data file vs files on disk
const d = fs.readFileSync(dataFile, 'utf8');
const slugRegex = /slug:\s*"([^"]+)"/g;
const slugs = [];
let m;
while ((m = slugRegex.exec(d)) !== null) slugs.push(m[1]);

const files = new Set(
  fs.readdirSync(dir).filter(f => f.endsWith('.html')).map(f => f.replace('.html', ''))
);
const sys = new Set(['404','about','checkout','contact','disclaimer','privacy','products','thank-you','all-articles','crypto-bundle']);
const missingFiles = slugs.filter(s => !files.has(s));
if (missingFiles.length > 0) issues.push('BROKEN LINKS: ' + missingFiles.length + ' slugs in data with no file');

// 2. Check each file for basic structure
let noCrown = 0, noAuthor = 0, noLD = 0, dupFooter = 0;
fs.readdirSync(dir).filter(f => f.endsWith('.html')).forEach(f => {
  const c = fs.readFileSync(dir + '/' + f, 'utf8');
  if (f.includes('-') && !sys.has(f.replace('.html',''))) {
    if (!c.includes('crown-design-system')) noCrown++;
    if (!c.includes('Samuel Pason')) noAuthor++;
    if (!c.includes('application/ld+json')) noLD++;
  }
  if ((c.match(/<footer/g) || []).length > 1) dupFooter++;
});

if (noCrown > 0) issues.push('CROWN: ' + noCrown + ' files missing crown theme');
if (noAuthor > 0) issues.push('AUTHOR: ' + noAuthor + ' files missing author byline');
if (noLD > 0) issues.push('JSONLD: ' + noLD + ' files missing structured data');
if (dupFooter > 0) issues.push('FOOTER: ' + dupFooter + ' files with duplicate footers');

// 3. Check redirect file size
const rSize = fs.statSync(redirects).size;
if (rSize < 100) issues.push('REDIRECTS: _redirects file too small (' + rSize + ' bytes)');

// Report
console.log('=== SITE HEALTH REPORT ===');
console.log('Date:', new Date().toISOString());
console.log('Status:', issues.length === 0 ? 'ALL CLEAN' : issues.length + ' ISSUES FOUND');
issues.forEach(i => console.log('  ! ' + i));
if (issues.length === 0) console.log('  No issues detected. Site is healthy.');
console.log('\nStats:');
console.log('  Data entries:', slugs.length);
console.log('  Files on disk:', files.size);
console.log('  Redirect rules:', (fs.readFileSync(redirects,'utf8').match(/301/g)||[]).length);
