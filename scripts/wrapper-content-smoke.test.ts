// @vitest-environment node
/**
 * Real-content smoke for the judging wrapper path.
 *
 * content-regression verifies reference solutions with a bare python3
 * subprocess — it never touches `buildWrappedCode`, so the actual judging
 * execution path (op-counter tracing + sandbox + I/O redirect) had ZERO
 * automated coverage with real challenge content. This suite closes that:
 * every challenge declaring `reference_solution` has its solution executed
 * THROUGH the wrapper (default 10M op limit, tracing active) against
 * sampled production-pool inputs, asserting the output still matches the
 * generator's expected output. Guards against the wrapper ever falsely
 * killing or corrupting a legitimate solution on real content.
 */
import { describe, it, expect } from 'vitest'
import { execFileSync, spawnSync } from 'node:child_process'
import { existsSync, readFileSync, readdirSync } from 'node:fs'
import { resolve, join } from 'node:path'

import { buildWrappedCode } from '../.vitepress/theme/workers/worker-utils'
import { buildPoolRequest, readChallenge, generateInputs, runGenerator } from './generate-pools.js'

const CHALLENGES_DIR = resolve(import.meta.dirname, '../docs/challenge')
/** Mirrors the worker's DEFAULT_OP_LIMIT (pyodide.worker.ts). */
const DEFAULT_OP_LIMIT = 10_000_000
const SAMPLES_PER_CHALLENGE = 3

function pythonAvailable(): boolean {
  try {
    execFileSync('python3', ['-c', 'import yaml'], { encoding: 'utf-8', timeout: 10_000 })
    return true
  } catch {
    return false
  }
}

const hasPython = pythonAvailable()
const files = existsSync(CHALLENGES_DIR)
  ? readdirSync(CHALLENGES_DIR)
      .filter((f) => f.endsWith('.md'))
      .sort()
  : []
const withRef = files.filter((f) =>
  /^reference_solution:/m.test(readFileSync(join(CHALLENGES_DIR, f), 'utf-8')),
)

describe('wrapper content smoke: reference solutions survive the judging wrapper', () => {
  it('at least one challenge declares reference_solution', () => {
    expect(withRef.length).toBeGreaterThan(0)
  })

  if (!hasPython) {
    it.skip('wrapper execution skipped — python3 or PyYAML unavailable', () => {})
    return
  }

  it.each(withRef)(
    '%s: reference_solution through the wrapper matches generator output',
    async (file) => {
      const c = readChallenge(join(CHALLENGES_DIR, file))
      const { spec, count } = buildPoolRequest(c, c.slug)
      const fullPool = await generateInputs(spec, count)
      // Deterministic spread: first, middle, last of the production pool.
      const indices = [0, Math.floor(count / 2), count - 1].slice(0, SAMPLES_PER_CHALLENGE)
      const rawInputs = indices.map((i) => fullPool[i]!)

      const expected = runGenerator(c.generator, rawInputs)

      for (const t of expected) {
        const wrapped = buildWrappedCode(c.reference_solution as string, t.input, DEFAULT_OP_LIMIT)
        const harness = `${wrapped}\nimport sys as _t\n_t.__stdout__.write(_output)\n`
        const res = spawnSync('python3', ['-c', harness], { encoding: 'utf-8', timeout: 30_000 })
        expect(res.stderr, `${file}: wrapper execution must not error`).toBe('')
        expect(res.status).toBe(0)
        expect(res.stdout.trimEnd()).toBe(t.expected_output.trimEnd())
      }
    },
    60_000,
  )
})
