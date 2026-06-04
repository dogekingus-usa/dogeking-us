const fs = require('fs');
const dataFile = 'C:/content-sites/dogeking.us/articles-data.js';
const articlesDir = 'C:/content-sites/dogeking.us/articles';
const redirectFile = 'C:/content-sites/dogeking.us/_redirects';

// Read data file
let data = fs.readFileSync(dataFile, 'utf8');
if (data.charCodeAt(0) === 0xFEFF) data = data.slice(1);

// Get slugs in data
const slugRegex = /slug:\s*"([^"]+)"/g;
let m;
const slugsInData = [];
while ((m = slugRegex.exec(data)) !== null) {
  slugsInData.push(m[1]);
}

// Get files on disk
const filesOnDisk = new Set(fs.readdirSync(articlesDir).filter(f => f.endsWith('.html')).map(f => f.replace('.html', '')));

const systemPages = new Set(['404','about','checkout','contact','disclaimer','privacy','products','thank-you','all-articles','crypto-bundle','template','nav-component-enhanced','preview-card','cta-snippets','fetched-live','ecosystem-section','sales-cta-overlay','sales-thank-you','dogeking-article-og-template','affiliate','dynamic-loader']);

const missing = slugsInData.filter(slug => !filesOnDisk.has(slug));
const extra = [...filesOnDisk].filter(f => !slugsInData.includes(f) && !systemPages.has(f));

console.log('Missing HTML files (data→404):', missing.length);
console.log('Extra unregistered articles:', extra.length);

// 1. Remove missing slugs from data file
let removedCount = 0;
let updatedData = data;
missing.forEach(slug => {
  // Find and remove the entire article object for this slug
  const regex = new RegExp('\\{\\s*title:"[^"]*",\\s*slug:"' + slug + '"[^}]*\\}[\\s,]*', 'g');
  const before = updatedData.length;
  updatedData = updatedData.replace(regex, '');
  if (updatedData.length < before) removedCount++;
  
  // Also add redirect rule for this slug
  const redirects = fs.readFileSync(redirectFile, 'utf8');
  if (!redirects.includes('/articles/' + slug)) {
    fs.appendFileSync(redirectFile, '\n/articles/' + slug + '* / 301');
  }
});

// Clean up trailing commas
updatedData = updatedData.replace(/,\s*\]/, '\n]');
updatedData = updatedData.replace(/,\s*,/g, ',');

fs.writeFileSync(dataFile, updatedData, 'utf8');
console.log('Removed', removedCount, 'broken entries from data file');

// 2. Add extra articles to the end of data file
let addedCount = 0;
extra.forEach(slug => {
  const fp = articlesDir + '/' + slug + '.html';
  const html = fs.readFileSync(fp, 'utf8');
  const titleMatch = html.match(/<h1[^>]*>([^<]+)<\/h1>/);
  const title = titleMatch ? titleMatch[1].replace(/"/g, '\\"') : slug.replace(/-/g, ' ');
  const cat = slug.includes('btc') || slug.includes('bitcoin') ? 'bitcoin' : 
              slug.includes('solana') ? 'solana' : 
              slug.includes('meme') || slug.includes('doge') || slug.includes('dking') ? 'meme-coins' :
              slug.includes('trading') || slug.includes('strategy') ? 'trading' :
              slug.includes('defi') || slug.includes('staking') ? 'defi' :
              slug.includes('wallet') || slug.includes('security') || slug.includes('seed') ? 'wallets' :
              slug.includes('airdrop') ? 'airdrops' :
              slug.includes('guide') || slug.includes('beginner') ? 'guides' : 'trading';
  
  const newEntry = '\n,\n{\n  title:"' + title.substring(0, 80) + '",\n  slug:"' + slug + '",\n  category:"' + cat + '",\n  date:"2026",\n  readTime:"5 min read",\n  excerpt:"' + title.substring(0, 80) + '"\n}';
  
  // Insert before the closing ];
  updatedData = updatedData.replace(/;\s*$/, '');
  updatedData = updatedData.replace(/\]\s*$/, '');
  updatedData += newEntry + '\n];';
  addedCount++;
});

fs.writeFileSync(dataFile, updatedData, 'utf8');
console.log('Added', addedCount, 'extra articles to data file');

// Verify final count
const finalCount = (updatedData.match(/slug:\s*"/g) || []).length;
console.log('Final data file count:', finalCount);
