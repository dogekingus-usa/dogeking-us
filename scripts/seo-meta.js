const fs = require('fs');
const dir = 'C:/content-sites/dogeking.us/articles';
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));

// Role: SEO & Content Dominator
// Add meta descriptions to articles missing them
let addedMeta = 0;
let fixedTitle = 0;

files.forEach(f => {
  const fp = dir + '/' + f;
  let c = fs.readFileSync(fp, 'utf8');
  if (c.charCodeAt(0) === 0xFEFF) c = c.slice(1);
  let mod = false;

  // Add meta description if missing
  if (!c.includes('meta name="description"') && !c.includes("meta name='description'")) {
    const h1 = c.match(/<h1[^>]*>([^<]+)<\/h1>/);
    const firstP = c.match(/<p>([^<]{30,200})/);
    const desc = firstP ? firstP[1].replace(/"/g, '&quot;').substring(0, 160) : 
                (h1 ? h1[1].replace(/"/g, '&quot;').substring(0, 160) : '');
    if (desc) {
      const meta = '\n<meta name="description" content="' + desc + '">\n';
      c = c.replace('<meta charset', meta + '<meta charset');
      mod = true;
      addedMeta++;
    }
  }

  // Fix <title> to include brand suffix
  if (c.includes('<title>') && !c.includes('| DogeKing') && !c.includes('- DogeKing') && !c.includes('DogeKing')) {
    c = c.replace(/<title>([^<]+)<\/title>/, '<title>$1 | DogeKing</title>');
    mod = true;
    fixedTitle++;
  }

  if (mod) fs.writeFileSync(fp, c, 'utf8');
});

console.log('Meta descriptions added:', addedMeta);
console.log('Titles fixed (added DogeKing suffix):', fixedTitle);
