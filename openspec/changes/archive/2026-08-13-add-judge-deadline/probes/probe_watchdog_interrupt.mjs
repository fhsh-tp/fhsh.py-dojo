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
parentPort.on('message', (m) => setTimeout(() => { if (buf[1] === m.gen) buf[0] = 2 }, m.ms))
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
    const d = py.runPython(code)                    // ← 同步，與提交的同步 Python 相符
    res = '回傳 ' + JSON.stringify(d?.toJs ? d.toJs() : d)
    d?.destroy?.()
  } catch (e) {
    res = '拋出 ' + (String(e).match(/KeyboardInterrupt|\w*Error/)?.[0] ?? '?')
  }
  buf[1] = ++gen; buf[0] = 0
  say(`${name} | 預算 ${budgetMs}ms | ${res} | 實際 ${Date.now() - t} ms`)
}

trial('1 誠實快解（應通過）', 'i=0\nwhile i < 2000000: i += 1\n("OK", i)', 3000)
trial('2 誠實慢解（應被中斷）', 'i=0\nwhile i < 200000000: i += 1\n("OK", i)', 3000)
trial('3 settrace(None) 繞道', 'import sys\nsys.settrace(None)\ni=0\nwhile i < 200000000: i += 1\n("OK", i)', 3000)
trial('4 同行攤平繞道', 'i=0\nwhile i < 200000000: i += 1; i += 1; i += 1; i += 1; i += 1; i += 1; i += 1; i += 1\n("OK", i)', 3000)
trial('5 bare except 吞中斷', 'i=0\nwhile i < 20000000:\n    try: i += 1\n    except: pass\n("SURVIVED", i)', 3000)
trial('6 中斷後 runtime 還活著嗎', 'sum(range(1000))', 3000)
trial('7 再跑一次誠實快解', 'i=0\nwhile i < 2000000: i += 1\n("OK", i)', 3000)
say('DONE')
wd.terminate()
