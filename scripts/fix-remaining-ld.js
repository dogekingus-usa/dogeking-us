const fs = require('fs');
const dir = 'C:/content-sites/dogeking.us/articles';

fs.readdirSync(dir).filter(f => f.endsWith('.html')).forEach(f => {
  const fp = dir + '/' + f;
  let c = fs.readFileSync(fp, 'utf8');
  if (c.charCodeAt(0) === 0xFEFF) c = c.slice(1);
  if (c.includes('application/ld+json')) return;
  if (f === '404.html') return; // skip 404
  const title = f.replace('.html', '').replace(/-/g, ' ');
  const site = 'https://dogeking.us';
  const ld = '\n<script type="application/ld+json">\n{\n  "@context": "https://schema.org",\n  "@type": "WebPage",\n  "name": "' + title + '",\n  "url": "' + site + '/' + f.replace('.html', '') + '",\n  "publisher": { "@type": "Organization", "name": "DogeKing", "url": "' + site + '" }\n}\n</script>\n';
  c = c.replace('</head>', ld + '</head>');
  fs.writeFileSync(fp, c, 'utf8');
  console.log('Added LD:', f);
});
