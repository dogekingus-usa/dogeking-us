const fs = require('fs');
const dataFile = 'C:/content-sites/dogeking.us/articles-data.js';
const articlesDir = 'C:/content-sites/dogeking.us/articles';
const redirectFile = 'C:/content-sites/dogeking.us/_redirects';

// Read data file
const d = fs.readFileSync(dataFile, 'utf8');
const cleanD = d.charCodeAt(0) === 0xFEFF ? d.slice(1) : d;

// Extract all article objects
const artRegex = /\{title:\s*"([^"]+)"\s*,\s*slug:\s*"([^"]+)"\s*,\s*category:\s*"([^"]+)"\s*,\s*date:\s*"([^"]+)"\s*,\s*readTime:\s*"([^"]+)"\s*,\s*excerpt:\s*"([^"]*)"\s*\}/g;
const arts = [];
let m;
while ((m = artRegex.exec(cleanD)) !== null) {
  arts.push({ title: m[1], slug: m[2], cat: m[3], date: m[4], read: m[5], excerpt: m[6] });
}

// Get files on disk
const files = fs.readdirSync(articlesDir).filter(f => f.endsWith('.html')).map(f => f.replace('.html', ''));
const sys = ['404','about','checkout','contact','disclaimer','privacy','products','thank-you','all-articles','crypto-bundle','template','nav-component-enhanced','preview-card','cta-snippets','fetched-live','ecosystem-section','sales-cta-overlay','sales-thank-you','dogeking-article-og-template','affiliate','dynamic-loader'];

const slugsInData = arts.map(a => a.slug);
const missing = slugsInData.filter(s => !files.includes(s));
const extra = files.filter(f => !slugsInData.includes(f) && !sys.includes(f));

console.log('Total in data:', arts.length);
console.log('Files on disk:', files.length - sys.length);
console.log('Missing (data has, no file):', missing.length);
console.log('Extra (file exists, not in data):', extra.length);

// Add redirects for missing slugs
let existingRedirects = fs.readFileSync(redirectFile, 'utf8');
let added = 0;
missing.forEach(slug => {
  if (!existingRedirects.includes(slug)) {
    fs.appendFileSync(redirectFile, '\n/articles/' + slug + ' / 301');
    added++;
  }
});
console.log('Redirect rules added:', added);

console.log('\nMissing slugs:');
missing.forEach(s => console.log('  ' + s));
console.log('\nExtra files:');
extra.forEach(s => console.log('  ' + s));
