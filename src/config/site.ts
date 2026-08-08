// site.ts — per-site configuration for the shared component library (Phase 1.2)
// Consumed by Header/Footer/NewsletterForm/ProductCard etc. Values are content
// only (nav structure, brand text, links) — styling comes from semantic tokens.

export interface SiteConfig {
  name: string;
  tagline: string;
  url: string;
  logo?: { src: string; alt: string };
  nav: { href: string; label: string }[];
  footerColumns: { heading: string; links: { href: string; label: string }[] }[];
  social: { label: string; href: string }[];
  newsletter: {
    magnetName: string;
    valueProp: string;
    downloadUrl: string;
  };
  legalNote: string;
}

export const site: SiteConfig = {
  name: 'DogeKing',
  tagline: 'Your guide to meme coin trading on Solana.',
  url: 'https://dogeking.us',
  logo: { src: '/assets/crown-logo.svg', alt: 'DogeKing' },
  nav: [
    { href: '/', label: 'Home' },
    { href: '/crypto-guide/', label: 'Crypto Guide' },
    { href: '/all-articles/', label: 'Articles' },
    { href: '/about/', label: 'About' },
  ],
  footerColumns: [
    {
      heading: 'Guides',
      links: [
        { href: '/crypto-guide/', label: 'Crypto Guide' },
        { href: '/all-articles/', label: 'All Articles' },
        { href: '/checklist/', label: 'Checklist' },
      ],
    },
    {
      heading: 'Resources',
      links: [
        { href: '/tools-comparison/', label: 'Tools' },
        { href: '/about/', label: 'About' },
        { href: '/contact/', label: 'Contact' },
      ],
    },
    {
      heading: 'Legal',
      links: [
        { href: '/privacy/', label: 'Privacy' },
        { href: '/terms-of-service/', label: 'Terms' },
        { href: '/disclaimer/', label: 'Disclaimer' },
      ],
    },
  ],
  social: [
    { label: 'X (Twitter)', href: 'https://x.com/DogeKingCoin' },
    { label: 'Telegram', href: 'https://t.me/DogeKing' },
    { label: 'Discord', href: 'https://discord.gg/DogeKing' },
  ],
  newsletter: {
    magnetName: 'Crypto Starter Guide',
    valueProp: 'Get the free Crypto Starter Guide — Solana & meme coin trading fundamentals in one clean page.',
    downloadUrl: '/downloads/crypto-starter-guide.html',
  },
  legalNote: 'Not financial advice. DYOR.',
};
