const { chromium } = require('C:/Users/SAMPC/AppData/Roaming/npm/node_modules/playwright');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch({ headless: true, args: ['--no-sandbox'] });

  // === DESKTOP SCREENSHOT ===
  const page1 = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  const errors = [];
  page1.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });

  await page1.goto('https://dogeking.us', { waitUntil: 'networkidle', timeout: 30000 });
  await page1.waitForTimeout(3000);

  await page1.screenshot({ path: 'C:/temp/dogeking-desktop.png', fullPage: true });
  console.log('âœâ€¦ Desktop screenshot saved');

  // === MOBILE SCREENSHOT ===
  const page2 = await browser.newPage({ viewport: { width: 375, height: 812 } });
  await page2.goto('https://dogeking.us', { waitUntil: 'networkidle', timeout: 30000 });
  await page2.waitForTimeout(3000);
  await page2.screenshot({ path: 'C:/temp/dogeking-mobile.png', fullPage: true });
  console.log('âœâ€¦ Mobile screenshot saved');

  // === RENDER ANALYSIS ===
  const html = await page1.content();
  const articleCards = (html.match(/article-card/g) || []).length;
  const bodyText = await page1.evaluate(() => document.body.innerText);
  const statCheck = bodyText.match(/332|Articles|Guides/);
  
  console.log('\n=== RENDER ANALYSIS ===');
  console.log('Article cards rendered:', articleCards);
  console.log('Stats visible:', statCheck ? statCheck[0] : 'NONE');
  
  // Extract visible headlines
  const headlines = await page1.evaluate(() => {
    return [...document.querySelectorAll('.article-card h3')].slice(0, 5).map(h => h.textContent.trim());
  });
  console.log('Visible article titles:');
  headlines.forEach((h, i) => console.log(`  ${i+1}. ${h}`));
  
  // Check if search is visible
  const searchVisible = await page1.evaluate(() => {
    const el = document.getElementById('search-articles');
    return el ? el.offsetParent !== null : false;
  });
  console.log('Search bar visible:', searchVisible);
  
  // Check category filter
  const catFilter = await page1.evaluate(() => {
    const el = document.querySelector('.category-filter');
    return el ? el.offsetParent !== null : false;
  });
  console.log('Category filter visible:', catFilter);

  // Check errors
  if (errors.length) {
    console.log('\nâš ï¸Â Console errors:');
    errors.forEach(e => console.log('  -', e));
  } else {
    console.log('âœâ€¦ No console errors');
  }

  // === PERFORMANCE METRICS ===
  const perf = await page1.evaluate(() => ({
    fcp: performance.getEntriesByType('paint').find(e => e.name === 'first-contentful-paint')?.startTime || 'N/A',
    dcl: performance.timing ? (performance.timing.domContentLoadedEventEnd - performance.timing.navigationStart) : 'N/A',
    load: performance.timing ? (performance.timing.loadEventEnd - performance.timing.navigationStart) : 'N/A',
  }));
  console.log('\n=== PERFORMANCE ===');
  console.log('FCP:', perf.fcp ? Math.round(perf.fcp) + 'ms' : 'N/A');
  console.log('DOM Content Loaded:', perf.dcl !== 'N/A' ? Math.round(perf.dcl) + 'ms' : 'N/A');
  console.log('Page Load:', perf.load !== 'N/A' ? Math.round(perf.load) + 'ms' : 'N/A');

  // === EXTERNAL LINK CHECK ===
  const links = await page1.evaluate(() => {
    return [...document.querySelectorAll('a[href]')].map(a => a.href).filter(h => h.includes('gumroad.com') || h.includes('amazon.com'));
  });
  console.log('\n=== EXTERNAL LINKS FOUND ===');
  [...new Set(links)].forEach(l => console.log('  ', l));

  await browser.close();
  console.log('\nâœâ€¦ Audit complete. Screenshots saved.');
})().catch(e => { console.error('FATAL:', e.message, e.stack); process.exit(1); });
