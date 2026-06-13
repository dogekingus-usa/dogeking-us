const fs = require('fs');
const dir = 'C:/content-sites/dogeking.us/articles';
const checks = ['404','about','checkout','contact','disclaimer','privacy','products','thank-you','all-articles','crypto-bundle'];

checks.forEach(slug => {
  const fp = dir + '/' + slug + '.html';
  if (!fs.existsSync(fp)) { console.log(slug + ': MISSING'); return; }
  const c = fs.readFileSync(fp, 'utf8');
  const hasStickyBar = c.includes('nav-bar');
  const hasSiteNav = c.includes('site-nav');
  const dogeCount = (c.match(/DogeKing/g) || []).length;
  const footerCount = (c.match(/<footer/g) || []).length;
  const navDupes = dogeCount > 3 ? 'DUPLICATE!' : 'OK';
  const footDupes = footerCount > 1 ? 'DUPLICATE!' : 'OK';
  console.log(slug + ': sticky=' + hasStickyBar + ' siteNav=' + hasSiteNav + ' DogeKing=' + dogeCount + ' ' + navDupes + ' footers=' + footerCount + ' ' + footDupes);
});
