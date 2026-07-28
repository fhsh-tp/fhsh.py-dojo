## Context

判題與執行的共同 wrapper `buildWrappedCode`(位於 .vitepress/theme/workers/worker-utils.ts)在模組頂層呼叫 `sys.settrace(_tracer)` 作為 op-count TLE 防線。CPython 的 `settrace` 只掛上「之後新建的 frame」,不會回溯掛上當下 frame;學生的扁平頂層程式碼恰在同一個模組 frame 內執行,因此 op_count 恆 0。四個 handler(`run`、`run_only`、`execute`、`generate`,位於 .vitepress/theme/workers/pyodide.worker.ts)全部共用此 wrapper。

現有 worker 測試(worker-utils.spec.ts 與 pyodide-worker-*.spec.ts)全是字串/型別斷言,零 Python 執行——這是缺陷潛伏 4 個月的根因。建置端 python3 已是既有相依(content-regression、build:pools 同款 preflight)。

## Goals / Non-Goals

**Goals:**

- 扁平頂層學生程式碼的 op-count 計數生效:超限時 dev 顯示 TLE、prod 回傳含 "Operation limit exceeded" 的 error(顯示為 RE),不再靜默零筆結果。
- generator 路徑(`generate` handler)豁免 op 計數,避免修復誤殺出題者的高運算量 generator。
- 建立「真正執行 Python」的整合測試,守住 wrapper 的執行語意(而非字串形狀)。
- 全題庫回歸全綠(既有測試 + content-regression)。

**Non-Goals:**

- 不改 judge.rs 的 verdict 映射(正式站 TLE 徽章屬後續 change《add-tle-verdict》)。
- 不動外層 N×6 秒總預算 kill 機制與 dev wall-clock 旁路。
- 不防學生 `sys.settrace(None)` 主動關閉(接受,記 BACKLOG)。
- 不解決 C 內建(`sorted`/`list.pop(0)`)不產生行事件的本質限制。

## Decisions

### D1:修復方式 — settrace 後補掛當下 frame

`sys.settrace(_tracer)` 之後補 `sys._getframe().f_trace = _tracer`。已於本機 CPython 3.13 與 repo 內建 Pyodide 0.29 雙重實測:扁平雙重迴圈 n=2500 從 op_count=0 變為正確拋 TimeoutError;tracer 拋例外時 CPython 自動解除 tracing,不洩漏到下一筆。

替代方案(駁回):(a) 把學生碼包進函式再呼叫——會改變學生程式的作用域語意(頂層變數變區域變數、`global` 行為改變),對教學平台是不可接受的語意破壞;(b) 改用 wall-clock per-case——依賴硬體速度,且無法在 Worker 內中斷同步執行的 Python。

### D2:generator 豁免機制 — opLimit 傳 null 時整段不注入 tracer

`buildWrappedCode(userCode, input, opLimit)` 的 `opLimit` 型別從 `number` 放寬為 `number | null`;`null` 時 wrapper **完全不注入** op-counter 區塊(含 teardown 的 `sys.settrace(None)` 一併省略,但保留 sandbox guard 與 stdin/stdout 區塊)。`handleGenerate` 呼叫時傳 `null`。

替代方案(駁回):(a) 給 generator 獨立高上限(如 100M)——仍是魔術數字,未來高運算 generator 依然可能誤殺,且 generator 是出題者可信碼、根本不需要防線;(b) 另立 `buildGeneratorCode` 函式——與現有 wrapper 大量重複,增加維護面。

`run`、`run_only`、`execute` 三個 handler 維持現行 `DEFAULT_OP_LIMIT = 10_000_000` 不變。

### D3:整合測試執行載體 — 系統 python3 子行程

新測試檔 worker-utils-python.spec.ts 以 `execFileSync('python3', ['-c', wrapped])` 直接執行 `buildWrappedCode` 的產出。理由:wrapper 產出是純標準庫 Python(sys/io),CPython 與 Pyodide 對「settrace + f_trace 的 frame 語意」行為一致(RCA 已雙重實測);python3 已是專案既有相依,沿用 content-regression 的 preflight-skip 模式(python3 缺席時 skip,CI 保證存在)。

替代方案(駁回):在 vitest 內載入 Pyodide npm——新增重依賴、首載數十秒拖慢單元測試,收益僅是把已人工雙重驗證過的「CPython≈Pyodide 等價性」自動化。

取出 `_output` 的方式:測試 harness 在 wrapped code 後附加 `import sys as _t; _t.__stdout__.write(_output)`,由子行程 stdout 讀回;超限案例斷言子行程失敗且 stderr 含 "Operation limit exceeded"。

### D4:op 上限與門檻數字不動

10M ops/筆的預設上限維持不變。修復後全部學生碼(含扁平)開始付 tracing 成本,正常解(教學解 ~108k ops)毫無壓力;門檻調整屬出題期決策(deque 題的 band 值域),不在本 change。

### D5:跨測資 trace 殘留 — JS 側解毒劑,置於 globals.clear() 之前(audit R1 新增)

wrapper 的 `sys.settrace(None)` teardown 物理上寫在 user code 之後,一般例外(常態 RE)會跳過它;殘留 tracer 的 `__globals__` 在 `globals.clear()` 後被清空,下一次執行的第一個 'call' 事件即拋 `NameError` 毒殺正確測資(毒發一筆後因 tracer 拋例外自動解除而自癒)。真 Pyodide 0.29 實測:RE/AC 交錯 6 筆,成績 3/6 → 0/6。

修法:worker 新增 `resetTraceState()`(執行 `import sys; sys.settrace(None)`,try/catch 包覆),4 個 handler 在每次執行前、`globals.clear()` **之前**呼叫。順序關鍵:clear 之前舊 tracer 的 `_op_count` 尚在,解毒劑本身不會被毒到(不依賴「tracer 拋例外自動解除」的間接保證);實測成本 0.29ms/次,最壞情況(解毒失效)行為退回現況、不會更糟。

替代方案(駁回):(a) 把 user code 縮排包進 try/finally——會破壞使用者多行字串的內容(縮排改變字串值),語意不可接受;(b) Python 側 prologue 解毒——毒在 frame 建立的 'call' 事件就爆,prologue 第一行都跑不到,實測證死;(c) tracer 狀態改 default-arg 閉包——殘留 tracer 會把計數帶進下一筆,把硬性 RE 換成更難察覺的偽 TLE。

此缺陷為既有(修復前後 settrace/teardown 位置相同,pre-fix wrapper 逐字重現同樣污染),非本次修復引入;本次修復讓 `handleGenerate` 改豁免反而少一個毒源。

## Implementation Contract

**行為契約:**

1. 扁平頂層 Python 碼(無函式定義)執行行數超過 opLimit 時,wrapper 拋出 `TimeoutError("Operation limit exceeded (N ops)")`——與函式包裝碼行為一致。
2. `opLimit` 為 `null` 時,wrapper 產出不含 `sys.settrace` 呼叫與 `_tracer` 定義,執行不受 op 上限約束;sandbox guard 與 stdin/stdout 捕捉行為不變。
3. `handleGenerate` 對 generator 碼一律以豁免模式(`opLimit: null`)執行;`run`/`run_only`/`execute` 維持預設 10,000,000。
4. 正常(未超限)程式碼的 `_output` 內容不受 tracer 影響——以「同一程式碼在 guarded(number)與 exempt(null)兩種模式下輸出 byte-identical」的對照測試坐實(tracer 只計數/拋例外,不觸碰 stdout)。
5. 任一測資拋一般例外後,同一 worker 內下一次執行不受殘留 tracer 影響:4 個 handler 每次執行前先 `resetTraceState()`(在 `globals.clear()` 之前),errored → 下一筆正確碼仍得正確輸出。

**介面形狀:**

- `buildWrappedCode(userCode: string, input: string, opLimit: number | null): string`——既有呼叫端傳 number 者行為完全不變。

**失敗模式:**

- 超限:`TimeoutError` 例外由各 handler 的既有 catch 捕捉——dev `run` 判為 TLE(既有字串偵測邏輯);`run_only`/`execute` 回傳 `error` 欄位含訊息(prod 端顯示 RE,屬既知現況,本 change 不改)。
- python3 缺席環境:整合測試 skip(比照 content-regression),但測試檔內「wrapper 形狀」類斷言照常執行。

**驗收判準:**

- 新整合測試至少涵蓋:(i) 扁平頂層超量迴圈 → 子行程失敗且 stderr 含 "Operation limit exceeded";(ii) 扁平頂層正常碼 → _output 正確、無錯誤;(iii) 函式包裝碼行為與修復前一致(超限觸發);(iv) `opLimit: null` → 超量迴圈也正常跑完不觸發。
- `pnpm test --run` 全綠(含全題庫 content-regression 與 challenge-params 冒煙)。
- `pnpm build:pools` 正常完成(建置端走原生 python3,不經 wrapper,應零影響——跑一次以證明)。

**範圍邊界:**

- In scope:worker-utils.ts 的 wrapper 產出、pyodide.worker.ts 的 handleGenerate 呼叫參數、新整合測試檔。
- Out of scope:judge.rs、useChallengeRunner.ts、外層 kill 預算、UI、任何題目內容檔。

## Risks / Trade-offs

- [tracing 讓所有學生碼變慢] → 行事件 tracer 對 CPython 有 2–4 倍常數開銷;正常解 op 量級 ~10^5,絕對耗時仍在毫秒級,可接受。10M 上限的 wall-time 上界(3–5 秒/筆)不變,因為既往量測本就是 traced(函式包裝)情境。實機佐證:smallest-prime-factor(題庫中 N 上限最大者)dev 模式單筆最重 339ms,距 5 秒 wall-clock 旁路仍有 10 倍餘裕。
- [學生主動 `import sys; sys.settrace(None)` 關閉計數] → op-counter 是防意外無限迴圈的防線,不是防蓄意繞過的沙盒;繞過者的結局是撞外層 wall-clock/總預算。教學平台威脅模型下接受,已記入 BACKLOG 已知限制。
- [CPython 與 Pyodide 行為差異] → 測試用 python3 執行,理論上與瀏覽器 Pyodide 有落差;RCA 已對兩者雙重實測 frame 語意一致,且 e2e(PR 前)會在真 Pyodide 上驗證。
- [generator 豁免後,出題者寫出無限迴圈 generator] → dev 模式會掛在 worker 內直到外層逾時;generator 是可信碼、建置期同樣無限制,風險與現況(盲區實質不設限)持平,未惡化。
- [修復後某些既有題的正解 op 量上升觸限] → 全題庫 content-regression + 手動 dev 冒煙守門;正解量級(10^5)距 10M 有兩個數量級餘裕。

## Migration Plan

單一 PR 內完成,無資料遷移。部署後即刻生效於所有題目;若發生誤殺(正常解被判 TLE),回滾即恢復原行為(缺點只是回到盲區現況,無資料損失)。

## Open Questions

(無——技術方案已經 RCA 實測驗證,唯一的下游決策「TLE verdict 顯示」已明確劃給後續 change。)
