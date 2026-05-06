import fs from 'node:fs'
import path from 'node:path'

/** Extract frontmatter title from a markdown file. Falls back to the filename stem. */
export function getFrontmatterTitle(filePath: string, fallback: string): string {
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
export function buildTutorSidebar(docsDir: string): Record<string, unknown> {
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
      const files = fs.readdirSync(chPath).filter(f => f.endsWith('.md'))
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
