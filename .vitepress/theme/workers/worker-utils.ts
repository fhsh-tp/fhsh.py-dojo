/**
 * Pure utility functions for the Pyodide worker.
 * Extracted for testability — no Worker globals or Pyodide dependency.
 */

export type Verdict = 'AC' | 'WA'

export type VerdictDetail = 'hidden' | 'actual' | 'full'

/**
 * Build the optional expected/actual fields for a TestcaseResult
 * based on the verdictDetail setting.
 *
 * - hidden: omit both
 * - actual: include actual only
 * - full:   include both
 */
export function buildTestcaseResultFields(
  actual: string,
  expected: string,
  verdictDetail: VerdictDetail,
): { actual?: string; expected?: string } {
  switch (verdictDetail) {
    case 'hidden':
      return {}
    case 'actual':
      return { actual }
    case 'full':
      return { actual, expected }
  }
}

/**
 * Compare actual output to expected output.
 * Strips trailing whitespace/newlines before comparison (mirrors typical judge behaviour).
 */
export function computeVerdict(actual: string, expected: string): Verdict {
  return actual.trimEnd() === expected.trimEnd() ? 'AC' : 'WA'
}

/**
 * Build the Python code that will be executed inside Pyodide.
 * Injects:
 *   1. sys.settrace op-counter (primary TLE guard) — skipped when
 *      opLimit is null (trusted code, e.g. challenge generators)
 *   2. sys.stdin simulation via io.StringIO
 *   3. sys.stdout capture via io.StringIO
 *   4. User code
 *   5. sys.settrace removal + output extraction
 *
 * The tracer is attached to the CURRENT frame as well as installed
 * globally: sys.settrace only hooks frames created afterwards, and the
 * user code runs flat in this very module frame — without the f_trace
 * line, flat top-level code is never counted (op_count stays 0).
 */
export function buildWrappedCode(
  userCode: string,
  input: string,
  opLimit: number | null,
): string {
  // Escape input for embedding in a Python string literal
  const escapedInput = input.replace(/\\/g, '\\\\').replace(/"""/g, '\\"\\"\\"')

  const opGuard =
    opLimit === null
      ? ''
      : `
# ── op-count TLE guard ────────────────────────────────────────────
_op_count = 0
_op_limit = ${opLimit}

def _tracer(frame, event, arg):
    global _op_count
    _op_count += 1
    if _op_count > _op_limit:
        raise TimeoutError("Operation limit exceeded (${opLimit} ops)")
    return _tracer

sys.settrace(_tracer)
sys._getframe().f_trace = _tracer
`

  return `
import sys
import sys as _sys
import io
${opGuard}
# ── sandbox guard ─────────────────────────────────────────────────
# Implements find_spec, the only meta-path protocol CPython still consults.
# The find_module/load_module pair this guard used to implement was removed in
# 3.12: a finder offering only those methods is skipped outright, so the guard
# read as protection while blocking nothing. Raising here rather than returning
# a loader keeps the refusal at the earliest point in the import.
class _SandboxFinder:
    _BLOCKED = ('js', 'pyodide_js', 'pyodide')

    def find_spec(self, fullname, path=None, target=None):
        root = fullname.partition('.')[0]
        if root in self._BLOCKED:
            raise ImportError(f"Module '{fullname}' is not available")
        return None

_sys.meta_path.insert(0, _SandboxFinder())
for _n in list(_sys.modules):
    if _n in ('js', 'pyodide_js', 'pyodide') or \
       _n.startswith(('js.', 'pyodide_js.', 'pyodide.')):
        del _sys.modules[_n]

# ── stdin / stdout redirect ───────────────────────────────────────
sys.stdin = io.StringIO("""${escapedInput}""")
_captured_stdout = io.StringIO()
sys.stdout = _captured_stdout

# ── user code ─────────────────────────────────────────────────────
${userCode}

# ── teardown ──────────────────────────────────────────────────────
${opLimit === null ? '' : 'sys.settrace(None)\n'}_output = _captured_stdout.getvalue()
`.trimStart()
}
