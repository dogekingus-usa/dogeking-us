const fs = require('fs');
const sample = fs.readFileSync('C:/content-sites/dogeking.us/articles/10-solana-meme-coins-under-1.html', 'utf8');
console.log('Has meta desc:', sample.includes('meta name="description"'));
const titleMatch = sample.match(/<title>([^<]+)<\/title>/);
console.log('Title:', titleMatch ? titleMatch[1] : 'NOT FOUND');
