const fs = require('fs');
const dir = 'C:/content-sites/dogeking.us/articles';
let fixed = 0;

fs.readdirSync(dir).filter(f => f.endsWith('.html')).forEach(file => {
  const fp = dir + '/' + file;
  let c = fs.readFileSync(fp, 'utf8');
  if (c.charCodeAt(0) === 0xFEFF) c = c.slice(1);
  let mod = false;

  // Fix Ã¢â€ Â â†â„¢ â†Â (left arrow)
  if (c.includes('Ã¢â€ Â')) { c = c.split('Ã¢â€ Â').join('\u2190'); mod = true; }
  // Fix Ã°Å¸â€Å“â€¹ â†â„¢ ðŸÅ“â€¹ (clipboard emoji)
  if (c.includes('Ã°\x9F\x93\x8B')) { c = c.split('Ã°\x9F\x93\x8B').join('\u{1F4CB}'); mod = true; }
  // Fix Ã¢â€ Â’ â†â„¢ â†â„¢ (right arrow)  
  if (c.includes('Ã¢â€ \x92')) { c = c.split('Ã¢â€ \x92').join('\u2192'); mod = true; }
  
  if (mod) { fs.writeFileSync(fp, c, 'utf8'); fixed++; }
});

console.log('Files fixed:', fixed);
