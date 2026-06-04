// Fix author bylines on OLD TEMPLATE articles
const fs = require('fs');
const path = require('path');

const dir = 'C:/content-sites/dogeking.us/articles';
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));

let fixed = 0;
let skipped = 0;

files.forEach(f => {
  const fp = path.join(dir, f);
  let html = fs.readFileSync(fp, 'utf8');
  if (html.charCodeAt(0) === 0xFEFF) html = html.slice(1);
  
  // Skip if already has author
  if (html.includes('Samuel Pason') || html.includes('By Samuel')) { skipped++; return; }
  
  // Skip system pages
  if (f.match(/^(404|about|checkout|contact|privacy|products|thank-you|all-articles|crypto-bundle|template|nav|preview|cta|fetched|eco|sales|dogeking|affiliate|dynamic)/)) { skipped++; return; }
  
  let modified = false;
  
  // Pattern: old template with .subtitle div after h1
  if (html.includes('class="subtitle"') && !html.includes('author-line')) {
    html = html.replace(
      /(<div class="subtitle">[^<]*<\/div>)/,
      '$1\n<div class="author-line" style="font-size:0.85rem;color:#7b72b0;margin-top:-0.5rem;margin-bottom:1.5rem;">By <a href="/about.html" style="color:var(--color-gold, #FFD700);text-decoration:none;">Samuel Pason</a> · DogeKing Editor</div>'
    );
    modified = true;
  }
  
  // Pattern: JSON-LD author schema
  if (!html.includes('"author":')) {
    const ldMatch = html.match(/<script type="application\/ld\+json">[\s\S]*?<\/script>/);
    if (ldMatch) {
      const ld = ldMatch[0];
      if (ld.includes('"@type":"Article"') && !ld.includes('"author"')) {
        const newLd = ld.replace(
          '"@type":"Article"',
          '"@type":"Article",\n  "author": {"@type":"Person","name":"Samuel Pason","url":"https://dogeking.us/about.html"}'
        );
        html = html.replace(ld, newLd);
        modified = true;
      }
    }
  }
  
  if (modified) {
    fs.writeFileSync(fp, html, 'utf8');
    fixed++;
  } else {
    skipped++;
  }
});

console.log(`Fixed: ${fixed}, Skipped: ${skipped} (already had author or can't match pattern)`);
