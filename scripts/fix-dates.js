const fs = require('fs');
const dir = 'C:/content-sites/dogeking.us/articles';
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));
let fixed = 0;

files.forEach(f => {
  const fp = dir + '/' + f;
  let c = fs.readFileSync(fp, 'utf8');
  if (c.charCodeAt(0) === 0xFEFF) c = c.slice(1);
  
  // Fix datePublished: "2026" → "2026-01-01" (valid ISO date for schema)
  const regex = /"datePublished":\s*"(\d{4})"(?!-)/g;
  if (regex.test(c)) {
    c = c.replace(regex, '"datePublished": "$1-01-01"');
    fs.writeFileSync(fp, c, 'utf8');
    fixed++;
  }
});

console.log('Fixed datePublished:', fixed);
