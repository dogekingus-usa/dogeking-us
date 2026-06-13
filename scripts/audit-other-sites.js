const fs = require('fs');
const sites = {
  'lifesystemos.com': 'LifeSystemOS',
  'remoteworkhub.net': 'RemoteWorkHub', 
  'resumeprotips.com': 'ResumeProTips'
};

Object.keys(sites).forEach(site => {
  const dir = 'C:/content-sites/' + site;
  const name = sites[site];
  console.log('=== ' + name + ' (' + site + ') ===');
  
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));
  files.forEach(f => {
    const c = fs.readFileSync(dir + '/' + f, 'utf8');
    const issues = [];
    if (!c.includes('<!DOCTYPE')) issues.push('NO DOCTYPE');
    if (!c.includes('</html>')) issues.push('NO CLOSING');
    if (!c.includes('application/ld+json')) issues.push('NO LD');
    if (!c.includes('rel="canonical"')) issues.push('NO CANONICAL');
    const footers = (c.match(/<footer/g) || []).length;
    if (footers > 1) issues.push('DUP FOOTER(' + footers + ')');
    const navs = (c.match(/nav-bar/g) || []).length;
    if (navs > 1) issues.push('DUP NAV(' + navs + ')');
    console.log('  ' + f + ': ' + (issues.length ? issues.join(', ') : 'CLEAN'));
  });
});
