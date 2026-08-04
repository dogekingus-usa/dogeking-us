import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import mdx from '@astrojs/mdx';

export default defineConfig({
  site: 'https://dogeking.us',
  output: 'static',
  integrations: [tailwind(), mdx()],
  build: {
    format: 'file',
  },
});
