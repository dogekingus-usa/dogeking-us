import defaultTheme from 'tailwindcss/defaultTheme';

export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: '#c9a84c',   // warm gold — primary brand accent
          300: '#f5d742',       // bright gold — highlights/glows
          400: '#e0be55',
          500: '#c9a84c',
          600: '#a8893a',
        },
        dark: {
          DEFAULT: '#0f172a',   // deep navy — background base
          700: '#111c33',
          800: '#0a0f1f',
          900: '#05070d',
        },
        solana: '#06b6d4',      // cyan — chain signal (small doses only)
        royal: '#4c1d95',       // purple — secondary accent
      },
      fontFamily: {
        heading: ['"Playfair Display"', 'serif'],
        body: ['Inter', ...defaultTheme.fontFamily.sans],
        mono: ['"JetBrains Mono"', ...defaultTheme.fontFamily.mono],
      },
    },
  },
  plugins: [],
};
