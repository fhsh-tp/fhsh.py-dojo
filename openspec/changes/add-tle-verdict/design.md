## Context

Change 1《fix-op-counter-blind-spot》後,op-counter 對扁平學生碼已生效,但正式站 verdict 映射(`testcase-generator/src/judge.rs` 的 `judge()`)只有 AC/WA/RE:超限的 TimeoutError 落入 `error` 欄位被判 RE。dev 模式 `run` handler(`pyodide.worker.ts`)早已依錯誤訊息特徵分類出 TLE。UI 的 TLE 黃色徽章與 x-mark 樣式(`TestResultPanel.vue`)已存在。資料流:worker `run_only` → `useChallengeRunner.runStudentCode` 收集結果 → `wasm.judge`(Rust)→ verdict 陣列 → executorStore。

## Goals / Non-Goals

**Goals:**

- 正式站對 op-limit 超限測資輸出 `TLE` verdict,與 dev 模式一致;`error` 置空不洩漏 op 上限。
- 資料介面向後相容:舊格式(無 `timed_out`)行為完全不變。
- 規格先行:先補 `wasm-pool-judge` TLE Scenario(缺口根因是 prose 無驗收場景)。

**Non-Goals:**

- 不改 op 上限、不加 per-case wall-clock、不動外層 N×6s 總預算與其 resolve(null) 行為。
- 不動 dev `run` handler 的 wall-clock 旁路與訊息協定(其 catch 分類改用與 prod 相同的 op-count 探測,見 D1);不做計分面。

## Decisions

### D1:超時分類做在 worker 端,以 op counter 探測、非字串比對(audit R1 修訂)

`handleRunOnly` 與 dev `run` handler 的 catch 皆改以 `opLimitExceeded(opLimit)` 分類:探測剛失敗那次執行殘留在 globals 的 `_op_count`,`count > limit` 才是 guard 拋出的超時。**不比對錯誤訊息文字**——學生自拋 `TimeoutError`(其 count 必然 ≤ limit,否則 guard 早就先拋)維持一般 RE 且保留原訊息,無法偽造 TLE(把 `_op_count` 改成超限值屬蓄意自毀,與 `sys.settrace(None)` 同威脅類別,接受)。超時時 `testcase_result` 帶 `timed_out: true` 且不傳 `error`。judge.rs 只讀結構化欄位。

替代方案(駁回):(a) judge.rs 對 error 字串比對——Rust 端耦合 Python 錯誤文字;(b) worker 端字串特徵比對(初版做法,audit R1 駁回)——學生自拋含 "TimeoutError" 字樣的例外會被誤判 TLE 且錯誤被吞,在正式計分路徑是行為劣化;(c) wrapper 內設 `_timed_out` 旗標——TimeoutError 拋出時 teardown 跑不到,旗標寫不進去;(d) 在 useChallengeRunner 分類——分類點離錯誤來源最遠。worker 是錯誤的第一手接收者且能直接讀 interpreter 狀態,是唯一正確位置。

### D2:StudentResult 以 Option<bool> + serde(default) 向後相容(audit R1 修訂)

`StudentResult` 增 `#[serde(default)] pub timed_out: Option<bool>`,判定用 `unwrap_or(false)`。**必須是 Option 而非裸 bool**:serde-wasm-bindgen 只把「物件完全沒有該 key」視為缺席;JS 物件字面量寫 `timed_out: msg.timed_out` 會產生「key 存在、值 undefined」,裸 bool 的 `deserialize_bool` 對 undefined 直接拋 invalid type、毒殺整批(audit R1 以真 wasm 產物實證);`deserialize_option` 則把 nullish 映為 None。雙層防禦:JS 收集端也只在值為 true 時附加該 key。不 bump 任何協定版本。

### D3:verdict 判定優先序 timed_out → error → 比對

`timed_out == true` → `TLE`(`error` 輸出 None,即使輸入帶有 error 也不外洩——超時的錯誤訊息含 op 上限數值,比照 dev handler 隱藏);否則 `error.is_some()` → `RE`(保留訊息);否則 constant-time 比對 → AC/WA。`actual`/`expected` 欄位的 verdict_detail 剝除規則不變(TLE 走與 RE 相同的 stdout 附帶規則——`actual` 依 verdict_detail 決定,超時時 stdout 為空字串,無資訊量)。

### D4:測試策略 — Rust 單元測試先行(TDD),worker/前端以既有 mock 模式補

judge.rs 新增測試:TLE 判定、TLE error 置空、`timed_out` 缺席時舊行為不變(向後相容)、timed_out 與 error 並存時 TLE 優先。cargo test 需先 `pnpm gen:keymaterial`(建置順序既定)。worker 端:`pyodide-worker-run-only.spec.ts` 補 timed_out 型別契約與分類行為(mock pyodide 驅動,比照 trace-reset 佈線測試模式);前端:`useChallengeRunner-prod.spec.ts` 斷言 judge 收到的結果陣列含 timed_out。

### D5:真 wasm 邊界整合測試(audit R1 新增)

Rust 單元測試建原生 struct、前端測試 mock WASM 模組——兩者都跨不過 serde_wasm_bindgen 這一層,而 critical 缺陷恰好就住在這層。新增 `scripts/judge-wasm-boundary.test.ts`:載入真 wasm-pack 產物 + 真加密池(hello-world.bin),以前端實際可能產生的物件形狀(含顯式 `timed_out: undefined` key)呼叫 `judge`,斷言整批不炸、TLE/RE/WA 各就各位。比照 challenge-params 慣例不設 skip guard(建置順序保證產物存在)。

## Implementation Contract

**行為契約:**

1. 正式站池判題:某測資執行失敗且 interpreter 的 `_op_count` 超過該次 op 上限(guard 拋出的超時)時,該筆 verdict 為 `TLE`,`error` 欄位不存在(undefined/None),UI 顯示黃色 TLE 徽章。
2. 一般錯誤(op count 未超限,含學生自拋的 TimeoutError)verdict 仍為 `RE` 且保留 `error` 訊息;AC/WA 判定與現行 byte-identical;dev 與 prod 分類一致。
3. `wasm.judge` 收到「不含 `timed_out` key」或「key 存在但值為 undefined/null」的結果陣列時,輸出皆與 Change 1 之前的行為完全一致(向後相容 + 不毒批)。
4. `timed_out: true` 與 `error` 並存時,TLE 優先且 error 不外洩。

**介面形狀:**

- worker `testcase_result`(run_only):具名型別 `RunOnlyTestcaseResult = {type, index, stdout, elapsed_ms, error?, timed_out?: boolean}`,postMessage 以 satisfies 收斂;timed_out 僅超時時為 true。
- 前端收集端:只在 `timed_out === true` 時附加該 key(顯式 undefined key 對 serde-wasm-bindgen 不等於缺席)。
- Rust `StudentResult`:`{stdout: String, error: Option<String>, elapsed_ms: f64, timed_out: Option<bool>(#[serde(default)],判定 unwrap_or(false))}`。
- `VerdictResult.verdict` 值域實際可達 `AC | WA | TLE | RE`。

**失敗模式:**

- 超時測資的 stdout 為空字串(執行中斷,無捕捉輸出);verdict_detail 為 actual/full 時 `actual` 為空字串,無資訊洩漏。
- 外層 N×6s 總預算強殺仍是整批 `resolve(null)`(不經 judge),與本 change 無交互。

**驗收判準:**

- cargo 單元測試:TLE 判定 / error 置空 / 向後相容 / 並存優先序 4 案例綠(CI verify 執行;本機 cargo test 前置 pnpm gen:keymaterial)。
- 真 wasm 邊界測試 `scripts/judge-wasm-boundary.test.ts`:顯式 undefined key 不毒批、TLE/RE/WA 各就各位(真 wasm-pack 產物 + 真加密池)。
- `pyodide-worker-run-only.spec.ts`(含學生自拋 TimeoutError → RE 案例)與 `useChallengeRunner-prod.spec.ts` 全綠;`pnpm test --run` 全套綠。
- 生產建置 e2e(PR 前):扁平超量迴圈解在正式池判題路徑得 TLE 徽章;正解 AC 不受影響;全 TLE 批次的 run_complete 須早於外層總預算送達(實測 wall-time,含 worker 冷啟 loadPyodide 成本)。

**範圍邊界:**

- In scope:judge.rs、pyodide.worker.ts 的 handleRunOnly 與 dev `run` handler 的 catch 分類、useChallengeRunner.ts 的 runStudentCode 結果收集、上述測試檔、wasm-pool-judge 與 python-generator delta specs。
- Out of scope:TestResultPanel.vue、executorStore、op 上限數值、外層 kill 預算、dev `run` handler 的 wall-clock 旁路、計分面。

## Risks / Trade-offs

- [學生操縱 `_op_count` 偽造/逃避 TLE] → 探測式分類依賴 wrapper 的 `_op_count` 全域;學生可 `_op_count = 10**9`(下一行事件即觸發 guard,判 TLE——他自己招的)或 `del _op_count`/歸零(慢解逃 TLE,結局撞外層總預算的靜默失敗)。皆屬蓄意自毀,與 `sys.settrace(None)` 同威脅類別,教學平台威脅模型下接受。
- [舊 pool/舊 session 相容] → timed_out 只存在於 worker→judge 的即時訊息,不進池、不進 session,無持久化相容問題;Option + serde(default) 覆蓋唯一的輸入面(缺席/undefined/null 全部映為未超時)。
- [TLE 與 wall-clock 總預算交互] → 全 TLE 情境:每筆在 op 上限(10M ops ≈ 3–5 秒/筆,dev 實測數字)觸發,N 筆合計可能逼近 N×6s 總預算;且 `runStudentCode` 每次提交新建 Worker、預算計時器先於 Worker 建立啟動,**Pyodide 冷啟(數秒)也吃同一份預算**——margin 比純 op 時間更薄(audit R1 指出,design 初版漏算)。每筆 TLE 是 worker 正常回訊(非卡死),但「run_complete 早於總預算」在真實瀏覽器的成立與否**必須由生產 e2e 實測**(驗收判準已列);若 margin 不足,處置是出題期下修 op 上限(handoff 既定方向),非本 change 內調 kill 預算。

## Migration Plan

單一 PR 內完成,無資料遷移、無協定版本 bump(serde default 向後相容)。回滾即恢復 RE 顯示,無資料損失。

## Open Questions

(無)
