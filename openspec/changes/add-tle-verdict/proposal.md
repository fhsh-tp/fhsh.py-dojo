## Problem

正式站判題永遠不會出現 TLE 徽章:`testcase-generator/src/judge.rs` 的 `judge()` verdict 映射只有 AC/WA/RE 三種輸出。Change 1《fix-op-counter-blind-spot》修復後,op-counter 對扁平學生碼已生效,但超限的 `TimeoutError` 走 `error` 欄位 → judge 判為 **RE**(錯誤訊息含 "Operation limit exceeded")。dev 模式的 `run` handler 早就會顯示 TLE,正式站與 dev 行為不一致;對學生而言「太慢」與「程式錯誤」是完全不同的教學訊號。

## Root Cause

`wasm-pool-judge/spec.md` 的 verdict 枚舉 prose 有列 `TLE`,但**沒有任何 TLE 驗收 Scenario**——實作照 Scenario 寫,TLE 分支就蒸發了(規格面缺驗收出口的典型後果)。資料面上,worker `run_only` 回傳的 `StudentResult` 也沒有任何欄位能讓 judge.rs 區分「超時」與「一般錯誤」。

## Proposed Solution

1. **先補 spec Scenario**(治根因):`wasm-pool-judge` delta spec 增列 TLE 判定 Scenario;`python-generator` delta spec 增列 run_only 結構化超時欄位 Scenario。
2. **worker 端結構化分類**:`handleRunOnly` 的 catch 依既有 dev `run` handler 同款特徵(errMsg 含 TimeoutError / Operation limit)分類,`testcase_result` 訊息增列 `timed_out: boolean`;超時時 `error` 不傳(比照 dev handler 隱藏 op 上限細節)。分類只發生在 worker 這一處——**judge.rs 不做字串比對**。
3. **judge.rs 增 TLE 分支**:`StudentResult` 增 `#[serde(default)] timed_out: bool`(向後相容:舊呼叫端未傳此欄位時為 false,行為不變);verdict 判定順序 `timed_out → TLE`、`error → RE`、其餘比對 AC/WA;TLE 的 `error` 欄位輸出 `None`(比照 RE 以外 verdict)。
4. **前端傳遞**:`useChallengeRunner.runStudentCode` 收集 `timed_out` 並隨結果陣列傳入 `wasm.judge`。UI 的 TLE 黃色徽章(`TestResultPanel.vue`)已存在,顯示層零改動;`useChallengeRunner` 既有的 `as 'AC'|'WA'|'TLE'|'RE'` 型別斷言自此成為真實可達的值域。

## Non-Goals

- 不改 op 上限數值、不加 per-case wall-clock、不動外層 N×6s 總預算(TLE 判定唯一來源是 op-counter 的 TimeoutError)。
- 不改 dev 模式 `run` handler 的既有 TLE 邏輯(已正確)。
- 不做計分面(BACKLOG §1 凍結範圍)。
- 不處理 wall-clock 型超時在正式站的顯示(prod 無 per-case wall-clock,總預算強殺仍是整批 resolve(null)——那是既有行為,非本 change 範圍)。

## Success Criteria

- 正式站(池判題路徑)提交扁平超量迴圈解:超限測資顯示 **TLE 黃色徽章**(而非 RE),生產建置 e2e 實測通過。
- TLE verdict 不洩漏任何錯誤訊息(`error` 為空,不出現 "Operation limit exceeded" 字樣與 op 上限數值)。
- 舊格式相容:不含 `timed_out` 欄位的 results 陣列判題行為與現行完全一致(judge.rs 單元測試)。
- 一般 RE(非超時)仍判 RE 且保留錯誤訊息;AC/WA 判定不變:judge.rs 既有測試全綠 + 新增 TLE 測試。
- `pnpm test --run` 全套綠(含 cargo 端由 CI verify 的 Rust 測試;本機 cargo test 需先 pnpm gen:keymaterial)。

## Impact

- Affected specs: `wasm-pool-judge`(TLE Scenario + StudentResult 形狀)、`python-generator`(run_only 結構化 timed_out 欄位)
- Affected code:
  - Modified: `testcase-generator/src/judge.rs`(StudentResult.timed_out + TLE 分支 + 單元測試)
  - Modified: `.vitepress/theme/workers/pyodide.worker.ts`(handleRunOnly 分類 + timed_out 欄位)
  - Modified: `.vitepress/theme/composables/useChallengeRunner.ts`(runStudentCode 傳遞 timed_out)
  - Modified: `.vitepress/theme/__tests__/pyodide-worker-run-only.spec.ts`(型別契約 + timed_out 案例)
  - Modified: `.vitepress/theme/__tests__/useChallengeRunner-prod.spec.ts`(timed_out 傳遞斷言)
