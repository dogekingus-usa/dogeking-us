// FULL VERIFICATION â€˝ check every claim against live main domain
const https = require('https');

function get(url) {
  return new Promise((resolve, reject) => {
    https.get(url, {headers:{'User-Agent':'Mozilla/5.0'}}, res => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => resolve({status: res.statusCode, cache: res.headers['cf-cache-status']||'N/A', html: data}));
    }).on('error', reject);
  });
}

(async () => {
  const main = await get('https://dogeking.us');
  const preview = await get('https://253302d9.dogeking-us.pages.dev');
  const h = main.html;
  const hp = preview.html;
  
  console.log('=== MAIN DOMAIN (dogeking.us) ===');
  console.log('Status:', main.status, '| Cache:', main.cache);
  const checks = [
    ['Crown CSS link', /crown-design-system\.css/.test(h)],
    ['theme-dogeking class', /theme-dogeking/.test(h)],
    ['Static articles in HTML', /Bitcoin.*Price Prediction/.test(h)],
    ['Font preload', /preload.*fonts/.test(h)],
    ['Non-blocking fonts', /media=.print.*onload/.test(h)],
    ['Organization schema', /"Organization"/.test(h)],
    ['SearchAction schema', /"SearchAction"/.test(h)],
    ['RSS feed link', /feed\.xml/.test(h)],
    ['JSON-LD present', /application\/ld\+json/.test(h)],
    ['Nav bar (DogeKing home)', /DogeKing.*Home.*Articles/.test(h)],
    ['Browse All button', /Browse All 350/.test(h)],
  ];
  checks.forEach(c => console.log(c[1] ? '  âœâ€¦ ' + c[0] : '  â˝Å’ ' + c[0]));
  
  console.log('\n=== PREVIEW URL (latest deploy) ===');
  console.log('Status:', preview.status, '| Cache:', preview.cache);
  const checksP = [
    ['Crown CSS link', /crown-design-system\.css/.test(hp)],
    ['Nav bar', /DogeKing.*Home.*Articles/.test(hp)],
    ['Browse All', /Browse All 350/.test(hp)],
  ];
  checksP.forEach(c => console.log(c[1] ? '  âœâ€¦ ' + c[0] : '  â˝Å’ ' + c[0]));
  
  console.log('\n=== DIFFERENCES ===');
  // Are they serving the same file?
  if (h.length === hp.length) console.log('IDENTICAL content length');
  else console.log(`DIFFERENT lengths: main=${h.length}, preview=${hp.length} (diff=${Math.abs(h.length-hp.length)})`);
  
  // Count Gumroad links
  const gMain = (h.match(/gumroad\.com\/l\//g) || []).length;
  const gPrev = (hp.match(/gumroad\.com\/l\//g) || []).length;
  console.log(`Gumroad links: main=${gMain}, preview=${gPrev}`);
  
  // Specific broken gumroad check
  if (h.includes('gumroad.com/l/crypto-bundle"')) console.log('â˝Å’ MAIN has BROKEN gumroad link (crypto-bundle without prefix)');
  else console.log('âœâ€¦ MAIN gumroad links are correct');
  
  // Article count from page
  const acMatch = h.match(/Showing\s+<strong[^>]*>(\d+)<\/strong>\s+articles/);
  console.log(`Article count on main: ${acMatch ? acMatch[1] : 'NOT FOUND'}`);
})().catch(e => console.error('Error:', e.message));
