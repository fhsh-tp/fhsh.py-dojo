// Probe harness: run a solution file against input files inside Pyodide with
// the same op-count tracer the judge uses. Usage:
//   node probe.mjs <sol.py> <in1.txt> [in2.txt ...]
import { loadPyodide } from '/Users/phoenix/dev/fhsh-projects/fhsh.py-dojo/node_modules/pyodide/pyodide.mjs'
import fs from 'node:fs'

const OP_LIMIT = 10_000_000

function wrap(userCode, input, opLimit) {
  const escapedInput = input.replace(/\\/g, '\\\\').replace(/"""/g, '\\"\\"\\"')
  const guard =
    opLimit === null
      ? ''
      : `
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
import io
${guard}
sys.stdin = io.StringIO("""${escapedInput}""")
_captured_stdout = io.StringIO()
sys.stdout = _captured_stdout

${userCode}

${opLimit === null ? '' : 'sys.settrace(None)\n'}_output = _captured_stdout.getvalue()
`.trimStart()
}

const [solPath, ...inPaths] = process.argv.slice(2)
const noGuard = process.env.NO_GUARD === '1'
const code = fs.readFileSync(solPath, 'utf8')

const py = await loadPyodide({ indexURL: '/Users/phoenix/dev/fhsh-projects/fhsh.py-dojo/node_modules/pyodide/' })

for (const inPath of inPaths) {
  const input = fs.readFileSync(inPath, 'utf8')
  const t0 = performance.now()
  let ops = 0
  let out = ''
  let err = null
  try {
    await py.runPythonAsync(wrap(code, input, noGuard ? null : OP_LIMIT))
    out = py.globals.get('_output') ?? ''
  } catch (e) {
    err = String(e).split('\n').filter(Boolean).slice(-2).join(' | ')
  }
  const ms = performance.now() - t0
  try {
    const c = py.globals.get('_op_count')
    ops = typeof c === 'bigint' ? Number(c) : (c ?? 0)
  } catch {
    ops = -1
  }
  const head = out.split('\n').slice(0, 3).join(' / ')
  console.log(
    JSON.stringify({
      in: inPath.split('/').pop(),
      ops,
      ms: Math.round(ms),
      outLen: out.length,
      out,
      head: head.length > 160 ? head.slice(0, 160) + '…' : head,
      err,
    }),
  )
  try {
    await py.runPythonAsync('import sys\nsys.settrace(None)')
  } catch {
    /* stale tracer */
  }
  py.globals.clear()
}
