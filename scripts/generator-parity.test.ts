// @vitest-environment node
/**
 * Dual-generator parity test.
 *
 * The project generates random challenge inputs in TWO places that must stay in
 * sync: the Rust `testcase-generator` crate (used at dev time and for prod
 * judging) and the embedded Python replica in `scripts/generate-pools.ts` (used
 * at build time to avoid loading WASM). If one side gains a parameter `type` or
 * changes a constraint without the other, prod pools silently diverge from what
 * the runtime expects — the exact class of bug behind the pool-collision fix.
 *
 * Because Rust `SmallRng` and Python `random` are different algorithms, we do
 * NOT assert byte-identical output. Instead we assert:
 *   1. Constraint conformance — the Python replica's output for a shared set of
 *      ParamSpec fixtures satisfies the declared constraints (charset, length,
 *      value range, count, separator, multiple_of).
 *   2. Type-set parity — the set of `type` values the two implementations
 *      support is identical, modulo an explicit allow-list of documented
 *      divergences. Type sets are EXTRACTED from source so adding a type to one
 *      side without the other fails this test.
 *
 * The Rust side's own constraint conformance is covered by
 * `testcase-generator/tests/param_conformance.rs`.
 */
import { describe, it, expect } from 'vitest'
import { execFileSync } from 'node:child_process'
import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'

import { generateInputs } from './generate-pools.js'

const SAMPLES = 100

// Types supported by Rust but intentionally NOT by the Python build replica.
// `faker` is a Rust-only, feature-gated type (needs the `fake` crate); the
// build-time Python path never uses it. Any OTHER divergence is a bug.
const TYPE_ALLOW_LIST = new Set(['faker'])

function pythonAvailable(): boolean {
  try {
    execFileSync('python3', ['-c', 'import random'], { encoding: 'utf-8', timeout: 10_000 })
    return true
  } catch {
    return false
  }
}

const hasPython = pythonAvailable()

/** Convert a Rust PascalCase enum variant to its serde snake_case tag. */
function pascalToSnake(name: string): string {
  return name.replace(/([a-z0-9])([A-Z])/g, '$1_$2').toLowerCase()
}

function extractRustTypes(): Set<string> {
  const src = readFileSync(
    resolve(import.meta.dirname, '../testcase-generator/src/parser.rs'),
    'utf-8',
  )
  const enumBlock = src.match(/enum ParamSpec\s*\{([\s\S]*?)\n\}/)
  if (!enumBlock) throw new Error('Could not locate `enum ParamSpec` in parser.rs')
  const variants = [...enumBlock[1]!.matchAll(/^\s{4}([A-Z][A-Za-z0-9]+)\s*\{/gm)].map((m) => m[1]!)
  return new Set(variants.map(pascalToSnake))
}

function extractPythonTypes(): Set<string> {
  const src = readFileSync(resolve(import.meta.dirname, 'generate-pools.ts'), 'utf-8')
  // Match the dispatch branches inside gen_value: `t == "int"`, etc.
  return new Set([...src.matchAll(/t == "([a-z_]+)"/g)].map((m) => m[1]!))
}

interface Fixture {
  name: string
  params: Record<string, unknown>
  check: (value: string) => boolean
}

const FIXTURES: Fixture[] = [
  {
    name: 'int range',
    params: { x: { type: 'int', min: 5, max: 20 } },
    check: (v) => {
      const n = Number(v)
      return Number.isInteger(n) && n >= 5 && n <= 20
    },
  },
  {
    name: 'int fixed (min==max)',
    params: { x: { type: 'int', min: 7, max: 7 } },
    check: (v) => v === '7',
  },
  {
    name: 'alpha_upper',
    params: { x: { type: 'alpha_upper', min_len: 3, max_len: 6 } },
    check: (v) => /^[A-Z]{3,6}$/.test(v),
  },
  {
    name: 'alpha_lower',
    params: { x: { type: 'alpha_lower', min_len: 3, max_len: 6 } },
    check: (v) => /^[a-z]{3,6}$/.test(v),
  },
  {
    name: 'alpha_mixed',
    params: { x: { type: 'alpha_mixed', min_len: 3, max_len: 6 } },
    check: (v) => /^[A-Za-z]{3,6}$/.test(v),
  },
  {
    name: 'hex_string',
    params: { x: { type: 'hex_string', min_len: 4, max_len: 8 } },
    check: (v) => /^[0-9a-f]{4,8}$/.test(v),
  },
  {
    name: 'printable_ascii',
    params: { x: { type: 'printable_ascii', min_len: 3, max_len: 6 } },
    check: (v) =>
      v.length >= 3 &&
      v.length <= 6 &&
      [...v].every((c) => {
        const n = c.charCodeAt(0)
        return n >= 0x21 && n < 0x7f
      }),
  },
  {
    name: 'enum',
    params: { x: { type: 'enum', values: ['red', 'green', 'blue'] } },
    check: (v) => ['red', 'green', 'blue'].includes(v),
  },
  {
    name: 'hex_string multiple_of 4',
    params: { x: { type: 'hex_string', min_len: 4, max_len: 12, multiple_of: 4 } },
    check: (v) => /^[0-9a-f]+$/.test(v) && v.length % 4 === 0 && v.length >= 4 && v.length <= 12,
  },
  {
    name: 'alpha_mixed multiple_of 3',
    params: { x: { type: 'alpha_mixed', min_len: 3, max_len: 12, multiple_of: 3 } },
    check: (v) => /^[A-Za-z]+$/.test(v) && v.length % 3 === 0 && v.length >= 3 && v.length <= 12,
  },
  {
    name: 'printable_ascii multiple_of 2',
    params: { x: { type: 'printable_ascii', min_len: 2, max_len: 8, multiple_of: 2 } },
    check: (v) =>
      v.length % 2 === 0 &&
      v.length >= 2 &&
      v.length <= 8 &&
      [...v].every((c) => {
        const n = c.charCodeAt(0)
        return n >= 0x21 && n < 0x7f
      }),
  },
  {
    name: 'int with count',
    params: { x: { type: 'int', min: 1, max: 100, count: { min: 3, max: 5, separator: ' ' } } },
    check: (v) => {
      const p = v.split(' ')
      return (
        p.length >= 3 &&
        p.length <= 5 &&
        p.every((s) => {
          const n = Number(s)
          return Number.isInteger(n) && n >= 1 && n <= 100
        })
      )
    },
  },
]

describe('generator parity: supported type sets are in sync', () => {
  it('Python replica supports exactly the Rust types minus the allow-list', () => {
    const rust = extractRustTypes()
    const python = extractPythonTypes()
    const expected = [...rust].filter((t) => !TYPE_ALLOW_LIST.has(t)).sort()
    const actual = [...python].sort()
    // If this fails, a `type` was added/removed on one side only. Update the
    // other side (and TYPE_ALLOW_LIST if the divergence is intentional).
    expect(actual).toEqual(expected)
  })
})

describe('generator parity: Python replica satisfies ParamSpec constraints', () => {
  if (!hasPython) {
    it.skip('skipped — python3 unavailable', () => {})
  } else {
    for (const f of FIXTURES) {
      it(`${f.name}`, () => {
        const samples = generateInputs(f.params, SAMPLES)
        expect(samples.length).toBe(SAMPLES)
        for (const s of samples) {
          expect(f.check(s), `value "${s}" violates ${f.name} constraint`).toBe(true)
        }
      }, 30_000)
    }
  }
})
