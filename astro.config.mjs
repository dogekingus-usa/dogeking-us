import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://dogeking.us',
  output: 'static',
  integrations: [tailwind()],
  build: {
    format: 'directory',
  },
  server: {
    port: 4321,
  },
});
