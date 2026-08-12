import { createRequire as _cr } from 'node:module'
import { fileURLToPath as _f2p } from 'node:url'
import { dirname as _dn, join as _join } from 'node:path'
import { existsSync as _ex } from 'node:fs'
function _repoRoot(start) {
  let cur = start
  for (;;) {
    if (_ex(_join(cur, 'package.json'))) return cur
    const up = _dn(cur)
    if (up === cur) throw new Error('找不到 repo 根（往上都沒有 package.json）：' + start)
    cur = up
  }
}
const _ROOT = _repoRoot(_dn(_f2p(import.meta.url)))
const { loadPyodide } = await import(_join(_ROOT, 'node_modules/pyodide/pyodide.mjs'))
const py = await loadPyodide()

// Two workloads: normal loop vs the "flatten K iterations onto one source line" bypass
const NORMAL = `
def work(n):
    t = 0
    i = 0
    while i < n:
        t += (i * 3) % 7
        i += 1
    return t
r = work(N)
`
const FLAT = `
def work(n):
    t = 0; i = 0
    while i < n: t += (i*3)%7; i += 1; t += (i*3)%7; i += 1; t += (i*3)%7; i += 1; t += (i*3)%7; i += 1; t += (i*3)%7; i += 1; t += (i*3)%7; i += 1; t += (i*3)%7; i += 1; t += (i*3)%7; i += 1
    return t
r = work(N)
`
const MODES = {
  settrace_line: `
import sys, time
_c = 0
def _t(f, e, a):
    global _c
    _c += 1
    return _t
_t0 = time.perf_counter()
sys.settrace(_t); sys._getframe().f_trace = _t
%%BODY%%
sys.settrace(None)
_ms = (time.perf_counter()-_t0)*1000
`,
  mon_line: `
import sys, time
M = sys.monitoring; TID = M.DEBUGGER_ID
_c = 0
def _cb(*a):
    global _c
    _c += 1
_t0 = time.perf_counter()
M.use_tool_id(TID, "judge")
M.register_callback(TID, M.events.LINE, _cb)
M.set_events(TID, M.events.LINE)
%%BODY%%
M.set_events(TID, 0); M.free_tool_id(TID)
_ms = (time.perf_counter()-_t0)*1000
`,
  mon_branch: `
import sys, time
M = sys.monitoring; TID = M.DEBUGGER_ID
_c = 0
def _cb(*a):
    global _c
    _c += 1
_t0 = time.perf_counter()
M.use_tool_id(TID, "judge")
M.register_callback(TID, M.events.BRANCH, _cb)
M.register_callback(TID, M.events.PY_START, _cb)
M.set_events(TID, M.events.BRANCH | M.events.PY_START)
%%BODY%%
M.set_events(TID, 0); M.free_tool_id(TID)
_ms = (time.perf_counter()-_t0)*1000
`,
  mon_instruction: `
import sys, time
M = sys.monitoring; TID = M.DEBUGGER_ID
_c = 0
def _cb(*a):
    global _c
    _c += 1
_t0 = time.perf_counter()
M.use_tool_id(TID, "judge")
M.register_callback(TID, M.events.INSTRUCTION, _cb)
M.set_events(TID, M.events.INSTRUCTION)
%%BODY%%
M.set_events(TID, 0); M.free_tool_id(TID)
_ms = (time.perf_counter()-_t0)*1000
`,
}
const N = 200000
const rows = []
for (const [mode, tmpl] of Object.entries(MODES)) {
  for (const [wname, body] of [['normal', NORMAL], ['flattened_x8', FLAT]]) {
    const code = `N = ${N}\n` + tmpl.replace('%%BODY%%', body)
    const d = await py.runPythonAsync(code + `\n(_c, _ms, r)`)
    const [c, ms] = d.toJs()
    rows.push({ mode, workload: wname, events: c, ms: Math.round(ms), ev_per_iter: (c / N).toFixed(3) })
    d.destroy?.()
  }
}
console.table(rows)
