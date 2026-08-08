// debug-axe.mjs - dump full axe target-size + contrast details for DK dist
import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';
import axeSource from 'axe-core';

const ROOT = process.cwd();
const distDir = path.resolve(ROOT, 'dist');
const pages = [
  { name: 'home', path: 'index.html' },
  { name: 'article', path: 'dogeking-price-prediction.html' },
  { name: 'product', path: 'products.html' },
  { name: '404', path: '404.html' },
];

const browser = await chromium.launch();
for (const p of pages) {
  const abs = path.join(distDir, p.path);
  if (!fs.existsSync(abs)) { console.log(`\n=== ${p.name}: MISSING ===`); continue; }
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  await page.goto('file://' + abs.replace(/\\/g, '/'), { waitUntil: 'load' });
  await page.addScriptTag({ content: axeSource.source });
  const results = await page.evaluate(async () => {
    const r = await window.axe.run(document, {
      resultTypes: ['violations'],
      rules: { 'color-contrast': { enabled: true }, 'target-size': { enabled: true } },
    });
    return r.violations.map((v) => ({
      id: v.id, impact: v.impact,
      nodes: v.nodes.map((n) => {
        const el = typeof n.target[0] === 'string' ? document.querySelector(n.target[0]) : null;
        let box = null;
        if (el) { const b = el.getBoundingClientRect(); box = { w: Math.round(b.width), h: Math.round(b.height), cls: el.className, tag: el.tagName, text: (el.textContent || '').trim().slice(0, 40), bg: getComputedStyle(el).backgroundColor, color: getComputedStyle(el).color, fs: getComputedStyle(el).fontSize }; }
        return { target: n.target.join(' '), html: (n.html || '').slice(0, 160), box };
      }),
    }));
  });
  console.log(`\n=== ${p.name} (${p.path}) ===`);
  for (const v of results) {
    console.log(`\n-- ${v.id} [${v.impact}] ×${v.nodes.length}`);
    v.nodes.forEach((n, i) => {
      if (i > 12) return;
      const b = n.box ? `box=${b_show(n.box)}` : 'no-box';
      console.log(`  ${n.target} | ${b} | ${n.html}`);
    });
  }
  await page.close();
}
await browser.close();

function b_show(b) { return `${b.w}x${b.h} cls="${b.cls.slice(0,80)}" bg=${b.bg} color=${b.color} fs=${b.fs} "${b.text}"`; }
