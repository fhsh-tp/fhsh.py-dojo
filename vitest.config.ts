import { fileURLToPath } from 'node:url'
import { mergeConfig, defineConfig, configDefaults } from 'vitest/config'
import vue from '@vitejs/plugin-vue'
import viteConfig from './.vitepress/config.mts'

export default mergeConfig(
  viteConfig.vite || {},
  defineConfig({
    plugins: [vue()],
    test: {
      environment: 'jsdom',
      setupFiles: ['./.vitepress/theme/__tests__/setup-idb.ts'],
      exclude: [...configDefaults.exclude, 'e2e/**'],
      root: fileURLToPath(new URL('./', import.meta.url)),
      server: {
        deps: {
          // CodeMirror 6 uses ESM-only packages; inline them so Vitest can process them
          inline: [/^@codemirror\//, /^codemirror$/],
        },
      },
    },
  }),
)
