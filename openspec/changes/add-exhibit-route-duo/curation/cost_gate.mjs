// 成本閘：plan013/plan014 的斷言牆只看得到「輸出對不對」，看不到 op 上限與牆鐘。
// 本檔把成本軸的契約也機械化——對出貨 literal 逐筆跑 probe，套用判題引擎的三道閘門
// （C1 op 上限、C3 每筆 5,000 ms 軟旗標、C4 累計預算），再比對契約得分。
//
// 執行：node cost_gate.mjs        （任一條不符即以非零碼結束）
import { spawn } from 'node:child_process'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const HERE = path.dirname(fileURLToPath(import.meta.url))
const OP_LIMIT = 10_000_000
// C3 的每筆 5,000 ms 軟旗標對同步 Python 不會觸發（清除計時器的 microtask 先於 timer
// macrotask），因此**不得**在本閘門模擬它——初版誤模擬導致 batch32 被誤判為 15/20。
// 唯一真正生效的牆鐘閘門是 C4 的累計硬砍。
const CUMULATIVE_MS = 20 * 6_000

// 契約：路線檔 → { challenge, expect }（expect = 應得分數）
const CONTRACTS = [
  { file: 'ref013.py', ch: 'c013', expect: 20 },
  { file: 'gen013.py', ch: 'c013', expect: 20 },
  { file: 'routes/r013_indexnaive.py', ch: 'c013', expect: 20 },
  { file: 'routes/r013_r1_mirror.py', ch: 'c013', expect: 20 },
  { file: 'ref014.py', ch: 'c014', expect: 20 },
  { file: 'gen014.py', ch: 'c014', expect: 20 },
  { file: 'routes/r014_levelwise.py', ch: 'c014', expect: 20 },
  { file: 'routes/r014_levelwise_rec.py', ch: 'c014', expect: 20 },
  { file: 'routes/r014_periodic.py', ch: 'c014', expect: 20 },
  // 大整數位元場寫法：語義正確、實測仍 20/20，但本身是 O(週期²)（每次 `1 << n`／`st >> n`
  // 都是 2^(D−1) 位元的大數運算），全場約 92 秒、佔 C4 累計預算 77% —— 收編承諾成立，
  // 但屬「已知的慢寫法」，故豁免本閘門的 70% 時間警戒線並在矩陣記錄（B8b）。
  { file: 'routes/r014_periodic_bits.py', ch: 'c014', expect: 20, slowOk: true },
  { file: 'routes/r014_naive.py', ch: 'c014', expect: 15 },
  { file: 'routes/r014_lean.py', ch: 'c014', expect: 15 },
  { file: 'routes/r014_flat.py', ch: 'c014', expect: 15 },
  // K 球攤平到同一行的寫法規避了 op 計數（C13），而 C3 軟旗標對同步碼無效（C3）：
  // 它是**已知且已記錄的平台層殘餘**，契約值即為實測值 20，不得被誤讀為「已封殺」。
  { file: 'routes/r014_batch32.py', ch: 'c014', expect: 20 },
]

function run(sol, inputs) {
  return new Promise((resolve) => {
    const p = spawn('node', [path.join(HERE, 'probe.mjs'), sol, ...inputs], { cwd: HERE })
    let out = ''
    p.stdout.on('data', (d) => (out += d))
    p.stderr.on('data', () => {})
    p.on('close', () => resolve(out.split('\n').filter((l) => l.startsWith('{')).map((l) => JSON.parse(l))))
  })
}

const problems = []
const report = []

for (const c of CONTRACTS) {
  const inputs = []
  for (let i = 1; i <= 20; i++) {
    inputs.push(path.join(HERE, 'literals', `${c.ch}_${String(i).padStart(2, '0')}.txt`))
  }
  const rows = await run(path.join(HERE, c.file), inputs)
  if (rows.length !== 20) {
    problems.push(`${c.file}: probe 只回報 ${rows.length} 筆`)
    continue
  }
  let score = 0
  let total = 0
  const verdicts = []
  for (let i = 0; i < 20; i++) {
    const r = rows[i]
    const expText = fs.readFileSync(inputs[i].replace(/\.txt$/, '.exp'), 'utf8')
    total += r.ms
    let v
    if (r.err) v = r.ops > OP_LIMIT ? 'TLE-op' : 'RE'
    else v = r.outLen === expText.length ? 'AC?' : 'WA'
    verdicts.push(v)
    if (v === 'AC?') score++
  }
  // 'AC?' 只比長度；正確性由 plan013/plan014 的斷言牆負責，此處只管成本軸
  report.push({ file: c.file, score, expect: c.expect, totalMs: total, verdicts })
  if (score !== c.expect) problems.push(`${c.file}: 成本軸得分 ${score}，契約要求 ${c.expect}`)
  if (!c.slowOk && total > CUMULATIVE_MS * 0.7) {
    problems.push(`${c.file}: 全場 ${total} ms 超過累計預算 ${CUMULATIVE_MS} ms 的七成，逼近 C4 中斷風險`)
  }
}

fs.writeFileSync(path.join(HERE, 'report_cost.json'), JSON.stringify({ report, problems }, null, 1))
for (const r of report) {
  console.log(`${r.file.padEnd(34)} ${String(r.score).padStart(2)}/20 (契約 ${r.expect}) 全場 ${r.totalMs} ms`)
}
if (problems.length) {
  console.log('\n成本閘失敗：')
  for (const p of problems) console.log('  -', p)
  process.exit(1)
}
console.log('\n成本閘全數通過。')
