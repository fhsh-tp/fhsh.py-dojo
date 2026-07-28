// @vitest-environment node
/**
 * Real-Python integration tests for buildWrappedCode.
 *
 * Every prior worker test asserted the wrapper's STRING SHAPE (contains
 * "sys.settrace") — none ever executed it. That gap let the flat top-level
 * blind spot sit unnoticed for four months: sys.settrace only hooks frames
 * created AFTER installation, so flat student code in the module frame was
 * never counted (op_count forever 0). These tests execute the wrapper with
 * a real interpreter and assert runtime behavior, so a regression in frame
 * coverage fails even if the wrapper still textually contains sys.settrace.
 *
 * Runs under system python3 (same preflight-skip pattern as
 * scripts/content-regression.test.ts — CPython and Pyodide agree on
 * settrace/f_trace frame semantics, both verified during the RCA).
 */
import { execFileSync, spawnSync } from 'node:child_process'
import { describe, it, expect } from 'vitest'

import { buildWrappedCode } from '../workers/worker-utils'

const LOW_OP_LIMIT = 50_000

/** Flat top-level loop that far exceeds LOW_OP_LIMIT line events. */
const FLAT_OVER_LIMIT = `
total = 0
for i in range(100000):
    total += i
print(total)
`.trimStart()

/** Same over-limit loop, wrapped in a function (pre-fix this WAS counted). */
const FUNC_OVER_LIMIT = `
def main():
    total = 0
    for i in range(100000):
        total += i
    print(total)
main()
`.trimStart()

/** Normal flat code well within the limit. */
const FLAT_NORMAL = `
x = int(input())
print(x * 2)
`.trimStart()

/**
 * Execute wrapped code under python3. The wrapper captures stdout into
 * `_output` without printing it, so the harness appends a real-stdout write
 * to read it back. Returns the subprocess result for status/stdout/stderr
 * assertions.
 */
function runWrapped(userCode: string, input: string, opLimit: number | null) {
  const wrapped = buildWrappedCode(userCode, input, opLimit)
  const harness = `${wrapped}\nimport sys as _t\n_t.__stdout__.write(_output)\n`
  return spawnSync('python3', ['-c', harness], {
    encoding: 'utf-8',
    timeout: 30_000,
  })
}

function pythonAvailable(): boolean {
  try {
    execFileSync('python3', ['-c', 'pass'], { encoding: 'utf-8', timeout: 10_000 })
    return true
  } catch {
    return false
  }
}

const hasPython = pythonAvailable()

// Shape assertions run even without python3 — but they are NOT the gate;
// the execution suite below is what proves runtime behavior.
describe('exempt wrapper shape (opLimit: null)', () => {
  it('injects no tracer and no settrace, keeps sandbox and stdout capture', () => {
    const wrapped = buildWrappedCode(FLAT_NORMAL, '1\n', null)
    expect(wrapped).not.toContain('settrace')
    expect(wrapped).not.toContain('_tracer')
    expect(wrapped).toContain('_SandboxFinder')
    expect(wrapped).toContain('_captured_stdout')
  })
})

if (!hasPython) {
  describe('real-python execution', () => {
    it.skip('skipped — python3 unavailable (CI guarantees it; see content-regression preflight)', () => {})
  })
} else {
  describe('real-python execution: op-count guard', () => {
    it('flat top-level loop exceeding the limit is terminated with Operation limit exceeded', () => {
      const res = runWrapped(FLAT_OVER_LIMIT, '', LOW_OP_LIMIT)
      expect(res.status, 'flat over-limit code must NOT run to completion').not.toBe(0)
      expect(res.stderr).toContain('Operation limit exceeded')
    })

    it('normal flat code completes with correct output and no error', () => {
      const res = runWrapped(FLAT_NORMAL, '21\n', LOW_OP_LIMIT)
      expect(res.stderr).toBe('')
      expect(res.status).toBe(0)
      expect(res.stdout).toBe('42\n')
    })

    it('function-wrapped loop exceeding the limit keeps pre-fix behavior', () => {
      const res = runWrapped(FUNC_OVER_LIMIT, '', LOW_OP_LIMIT)
      expect(res.status).not.toBe(0)
      expect(res.stderr).toContain('Operation limit exceeded')
    })

    it('exempt mode (opLimit: null) runs an over-limit loop to completion', () => {
      const res = runWrapped(FLAT_OVER_LIMIT, '', null)
      expect(res.stderr).toBe('')
      expect(res.status).toBe(0)
      expect(res.stdout).toBe('4999950000\n')
    })
  })
}
