const fs = require('fs');
let c = fs.readFileSync('C:/content-sites/dogeking.us/index.html', 'utf8');

if (c.includes('social-proof-badges')) {
  console.log('Already has badges');
  process.exit(0);
}

const badges = `<div class="social-proof-badges" style="display:flex;justify-content:center;gap:20px;flex-wrap:wrap;margin-top:24px;">
<div style="display:flex;align-items:center;gap:10px;background:rgba(255,215,0,0.08);border:1px solid rgba(255,215,0,0.15);border-radius:10px;padding:10px 18px;">
<span style="font-size:1.4rem;">ðŸÅ“¥</span><div><div style="font-size:1.1rem;font-weight:700;color:#f5f5ff;">500+</div><div style="font-size:0.75rem;color:#8080a0;">Traders</div></div></div>
<div style="display:flex;align-items:center;gap:10px;background:rgba(255,215,0,0.08);border:1px solid rgba(255,215,0,0.15);border-radius:10px;padding:10px 18px;">
<span style="font-size:1.4rem;">â­Â</span><div><div style="font-size:1.1rem;font-weight:700;color:#f5f5ff;">4.8/5</div><div style="font-size:0.75rem;color:#8080a0;">Rating</div></div></div>
<div style="display:flex;align-items:center;gap:10px;background:rgba(255,215,0,0.08);border:1px solid rgba(255,215,0,0.15);border-radius:10px;padding:10px 18px;">
<span style="font-size:1.4rem;">âš¡</span><div><div style="font-size:1.1rem;font-weight:700;color:#f5f5ff;">3min</div><div style="font-size:0.75rem;color:#8080a0;">Delivery</div></div></div>
</div>`;

c = c.replace('</header>', badges + '\n</header>');
fs.writeFileSync('C:/content-sites/dogeking.us/index.html', c, 'utf8');
console.log('Social proof badges added');
