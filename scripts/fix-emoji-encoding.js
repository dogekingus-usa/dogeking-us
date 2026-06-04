const fs = require('fs');
const dir = 'C:/content-sites/dogeking.us/articles';
let fixed = 0;

fs.readdirSync(dir).filter(f => f.endsWith('.html')).forEach(file => {
  const fp = dir + '/' + file;
  let c = fs.readFileSync(fp, 'utf8');
  if (c.charCodeAt(0) === 0xFEFF) c = c.slice(1);
  let mod = false;

  // Fix â† → ← (left arrow)
  if (c.includes('â†')) { c = c.split('â†').join('\u2190'); mod = true; }
  // Fix ðŸ“‹ → 📋 (clipboard emoji)
  if (c.includes('ð\x9F\x93\x8B')) { c = c.split('ð\x9F\x93\x8B').join('\u{1F4CB}'); mod = true; }
  // Fix â† → → (right arrow)  
  if (c.includes('â†\x92')) { c = c.split('â†\x92').join('\u2192'); mod = true; }
  
  if (mod) { fs.writeFileSync(fp, c, 'utf8'); fixed++; }
});

console.log('Files fixed:', fixed);
