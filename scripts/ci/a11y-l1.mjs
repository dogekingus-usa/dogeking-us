#!/usr/bin/env node
/**
 * a11y-l1.mjs — GATE L3 (axe-core L1 automated scan)
 * CI-CD-STANDARD.md §5 L3 / A11Y-QA-GATE-SPEC.md §2.0 (Ula spec, Bolt runner)
 *
 * L1 contract: axe-core 4.x + chromium on BUILT pages — 0 critical, 0 serious
 * on the key page set (home, article, category, product, 404, thank-you).
 * M3 contrast + canary #4/#5 ride inside canary.mjs (this gate = axe only).
 *
 * Page set from config/a11y-pages.json:
 *   { "pages": [ { "name": "home", "path": "index.html",
 *                  "skip": "SKIPPED-PENDING", "reason": "Phase 1.2 thank-you" } ] }
 *   - omit "skip" to scan; SKIPPED-PENDING pages log + stay green
 *   - default when config absent: index.html + 404.html (+ thank-you.html SKIPPED-PENDING)
 *
 * Usage: node scripts/ci/a11y-l1.mjs [distDir=dist]
 * Exit: 0 = pass (0 critical + 0 serious; skipped honored), 1 = fail (deploy-blocking)
 * Deps (repo package.json devDependencies): axe-core, playwright; `npx playwright install chromium`
 */
import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import { chromium } from 'playwright';
import axeSource from 'axe-core'; // resolves axe.min.js source via node export

const ROOT = process.cwd();
const distDir = path.resolve(ROOT, process.argv[2] || 'dist');

/**
 * Serve distDir over localhost HTTP.
 * WHY: page.goto('file://...') cannot resolve absolute asset URLs
 * (/crown-design-system.css, /_astro/*.css) — they resolve to the drive
 * root and never load, so axe measures UNSTYLED DOM (every link = 17px UA
 * default -> mass false-positive target-size + contrast failures).
 * Local HTTP = real rendered CSS = valid axe results. (frontend-engineer fix 2026-08-08)
 */
const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.avif': 'image/avif',
  '.ico': 'image/x-icon',
  '.woff2': 'font/woff2',
  '.woff': 'font/woff',
  '.json': 'application/json',
  '.txt': 'text/plain; charset=utf-8',
};

function createServer() {
  return http.createServer((req, res) => {
    let urlPath = decodeURIComponent((req.url || '/').split('?')[0]);
    if (urlPath === '/') urlPath = '/index.html';
    const filePath = path.join(distDir, urlPath);
    // path traversal guard
    if (!filePath.startsWith(distDir) || !fs.existsSync(filePath) || !fs.statSync(filePath).isFile()) {
      res.writeHead(404);
      res.end('not found');
      return;
    }
    res.writeHead(200, { 'Content-Type': MIME[path.extname(filePath)] || 'application/octet-stream' });
    fs.createReadStream(filePath).pipe(res);
  });
}

function listen(server) {
  return new Promise((resolve) => {
    server.listen(0, '127.0.0.1', () => resolve(server.address().port));
  });
}

function loadPages() {
  const cfgPath = path.join(ROOT, 'config', 'a11y-pages.json');
  if (fs.existsSync(cfgPath)) {
    const cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
    return cfg.pages.map((p) => ({ ...p, skip: p.skip || null, reason: p.reason || null }));
  }
  return [
    { name: 'home', path: 'index.html', skip: null, reason: null },
    { name: '404', path: '404.html', skip: null, reason: null },
    { name: 'thank-you', path: 'thank-you.html', skip: 'SKIPPED-PENDING', reason: 'Phase 1.2 in-repo route' },
  ];
}

const pages = loadPages();
const failures = [];
const skipped = [];

const server = createServer();
const port = await listen(server);
const baseUrl = `http://127.0.0.1:${port}/`;

const browser = await chromium.launch();
try {
for (const p of pages) {
  if (!fs.existsSync(path.join(distDir, p.path))) {
    if (p.skip) { skipped.push(`${p.name} (${p.path}) — missing but ${p.skip}: ${p.reason}`); continue; }
    failures.push(`${p.name}: ${p.path} missing in dist — page set incomplete`);
    continue;
  }
  if (p.skip) { skipped.push(`${p.name} (${p.path}) — ${p.skip}: ${p.reason}`); continue; }

  try {
    const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
    await page.goto(baseUrl + p.path, { waitUntil: 'load' });
    await page.addScriptTag({ content: axeSource.source });
    const results = await page.evaluate(async () => {
      const r = await window.axe.run(document, {
        resultTypes: ['violations'],
        rules: { 'color-contrast': { enabled: true }, 'target-size': { enabled: true } },
      });
      return r.violations.map((v) => ({ id: v.id, impact: v.impact, help: v.help, nodes: v.nodes.length, targets: v.nodes.slice(0, 3).map((n) => n.target.join(' ')) }));
    });
    const bad = results.filter((v) => v.impact === 'critical' || v.impact === 'serious');
    if (bad.length) {
      for (const v of bad) {
        failures.push(`${p.name}: axe ${v.id} (${v.impact}) — ${v.help} ×${v.nodes} ${v.targets.join(' | ')}`);
      }
    } else {
      console.log(`axe ${p.name} PASS (${results.length} non-critical violation types)`);
    }
    await page.close();
  } catch (e) {
    failures.push(`${p.name}: scan error — ${e.message}`);
  }
}
} finally {
  await browser.close();
  server.close();
}

for (const s of skipped) console.log(`SKIPPED ${s}`);

if (failures.length) {
  console.error(`A11Y L1 GATE FAIL (${failures.length}):`);
  failures.slice(0, 40).forEach((x) => console.error('  FAIL ' + x));
  if (failures.length > 40) console.error(`  ... and ${failures.length - 40} more`);
  console.error(`A11Y L1 GATE RESULT: ${failures.length} FAILURE(S) — DEPLOY BLOCKED (0 critical + 0 serious required)`);
  process.exit(1);
}
console.log(`A11Y L1 GATE PASS (${pages.length - skipped.length} scanned, ${skipped.length} skipped)`);
