const fs = require('fs');
const dir = 'C:/content-sites/dogeking.us/articles';
let badCount = 0;

fs.readdirSync(dir).filter(f => f.endsWith('.html')).forEach(f => {
  const fp = dir + '/' + f;
  let c = fs.readFileSync(fp, 'utf8');
  let mod = false;
  
  if (c.includes('Â©')) { c = c.split('Â©').join('\u00A9'); mod = true; }
  if (c.includes('â€"')) { c = c.split('â€"').join('\u2014'); mod = true; }
  if (c.includes('â€™')) { c = c.split('â€™').join('\u2019'); mod = true; }
  if (c.includes('â€œ')) { c = c.split('â€œ').join('\u201C'); mod = true; }
  if (c.includes('â€')) { c = c.split('â€').join('\u201D'); mod = true; }
  
  if (mod) { fs.writeFileSync(fp, c, 'utf8'); badCount++; }
});

console.log('Files with encoding fixes:', badCount);
