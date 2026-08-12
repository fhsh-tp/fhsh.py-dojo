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
const out = await py.runPythonAsync(`
import sys
res = {}
res['version'] = sys.version
res['has_monitoring'] = hasattr(sys, 'monitoring')
if hasattr(sys, 'monitoring'):
    m = sys.monitoring
    res['events'] = [e for e in dir(m.events) if e.isupper()]
    res['tool_ids'] = [n for n in dir(m) if n.endswith('_ID')]
res
`)
console.log(JSON.stringify(out.toJs({dict_converter: Object.fromEntries}), null, 2))
