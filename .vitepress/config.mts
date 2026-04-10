import { fileURLToPath, URL } from 'node:url'
import fs from 'node:fs'
import path from 'node:path'

import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'
import vueJsx from '@vitejs/plugin-vue-jsx'
import vueDevTools from 'vite-plugin-vue-devtools'
import tailwindcss from '@tailwindcss/vite'
import wasm from 'vite-plugin-wasm'
import topLevelAwait from 'vite-plugin-top-level-await'
import { stripGenerator } from './plugins/strip-generator'
import yaml from 'js-yaml'

// ── Helpers ─────────────────────────────────────────────────────────────────

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

/** Extract frontmatter title from a markdown file. Falls back to the filename stem. */
function getFrontmatterTitle(filePath: string, fallback: string): string {
  try {
    const content = fs.readFileSync(filePath, 'utf8')
    const match = content.match(/^title:\s*(.+)$/m)
    if (match) return match[1].trim()
  } catch {
    // ignore
  }
  return fallback
}

/**
 * Dynamically build a VitePress multi-sidebar object by scanning docs/tutor/.
 * - Keys: /tutor/<subject>/ and /tutor/<subject>/chN/
 * - index.md is placed first; remaining files sorted alphabetically.
 * - Gracefully returns {} for empty or missing directories.
 */
function buildTutorSidebar(docsDir: string): Record<string, unknown> {
  const tutorDir = path.join(docsDir, 'tutor')
  if (!fs.existsSync(tutorDir)) return {}

  const sidebar: Record<string, unknown> = {}

  const subjects = fs.readdirSync(tutorDir).filter(entry => {
    const full = path.join(tutorDir, entry)
    return fs.statSync(full).isDirectory() && !entry.startsWith('.')
  })

  for (const subject of subjects) {
    const subjectDir = path.join(tutorDir, subject)
    const chapterDirs = fs.readdirSync(subjectDir).filter(entry => {
      const full = path.join(subjectDir, entry)
      return fs.statSync(full).isDirectory() && /^ch\d+$/.test(entry)
    }).sort()

    if (chapterDirs.length === 0) continue

    const allChapterGroups: unknown[] = []

    for (const chDir of chapterDirs) {
      const chPath = path.join(subjectDir, chDir)
      const files = fs.readdirSync(chPath).filter(f => f.endsWith('.md') && f !== 'appendix.md')
      if (files.length === 0) continue

      // index.md first, then alphabetical
      const sorted = [
        ...files.filter(f => f === 'index.md'),
        ...files.filter(f => f !== 'index.md').sort(),
      ]

      const items = sorted.map(file => {
        const filePath = path.join(chPath, file)
        const stem = file.replace(/\.md$/, '')
        const title = getFrontmatterTitle(filePath, stem)
        const link = `/tutor/${subject}/${chDir}/${stem === 'index' ? '' : stem}`
        return { text: title, link }
      })

      const chIndexPath = path.join(chPath, 'index.md')
      const chapterTitle = getFrontmatterTitle(chIndexPath, chDir)
      const group = { text: chapterTitle, collapsed: false, items }

      // Per-chapter sidebar key
      sidebar[`/tutor/${subject}/${chDir}/`] = [group]
      allChapterGroups.push(group)
    }

    // Subject-level sidebar key (all chapters)
    if (allChapterGroups.length > 0) {
      sidebar[`/tutor/${subject}/`] = allChapterGroups
    }
  }

  return sidebar
}

// ── Config ───────────────────────────────────────────────────────────────────

const srcDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', 'docs')

// https://vitepress.dev/reference/site-config
export default withMermaid(defineConfig({
  srcDir: 'docs',

  title: '台北市立復興高級中學 Python 自學道場',
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
  },
  vite: {
    plugins: [vueJsx(), vueDevTools(), tailwindcss(), wasm(), topLevelAwait(), stripGenerator()],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./.vitepress/theme', import.meta.url)),
      },
    },
    server: {
      headers: {
        // Required for SharedArrayBuffer used by Pyodide
        'Cross-Origin-Opener-Policy': 'same-origin',
        'Cross-Origin-Embedder-Policy': 'require-corp',
      },
    },
  },
}))
