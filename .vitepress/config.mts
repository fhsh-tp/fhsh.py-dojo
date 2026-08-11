import { fileURLToPath, URL } from 'node:url'
import fs from 'node:fs'
import path from 'node:path'

import { defineConfig } from 'vitepress'
import { mermaidPlugin } from './plugins/markdown-mermaid'
import vueJsx from '@vitejs/plugin-vue-jsx'
import vueDevTools from 'vite-plugin-vue-devtools'
import tailwindcss from '@tailwindcss/vite'
import wasm from 'vite-plugin-wasm'
import topLevelAwait from 'vite-plugin-top-level-await'
import { stripGenerator } from './plugins/strip-generator'
import yaml from 'js-yaml'
import { buildTutorSidebar } from './sidebar.ts'

// ── Helpers ─────────────────────────────────────────────────────────────────

/**
 * Serve the cross-origin isolation headers in dev.
 *
 * These were previously declared through `vite.server.headers`, which
 * VitePress 2 does not forward — verified by requesting the dev server and
 * finding neither header present. The judge's per-testcase deadline needs
 * `SharedArrayBuffer` to interrupt a running testcase; without isolation it
 * silently degrades to adjudicating the deadline only after the testcase has
 * already run to completion, so a dev-only gap would hide the very behaviour
 * being developed. Production gets the same pair from `docs/public/_headers`.
 */
function crossOriginIsolation() {
  const headers = {
    'Cross-Origin-Opener-Policy': 'same-origin',
    'Cross-Origin-Embedder-Policy': 'require-corp',
  }
  const apply = (server: { middlewares: { use: (fn: (req: unknown, res: { setHeader: (k: string, v: string) => void }, next: () => void) => void) => void } }) => {
    server.middlewares.use((_req, res, next) => {
      for (const [key, value] of Object.entries(headers)) res.setHeader(key, value)
      next()
    })
  }
  return {
    name: 'fhsh-cross-origin-isolation',
    configureServer: apply,
    configurePreviewServer: apply,
  }
}



function loadYaml(file: string): unknown {
  try {
    const filePath = path.resolve(path.dirname(fileURLToPath(import.meta.url)), file)
    if (fs.existsSync(filePath)) {
      return yaml.load(fs.readFileSync(filePath, 'utf8'))
    }
  } catch (e) {
    console.error(`[config] Error loading ${file}:`, e)
  }
  return []
}

// ── Config ───────────────────────────────────────────────────────────────────

const srcDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', 'docs')

// https://vitepress.dev/reference/site-config
export default defineConfig({
  srcDir: 'docs',

  title: 'Python 自學道場',
  description: 'Python 自學道場：在解題中學習 Python 程式設計',
  head: [
    ['link', { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' }],
    [
      'meta',
      {
        'http-equiv': 'Content-Security-Policy',
        content:
          "default-src 'self'; script-src 'self' 'unsafe-inline' 'wasm-unsafe-eval'; style-src 'self' 'unsafe-inline'; worker-src 'self' blob:; connect-src 'self'; img-src 'self' data:; font-src 'self';",
      },
    ],
  ],
  themeConfig: {
    logo: '/favicon.svg',
    nav: loadYaml('nav.yml') as never,
    sidebar: buildTutorSidebar(srcDir) as never,
    socialLinks: [{ icon: 'github', link: 'https://github.com/fhsh-tp/fhsh.py-dojo' }],
  },
  markdown: {
    math: true,
    config(md) {
      mermaidPlugin(md)
    },
  },
  vite: {
    plugins: [crossOriginIsolation(), vueJsx(), vueDevTools(), tailwindcss(), wasm(), topLevelAwait(), stripGenerator()],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./.vitepress/theme', import.meta.url)),
      },
    },

  },
})
