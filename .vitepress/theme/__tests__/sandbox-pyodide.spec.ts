// @vitest-environment node
/**
 * Real-Pyodide check that the sandbox guard blocks the JS bridge.
 *
 * `worker-utils-python.spec.ts` already exercises the guard under the system
 * interpreter, which shares CPython 3.13's import protocol. This suite closes
 * the remaining gap: it runs the guard inside the runtime that actually has
 * `js` and `pyodide_js` to reach. Under the system interpreter a dead guard and
 * a live one can both end in ImportError — one says "No module named", the
 * other "is not available" — so only here does a bypass become an observable
 * capability rather than a message difference.
 *
 * The wrapper comes from `buildWrappedCode`, never from a copy. An earlier
 * probe for this defect embedded its own transcription of the guard and kept
 * reporting a bypass after the real guard was fixed.
 */
import { createRequire } from 'node:module'
import { describe, it, expect, beforeAll } from 'vitest'

import { buildWrappedCode } from '../workers/worker-utils'

const require = createRequire(import.meta.url)

let pyodideAvailable = true
try {
  require.resolve('pyodide/pyodide.mjs')
} catch {
  pyodideAvailable = false
}

const OP_LIMIT = 1_000_000

describe.skipIf(!pyodideAvailable)('sandbox guard inside Pyodide', () => {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  let pyodide: any

  beforeAll(async () => {
    const { loadPyodide } = await import('pyodide/pyodide.mjs')
    pyodide = await loadPyodide({ stdout: () => {}, stderr: () => {} })
  }, 120_000)

  /** Run student code through the real wrapper; report what escaped. */
  function run(userCode: string): { ok: boolean; error: string } {
    try {
      pyodide.runPython(buildWrappedCode(userCode, '', OP_LIMIT))
      return { ok: true, error: '' }
    } catch (err) {
      return { ok: false, error: String(err) }
    }
  }

  it.each(['js', 'pyodide_js', 'pyodide'])('blocks `import %s` where the module genuinely exists', (mod) => {
    const res = run(`import ${mod}`)
    expect(res.ok).toBe(false)
    expect(res.error).toContain('is not available')
  })

  it('blocks reaching the bridge through a submodule', () => {
    const res = run('import pyodide.ffi')
    expect(res.ok).toBe(false)
    expect(res.error).toContain('is not available')
  })

  it('blocks the from-import spelling', () => {
    const res = run('from js import Object')
    expect(res.ok).toBe(false)
    expect(res.error).toContain('is not available')
  })

  it('blocks importlib as an indirect route to the bridge', () => {
    const res = run('import importlib\nimportlib.import_module("js")')
    expect(res.ok).toBe(false)
    expect(res.error).toContain('is not available')
  })

  it('still allows ordinary standard-library imports', () => {
    const res = run('import json, math\nprint(json.dumps(math.floor(2.7)))')
    expect(res.ok).toBe(true)
  })
})

/**
 * The operation counter must survive a submission that tampers with the
 * tracing API.
 *
 * `globals.clear()` empties the execution namespace but cannot reach
 * `sys.modules`, which persists across every testcase of one submission. Two
 * lines at the top of a submission — rebinding `sys.settrace` — used to make
 * the wrapper's own tracer installation a no-op for every later testcase, so
 * the counter read zero and the op limit stopped existing. Measured before the
 * fix: a testcase that should record two million operations recorded none,
 * which turns a 12/20 route into 20/20.
 */
describe.skipIf(!pyodideAvailable)('tracing API is restored between testcases', () => {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  let pyodide: any
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  let pristineSys: any
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  let pristineSettrace: any

  beforeAll(async () => {
    const { loadPyodide } = await import('pyodide/pyodide.mjs')
    pyodide = await loadPyodide({ stdout: () => {}, stderr: () => {} })
    pristineSys = pyodide.runPython('import sys; sys')
    pristineSettrace = pyodide.runPython('import sys; sys.settrace')
  }, 120_000)

  /** Mirror of the Worker's per-testcase preamble. */
  function resetBetweenTestcases(): void {
    pyodide.globals.set('__judge_sys', pristineSys)
    pyodide.globals.set('__judge_settrace', pristineSettrace)
    // Through the captured module object, never through `import sys`: a
    // submission that swapped the `sys` entry would hand the restore its own
    // decoy, which has no module table to repair.
    pyodide.runPython(
      "__judge_sys.modules['sys'] = __judge_sys\n" + '__judge_sys.settrace = __judge_settrace\n',
    )
    pyodide.runPython('import sys\nsys.settrace(None)')
    try {
      pyodide.globals.clear()
    } catch {
      /* older runtimes */
    }
  }

  /** Run one testcase through the real wrapper and report the counted ops. */
  function opsFor(userCode: string): number {
    resetBetweenTestcases()
    try {
      pyodide.runPython(buildWrappedCode(userCode, '', OP_LIMIT))
    } catch {
      /* limit or error — the count is what matters */
    }
    const n = pyodide.runPython('globals().get("_op_count", -1)')
    return typeof n === 'bigint' ? Number(n) : n
  }

  const WORK = 'total = 0\nfor i in range(50000): total += i'

  it('counts operations normally before any tampering', () => {
    expect(opsFor(WORK)).toBeGreaterThan(50_000)
  }, 60_000)

  it('keeps counting after a submission rebinds sys.settrace', () => {
    opsFor('import sys\nsys.settrace = lambda *a: None')
    expect(opsFor(WORK)).toBeGreaterThan(50_000)
  }, 60_000)

  it('keeps counting after a submission replaces the sys entry in sys.modules', () => {
    opsFor('import sys\nclass _Fake:\n    settrace = staticmethod(lambda *a: None)\nsys.modules["sys"] = _Fake()')
    expect(opsFor(WORK)).toBeGreaterThan(50_000)
  }, 60_000)

  it('still enforces the op limit on a later testcase after tampering', () => {
    opsFor('import sys\nsys.settrace = lambda *a: None')
    const ops = opsFor('total = 0\nfor i in range(2000000): total += i')
    expect(ops).toBeGreaterThan(OP_LIMIT)
  }, 60_000)
})
