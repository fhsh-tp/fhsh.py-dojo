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

計數器路線（**全部否決**，保留於此以免後續 change 重跑同樣的死路）。稀釋倍率＝同一段迴圈在「一般寫法」與「攤平 ×8 寫法」下的事件數比值，數字直接由 `probes/bench_counting_modes.mjs` 的輸出相除得出；重跑該探針即可核對本表每一格。

| ID | 候選 | 攤平稀釋倍率 | 成本單位膨脹 | 執行時間 | 否決理由 | 證據 |
|----|------|--------------|--------------|----------|----------|------|
| M1 | `sys.settrace` line（現況） | 24.0× | 1×（基準） | 126 ms | 就是缺陷本身 | `probes/bench_counting_modes.mjs` |
| M2 | `sys.monitoring` BRANCH | **8.0×**（200,002 ÷ 25,002；比 M1 好但仍被大幅稀釋） | — | 70 ms | 「同行攤平」本質是 loop unrolling，真的消掉迴圈回邊，分支事件同樣被稀釋 | 同上 |
| M3 | `sys.monitoring` LINE | 100,001×（600,007 ÷ 6；更糟） | — | 36 ms | 停留同一行時不重複觸發（攤平版全場僅 6 個事件） | 同上 |
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
| P5 | 同行攤平繞道被中斷 | 3,002 ms 拋出（node 探針）；**真 Pyodide 測試** `deadline-pyodide.spec.ts` 的「stops code that diluted its operation cost by flattening onto one line」逐次覆核 | 同上 | **未於瀏覽器覆核，且刻意不補**：要在瀏覽器示範需要一份「攤平到足以逃過 op 上限、又仍然慢」且**輸出正確**的解法；實測 gem-blast 的攤平版稀釋幅度不足，仍被 op 上限擋在 12/20，所以瀏覽器上看到的 TLE 來自計數器而非時鐘。與其編造一份不具代表性的解法，本矩陣以真 Pyodide 測試作為該事實的證據並在此標明差異 |
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
| E2b | 標頭的單一定義為 `docs/public/_headers`，由 Cloudflare 提供；`config.mts` 中已證實無效的宣告移除，不以 Vite middleware 複製一份 | 決策記錄於 design D6；本機驗證管道為 `pnpm preview:cf`（`wrangler pages dev` 服務建置輸出） | **是**（wrangler 下實測標頭與 `crossOriginIsolated`） |
| E2c | **接受的後果**：`vitepress dev` 無隔離 → 開發期無 `SharedArrayBuffer` → deadline 退化為事後裁決（仍生效、不即時），`deadline.ts` 每頁告警一次 | `deadline.ts` 的 `reportDegradation`；`config.mts` 註解 | 否 |
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

## O 表：量測結果（已完成，2026-08-11）

全部在 `pnpm preview:cf` 的生產路徑實測；重跑指令 `measure/sweep.sh`，逐筆原始資料 `measure/results.jsonl`。

| ID | 項目 | 實測值 | 對常數的作用 |
|----|------|--------|--------------|
| O1 | 計數器隱形繞道的單筆牆鐘 | `settrace(None)` 5,009 ms（被 deadline 截斷，真值 > 5 秒）；同行攤平由 op 上限擋下 | 下界 |
| O2 | 16 支 `reference_solution` 的單筆最大 | **376 ms**（`prize-order-code`），16 題全部維持滿分 | 上界（非拘束） |
| O3 | 收編路線的單筆最大 | **原記載「併入 O2 量測」為偽——收編路線當時一條都沒量。** 第一次補量**兩條都實作錯**（取最貴寫法），得到相反結論；以最便宜寫法重量的真值：`math.perm` ＋ Legendre（prize-order-code）**20/20、2,234 ms**；`str.replace`（gem-blast）**20/20、3,115 ms**；對照組 `math.factorial` 0/20（spec 要求它失敗） | **拘束上界 = 3,115 ms**；可行域非空 |
| O5 | `expression-eval-challenges` 四條收編路線 | 全部 20/20：E1 對調 eval 52 ms、R2 regex 括弧化 12 ms、N1 C 層重寫 57 ms、E3′ 冪次編碼 65 ms。路線檔已佚失、由 spec 名稱重新實作，先經 `measure/verify_routes.py` 對該題 20 筆 literal 驗明輸出等同 `reference_solution` 才量 | 不影響上界（100 ms 量級）；使 O3 的涵蓋範圍完整——六條收編路線全數量畢 |
| O4 | gem-blast 的 `str.replace` 繞道逐筆 | 最便宜寫法（只掃 `set(s)`）20/20、單筆最大 3,115 ms；最貴寫法（掃 26 字母）18/20、5,005 ms | 該題 spec 的接受條件**仍然成立**，條文改記真值 |

**結論**：`DEADLINE_MS = 5,000`。相對正解上界 376 ms 為 13.3 倍，但**實際受到約束的是收編上界 3,115 ms，餘裕僅 1.61 倍**。D5 所擔心的空集合未發生；兩份針對已上線題目的 spec 修訂中，`rank-code-challenges` 一份已撤銷（其主 spec 原本就正確），`gem-blast-challenge` 一份改記真值後保留（該題主 spec 明文要求本 change 修訂該條文）。

### 量測工具本身的缺陷與修正（記錄以免重蹈）

| 缺陷 | 症狀 | 修正 |
|------|------|------|
| `agent-browser eval` 的回傳被再包一層並跳脫 | shell 端比對 `"done":true` 永不命中；結果早已產生，輪詢卻空轉到逾時，症狀看起來像頁面掛住 | 比對改為容忍跳脫，解析交給 Python；並加自我測試 |
| DOM 選擇器未限定於結果面板 | 題目說明的 markdown 表格被當成測資列；`coupon-combo-quote` 誤報 20/24、單筆最大 66 ms（實為 20/20、47 ms） | 選擇器限定 `[data-testid="result-panel"]`，並加「抓到 0 列即明確失敗」守門 |
| 首版整合測試用 20 億次迴圈 | 中斷若失效需 250 秒才紅，等於掛住套件而非快速失敗 | 縮為 3,000 萬次，失敗代價降到數秒 |

第一輪受污染的資料保留於 `measure/results.contaminated.jsonl` 供對照；除 `coupon-combo-quote` 外，兩輪差異都在 ±7 ms 的執行抖動內。
