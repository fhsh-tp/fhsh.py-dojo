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
const COMPREH = `
def work(n):
    return sum((i*3)%7 for i in range(n))
r = work(N)
`
const SETTRACE = `
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
`
const WSETTRACE = `
import sys, time, dis
_c = 0
_W = {}
def _wt(code):
    w = {}
    for ins in dis.get_instructions(code):
        ln = ins.line_number
        if ln is not None: w[ln] = w.get(ln, 0) + 1
    _W[code] = w
    return w
def _t(f, e, a):
    global _c
    c = f.f_code
    w = _W.get(c) or _wt(c)
    _c += w.get(f.f_lineno, 1)
    return _t
_t0 = time.perf_counter()
sys.settrace(_t); sys._getframe().f_trace = _t
%%BODY%%
sys.settrace(None)
_ms = (time.perf_counter()-_t0)*1000
`
const N = 200000
const rows = []
for (const [mode, tmpl] of [['settrace(現況)', SETTRACE], ['settrace+加權(新案)', WSETTRACE]]) {
  for (const [wname, body] of [['normal', NORMAL], ['flattened_x8', FLAT], ['genexpr(C層)', COMPREH]]) {
    const code = `N = ${N}\n` + tmpl.replace('%%BODY%%', body)
    const d = await py.runPythonAsync(code + `\n(_c, _ms)`)
    const [c, ms] = d.toJs()
    rows.push({ mode, workload: wname, cost: c, ms: Math.round(ms), per_iter: (c/N).toFixed(3) })
    d.destroy?.()
  }
}
console.table(rows)
const g=(m,w)=>rows.find(r=>r.mode===m&&r.workload===w).cost
console.log('攤平稀釋倍率  現況:', (g('settrace(現況)','normal')/g('settrace(現況)','flattened_x8')).toFixed(2),
            ' 新案:', (g('settrace+加權(新案)','normal')/g('settrace+加權(新案)','flattened_x8')).toFixed(2))
console.log('新案/現況 成本單位比 (normal):', (g('settrace+加權(新案)','normal')/g('settrace(現況)','normal')).toFixed(2))
