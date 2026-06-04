const fs = require('fs');
const path = require('path');
const dir = 'C:/content-sites/dogeking.us/articles';
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));

let results = {
  total: files.length,
  crown: 0,
  missingAuthor: 0,
  missingLD: 0,
  missingCanon: 0,
  badPrice: 0,
  brokenGumroad: 0,
  emptyFiles: 0,
  tooShort: 0,
  noH1: 0,
  badEncoding: 0,
  correctedLinks: 0,
  authorCount: 0,
  systemPages: 0
};

const systemSlugs = ['404','about','checkout','contact','privacy','products','thank-you','all-articles',
  'crypto-bundle','template','nav-component-enhanced','preview-card','cta-snippets','fetched-live',
  'ecosystem-section','sales-cta-overlay','sales-thank-you','dogeking-article-og-template',
  'affiliate','dynamic-loader'];

files.forEach(f => {
  const slug = f.replace('.html', '');
  const fp = path.join(dir, f);
  let html = fs.readFileSync(fp, 'utf8');
  
  if (systemSlugs.includes(slug)) { results.systemPages++; return; }
  
  // BOM
  if (html.charCodeAt(0) === 0xFEFF) results.badEncoding++;
  
  if (html.includes('crown-design-system')) results.crown++;
  if (html.includes('Samuel Pason')) results.authorCount++;
  else results.missingAuthor++;
  if (!html.includes('application/ld+json')) results.missingLD++;
  if (!html.includes('rel="canonical"')) results.missingCanon++;
  if (html.includes('$29.99')) results.badPrice++;
  if (html.match(/gumroad\.com\/l\/crypto-bundle[^d]/)) results.brokenGumroad++;
  
  // Content quality
  const body = html.replace(/<[^>]+>/g, '').trim();
  if (body.length < 100 && !html.match(/<script/i)) results.emptyFiles++;
  else if (body.length < 500) results.tooShort++;
  
  if (!html.match(/<h[1-6]/i)) results.noH1++;
  
  // Check for root-level hrefs that should point to /articles/
  const linkRegex = /href="\/([a-zA-Z0-9][^"]*\.html)"/g;
  let m;
  while ((m = linkRegex.exec(html)) !== null) {
    const slug2 = m[1].replace('.html', '');
    if (!slug2.startsWith('articles/') && !['all-articles','privacy','contact','disclaimer',
        'products','crypto-bundle','checkout','thank-you','about','feed','index','404',
        'crown-design-system','sales-cta-overlay'].includes(slug2) && slug2.includes('-')) {
      results.correctedLinks++;
    }
  }
});

console.log('=== ARTICLE CONTENT AUDIT ===');
console.log('Total articles:', results.total);
console.log('');
console.log('--- GOOD ---');
console.log('Crown theme:', results.crown + '/' + (results.total - results.systemPages));
console.log('With author byline:', results.authorCount);
console.log('JSON-LD present:', (results.total - results.systemPages - results.missingLD) + '/' + (results.total - results.systemPages));
console.log('Canonical URLs:', (results.total - results.systemPages - results.missingCanon) + '/' + (results.total - results.systemPages));
console.log('');
console.log('--- PROBLEMS ---');
console.log('Missing author byline:', results.missingAuthor);
console.log('Missing JSON-LD:', results.missingLD);
console.log('Missing canonical:', results.missingCanon);
console.log('Bad encoding (BOM):', results.badEncoding);
console.log('Bad price ($29.99):', results.badPrice);
console.log('Broken Gumroad links:', results.brokenGumroad);
console.log('Empty files (<100 chars body):', results.emptyFiles);
console.log('Very short files (<500 chars body):', results.tooShort);
console.log('No H1 heading:', results.noH1);
console.log('Root-level article links (should be /articles/):', results.correctedLinks);
