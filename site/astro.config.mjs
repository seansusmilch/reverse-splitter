// @ts-check
import { defineConfig, envField } from 'astro/config';

import tailwind from '@astrojs/tailwind';

import vercel from '@astrojs/vercel/serverless';

// https://astro.build/config
export default defineConfig({
  output: 'server',
  integrations: [tailwind({ applyBaseStyles: true })],

  experimental: {
    env: {
      schema: {
        PB_URL: envField.string({ context: 'server', access: 'public' }),
        PB_USER: envField.string({ context: 'server', access: 'public' }),
        PB_PASS: envField.string({ context: 'server', access: 'public' }),
      },
    },
  },

  adapter: vercel(),
});
