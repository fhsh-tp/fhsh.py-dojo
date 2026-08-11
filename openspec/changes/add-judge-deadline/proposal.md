## Why

判題引擎目前沒有任何生效的「每筆測資時間上限」。worker 內的 5,000 ms 軟旗標是 `setTimeout` 排的 macrotask，而 `await pyodide.runPythonAsync(...)` 回來後的 `clearTimeout` 走 microtask、必定先執行——對同步的學生程式碼（也就是全部的提交）這個旗標永遠不會觸發。生產路徑的 `run_only` handler 連這個失效的旗標都沒有。

後果不是「偶爾漏判一筆」，而是整條成本鑑別軸失守：學生只要在提交開頭寫 `sys.settrace(None)` 就能凍結 op 計數器（實測全場 5 ops），或把 K 次迴圈攤平到同一個 source line 把 op 成本稀釋 24 倍，兩種寫法都能讓「應該 TLE」的解拿到滿分。全站以成本為鑑別軸的題目（apcs005／006／007／008／010／014 等）都受影響。這件事已在 `openspec/BACKLOG.md` 第 2.8 節跨三輪 RCA 累積記錄，而 `openspec/specs/gem-blast-challenge/spec.md` 更已預先登記：實作這項修復的 change 必須經正常 spec-delta 流程修訂該條文。

## What Changes

- 新增每筆測資的真實 deadline：主執行緒 watchdog 在每筆測資開始時武裝，到期即透過 `SharedArrayBuffer` 中斷緩衝區（Pyodide 的 `setInterruptBuffer`）中斷正在執行的 Python，worker 存活並繼續下一筆。
- 新增第二層裁決：worker 在每筆結束後以自己量到的 elapsed 時間補判 TLE。這一層同時是無 `SharedArrayBuffer` 環境的 fallback 路徑，讓功能在未跨來源隔離的部署下降級而非失效。
- 判題執行從 `runPythonAsync` 改為同步 `runPython`。中斷產生的 `KeyboardInterrupt` 在非同步路徑上會從 Immediate 回呼逃出 try/catch 並終結整個 worker。
- 三個執行 handler（`run`、`run_only`、`execute`）套用同一套 deadline 語義，生產路徑的 `run_only` 因此首次獲得每筆時間上限，並沿用既有的 `timed_out` 結構化欄位讓 WASM judge 產生 TLE 判定。
- 生產環境與 dev server 都送出 `Cross-Origin-Opener-Policy` 與 `Cross-Origin-Embedder-Policy` 標頭，使 `SharedArrayBuffer` 可用。dev 原本宣告於 `vite.server.headers` 的設定經實測**從未生效**（VitePress 2 不轉發），已移除；標頭的單一定義為 `docs/public/_headers`，本機以新增的 `preview:cf` 腳本（`wrangler pages dev`）驗證。
- 修正累計硬砍時的結果呈現：結果表格改以測資總數為分母，使被中斷的執行不再看起來全綠。
- **BREAKING**：既有題目中，任何單筆執行時間超過新 deadline 的正解或收編路線會由 AC 變成 TLE。本 change 必須逐題量測既有題目的正解與收編路線並記錄，deadline 常數依量測結果選定。

## Capabilities

### New Capabilities

- `judge-deadline`: 每筆測資的牆鐘 deadline——watchdog 武裝與解除、中斷緩衝區協定、elapsed 事後裁決、無 SharedArrayBuffer 時的降級行為，以及三個執行 handler 的一致語義。

### Modified Capabilities

- `execute-mode`: `useExecutor` 的牆鐘語義由「整批 N×6 秒一次性 timer」擴充為「每筆 deadline ＋ 整批上限」，`execute` handler 亦套用每筆 deadline。
- `pyodide-sandbox-guard`: `buildWrappedCode` 產生的包裝碼組成與執行方式改變（同步執行、中斷武裝時機），既有的注入順序條文需對應修訂。
- `gem-blast-challenge`: 該 spec 中記錄「worker 牆鐘旗標對同步學生碼失效、因此不以測資獵殺 C 內建繞道」的條文，依其自身規定於本修復實作時修訂。

## Impact

- Affected specs: 新增 `judge-deadline`；修訂 `execute-mode`、`pyodide-sandbox-guard`、`gem-blast-challenge`
- Affected code:
  - New:
    - `docs/public/_headers`
  - Modified:
    - `.vitepress/theme/workers/pyodide.worker.ts`
    - `.vitepress/theme/workers/worker-utils.ts`
    - `.vitepress/theme/composables/useExecutor.ts`
    - `.vitepress/theme/composables/useChallengeRunner.ts`
    - `.vitepress/theme/components/editor/TestResultPanel.vue`
    - `.vitepress/config.mts`
    - `package.json`
    - `openspec/BACKLOG.md`
  - Removed: （無）
