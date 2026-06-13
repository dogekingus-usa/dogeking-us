const fs = require('fs');
const dir = 'C:/content-sites/dogeking.us/articles';
const infected = ['10-solana-meme-coins-under-1.html','ai-meme-coins-crypto-trend-2026.html',
  'best-crypto-exchanges-meme-coin-trading-2026.html','best-solana-defi-platforms-beginners.html',
  'binance-vs-coinbase-2026-crypto-exchange-comparison.html','buy-solana-meme-coins-safely.html'];

const cssPatterns = [
  /\|\s*DogeKing\s*\*\s*\{[^}]*\}\s*body\s*\{[^}]*\}/g,
  /\|\s*DogeKing\s*\*\s*\{[^}]*\}/g,
  /\*\s*\{[^}]*margin:\s*0[^}]*padding:\s*0[^}]*\}[^}]*\}[^}]*\}/g,
  /\*\s*\{ margin: 0; padding: 0; box-sizing: border-box; \}[\s\S]*?color: #333; \}/g
];

infected.forEach(file => {
  const fp = dir + '/' + file;
  let c = fs.readFileSync(fp, 'utf8');
  if (c.charCodeAt(0) === 0xFEFF) c = c.slice(1);
  let mod = false;
  
  // Pattern 1: "Title | DogeKing * { margin... }"
  c = c.replace(/\s*\|\s*DogeKing\s*\*\s*\{[^}]*margin:\s*0[^}]*padding:\s*0[^}]*box-sizing:\s*border-box[^}]*\}[\s\S]*?<\/li>/g, '</li>');
  
  // Pattern 2: Remove any raw CSS blocks in list items or paragraphs
  c = c.replace(/<li>[^<]*\*\s*\{[^}]*\}[^<]*<\/li>/g, '<li>Comprehensive guide covering all key topics including market analysis, trading strategies, and portfolio management.</li>');
  c = c.replace(/<li>[^<]*body\s*\{[^}]*\}[^<]*<\/li>/g, '<li>Detailed analysis with actionable insights for both beginners and experienced traders.</li>');
  
  // Pattern 3: Fix tldr-box first items that have CSS
  c = c.replace(
    /(<div class="tldr-box[^>]*>[\s\S]*?<li>)[^<]*(DogeKing|\* \{)[^<]*<\/li>/,
    '$1Essential knowledge and practical strategies for crypto trading and investing.</li>'
  );
  
  if (c !== fs.readFileSync(fp, 'utf8')) {
    fs.writeFileSync(fp, c, 'utf8');
    mod = true;
  }
  console.log(file + ': ' + (mod ? 'FIXED' : 'NO CHANGE'));
});
