import { Worker } from 'node:worker_threads'
import fs from 'node:fs'
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
const LOG = process.argv[2]; fs.writeFileSync(LOG, '')
const say = (...a) => fs.appendFileSync(LOG, a.join(' ') + '\n')
process.on('uncaughtException', (e) => say('!! uncaught:', String(e).slice(0, 80)))
const wdSrc = `
const { parentPort, workerData } = require('node:worker_threads')
const buf = new Uint8Array(workerData.sab)
parentPort.on('message', (m) => setTimeout(() => { if (buf[1] === m.gen) { buf[0] = 2 } }, m.ms))
`
const sab = new SharedArrayBuffer(2)
const buf = new Uint8Array(sab)
const wd = new Worker(wdSrc, { eval: true, workerData: { sab } })
const py = await loadPyodide({ stdout: () => {}, stderr: () => {} })
py.setInterruptBuffer(buf)
let gen = 0
function trial(name, code, budgetMs) {
  buf[0] = 0; buf[1] = ++gen
  wd.postMessage({ ms: budgetMs, gen })
  const t = Date.now()
  let res
  try {
    const d = py.runPython(code)
    res = '回傳 ' + JSON.stringify(d?.toJs ? d.toJs() : d)
    d?.destroy?.()
  } catch (e) { res = '拋出 type=' + (e?.type ?? '?') + ' 首行=' + String(e).split('\n').filter(x=>x.trim()).pop()?.slice(0,60) }
  const el = Date.now() - t
  const flagAfter = buf[0]
  buf[1] = ++gen; buf[0] = 0
  say(`${name} | 預算 ${budgetMs}ms | ${res} | 實際 ${el} ms | 事後旗標=${flagAfter}`)
}
const N = '2000000000'
trial('1 bare except 包整段', `i=0\ntry:\n    while i < ${N}: i += 1\nexcept: pass\n("SURVIVED", i)`, 3000)
trial('2 明示 except KeyboardInterrupt', `i=0\ntry:\n    while i < ${N}: i += 1\nexcept KeyboardInterrupt: pass\n("SURVIVED", i)`, 3000)
trial('3 except BaseException 包整段', `i=0\ntry:\n    while i < ${N}: i += 1\nexcept BaseException: pass\n("SURVIVED", i)`, 3000)
trial('4 迴圈外層 while + 內層重試', `i=0\nfor _ in range(1000):\n    try:\n        while i < ${N}: i += 1\n        break\n    except BaseException: pass\n("SURVIVED", i)`, 3000)
trial('5 誠實快解（對照）', 'i=0\nwhile i < 2000000: i += 1\n("OK", i)', 30000)
say('DONE')
wd.terminate()
