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
import { mkdtempSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { afterAll, describe, it, expect } from 'vitest'

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

    it('the tracer does not alter program output (guarded vs exempt identical)', () => {
      const guarded = runWrapped(FLAT_NORMAL, '21\n', LOW_OP_LIMIT)
      const exempt = runWrapped(FLAT_NORMAL, '21\n', null)
      expect(guarded.stdout).toBe('42\n')
      expect(exempt.stdout).toBe(guarded.stdout)
    })
  })

  describe('real-python execution: cross-run trace state', () => {
    const tmp = mkdtempSync(join(tmpdir(), 'wrapper-trace-'))
    afterAll(() => rmSync(tmp, { recursive: true, force: true }))

    it('an errored run does not poison the next run under the handler sequence', () => {
      // An ordinary user exception (the normal RE path) skips the wrapper's
      // own settrace(None) teardown, leaking the tracer into the shared
      // interpreter. The worker handlers guard this with resetTraceState()
      // BEFORE globals.clear() — this test replays that exact sequence in
      // one interpreter: errored run → antidote → clear → next run must be
      // clean. Without the antidote step, the second exec dies in its
      // 'call' event with a NameError from the stale tracer.
      const wrappedBad = buildWrappedCode('lst = []\nprint(lst[5])\n', '', LOW_OP_LIMIT)
      const wrappedGood = buildWrappedCode(FLAT_NORMAL, '21\n', LOW_OP_LIMIT)
      writeFileSync(join(tmp, 'w1.py'), wrappedBad, 'utf-8')
      writeFileSync(join(tmp, 'w2.py'), wrappedGood, 'utf-8')

      const driver = `
import pathlib
import sys

G = {}
try:
    exec(compile(pathlib.Path(${JSON.stringify(join(tmp, 'w1.py'))}).read_text(), "<w1>", "exec"), G)
except Exception as e:
    print("W1_ERR", type(e).__name__, file=sys.stderr)

# resetTraceState() equivalent — must come BEFORE G.clear() (worker order)
try:
    exec(compile("import sys\\nsys.settrace(None)", "<antidote>", "exec"), G)
except Exception:
    pass
G.clear()

exec(compile(pathlib.Path(${JSON.stringify(join(tmp, 'w2.py'))}).read_text(), "<w2>", "exec"), G)
sys.__stdout__.write(G["_output"])
`.trimStart()

      const res = spawnSync('python3', ['-c', driver], { encoding: 'utf-8', timeout: 30_000 })
      expect(res.stderr.trim()).toBe('W1_ERR IndexError')
      expect(res.status).toBe(0)
      expect(res.stdout).toBe('42\n')
    })
  })
}
