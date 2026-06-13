// ═══════════════════════════════════════════════════════════════
//  dogeking.us — Affiliate Configuration
//  Feature-flagged. Flip ENABLED=true to activate.
// ═══════════════════════════════════════════════════════════════

export const AFFILIATE_CONFIG = {
  // Master switch — toggles the injected footer CTA
  ENABLED: true,

  // --- Gumroad Product (zero new accounts — existing store) ---
  // All products at https://dogeking0.gumroad.com/
  GUMROAD: {
    REF_URL: 'https://dogeking0.gumroad.com/l/dogeking-crypto-bundle',
    LABEL: 'Get the Crypto Bundle',
    DESCRIPTION: 'Crypto portfolio strategies + meme coin framework — $29.99',
  },

  // --- DexScreener Embed (no affiliate, always-on content) ---
  DEXSCREENER: {
    CHAIN: 'solana',
    PAIR_ADDRESS: '',   // e.g. '8RH9xY...'
    LABEL: 'View DogeKing on DexScreener',
  },
};
