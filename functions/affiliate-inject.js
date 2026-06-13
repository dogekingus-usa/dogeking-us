// ═══════════════════════════════════════════════════════════════
//  dogeking.us — Affiliate Link Injection (Cloudflare Pages Function)
//  Injects affiliate CTAs into page HTML without modifying origin files.
//  Controlled by AFFILIATE_CONFIG.ENABLED flag.
// ═══════════════════════════════════════════════════════════════

import { AFFILIATE_CONFIG } from '../affiliate-config.js';

/**
 * Inject affiliate content into HTML responses.
 * Targets </body> to add footer/sidebar CTAs.
 */
function injectAffiliateHTML(html) {
  const cfg = AFFILIATE_CONFIG;

  // --- Gumroad Product CTA banner (injected before </body>) ---
  const gumroadCTA = `
<!-- Affiliate: Gumroad Product (${cfg.ENABLED ? 'active' : 'disabled'}) -->
<div id="affiliate-gumroad-banner" style="
  display:${cfg.ENABLED ? 'block' : 'none'};
  position:fixed;
  bottom:0;left:0;right:0;
  z-index:9999;
  background:linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  color:#fff;
  padding:12px 20px;
  text-align:center;
  font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  font-size:14px;
  box-shadow:0 -2px 12px rgba(0,0,0,0.3);
">
  <span style="font-weight:600;">📦 ${cfg.GUMROAD.DESCRIPTION}</span>
  &nbsp;
  <a href="${cfg.GUMROAD.REF_URL}" target="_blank" rel="noopener noreferrer" style="
    display:inline-block;
    background:#e94560;
    color:#fff;
    padding:6px 18px;
    border-radius:20px;
    font-weight:700;
    text-decoration:none;
    margin-left:10px;
    font-size:13px;
  ">${cfg.GUMROAD.LABEL} →</a>
  <button onclick="document.getElementById('affiliate-gumroad-banner').style.display='none'" style="
    background:transparent;border:1px solid rgba(255,255,255,0.4);color:#fff;
    border-radius:50%;width:24px;height:24px;font-size:14px;line-height:24px;
    padding:0;cursor:pointer;vertical-align:middle;margin-left:12px;
  ">✕</button>
</div>`;

  // Inject before </body>
  if (html.includes('</body>')) {
    html = html.replace('</body>', gumroadCTA + '\n</body>');
  }

  return html;
}

/**
 * Cloudflare Pages onRequest handler.
 * Transforms HTML responses to inject affiliate content.
 */
export async function onRequest(context) {
  const { request, next } = context;
  const url = new URL(request.url);

  // Skip non-HTML paths (assets, images, scripts, data files)
  const path = url.pathname;
  if (
    path.startsWith('/assets/') ||
    path.startsWith('/images/') ||
    path.startsWith('/og-images/') ||
    path.startsWith('/scripts/') ||
    path.endsWith('.css') ||
    path.endsWith('.js') ||
    path.endsWith('.json') ||
    path.endsWith('.xml') ||
    path.endsWith('.svg') ||
    path.endsWith('.png') ||
    path.endsWith('.jpg') ||
    path.endsWith('.ico') ||
    path.endsWith('.webp')
  ) {
    return await next();
  }

  const response = await next();
  const contentType = response.headers.get('content-type') || '';

  // Only transform HTML responses
  if (!contentType.includes('text/html')) {
    return response;
  }

  const html = await response.text();
  const modifiedHTML = injectAffiliateHTML(html);

  return new Response(modifiedHTML, {
    status: response.status,
    statusText: response.statusText,
    headers: response.headers,
  });
}
