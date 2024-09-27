// @ts-check
import { defineConfig, envField } from 'astro/config';

import tailwind from '@astrojs/tailwind';

import node from '@astrojs/node';

// https://astro.build/config
export default defineConfig({
  output: 'server',
  integrations: [tailwind()],

  experimental: {
    env: {
      schema: {
        PB_URL: envField.string({ context: 'server', access: 'public' }),
        PB_USER: envField.string({ context: 'server', access: 'public' }),
        PB_PASS: envField.string({ context: 'server', access: 'public' }),
      },
    },
  },

  adapter: node({
    mode: 'standalone',
  }),
});