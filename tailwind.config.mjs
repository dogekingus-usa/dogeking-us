/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#fff9e6',
          100: '#fff0b3',
          200: '#ffe680',
          300: '#ffd94d',
          400: '#ffcf1a',
          500: '#FFD700',
          600: '#ccac00',
          700: '#998100',
          800: '#665600',
          900: '#332b00',
        },
        dark: {
          50: '#e0e0e8',
          100: '#b3b3c4',
          200: '#80809e',
          300: '#4d4d78',
          400: '#262652',
          500: '#1A1A2E',
          600: '#151525',
          700: '#10101c',
          800: '#0a0a12',
          900: '#050509',
        },
      },
      fontFamily: {
        heading: ['Orbitron', 'sans-serif'],
        body: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
