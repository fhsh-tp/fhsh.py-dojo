## 1. Scaffold

- [x] 1.1 （spec: rank-code-backfill challenge contract、prize-order-code challenge contract）以 `pnpm new-challenge rank-code-backfill --title "每日榜單驗證碼回填" --difficulty medium --category apcs --type competition` 與 `pnpm new-challenge prize-order-code --title "頒獎順位驗證碼" --difficulty hard --category apcs --type competition` 建立兩題骨架；驗證：`docs/challenge/rank-code-backfill.md` 與 `docs/challenge/prize-order-code.md` 存在且 id 為 apcs 前綴連號。

## 2. rank-code-backfill（568 版）

- [x] 2.1 （spec: rank-code-backfill challenge contract、TLE cliff via op counter）依 design「D3 參數與範圍」撰寫 params（t int 1..500；group repeat t 內含 n int 1..200000）與「D4 testcase_plan 結構」的 testcase_plan 20 筆（第 1 筆＝題面範例 literal、暖身 band、中段 band、壓力 band ≥6 筆、N=1 與 N=200000 邊界 literal）；驗證：`pnpm build:pools` 成功且該題 20 筆。
- [x] 2.2 （spec: answer semantics including factor bookkeeping、independent reference solutions）依 design「D5 演算法契約」撰寫 generator（增量建表，r mod 10＋twos 盈餘）與實質不同實作策略的 reference_solution（排序後單趟增量掃描＋週期表 vs generator 的一次建表＋pow；sys.stdin.read vs input()），starter_code 留空；驗證：兩者對 spec R1 Example（5→2、1→1、10→8）輸出一致。
- [x] 2.3 （spec: literacy-style problem statements）依 design「D1 考點轉譯與語義」撰寫題面：檢查碼引言、輸入輸出說明、範圍（T ≤ 500、N ≤ 200000、大值警語）、範例區塊與第 1 筆 literal 逐字一致、零資料結構術語；驗證：對照 spec R7 禁字清單掃描通過。

## 3. prize-order-code（10212 版）

- [x] 3.1 （spec: prize-order-code challenge contract、TLE cliff via op counter）依 design「D3 參數與範圍」撰寫 params（t int 1..3；group repeat t 內含 n int 100000..1000000000、m int 0..100000）與「D4 testcase_plan 結構」testcase_plan 20 筆（範例 literal、暖身 band、中段 band、壓力 band ≥6 筆、M=0／P(25,1)／P(26,2)／M=N=100000 literal）；驗證：`pnpm build:pools` 成功且該題 20 筆。
- [x] 3.2 （spec: answer semantics including factor bookkeeping、independent reference solutions）依 design「D5 演算法契約」撰寫 generator（c2/c5 分開追蹤）與實質不同實作策略的 reference_solution（淨差 bal＋2 的冪次週期表 vs generator 的 c2/c5 分開計數），starter_code 留空；驗證：對 spec R2 Example（P(10,2)→9、P(25,1)→5、M=0→1）輸出一致。
- [x] 3.3 （spec: literacy-style problem statements）依 design「D1 考點轉譯與語義」撰寫題面（同 2.3 標準，範圍明示 N ≤ 10⁹、M ≤ 100000、M ≤ N）；驗證：禁字掃描通過。

## 4. 建置與校準

- [x] 4.1 執行 `pnpm gen:keymaterial && pnpm build:wasm && pnpm build:pools`，以引擎 worst-case 估算校準兩題 `input_budget`（預期 568 版預設 4096 足夠；不足即調升至估算值）；驗證：build:pools 零警告完成、兩題各 10 blocks×20 筆。

## 5. 判題斷崖驗證（design D2／D6）

- [x] 5.1 （spec: TLE cliff via op counter；design「D2 斷崖機制對映」）以 settrace 同款計數器對正式測資輸入實測並記入 `openspec/changes/add-rank-code-challenge-duo/dev-verification-notes.md`：兩題正解 ops ≤ 2.5M（上限/4）；568 天真解於壓力筆 ≥ 20M ops；10212 天真解（1..N 全乘）於壓力筆 ≥ 20M ops；驗證：門檻全數達標。
- [x] 5.2 （spec: C-builtin bypass lethality）實測「D6 繞道獵殺驗收」繞道清單並記入同檔：568 逐查詢 math.factorial 壓力筆總牆鐘 native×2 ≥ 240s；10212 大數連乘＋剝零 native×2 ≥ 240s（跨壓力筆合計）；str() 路線 ValueError；驗證：D6.a 每條繞道有實測數據與死法結論；D6.b 每條殘餘有實測存活數據與「不可由測資消滅」論證（記入 notes 5.2b）。

## 6. 測試守門

- [x] 6.1 （spec: independent reference solutions）執行 `node_modules/.bin/vitest --run scripts/challenge-params.test.ts scripts/content-regression.test.ts` 與 `pnpm typecheck`、`pnpm lint`；驗證：全綠，content-regression 覆蓋兩題 reference_solution。

## 7. R3／RCA 終局處置（math.perm 收編）

- [x] 7.1 （spec: C-builtin bypass lethality）矩陣 F19/F20 先行落地，派生 design（Context #10、D2、D6.a/D6.b 分流、Goals/Non-Goals、Risks、D1 語氣契約、D5）、proposal What Changes、spec R5（存活例外句＋accepted residual Scenario）、notes（5.1 對照列、5.2b、驗收預測矩陣聰明解列）；驗證：grep 全 change 目錄無「D6 清單」單一指涉殘留、spectra validate 通過。
- [x] 7.2 （spec: literacy-style problem statements）改寫 prize-order-code 題面提示句為經實測為真的成本警語（去除不可能性承諾）；驗證：R7 禁字掃描通過、`node_modules/.bin/vitest --run scripts/challenge-params.test.ts scripts/content-regression.test.ts` 全綠。
- [x] 7.3 於 openspec/BACKLOG.md §2.8 補記「單一 stdlib API 可解題型必有不可獵殺路徑」推論與兩案例索引；驗證：該段文字落地。
