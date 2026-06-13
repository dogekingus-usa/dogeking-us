const fs = require('fs');
const dataFile = 'C:/content-sites/dogeking.us/articles-data.js';
const articlesDir = 'C:/content-sites/dogeking.us/articles';

// Backup broken file
fs.copyFileSync(dataFile, dataFile.replace('.js', '.bak.js'));

const d = fs.readFileSync(dataFile, 'utf8');
const cleanD = d.charCodeAt(0) === 0xFEFF ? d.slice(1) : d;

// Extract valid article objects using regex
const artRegex = /\{title:\s*"([^"]+)"\s*,\s*slug:\s*"([^"]+)"\s*,\s*category:\s*"([^"]+)"\s*,\s*date:\s*"([^"]+)"\s*,\s*readTime:\s*"([^"]+)"\s*,\s*excerpt:\s*"([^"]*)"\s*\}/g;
const arts = [];
let m;
while ((m = artRegex.exec(cleanD)) !== null) {
  arts.push({ title: m[1], slug: m[2], cat: m[3], date: m[4], read: m[5], excerpt: m[6] });
}
console.log('Extracted', arts.length, 'valid article objects from broken file');

// Get files on disk (real articles only)
const files = fs.readdirSync(articlesDir).filter(f => f.endsWith('.html')).map(f => f.replace('.html', ''));
const sys = ['404','about','checkout','contact','disclaimer','privacy','products','thank-you','all-articles','crypto-bundle','template','nav-component-enhanced','preview-card','cta-snippets','fetched-live','ecosystem-section','sales-cta-overlay','sales-thank-you','dogeking-article-og-template','affiliate','dynamic-loader'];

const realFiles = files.filter(f => !sys.includes(f));
const slugsInData = arts.map(a => a.slug);
const extraFiles = realFiles.filter(f => !slugsInData.includes(f));
const missingFiles = slugsInData.filter(s => !realFiles.includes(s));

console.log('Extra files to add:', extraFiles.length);
console.log('Missing files to remove:', missingFiles.length);

// Build new array: keep only articles that have matching files
let newArts = arts.filter(a => realFiles.includes(a.slug));

// Add extra articles
extraFiles.forEach(slug => {
  const fp = articlesDir + '/' + slug + '.html';
  const html = fs.readFileSync(fp, 'utf8');
  const titleMatch = html.match(/<h1[^>]*>([^<]+)<\/h1>/);
  const title = titleMatch ? titleMatch[1].replace(/"/g, '\\"').replace(/\n/g, '').trim() : slug.replace(/-/g, ' ');
  const cat = slug.includes('btc') || slug.includes('bitcoin') ? 'bitcoin' : 
              slug.includes('solana') ? 'solana' : 
              slug.includes('meme') || slug.includes('doge') || slug.includes('dking') ? 'meme-coins' :
              slug.includes('trading') || slug.includes('strategy') ? 'trading' :
              slug.includes('defi') || slug.includes('staking') || slug.includes('lend') ? 'defi' :
              slug.includes('wallet') || slug.includes('security') || slug.includes('seed') ? 'wallets' :
              slug.includes('airdrop') || slug.includes('farming') ? 'airdrops' :
              slug.includes('guide') || slug.includes('beginner') || slug.includes('how-to') ? 'guides' : 'trading';
  
  newArts.push({
    title: title.substring(0, 120),
    slug: slug,
    cat: cat,
    date: '2026',
    read: '5 min read',
    excerpt: title.substring(0, 120)
  });
});

// Write new file
let output = 'const articles = [\n';
newArts.forEach((a, i) => {
  if (i > 0) output += ',\n';
  output += '  {\n';
  output += '    title: "' + a.title + '",\n';
  output += '    slug: "' + a.slug + '",\n';
  output += '    category: "' + a.cat + '",\n';
  output += '    date: "' + a.date + '",\n';
  output += '    readTime: "' + a.read + '",\n';
  output += '    excerpt: "' + a.excerpt + '"\n';
  output += '  }';
});
output += '\n];\n';

fs.writeFileSync(dataFile, output, 'utf8');
console.log('Wrote', newArts.length, 'articles to data file');

// Verify
try {
  eval(output.replace('const articles =', 'var articles ='));
  console.log('VALID syntax. Total:', articles.length);
} catch(e) {
  console.log('STILL BROKEN:', e.message.substring(0, 100));
}

// Add redirects for missing files
const redirectFile = 'C:/content-sites/dogeking.us/_redirects';
let redirects = fs.readFileSync(redirectFile, 'utf8');
let added = 0;
missingFiles.forEach(slug => {
  if (!redirects.includes('/articles/' + slug)) {
    fs.appendFileSync(redirectFile, '\n/articles/' + slug + ' / 301');
    added++;
  }
});
console.log('Added', added, 'redirect rules for missing files');
