const fs = require('fs');
const path = require('path');
const dir = 'C:/content-sites/dogeking.us/articles';
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));

const systemSlugs = ['404','about','checkout','contact','privacy','products','thank-you','all-articles',
  'crypto-bundle','template','nav-component-enhanced','preview-card','cta-snippets','fetched-live',
  'ecosystem-section','sales-cta-overlay','sales-thank-you','dogeking-article-og-template',
  'affiliate','dynamic-loader'];

let fixCounts = { bom: 0, price: 0, ld: 0, author: 0, links: 0 };

const authorBlock = '<p style="font-size:0.85rem;color:#8080a0;margin:8px 0 16px;">By <a href="/about.html" style="color:#FFD700;text-decoration:none;">Samuel Pason</a> \u00b7 DogeKing Editor</p>';
const authorBlockOld = '<p style="font-size:0.85rem;color:#8080a0;margin:8px 0 16px 0;font-family:Arial,sans-serif;">By <a href="/about.html" style="color:#FFD700;text-decoration:none;">Samuel Pason</a> \u00b7 DogeKing Editor</p>';
const siteUrl = 'https://dogeking.us';

files.forEach(f => {
  const slug = f.replace('.html', '');
  const fp = path.join(dir, f);
  let html = fs.readFileSync(fp, 'utf8');
  let modified = false;
  
  // 1. Fix BOM
  if (html.charCodeAt(0) === 0xFEFF) {
    html = html.slice(1);
    modified = true;
    fixCounts.bom++;
  }
  
  if (systemSlugs.includes(slug)) {
    if (modified) fs.writeFileSync(fp, html, 'utf8');
    return;
  }
  
  // 2. Fix $29.99 â†â„¢ $29
  if (html.includes('$29.99')) {
    html = html.replace(/\$29\.99/g, '$29');
    modified = true;
    fixCounts.price++;
  }
  
  // 3. Fix missing JSON-LD (14 articles)
  if (!html.includes('application/ld+json')) {
    const titleMatch = html.match(/<h1[^>]*>([^<]+)<\/h1>/);
    const title = titleMatch ? titleMatch[1].replace(/"/g, '&quot;') : slug.replace(/-/g, ' ');
    const articleUrl = siteUrl + '/articles/' + slug + '.html';
    
    const jsonld = '\n<script type="application/ld+json">\n' +
      '{\n  "@context": "https://schema.org",\n  "@type": "Article",\n' +
      '  "headline": "' + title + '",\n' +
      '  "author": {"@type":"Person","name":"Samuel Pason","url":"' + siteUrl + '/about.html"},\n' +
      '  "publisher": {"@type":"Organization","name":"DogeKing","logo":{"@type":"ImageObject","url":"' + siteUrl + '/assets/crown-logo.svg"}},\n' +
      '  "datePublished": "2026",\n' +
      '  "mainEntityOfPage": {"@type":"WebPage","@id":"' + articleUrl + '"},\n' +
      '  "image": "' + siteUrl + '/assets/og-image.svg"\n' +
      '}\n</script>\n';
    
    html = html.replace('</head>', jsonld + '</head>');
    modified = true;
    fixCounts.ld++;
  }
  
  // 4. Fix missing author byline
  if (!html.includes('Samuel Pason')) {
    // Try after </h1>
    if (html.match(/<\/h1>/)) {
      if (html.includes('crown-design-system') || html.includes('theme-dogeking')) {
        html = html.replace(/<\/h1>/, '</h1>\n' + authorBlock);
      } else {
        html = html.replace(/<\/h1>/, '</h1>\n' + authorBlockOld);
      }
      modified = true;
      fixCounts.author++;
    }
  }
  
  // 5. Fix root-level article links â†â„¢ /articles/ links
  const linkRegex = /href="\/([a-zA-Z0-9][^"]*\.html)"/g;
  let m;
  while ((m = linkRegex.exec(html)) !== null) {
    const linkSlug = m[1].replace('.html', '');
    if (!linkSlug.startsWith('articles/') && !['all-articles','privacy','contact','disclaimer',
        'products','crypto-bundle','checkout','thank-you','about','feed','index','404',
        'crown-design-system','sales-cta-overlay','dynamic-loader'].includes(linkSlug) 
        && linkSlug.includes('-')) {
      html = html.replace(
        'href="/' + linkSlug + '.html"',
        'href="/articles/' + linkSlug + '.html"'
      );
      modified = true;
      fixCounts.links++;
    }
  }
  
  if (modified) {
    fs.writeFileSync(fp, html, 'utf8');
  }
});

console.log('FIXES APPLIED:');
console.log('  BOM encoding fixed:', fixCounts.bom);
console.log('  $29.99 â†â„¢ $29 fixed:', fixCounts.price);
console.log('  JSON-LD added:', fixCounts.ld);
console.log('  Author bylines added:', fixCounts.author);
console.log('  Rootâ†â„¢/articles/ links fixed:', fixCounts.links);
