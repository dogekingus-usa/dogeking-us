const fs = require('fs');
const sites = {
  'lifesystemos.com': 'LifeSystemOS',
  'remoteworkhub.net': 'RemoteWorkHub',
  'resumeprotips.com': 'ResumeProTips'
};

Object.keys(sites).forEach(site => {
  const dir = 'C:/content-sites/' + site;
  const name = sites[site];
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));
  
  files.forEach(f => {
    const fp = dir + '/' + f;
    let c = fs.readFileSync(fp, 'utf8');
    if (c.charCodeAt(0) === 0xFEFF) c = c.slice(1);
    let mod = false;
    
    // Add canonical
    if (!c.includes('rel="canonical"')) {
      const slug = f.replace('.html', '');
      const canon = '\n<link rel="canonical" href="https://' + site + '/' + slug + '">\n';
      c = c.replace('</head>', canon + '</head>');
      mod = true;
    }
    
    // Add JSON-LD
    if (!c.includes('application/ld+json')) {
      const titleMatch = c.match(/<h1[^>]*>([^<]+)<\/h1>/);
      const title = titleMatch ? titleMatch[1].replace(/"/g, '&quot;') : f.replace('.html', '').replace(/-/g, ' ');
      const jsonld = '\n<script type="application/ld+json">\n{\n  "@context": "https://schema.org",\n';
      
      if (f === 'index.html') {
        c = c.replace('</head>', jsonld + '  "@type": "WebSite",\n  "name": "' + title + '",\n  "url": "https://' + site + '"\n}\n</script>\n' + '</head>');
      } else {
        c = c.replace('</head>', jsonld + '  "@type": "WebPage",\n  "name": "' + title + '",\n  "url": "https://' + site + '/' + f.replace('.html', '') + '"\n}\n</script>\n' + '</head>');
      }
      mod = true;
    }
    
    if (mod) {
      fs.writeFileSync(fp, c, 'utf8');
      console.log(site + '/' + f + ': JSON-LD + canonical added');
    }
  });
});

console.log('\nDone. All 3 sites updated.');
