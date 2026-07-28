## Context

Change 1《fix-op-counter-blind-spot》後,op-counter 對扁平學生碼已生效,但正式站 verdict 映射(`testcase-generator/src/judge.rs` 的 `judge()`)只有 AC/WA/RE:超限的 TimeoutError 落入 `error` 欄位被判 RE。dev 模式 `run` handler(`pyodide.worker.ts`)早已依錯誤訊息特徵分類出 TLE。UI 的 TLE 黃色徽章與 x-mark 樣式(`TestResultPanel.vue`)已存在。資料流:worker `run_only` → `useChallengeRunner.runStudentCode` 收集結果 → `wasm.judge`(Rust)→ verdict 陣列 → executorStore。

## Goals / Non-Goals

**Goals:**

- 正式站對 op-limit 超限測資輸出 `TLE` verdict,與 dev 模式一致;`error` 置空不洩漏 op 上限。
- 資料介面向後相容:舊格式(無 `timed_out`)行為完全不變。
- 規格先行:先補 `wasm-pool-judge` TLE Scenario(缺口根因是 prose 無驗收場景)。

**Non-Goals:**

- 不改 op 上限、不加 per-case wall-clock、不動外層 N×6s 總預算與其 resolve(null) 行為。
- 不改 dev `run` handler 既有 TLE 邏輯;不做計分面。

## Decisions

### D1:超時分類做在 worker 端,judge.rs 只讀結構化欄位

`handleRunOnly` 的 catch 沿用 dev `run` handler 既有特徵(errMsg 含 TimeoutError 或 Operation limit)分類,`testcase_result` 增 `timed_out: boolean`;超時時不傳 `error`。judge.rs 只依 `timed_out` 布林值判 TLE,**不做任何字串比對**。

替代方案(駁回):(a) judge.rs 對 error 字串比對——Rust 端耦合 Python 錯誤文字,且錯誤訊息本就不該送進 judge;(b) wrapper 內設 `_timed_out` 旗標——TimeoutError 拋出時 teardown 跑不到,旗標寫不進去(Change 1 已證實 teardown 在例外路徑不執行);(c) 在 useChallengeRunner 分類——分類點離錯誤來源最遠,且 dev/prod 會出現兩份重複邏輯。worker 是錯誤的第一手接收者、dev handler 已有同款邏輯,是唯一不增加重複的位置。

### D2:StudentResult 以 #[serde(default)] 向後相容

`StudentResult` 增 `#[serde(default)] pub timed_out: bool`。舊呼叫端(或快取的舊 worker 訊息)未帶欄位時 deserialize 為 false,verdict 判定與現行完全一致。不 bump 任何協定版本。

### D3:verdict 判定優先序 timed_out → error → 比對

`timed_out == true` → `TLE`(`error` 輸出 None,即使輸入帶有 error 也不外洩——超時的錯誤訊息含 op 上限數值,比照 dev handler 隱藏);否則 `error.is_some()` → `RE`(保留訊息);否則 constant-time 比對 → AC/WA。`actual`/`expected` 欄位的 verdict_detail 剝除規則不變(TLE 走與 RE 相同的 stdout 附帶規則——`actual` 依 verdict_detail 決定,超時時 stdout 為空字串,無資訊量)。

### D4:測試策略 — Rust 單元測試先行(TDD),worker/前端以既有 mock 模式補

judge.rs 新增測試:TLE 判定、TLE error 置空、`timed_out` 缺席時舊行為不變(向後相容)、timed_out 與 error 並存時 TLE 優先。cargo test 需先 `pnpm gen:keymaterial`(建置順序既定)。worker 端:`pyodide-worker-run-only.spec.ts` 補 timed_out 型別契約與分類行為(mock pyodide 驅動,比照 trace-reset 佈線測試模式);前端:`useChallengeRunner-prod.spec.ts` 斷言 judge 收到的結果陣列含 timed_out。

## Implementation Contract

**行為契約:**

1. 正式站池判題:某測資執行拋出含 "TimeoutError"/"Operation limit" 特徵的錯誤時,該筆 verdict 為 `TLE`,`error` 欄位不存在(undefined/None),UI 顯示黃色 TLE 徽章。
2. 一般錯誤(不含超時特徵)verdict 仍為 `RE` 且保留 `error` 訊息;AC/WA 判定與現行 byte-identical。
3. `wasm.judge` 收到不含 `timed_out` 欄位的結果陣列時,輸出與 Change 1 之前的行為完全一致(向後相容)。
4. `timed_out: true` 與 `error` 並存時,TLE 優先且 error 不外洩。

**介面形狀:**

- worker `testcase_result`(run_only):`{type, index, stdout, elapsed_ms, error?, timed_out?: boolean}`(timed_out 僅超時時為 true;非超時可缺席)。
- Rust `StudentResult`:`{stdout: String, error: Option<String>, elapsed_ms: f64, timed_out: bool(#[serde(default)])}`。
- `VerdictResult.verdict` 值域實際可達 `AC | WA | TLE | RE`。

**失敗模式:**

- 超時測資的 stdout 為空字串(執行中斷,無捕捉輸出);verdict_detail 為 actual/full 時 `actual` 為空字串,無資訊洩漏。
- 外層 N×6s 總預算強殺仍是整批 `resolve(null)`(不經 judge),與本 change 無交互。

**驗收判準:**

- cargo 單元測試:TLE 判定 / error 置空 / 向後相容 / 並存優先序 4 案例綠(CI verify 執行;本機 cargo test 前置 pnpm gen:keymaterial)。
- `pyodide-worker-run-only.spec.ts` 與 `useChallengeRunner-prod.spec.ts` 更新後全綠;`pnpm test --run` 全套綠。
- 生產建置 e2e(PR 前):扁平超量迴圈解在正式池判題路徑得 TLE 徽章;正解 AC 不受影響。

**範圍邊界:**

- In scope:judge.rs、pyodide.worker.ts 的 handleRunOnly、useChallengeRunner.ts 的 runStudentCode 結果收集、上述測試檔、wasm-pool-judge 與 python-generator delta specs。
- Out of scope:dev `run` handler、TestResultPanel.vue、executorStore、op 上限數值、外層 kill 預算、計分面。

## Risks / Trade-offs

- [worker 分類仍是字串特徵比對] → 特徵字串("Operation limit exceeded")是 Change 1 wrapper 自產的訊息,與 dev handler 共用同一組特徵;若未來改 wrapper 訊息文字,dev 與 prod 兩處分類同步失效、e2e 會抓到。集中到 worker 單點已是不增加新耦合的最小面。
- [舊 pool/舊 session 相容] → timed_out 只存在於 worker→judge 的即時訊息,不進池、不進 session,無持久化相容問題;serde(default) 覆蓋唯一的輸入面。
- [TLE 與 wall-clock 總預算交互] → 全 TLE 情境:每筆在 op 上限(10M ops ≈ 3–5 秒/筆)觸發,N 筆合計可能逼近 N×6s 總預算;但每筆 TLE 是 worker 正常回訊(非卡死),run_complete 會在總預算前送達——由生產 e2e 實測驗證,若逼近再於出題期(deque 題 band 值域)調整,非本 change 範圍。

## Migration Plan

單一 PR 內完成,無資料遷移、無協定版本 bump(serde default 向後相容)。回滾即恢復 RE 顯示,無資料損失。

## Open Questions

(無)
