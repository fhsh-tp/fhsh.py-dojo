// @vitest-environment node
import { describe, it, expect, beforeEach, afterEach } from 'vitest'
import os from 'node:os'
import fs from 'node:fs'
import path from 'node:path'
import { buildTutorSidebar } from './sidebar'

describe('buildTutorSidebar', () => {
  let tmpDir: string

  beforeEach(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'tutor-sidebar-test-'))

    // Create docs/tutor/py/ch1/ structure
    const ch1Dir = path.join(tmpDir, 'tutor', 'py', 'ch1')
    fs.mkdirSync(ch1Dir, { recursive: true })

    // index.md with title
    fs.writeFileSync(path.join(ch1Dir, 'index.md'), '---\ntitle: Chapter 1\n---\n')
    // appendix.md with title
    fs.writeFileSync(path.join(ch1Dir, 'appendix.md'), '---\ntitle: Appendix\n---\n')
    // reference.md with title
    fs.writeFileSync(path.join(ch1Dir, 'reference.md'), '---\ntitle: Reference\n---\n')
  })

  afterEach(() => {
    fs.rmSync(tmpDir, { recursive: true, force: true })
  })

  it('includes appendix in the sidebar items for /tutor/py/ch1/', () => {
    const sidebar = buildTutorSidebar(tmpDir)
    const key = '/tutor/py/ch1/'
    expect(sidebar).toHaveProperty(key)

    const groups = sidebar[key] as Array<{ items: Array<{ text: string; link: string }> }>
    const items = groups[0].items

    const links = items.map(item => item.link)
    expect(links.some(l => l.includes('appendix'))).toBe(true)
  })

  it('places appendix before reference in the sidebar items', () => {
    const sidebar = buildTutorSidebar(tmpDir)
    const key = '/tutor/py/ch1/'

    const groups = sidebar[key] as Array<{ items: Array<{ text: string; link: string }> }>
    const items = groups[0].items

    const links = items.map(item => item.link)
    const appendixIdx = links.findIndex(l => l.includes('appendix'))
    const referenceIdx = links.findIndex(l => l.includes('reference'))

    expect(appendixIdx).toBeGreaterThanOrEqual(0)
    expect(referenceIdx).toBeGreaterThanOrEqual(0)
    expect(appendixIdx).toBeLessThan(referenceIdx)
  })
})
