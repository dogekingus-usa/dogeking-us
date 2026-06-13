// ═══════════════════════════════════════════════════════════════
//  dogeking.us — Middleware Chain
//  1. Domain redirect (www, pages.dev → primary)
//  2. Affiliate CTA injection (feature-flagged)
// ═══════════════════════════════════════════════════════════════

// ═══════════════════════════════════════════════════════════════
//  dogeking.us — Middleware Chain
//  1. Domain redirect (www, pages.dev → primary)
//  2. Affiliate CTA injection (feature-flagged, short-circuited when disabled)
// ═══════════════════════════════════════════════════════════════

import { AFFILIATE_CONFIG } from '../affiliate-config.js';

const PRIMARY_DOMAIN = 'dogeking.us';
const ALIAS_DOMAINS = ['www.dogeking.us', 'dogeking-us.pages.dev', 'platform.dogeking.us'];

export async function onRequest(context) {
  const { request, next } = context;
  const url = new URL(request.url);
  const host = url.hostname;

  // Step 1: Redirect alias domains → primary domain
  if (host !== PRIMARY_DOMAIN) {
    const newUrl = `https://${PRIMARY_DOMAIN}${url.pathname}${url.search}`;
    return Response.redirect(newUrl, 301);
  }

  // Step 2: Affiliate inject — short-circuit when disabled to save Workers CPU
  if (!AFFILIATE_CONFIG.ENABLED) {
    return await next();
  }

  // Step 2b: Only import and run the inject handler when actively needed
  const { onRequest: affiliateInject } = await import('./affiliate-inject.js');
  return await affiliateInject(context);
}
