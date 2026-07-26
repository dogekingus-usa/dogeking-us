import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = __dirname;

const htmlFiles = fs.readdirSync(root).filter(f => f.endsWith('.html'));
const cssFiles = fs.readdirSync(root).filter(f => f.endsWith('.css'));
const jsFiles = [...fs.readdirSync(root).filter(f => f.endsWith('.js'))];

// Include subdirs
for (const d of ['scripts', 'js', 'css', 'assets']) {
  const dp = path.join(root, d);
  if (fs.existsSync(dp) && fs.statSync(dp).isDirectory()) {
    for (const f of fs.readdirSync(dp)) {
      const fp = path.join(dp, f);
      if (fs.statSync(fp).isFile()) {
        if (f.endsWith('.html')) htmlFiles.push(path.join(d, f));
        if (f.endsWith('.css')) cssFiles.push(path.join(d, f));
        if (f.endsWith('.js')) jsFiles.push(path.join(d, f));
      }
    }
  }
}

console.log('=== ENCODING CORRUPTION SCAN ===');
console.log(`Scanning ${htmlFiles.length} HTML, ${cssFiles.length} CSS, ${jsFiles.length} JS files\n`);

const mojibakePatterns = {
  'ΓÇö': { replacement: '—', desc: 'em dash' },
  'ΓÇ£': { replacement: '"', desc: 'left quote' },
  'ΓÇ¥': { replacement: '"', desc: 'right quote' },
  'ΓÇÉ': { replacement: '-', desc: 'hyphen' },
  'ΓÇó': { replacement: '•', desc: 'bullet' },
  'ΓÇÖ': { replacement: "'", desc: 'apostrophe' },
  'ΓÇô': { replacement: '–', desc: 'en dash' },
  'ΓÇÿ': { replacement: "'", desc: 'left single quote' },
  'ΓÇª': { replacement: '…', desc: 'ellipsis' },
  'ΓÇ▒': { replacement: ' ', desc: 'space' },
};

let totalIssues = 0;

// Check all HTML files
console.log('--- HTML files ---');
let htmlWithIssues = [];
for (const fname of htmlFiles) {
  const fp = path.join(root, fname);
  if (!fs.existsSync(fp)) continue;
  const content = fs.readFileSync(fp, 'utf8');
  const fileIssues = [];
  
  for (const [pattern, info] of Object.entries(mojibakePatterns)) {
    const regex = new RegExp(pattern.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g');
    const matches = content.match(regex);
    if (matches) {
      fileIssues.push(`${pattern} (${info.desc}) x${matches.length}`);
    }
  }
  
  if (fileIssues.length > 0) {
    htmlWithIssues.push({ file: fname, issues: fileIssues });
    totalIssues += fileIssues.length;
  }
}

if (htmlWithIssues.length === 0) {
  console.log('  No encoding issues found in HTML files');
} else {
  for (const f of htmlWithIssues) {
    console.log(`  ${f.file}: ${f.issues.join(', ')}`);
  }
}

// Check all CSS files
console.log('\n--- CSS files ---');
let cssWithIssues = [];
for (const fname of cssFiles) {
  const fp = path.join(root, fname);
  if (!fs.existsSync(fp)) continue;
  const content = fs.readFileSync(fp, 'utf8');
  const fileIssues = [];
  
  for (const [pattern, info] of Object.entries(mojibakePatterns)) {
    const regex = new RegExp(pattern.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g');
    const matches = content.match(regex);
    if (matches) {
      fileIssues.push(`${pattern} (${info.desc}) x${matches.length}`);
    }
  }
  
  if (fileIssues.length > 0) {
    cssWithIssues.push({ file: fname, issues: fileIssues });
    totalIssues += fileIssues.length;
  }
}

if (cssWithIssues.length === 0) {
  console.log('  No encoding issues found in CSS files');
} else {
  for (const f of cssWithIssues) {
    console.log(`  ${f.file}: ${f.issues.join(', ')}`);
  }
}

// Check all JS files
console.log('\n--- JS files ---');
let jsWithIssues = [];
for (const fname of jsFiles) {
  const fp = path.join(root, fname);
  if (!fs.existsSync(fp)) continue;
  const content = fs.readFileSync(fp, 'utf8');
  const fileIssues = [];
  
  for (const [pattern, info] of Object.entries(mojibakePatterns)) {
    const regex = new RegExp(pattern.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g');
    const matches = content.match(regex);
    if (matches) {
      fileIssues.push(`${pattern} (${info.desc}) x${matches.length}`);
    }
  }
  
  if (fileIssues.length > 0) {
    jsWithIssues.push({ file: fname, issues: fileIssues });
    totalIssues += fileIssues.length;
  }
}

if (jsWithIssues.length === 0) {
  console.log('  No encoding issues found in JS files');
} else {
  for (const f of jsWithIssues) {
    console.log(`  ${f.file}: ${f.issues.join(', ')}`);
  }
}

console.log(`\nTotal encoding issues found: ${totalIssues}`);

// Check for missing CSS files referenced in HTML
console.log('\n=== BROKEN CSS REFERENCES ===');
for (const fname of htmlFiles) {
  const fp = path.join(root, fname);
  if (!fs.existsSync(fp)) continue;
  const content = fs.readFileSync(fp, 'utf8');
  const refs = [...content.matchAll(/href="([^"]+\.css[^"]*)"/g)];
  for (const m of refs) {
    let href = m[1].split('?')[0].replace(/^\//, '');
    const fullPath = path.join(root, href);
    if (!fs.existsSync(fullPath)) {
      console.log(`  ${fname}: MISSING CSS -> ${m[1]}`);
    }
  }
}

// Check for missing JS files referenced in HTML
console.log('\n=== BROKEN JS REFERENCES ===');
for (const fname of htmlFiles) {
  const fp = path.join(root, fname);
  if (!fs.existsSync(fp)) continue;
  const content = fs.readFileSync(fp, 'utf8');
  const refs = [...content.matchAll(/src="([^"]+\.js[^"]*)"/g)];
  for (const m of refs) {
    const src = m[1].split('?')[0];
    if (src.startsWith('http')) continue;
    const fpath = src.replace(/^\//, '');
    const fullPath = path.join(root, fpath);
    if (!fs.existsSync(fullPath)) {
      console.log(`  ${fname}: MISSING JS -> ${m[1]}`);
    }
  }
}

console.log('\n=== DONE ===');
