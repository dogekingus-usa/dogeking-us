const fs = require('fs');
let c = fs.readFileSync('C:/content-sites/dogeking.us/index.html', 'utf8');

const shareHTML = '<div class="social-share" style="display:flex;justify-content:center;gap:10px;margin-top:16px;flex-wrap:wrap;">'
  + '<a href="https://twitter.com/intent/tweet?text=Check+out+DogeKing+crypto+guides&amp;url=https://dogeking.us" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;gap:6px;padding:8px 16px;border-radius:8px;background:rgba(29,161,242,0.1);color:#1DA1F2;text-decoration:none;font-size:0.85rem;border:1px solid rgba(29,161,242,0.2);">\u{1F4E2} X Share</a>'
  + '<a href="https://t.me/share/url?url=https://dogeking.us&amp;text=DogeKing" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;gap:6px;padding:8px 16px;border-radius:8px;background:rgba(0,136,204,0.1);color:#0088CC;text-decoration:none;font-size:0.85rem;border:1px solid rgba(0,136,204,0.2);">\u{1F5E8}\uFE0F Telegram</a>'
  + '<a href="https://www.reddit.com/submit?url=https://dogeking.us&amp;title=DogeKing" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;gap:6px;padding:8px 16px;border-radius:8px;background:rgba(255,69,0,0.1);color:#FF4500;text-decoration:none;font-size:0.85rem;border:1px solid rgba(255,69,0,0.2);">\u{1F51D} Reddit</a>'
  + '</div>';

if (!c.includes('social-share')) {
  c = c.replace('<div class="social-proof-badges"', shareHTML + '\n<div class="social-proof-badges"');
  fs.writeFileSync('C:/content-sites/dogeking.us/index.html', c, 'utf8');
  console.log('Social share buttons added to homepage');
} else {
  console.log('Already present');
}
