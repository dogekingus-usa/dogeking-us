// Cloudflare Pages Function â€˝ Domain Redirect Middleware
// Redirects www, pages.dev, and platform subdomains â†â„¢ dogeking.us

const PRIMARY_DOMAIN = 'dogeking.us';
const ALIAS_DOMAINS = ['www.dogeking.us', 'dogeking-us.pages.dev', 'platform.dogeking.us'];

export async function onRequest(context) {
  const { request, next } = context;
  const url = new URL(request.url);
  const host = url.hostname;

  // If already on primary domain, pass through
  if (host === PRIMARY_DOMAIN) {
    return await next();
  }

  // If on an alias domain, redirect to primary
  if (ALIAS_DOMAINS.includes(host)) {
    const newUrl = `https://${PRIMARY_DOMAIN}${url.pathname}${url.search}`;
    return Response.redirect(newUrl, 301);
  }

  // Unknown domain â€˝ also redirect
  const newUrl = `https://${PRIMARY_DOMAIN}${url.pathname}${url.search}`;
  return Response.redirect(newUrl, 301);
}
