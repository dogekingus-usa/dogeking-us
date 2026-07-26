import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = __dirname;

const htmlFiles = fs.readdirSync(root).filter(f => f.endsWith('.html'));

// Files that ONLY reference crown-v1.css (need link changed to crown-design-system.css)
console.log('=== FIXING files with ONLY crown-v1.css (change to crown-design-system.css) ===');
const onlyV1 = [
  'best-ai-agent-tokens-solana-2026.html',
  'crypto-copy-trading-meme-coins-solana-2026.html',
  'meme-coin-sniping-solana-bots-strategies-2026.html',
  'products.html',
  'solana-transaction-failed-troubleshooting-guide-2026.html',
  'solana-vs-ethereum-2026-complete.html',
  'store.html',
];

for (const fname of onlyV1) {
  const fp = path.join(root, fname);
  if (!fs.existsSync(fp)) {
    console.log(`  ${fname}: SKIP (not found)`);
    continue;
  }
  let content = fs.readFileSync(fp, 'utf8');
  const lines = content.split('\n');
  let modified = false;
  const newLines = lines.map(line => {
    if (line.includes('crown-v1.css')) {
      modified = true;
      return line.replace('crown-v1.css', 'crown-design-system.css');
    }
    return line;
  });
  if (modified) {
    fs.writeFileSync(fp, newLines.join('\n'), 'utf8');
    console.log(`  ${fname}: FIXED (crown-v1.css → crown-design-system.css)`);
  } else {
    console.log(`  ${fname}: no changes needed`);
  }
}

// Files that reference BOTH (remove crown-v1.css line)
console.log('\n=== FIXING files with BOTH crown-v1.css AND crown-design-system.css (remove crown-v1.css) ===');
let bothCount = 0;
for (const fname of htmlFiles) {
  if (onlyV1.includes(fname)) continue;
  const fp = path.join(root, fname);
  if (!fs.existsSync(fp)) continue;
  let content = fs.readFileSync(fp, 'utf8');
  const lines = content.split('\n');
  let modified = false;
  // Remove lines that exclusively reference crown-v1.css (not the design system)
  const newLines = lines.filter(line => {
    if (line.includes('crown-v1.css') && !line.includes('crown-design-system.css')) {
      modified = true;
      return false;
    }
    return true;
  });
  if (modified) {
    fs.writeFileSync(fp, newLines.join('\n'), 'utf8');
    bothCount++;
    console.log(`  ${fname}: REMOVED crown-v1.css reference`);
  }
}
console.log(`  Total files fixed: ${bothCount}`);

// Remove sales-cta-overlay.css references
console.log('\n=== FIXING sales-cta-overlay.css references ===');
const ctaFiles = ['index.html', 'live-html.html'];
for (const fname of ctaFiles) {
  const fp = path.join(root, fname);
  if (!fs.existsSync(fp)) continue;
  let content = fs.readFileSync(fp, 'utf8');
  const lines = content.split('\n');
  let modified = false;
  const newLines = lines.filter(line => {
    if (line.includes('sales-cta-overlay.css')) {
      modified = true;
      return false;
    }
    return true;
  });
  if (modified) {
    fs.writeFileSync(fp, newLines.join('\n'), 'utf8');
    console.log(`  ${fname}: REMOVED sales-cta-overlay.css reference`);
  } else {
    console.log(`  ${fname}: no changes needed`);
  }
}

console.log('\n=== ALL CSS FIXES COMPLETE ===');
