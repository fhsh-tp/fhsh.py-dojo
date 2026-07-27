// @vitest-environment node
/**
 * Regression suite for the strip-generator plugin — the only mechanism
 * standing between challenge answers and the production bundle.
 *
 * Case groups (from the adversarial review of audit finding H-R2-1):
 * A: stripping correctness across YAML scalar styles
 * B: non-destructiveness for every other field
 * C: fail-loud assertions
 * D: applicability scope
 * E: architectural guards against bypassing the plugin entirely
 */
import { readFileSync, readdirSync } from 'node:fs'
import { join, resolve } from 'node:path'
import yaml from 'js-yaml'
import { describe, expect, it } from 'vitest'

import { stripGenerator } from '../strip-generator'

const CHALLENGE_ID = '/repo/docs/challenge/test-case.md'
const SECRET = 'SECRET_ANSWER_TOKEN'

function transform(code: string, id: string = CHALLENGE_ID) {
  return stripGenerator().transform!(code, id)
}

function md(frontmatter: string, body = '\n## 題目\n內文\n'): string {
  return `---\n${frontmatter}\n---${body}`
}

/** Assert both fields gone, secret token gone, and YAML still valid. */
function expectClean(result: { code: string } | null) {
  expect(result).not.toBeNull()
  const out = result!.code
  expect(out).not.toContain(SECRET)
  const fm = out.match(/^---\r?\n([\s\S]*?)\r?\n---/)![1]!
  const parsed = yaml.load(fm.replace(/\r/g, '')) as Record<string, unknown>
  expect(parsed).not.toHaveProperty('generator')
  expect(parsed).not.toHaveProperty('reference_solution')
  return parsed
}

describe('A: 各種 YAML scalar 寫法都必須剝除', () => {
  const A_CASES: Array<[string, string]> = [
    ['A1 baseline pipe', `generator: |\n  print("${SECRET}")`],
    ['A2 block 內含空行', `generator: |\n  a = 1\n\n  print("${SECRET}")`],
    ['A3 block 內含純空白行', `generator: |\n  a = 1\n   \n  print("${SECRET}")`],
    ['A4 標頭尾隨註解', `generator: | # 正解勿外流\n  print("${SECRET}")`],
    ['A5 keep chomping |+', `generator: |+\n  print("${SECRET}")`],
    ['A6 strip chomping |-', `generator: |-\n  print("${SECRET}")`],
    ['A7 縮排指示子 |2', `generator: |2\n  print("${SECRET}")`],
    ['A8 folded keep >+', `generator: >+\n  print("${SECRET}")`],
    ['A9 folded strip >-', `generator: >-\n  print("${SECRET}")`],
    ['A10 雙引號 key', `"generator": |\n  print("${SECRET}")`],
    ['A11 單引號 key', `'generator': |\n  print("${SECRET}")`],
    ['A12 key 與冒號間有空白', `generator : |\n  print("${SECRET}")`],
    ['A13 inline 單行', `generator: "print('${SECRET}')"`],
    ['A14 folded 無指示子', `generator: >\n  print ${SECRET}`],
    [
      'A15 兩欄位同時存在',
      `generator: |\n  print("${SECRET}")\nreference_solution: |\n  print("${SECRET}")`,
    ],
    [
      'A16 reference_solution 空行+chomping',
      `reference_solution: |+\n  a = 1\n\n  print("${SECRET}")`,
    ],
  ]

  it.each(A_CASES)('%s', (_name, field) => {
    const parsed = expectClean(transform(md(`id: 1\ntitle: 測試\n${field}\ndifficulty: easy`)))
    expect(parsed).toMatchObject({ id: 1, title: '測試', difficulty: 'easy' })
  })

  it('A17 欄位在 frontmatter 最末(緊鄰 ---)', () => {
    expectClean(transform(md(`id: 1\ngenerator: |\n  print("${SECRET}")`)))
  })

  it('A18 欄位在 frontmatter 最前', () => {
    expectClean(transform(md(`generator: |\n  print("${SECRET}")\nid: 1`)))
  })

  it('A19 CRLF 行尾', () => {
    const code = `---\r\nid: 1\r\ngenerator: |\r\n  print("${SECRET}")\r\ntitle: t\r\n---\r\n\r\n內文\r\n`
    const result = transform(code)
    expect(result).not.toBeNull()
    expect(result!.code).not.toContain(SECRET)
  })
})

describe('B: 其他欄位不可被破壞', () => {
  it('B1 flow sequence 保持原樣(不被重排)', () => {
    const result = transform(md(`id: 1\ntags: [for, range, 迴圈]\ngenerator: |\n  x = 1\ntitle: t`))
    expect(result!.code).toContain('tags: [for, range, 迴圈]')
  })

  it('B2/B3 巢狀 params 與 starter_code(含 # 註解)逐字保留', () => {
    const fm = `id: 1\nparams:\n  n:\n    type: int\n    min: 1\n    max: 50\ngenerator: |\n  x = 1\nstarter_code: |\n  # 讀取輸入\n  n = int(input())`
    const parsed = expectClean(transform(md(fm))) as Record<string, unknown>
    expect(parsed.params).toEqual({ n: { type: 'int', min: 1, max: 50 } })
    expect(parsed.starter_code).toBe('# 讀取輸入\nn = int(input())\n')
  })

  it('B5 前綴相似欄位不被誤刪', () => {
    const parsed = expectClean(
      transform(md(`id: 1\ngenerator_note: keep-me\ngenerator: |\n  x = 1`)),
    ) as Record<string, unknown>
    expect(parsed.generator_note).toBe('keep-me')
  })

  it('B6 全部真實題目:剝除成功、其他欄位無損(外掛內建斷言把關)', () => {
    const dir = resolve(import.meta.dirname, '../../../docs/challenge')
    const files = readdirSync(dir).filter((f) => f.endsWith('.md'))
    expect(files.length).toBeGreaterThan(0)
    for (const f of files) {
      const code = readFileSync(join(dir, f), 'utf-8')
      // transform 內部的 fail-loud 斷言會在任何欄位受損時 throw
      const result = transform(code, `/repo/docs/challenge/${f}`)
      expect(result, f).not.toBeNull()
      const fm = result!.code.match(/^---\n([\s\S]*?)\n---/)![1]!
      const parsed = yaml.load(fm) as Record<string, unknown>
      expect(parsed, f).not.toHaveProperty('generator')
      expect(parsed, f).not.toHaveProperty('reference_solution')
    }
  })
})

describe('C: fail-loud — 任何可疑狀態必須讓建置爆掉', () => {
  it('C2 跨行 flow map 內含 column-0 同名 key → 偵測到欄位受損而 throw', () => {
    const fm = `id: 1\nparams: {\ngenerator: 1,\nb: 2 }\ntitle: t`
    expect(() => transform(md(fm))).toThrow(/damaged|invalid YAML/)
  })

  it('C4 來源 frontmatter 本身是壞 YAML → throw 且訊息指向來源檔', () => {
    const fm = `id: 1\n  badindent: [\ngenerator: |\n  x = 1`
    expect(() => transform(md(fm))).toThrow(/invalid YAML/)
  })
})

describe('D: 適用範圍', () => {
  it.each([
    ['D1 tutor 路徑', '/repo/docs/tutor/py/ch1/1-1.md'],
    ['D2 非 .md', '/repo/docs/challenge/x.vue'],
  ])('%s → 不處理(回傳 null)', (_name, id) => {
    expect(transform(md(`id: 1\ngenerator: |\n  x = 1`), id)).toBeNull()
  })

  it('D3 無 frontmatter → null', () => {
    expect(transform('# 只有內文\n')).toBeNull()
  })

  it('D5 只在 build 模式掛載', () => {
    expect(stripGenerator().apply).toBe('build')
  })
})

describe('E: 架構護欄 — 防止繞過 plugin 的資料路徑', () => {
  const dataLoaderSrc = readFileSync(
    resolve(import.meta.dirname, '../../../docs/shared/challenge.data.ts'),
    'utf-8',
  )

  it('E1 challenge.data.ts 維持白名單映射,不得 spread frontmatter', () => {
    // createContentLoader 直接讀磁碟、不經 Vite transform——此 loader 一旦
    // 改成展開 frontmatter,strip-generator 完全擋不住。
    expect(dataLoaderSrc).not.toMatch(/\.\.\.\s*challenge\.frontmatter/)
    expect(dataLoaderSrc).not.toContain('frontmatter.generator')
    expect(dataLoaderSrc).not.toContain('frontmatter.reference_solution')
  })

  it('E2 challenge.data.ts 維持 includeSrc: false', () => {
    expect(dataLoaderSrc).toMatch(/includeSrc:\s*false/)
  })
})
