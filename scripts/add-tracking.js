const fs = require('fs');
const idx = fs.readFileSync('C:/content-sites/dogeking.us/index.html', 'utf8');

// Role: Analytics & Behavior Analyst
// Check existing GA setup
const hasGA = idx.includes('G-8CVE2X8R5L');
const hasGTag = idx.includes('gtag');
const hasScrollTracking = idx.includes('scroll');
const hasClickTracking = idx.includes('click');

console.log('=== ANALYTICS AUDIT ===');
console.log('GA4 tag present:', hasGA);
console.log('gtag.js loaded:', hasGTag);
console.log('Scroll depth tracking:', hasScrollTracking);
console.log('Click tracking:', hasClickTracking);

if (hasGA && hasGTag && !hasScrollTracking) {
  // Add scroll depth + click tracking events
  const analyticsJS = `
<script>
// Scroll depth tracking
let scrollDepths = [25, 50, 75, 100];
scrollDepths.forEach(d => {
  window.addEventListener('scroll', function handler() {
    const scrolled = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100;
    if (scrolled >= d) {
      gtag('event', 'scroll_depth', { depth: d + '%' });
      window.removeEventListener('scroll', handler);
    }
  });
});
// Article click tracking
document.addEventListener('click', function(e) {
  const link = e.target.closest('a');
  if (link && link.href && link.href.includes('/articles/')) {
    gtag('event', 'article_click', { article_url: link.href });
  }
  if (link && link.href && link.href.includes('gumroad.com')) {
    gtag('event', 'bundle_click', { url: link.href });
  }
});
</script>`;
  
  const newIdx = idx.replace('</body>', analyticsJS + '\n</body>');
  fs.writeFileSync('C:/content-sites/dogeking.us/index.html', newIdx, 'utf8');
  console.log('âœâ€¦ Scroll + click tracking added');
} else if (!hasGA) {
  console.log('â˝Å’ GA tag missing');
} else {
  console.log('âš ï¸Â Check status:', hasScrollTracking ? 'scroll OK' : 'scroll MISSING', hasClickTracking ? 'click OK' : 'click MISSING');
}
