// RSS Feed Generator - Run on article updates
// Generates feed.xml from articles-data.js
const fs = require("fs");

// Read and evaluate the articles data
const dataJs = fs.readFileSync("C:/content-sites/dogeking.us/articles-data.js", "utf8");
const match = dataJs.match(/const articles = (\[[\s\S]*?\]);/);
if (!match) { console.error("Could not parse articles data"); process.exit(1); }

const articles = JSON.parse(match[1].replace(/(\w+):/g, '"$1":').replace(/'/g, '"'));
const siteUrl = "https://dogeking.us";
const now = new Date().toUTCString();

let rss = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/">
<channel>
  <title>DogeKing - Meme Coin Trading Guides & Crypto Insights</title>
  <link>${siteUrl}</link>
  <description>Expert meme coin trading guides, Solana crypto insights, and the DogeKing Crypto Bundle.</description>
  <language>en-us</language>
  <lastBuildDate>${now}</lastBuildDate>
  <atom:link href="${siteUrl}/feed.xml" rel="self" type="application/rss+xml"/>
`;

// Add the 50 most recent articles
const recent = articles.slice(0, 50);
recent.forEach((article) => {
  const title = (article.title || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  const excerpt = (article.excerpt || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  const url = article.slug ? `${siteUrl}/articles/${article.slug}.html` : siteUrl;
  const cat = (article.category || "general").toLowerCase();
  
  rss += `  <item>
    <title><![CDATA[${title}]]></title>
    <link>${url}</link>
    <guid isPermaLink="true">${url}</guid>
    <description><![CDATA[${excerpt}]]></description>
    <category>${cat}</category>
    <pubDate>${now}</pubDate>
  </item>
`;
});

rss += `</channel>
</rss>`;

fs.writeFileSync("C:/content-sites/dogeking.us/feed.xml", rss, "utf8");
console.log("RSS feed generated: feed.xml");
