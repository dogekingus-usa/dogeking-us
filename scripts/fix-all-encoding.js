const fs = require('fs');
const dir = 'C:/content-sites/dogeking.us/articles';

// ONLY verified byte-sequence replacements
const fixes = {
  // Ã¢â‚¬Â (6 bytes) -> ← (3 bytes) - left arrow
  'c3a2e280a0c290': 'e28690',
  // Ã°Å¸ï¿½ (10 bytes) -> 📋 (4 bytes) - clipboard emoji
  'c3b0c5b8e2809ce280b9': 'f09f938b',
};

const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));
let totalFixed = 0;

files.forEach(file => {
  let b = fs.readFileSync(dir + '/' + file);
  if (b[0] === 0xEF && b[1] === 0xBB && b[2] === 0xBF) b = b.slice(3);
  const h = b.toString('hex').toLowerCase();
  let newH = h;
  let mod = false;
  
  Object.keys(fixes).forEach(bad => {
    if (newH.includes(bad)) {
      const before = newH.length;
      newH = newH.split(bad).join(fixes[bad]);
      if (newH.length !== before) mod = true;
    }
  });
  
  if (mod) {
    fs.writeFileSync(dir + '/' + file, Buffer.from(newH, 'hex'));
    totalFixed++;
  }
});

console.log('Files fixed:', totalFixed);

// Verify
let remaining = 0;
files.forEach(file => {
  const h = fs.readFileSync(dir + '/' + file).toString('hex').toLowerCase();
  Object.keys(fixes).forEach(bad => { if (h.includes(bad)) remaining++; });
});
console.log('Remaining with issues:', remaining);
