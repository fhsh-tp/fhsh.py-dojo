# 追溯矩陣（change：add-judge-deadline）

本檔為本 change 的**單一真相來源（SSOT）**。proposal／design／spec／tasks 的每一句量化敘述都必須指回這裡的事實 ID；沒有 ID 的數字不得出現在任何文件。稽核者從本矩陣派生，不從散文派生。

**量測環境**：node-Pyodide（`node_modules/pyodide` 0.29.3，與站台自架版本同源）。牆鐘數字為 node 環境值，僅作**相對量級**參考。凡「需瀏覽器覆核」欄為「是」的事實，在瀏覽器實測完成前**不得**作為釘定常數的依據。

**證據腳本**：本 change 的 `probes/` 目錄。全部以 `node <script>` 執行，不需參數（`probe_watchdog_interrupt.mjs` 與 `probe_interrupt_swallow.mjs` 需一個輸出檔路徑參數）。腳本以往上尋找 `package.json` 的方式定位 repo 根，不依賴任何絕對路徑。

---

## C 表：現況缺陷（本 change 的存在理由）

| ID | 事實 | 證據 | 需瀏覽器覆核 | proposal | design | spec |
|----|------|------|--------------|----------|--------|------|
| C1 | worker 每筆 5,000 ms 軟旗標對同步 Python 永不觸發：旗標是 `setTimeout` macrotask，`await pyodide.runPythonAsync(...)` 之後的 `clearTimeout` 走 microtask 必先執行 | `pyodide.worker.ts` 的 `wallClock`／`wallClockTle`；既有記錄見 `openspec/specs/gem-blast-challenge/spec.md` 的 Bypass acceptance 條文與 `openspec/BACKLOG.md` §2.8 | 否（既有實測已記錄） | Why 第 1 段 | Context 第 1 點 | gem-blast MODIFIED 第 1 段 |
| C2 | `run_only`（生產路徑）連失效的旗標都沒有，完全無每筆時間上限 | `pyodide.worker.ts` 的 `handleRunOnly` | 否 | Why 第 1 段 | Context 第 1 點 | judge-deadline「Production judging receives the deadline verdict」 |
| C3 | 主執行緒硬砍為「測資數 × 6,000 ms」一次性 timer，粒度是整批 | `useExecutor.ts` 的 `WALL_CLOCK_KILL_MS` 與 `totalBudget` | 否 | Why 第 1 段 | Context 第 2 點 | execute-mode MODIFIED |
| C4 | 硬砍觸發時得分分母正確但結果表格以已回報列數為分母 → 中斷的執行可能看起來全綠 | `useExecutor.ts` 的 `stop()` 與 `TestResultPanel.vue` | 否 | What Changes 第 6 點 | D7 | judge-deadline「Interrupted batches are displayed honestly」 |
| C5 | `sys.settrace(None)` 寫在提交開頭即凍結 op 計數（實測全場 5 ops） | change C 的 R1 賞金實測；本 change 由 P4 於中斷機制下複驗 | 是（列為驗收條件） | Why 第 2 段 | Context 第 3 點 | judge-deadline「Deadline holds when the operation counter is disabled」 |
| C6 | op 計數只數 line 事件，把 K 次迴圈攤到同一 source line 可稀釋成本 | `probes/bench_counting_modes.mjs`：一般迴圈 3.000 事件/迭代、攤平 ×8 版 0.125 事件/迭代 → **稀釋 24.0 倍** | 是（列為驗收條件） | Why 第 2 段 | Context 第 3 點 | judge-deadline「Deadline holds when operation cost is diluted by source layout」 |
| C7 | `judge.rs` 的 `judge()` **已有** TLE 分支，由 worker 傳的 `timed_out: Option<bool>` 驅動 | `testcase-generator/src/judge.rs` 的 `VerdictResult` 與 `timed_out.unwrap_or(false)` 分支 | 否 | Impact（BACKLOG 修訂） | Implementation Contract／介面 | judge-deadline「Production judging receives the deadline verdict」 |
| C7b | **`BACKLOG.md` §2.8 在 C7 這點上已過期**——該節仍記載「`judge()` 沒有 TLE 分支，正式站永遠不會出現 TLE」。同節「`sys.settrace(None)` 為接受的繞過」亦將因本 change 失效 | `openspec/BACKLOG.md` §2.8 與 C7 的原始碼對照 | 否 | Impact（Modified：BACKLOG） | — | tasks 5.2 |

---

## M 表：機制候選的量測比較（D1／D3 的依據）

計數器路線（**全部否決**，保留於此以免後續 change 重跑同樣的死路）：

| ID | 候選 | 攤平稀釋倍率 | 成本單位膨脹 | 執行時間 | 否決理由 | 證據 |
|----|------|--------------|--------------|----------|----------|------|
| M1 | `sys.settrace` line（現況） | 24.0× | 1×（基準） | 126 ms | 就是缺陷本身 | `probes/bench_counting_modes.mjs` |
| M2 | `sys.monitoring` BRANCH | 24.0×（無改善） | — | 70 ms | 「同行攤平」本質是 loop unrolling，真的消掉迴圈回邊，分支事件同樣被稀釋 | 同上 |
| M3 | `sys.monitoring` LINE | ~100,000×（更糟） | — | 36 ms | 停留同一行時不重複觸發（攤平版全場僅 6 個事件） | 同上 |
| M4 | `sys.monitoring` INSTRUCTION | 1.43× | 5× | 529 ms（**4.2 倍慢**） | 可行但改變成本單位 → 作廢全站 8 道 op 斷崖題的既有校準 | 同上 |
| M5 | `settrace` ＋ 逐行指令加權 | 1.66× | 6×（**非均勻**：一般迴圈 6×、genexpr 18×） | 400 ms | 同 M4 的校準問題，且對 comprehension／generator 系統性超收 | `probes/bench_weighted_settrace.mjs` |

**結論（記為 M6）**：兩條 op 繞道（C5／C6）繞得過**計數器**，繞不過**時鐘**。因此本 change 不動計數器，改補時間軸。此結論是 D1 的直接依據。

---

## P 表：中斷機制的量測（D1／D2／D3／D4 的依據）

| ID | 事實 | 數值 | 證據 | 需瀏覽器覆核 |
|----|------|------|------|--------------|
| P1 | Pyodide 0.29.3 帶 CPython 3.13.2，`setInterruptBuffer` 存在 | `typeof py.setInterruptBuffer === 'function'` | `probes/probe_monitoring_availability.mjs`、`probes/probe_watchdog_interrupt.mjs` | 否 |
| P2 | 獨立執行緒在期限寫入中斷值可準時中斷同步 Python | 預算 3,000 ms → 實測 3,001–3,004 ms（誤差 ≤ 4 ms） | `probes/probe_watchdog_interrupt.mjs` | **是** |
| P3 | 誠實快解不受影響 | 同一基準解 218–228 ms 正常回傳 | 同上 | 是 |
| P4 | `sys.settrace(None)` 繞道被中斷 | 3,002 ms 拋出 | 同上 | **是** |
| P5 | 同行攤平繞道被中斷 | 3,002 ms 拋出 | 同上 | **是** |
| P6 | 中斷後 runtime 存活且無效能劣化 | 中斷後立即 1 ms 完成一次 `sum(range(1000))`；再跑基準解 223–225 ms | 同上 | **是** |
| P7 | 學生層級的例外處理無法吞掉中斷 | `except:`／`except KeyboardInterrupt:`／`except BaseException:`／外層 for 重試四種寫法皆於 3,002–3,004 ms 拋出，例外型別為 `KeyboardInterrupt`，一路穿到 JS | `probes/probe_interrupt_swallow.mjs` | **是**（D2 第二層即為此結論不成立時的防線） |
| P8 | `runPythonAsync` 路徑的中斷例外會逃出呼叫端 try/catch | 例外自 Pyodide 內部 `Immediate.wrapper` 冒出成為未捕捉例外並終結行程；改同步 `runPython` 後落在 try/catch 內 | `probes/probe_watchdog_interrupt.mjs`（非同步版）與 `probes/probe_interrupt_swallow.mjs`（同步版）對照 | 否（機制性） |
| P9 | 中斷旗標若在呼叫前就設定，會落在 Pyodide 自身 asyncio 機制內並使 runtime 進入不可用狀態 | 實測 3 ms 即拋出，堆疊指向 `asyncio/tasks.py` 的 `ensure_future`；該次之後同一 runtime 的後續 trial 無法完成 | 早期探針（結論已落入 D4，腳本未保留：其行為由 `probes/probe_watchdog_interrupt.mjs` 的世代編號協定反向覆蓋） | 否 |
| P10 | 中斷後旗標由 Pyodide 清零 | 每次 trial 結束讀取緩衝區皆為 0 | `probes/probe_interrupt_swallow.mjs` 的「事後旗標」欄 | 否 |

**P9 的證據狀態**：這是本矩陣中**唯一沒有可重跑腳本**的事實。它來自一支已被後續版本取代的探針。處置：D4 的協定（只在使用者程式碼期間武裝）使該情境不再可能發生，而 tasks 1.1 要求為「世代編號使過期到期失效」寫測試——若 P9 的結論不成立，該測試不會失敗，因此**P9 目前是一條未被驗收出口覆蓋的事實**。稽核時應視為待補證據。

---

## E 表：部署前提（D6 的依據）

| ID | 事實 | 證據 | 需瀏覽器覆核 |
|----|------|------|--------------|
| E1 | `SharedArrayBuffer` 需要 `COOP: same-origin` ＋ `COEP: require-corp` | Web 平台既有規範 | 否 |
| E2 | ~~dev server 已送出這兩個標頭~~ **此事實為偽，已於 apply 期推翻**。`.vitepress/config.mts` 確實宣告了 `vite.server.headers`，但 VitePress 2.0.0-alpha.16 不轉發該設定 | 實測 `curl -s -D - -o /dev/null http://localhost:5173/` → 兩個標頭皆不存在。宣告自 Pyodide 整合以來一直無效而未被察覺，因為 Pyodide 本身不需要 SharedArrayBuffer | 否（已實測） |
| E2b | dev 的跨來源隔離改由 `configureServer`／`configurePreviewServer` middleware 外掛提供 | 修正後實測同一指令 → `Cross-Origin-Opener-Policy: same-origin`、`Cross-Origin-Embedder-Policy: require-corp` 皆存在 | 否（已實測） |
| E3 | 生產部署沒有 `_headers` 檔 | `git ls-files` 無任何 `_headers`；`docs/public/_redirects` 為建置產生且被 gitignore | 否 |
| E4 | Pyodide 與 WASM 皆為同源自架資源（`COEP: require-corp` 的主要風險面） | `pyodide.worker.ts` 的 `PYODIDE_CDN = '/pyodide/'`；`docs/public/pyodide/`、`docs/public/wasm/` | **是**（staging 逐頁確認） |
| E5 | 生產環境的 `_headers` 可為靜態追蹤檔，不需產生腳本（內容不依賴任何題目資料） | 對照 `scripts/generate-redirects.ts`——別名需由題目檔派生，標頭不需要 | 否 |

---

## R 表：需求 → 任務 → 驗收出口

| spec 需求 | 依據事實 | 任務 | 驗收出口 |
|---|---|---|---|
| Every judged testcase has an enforced wall-clock deadline | C1、C2、M6 | 1.2–1.5、2.3 | 5.1 瀏覽器逐條 |
| The deadline is enforced by an interrupt buffer armed per testcase | P1、P2、P6、P9 | 1.1、1.2、2.2 | 1.1 單元測試 ＋ 5.1 連續中斷情境 |
| Student code cannot suppress the deadline verdict | P7 | 2.3、5.1 | 5.1 |
| Judging degrades rather than fails without SharedArrayBuffer | E1、E3 | 2.1、2.4 | 2.1 單元測試 |
| Production judging receives the deadline verdict | C2、C7 | 1.4、5.1 | 5.1 staging 生產路徑 |
| The deadline constant is derived from measurement of shipped challenges | 待量測（O1–O3） | 4.1–4.5 | 4.5 常數與 design 數字一致 |
| Interrupted batches are displayed honestly | C4 | 3.1、5.1 | 3.1 元件測試 |
| Execute Composable Method | C3 | 1.5、2.2 | 既有 `useExecutor.spec.ts` ＋ 新逾時情境 |
| Sandbox guard is injected before user code in every execution | P8 | 1.3–1.5 | 既有 sandbox 測試維持全綠 |
| Bypass acceptance after hunt downgrade | 待量測（O4） | 4.4 | 逐筆數字寫入 design |

---

## O 表：待量測（釘定常數前必須有值）

| ID | 待量測項目 | 由誰產出 | 為什麼阻擋 |
|----|------------|----------|------------|
| O1 | 兩條繞道路線在**瀏覽器**的單筆牆鐘 | tasks 4.2 | deadline 必須小於此值，否則擋不住 |
| O2 | 全站既有題目 `reference_solution` 的單筆最大牆鐘 | tasks 4.3 | deadline 必須大於此值乘安全倍率，否則誤殺線上題目 |
| O3 | 各題已收編路線的單筆最大牆鐘 | tasks 4.3 | 同 O2；收編路線依契約必須維持原得分 |
| O4 | gem-blast 的 `str.replace` 繞道逐筆牆鐘 | tasks 4.4 | 該題 spec 修訂條文明文要求記錄；歷史記錄顯示它曾在單筆達 6,984 ms，很可能落在 deadline 兩側的臨界 |

**若 O1 的下界低於 O2／O3 的上界乘安全倍率，則不存在可用常數**——D5 已規定此時記錄衝突並保留舊行為，不得選一個會改變既有題目判定的值。
