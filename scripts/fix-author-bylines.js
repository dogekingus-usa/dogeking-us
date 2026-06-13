// Fix author bylines in ALL articles - handles both old and new templates
const fs = require('fs');
const path = require('path');

const dir = 'C:/content-sites/dogeking.us/articles';
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));

const systemPages = ['404','about','checkout','contact','privacy','products','thank-you','all-articles','crypto-bundle',
  'template','nav-component-enhanced','preview-card','cta-snippets','fetched-live','ecosystem-section',
  'sales-cta-overlay','sales-thank-you','dogeking-article-og-template','affiliate','dynamic-loader'];

let fixed = 0;
let skipped = 0;
let errors = 0;

files.forEach(f => {
  const slug = f.replace('.html','');
  if (systemPages.includes(slug)) { skipped++; return; }
  
  try {
    let html = fs.readFileSync(path.join(dir, f), 'utf8');
    if (html.charCodeAt(0) === 0xFEFF) html = html.slice(1);
    
    // Skip if already has author byline
    if (html.includes('Samuel Pason') || html.includes('By Samuel')) { skipped++; return; }
    
    let modified = false;
    
    // Pattern 1: New template - <div class="meta">X min read</div>
    if (html.includes('class="meta"') && !html.includes('author-byline')) {
      html = html.replace(
        /(<div class="meta">[^<]*?min read[^<]*?<\/div>)/,
        '$1\n<div class="author-byline" style="font-size:0.85rem;color:var(--text-muted);margin-top:8px;">By <a href="/about.html" style="color:var(--accent);">Samuel Pason</a> · DogeKing Editor</div>'
      );
      modified = true;
    }
    
    // Pattern 2: Old template - inline article-header
    if (html.includes('class="article-header"') && !html.includes('By Samuel')) {
      html = html.replace(
        /(<div class="article-header"[^>]*>[\s\S]*?<p[^>]*>.*?<\/p>)/,
        '$1\n<p style="font-size:0.85rem;color:#8080a0;margin-top:8px;">By <a href="/about.html" style="color:#FFD700;">Samuel Pason</a> · DogeKing Editor</p>'
      );
      modified = true;
    }
    
    // Pattern 3: Any article with first <p> after header-like div
    if (!modified && html.includes('class="article-card-content"')) {
      // It's a card, not an article page, skip
      skipped++;
      return;
    }
    
    if (modified) {
      fs.writeFileSync(path.join(dir, f), html, 'utf8');
      fixed++;
    } else {
      skipped++;
    }
  } catch(e) {
    errors++;
  }
});

console.log(`Fixed: ${fixed}, Skipped: ${skipped}, Errors: ${errors}`);
