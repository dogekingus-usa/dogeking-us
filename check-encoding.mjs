import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Check crown-design-system.css
const cssPath = path.join(__dirname, 'crown-design-system.css');
const css = fs.readFileSync(cssPath, 'utf8');

console.log('=== CROWN-DESIGN-SYSTEM.CSS ENCODING CHECK ===');

// Check for mojibake patterns
const checks = [
  { name: 'ΓÇö', pattern: /ΓÇö/g, replacement: '—' },
  { name: 'ΓÇ£', pattern: /ΓÇ£/g, replacement: '"' },
  { name: 'ΓÇ¥', pattern: /ΓÇ¥/g, replacement: '"' },
  { name: 'ΓÇÉ', pattern: /ΓÇÉ/g, replacement: '-' },
  { name: 'ΓÇó', pattern: /ΓÇó/g, replacement: '•' },
  { name: 'ΓÇÖ', pattern: /ΓÇÖ/g, replacement: "'" },
  { name: 'ΓÇô', pattern: /ΓÇô/g, replacement: '–' },
  { name: 'ΓÇÿ', pattern: /ΓÇÿ/g, replacement: "'" },
  { name: 'ΓÇ¢', pattern: /ΓÇ¢/g, replacement: '’' },
  { name: 'ΓÇª', pattern: /ΓÇª/g, replacement: '…' },
  { name: 'ΓÇ░', pattern: /ΓÇ░/g, replacement: '%' },
];

let hasIssues = false;
for (const check of checks) {
  const matches = css.match(check.pattern);
  if (matches) {
    hasIssues = true;
    console.log(`  FOUND ${matches.length}x: ${check.name} (should be "${check.replacement}")`);
    // Show context for first match
    const idx = css.indexOf(matches[0]);
    console.log(`    Context: ...${css.substring(Math.max(0,idx-20), idx+30).replace(/\n/g, ' ')}...`);
  }
}

if (!hasIssues) {
  console.log('  No mojibike patterns found in crown-design-system.css');
}

// Now check the index.html
console.log('\n=== INDEX.HTML ENCODING CHECK ===');
const htmlPath = path.join(__dirname, 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');

for (const check of checks) {
  const matches = html.match(check.pattern);
  if (matches) {
    console.log(`  FOUND ${matches.length}x: ${check.name} (should be "${check.replacement}")`);
  }
}

// Check for HTML issues in index.html
console.log('\n=== INDEX.HTML STRUCTURE CHECK ===');

// Check for title tag
if (html.includes('<title>')) {
  const titleMatch = html.match(/<title>(.*?)<\/title>/);
  console.log(`  TITLE: ${titleMatch ? titleMatch[1] : 'missing'}`);
}

// Check meta description
if (html.includes('meta name="description"')) {
  const descMatch = html.match(/meta name="description" content="([^"]+)"/);
  console.log(`  META DESCRIPTION: ${descMatch ? descMatch[1].substring(0, 80) + '...' : 'missing'}`);
}

// Check og tags
const ogChecks = ['og:title', 'og:description', 'og:image', 'og:url'];
for (const og of ogChecks) {
  const has = html.includes(`property="${og}"`) || html.includes(`property='${og}'`);
  console.log(`  ${og}: ${has ? 'PRESENT' : 'MISSING'}`);
}

// Check twitter tags
const twChecks = ['twitter:card', 'twitter:title', 'twitter:description', 'twitter:image'];
for (const tw of twChecks) {
  const has = html.includes(`name="${tw}"`) || html.includes(`name='${tw}'`);
  console.log(`  ${tw}: ${has ? 'PRESENT' : 'MISSING'}`);
}

// Check canonical
console.log(`  CANONICAL: ${html.includes('rel="canonical"') ? 'PRESENT' : 'MISSING'}`);

// Check JSON-LD
console.log(`  JSON-LD: ${html.includes('application/ld+json') ? 'PRESENT' : 'MISSING'}`);

// Check schema
console.log(`  SCHEMA.ORG: ${html.includes('schema.org') ? 'PRESENT' : 'MISSING'}`);

// Check robots meta
console.log(`  ROBOTS: ${html.includes('name="robots"') ? 'PRESENT' : 'MISSING'}`);

// Check favicon
console.log(`  FAVICON: ${html.includes('rel="icon"') ? 'PRESENT' : 'MISSING'}`);

// Check for broken CTA buttons
console.log('\n=== CTA/BUTTON CHECK ===');
// Check for empty hrefs
const emptyHrefs = html.match(/href=""/g) || [];
console.log(`  Empty hrefs: ${emptyHrefs.length > 0 ? 'FOUND: ' + emptyHrefs.length : 'none'}`);

// Check for missing alt text on images
const imgs = html.match(/<img[^>]*>/g) || [];
let missingAlt = 0;
for (const img of imgs) {
  if (!img.includes('alt=')) missingAlt++;
}
console.log(`  Images without alt: ${missingAlt}${missingAlt > 0 ? ' (FOUND!)' : ''}`);

// Check for broken emoji patterns (like &#xxxx; without proper encoding)
console.log('\n=== EMOJI CHECK ===');
const htmlEntities = html.match(/&#[0-9]+;/g) || [];
console.log(`  HTML entities found: ${htmlEntities.length}`);
if (htmlEntities.length > 0) {
  console.log('  Sample entities:', htmlEntities.slice(0, 10).join(', '));
}

// Check for broken links
console.log('\n=== BROKEN CSS/LINK CHECK ===');
const cssLinks = html.match(/href="([^"]+\.css[^"]*)"/g) || [];
for (const link of cssLinks) {
  const href = link.match(/href="([^"]+)"/)[1];
  const filePath = href.split('?')[0].replace(/^\//, '');
  const fullPath = path.join(__dirname, filePath);
  console.log(`  ${href}: ${fs.existsSync(fullPath) ? 'EXISTS' : 'MISSING!'}`);
}

const jsLinks = html.match(/src="([^"]+\.js[^"]*)"/g) || [];
for (const link of jsLinks) {
  const src = link.match(/src="([^"]+)"/)[1];
  // Skip external URLs
  if (src.startsWith('http')) {
    console.log(`  ${src}: EXTERNAL`);
    continue;
  }
  const filePath = src.split('?')[0].replace(/^\//, '');
  const fullPath = path.join(__dirname, filePath);
  console.log(`  ${src}: ${fs.existsSync(fullPath) ? 'EXISTS' : 'MISSING!'}`);
}

console.log('\n=== DONE ===');
