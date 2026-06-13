const fs = require('fs');
let c = fs.readFileSync('C:/content-sites/dogeking.us/index.html', 'utf8');
c = c.replace('class=" stat-label>', 'class="stat-label">');
fs.writeFileSync('C:/content-sites/dogeking.us/index.html', c, 'utf8');
console.log('Fixed');
