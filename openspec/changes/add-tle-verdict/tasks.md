## 1. Rust judge TLE 分支(TDD:紅燈先行)

- [x] 1.1 `testcase-generator/src/judge.rs` 先寫 4 個新單元測試(落實 design 決策「D4:測試策略 — Rust 單元測試先行(TDD),worker/前端以既有 mock 模式補」「D3:verdict 判定優先序 timed_out → error → 比對」「D2:StudentResult 以 #[serde(default)] 向後相容」與 spec requirement「WASM module judges student outputs internally」的 3 個新 Scenario):(i) `timed_out: true` → verdict "TLE";(ii) TLE 時 `error` 為 None(即使輸入帶 error,對應 Timed-out result produces TLE verdict 場景);(iii) 不帶 timed_out 欄位(以 `..Default` 或建構子預設)→ 行為與現行一致(Results without timed_out keep legacy behavior 場景);(iv) timed_out 與 error 並存 → TLE 優先。驗證:先跑 `pnpm gen:keymaterial` 再 `cargo test`(於 testcase-generator/),新測試紅燈(TLE 分支尚不存在,編譯期即失敗亦算紅);隨後實作 `StudentResult` 增 `#[serde(default)] timed_out: bool` + verdict 優先序,4 案例轉綠、既有 judge 測試全綠。
- [x] 1.2 重建 WASM:`pnpm build:wasm` 成功(judge 介面變更需重編才會反映到前端)。驗證:命令零錯誤,`docs/public/wasm/` 產物更新。

## 2. Worker 與前端傳遞

- [x] 2.1 `.vitepress/theme/workers/pyodide.worker.ts` 的 `handleRunOnly` catch 分類(落實 design 決策「D1:超時分類做在 worker 端,judge.rs 只讀結構化欄位」與 spec requirement「RunOnly results carry a structured timeout flag」):沿用 dev `run` handler 同款特徵(errMsg 含 TimeoutError 或 Operation limit)判定 `isTle`;超時時 post `{stdout: '', elapsed_ms, timed_out: true}`(不含 error),非超時維持現行 `{stdout: '', elapsed_ms, error}`。`RunOnlyRequest`/結果型別註解同步。驗證:`pyodide-worker-run-only.spec.ts` 補 timed_out 型別契約案例 + 以 mock pyodide 驅動 worker 模組的分類行為測試(比照 `pyodide-worker-trace-reset.spec.ts` 模式:mock runPythonAsync 拋含 Operation limit 的錯誤 → 斷言 posted 訊息 timed_out: true 且無 error;拋一般錯誤 → 斷言有 error 無 timed_out),全綠。
- [x] 2.2 `.vitepress/theme/composables/useChallengeRunner.ts` 的 `runStudentCode` 結果收集增 `timed_out: msg.timed_out`(落實 spec「RunOnly results carry a structured timeout flag」的 Frontend passes the flag through 場景);`submit` 內傳給 `wasm.judge` 的陣列自然帶上該欄位,verdict 處理零改動(TLE 徽章樣式已存在)。驗證:`useChallengeRunner-prod.spec.ts` 補案例——mock worker post 一筆 timed_out 結果,斷言 `wasm.judge` 收到的陣列該筆含 `timed_out: true`;`pnpm typecheck` 通過。

## 3. 回歸與收尾

- [x] 3.1 `pnpm test --run` 全套 + `pnpm lint` 全綠(含 Change 1 的整合測試不受影響)。驗證:命令零失敗。
- [x] 3.2 本機 `cargo test`(先 `pnpm gen:keymaterial`)全綠,證明 Rust 端與 CI verify 同步。驗證:命令零失敗。

## 4. Audit R1 修正(confirmed findings 落地)

- [x] 4.1 修復 serde-wasm-bindgen 毒批 critical(落實 design 決策「D2:StudentResult 以 Option<bool> + serde(default) 向後相容(audit R1 修訂)」與 spec「Explicit undefined timed_out keys do not poison the batch」場景):Rust `timed_out` 改 `Option<bool>` + `unwrap_or(false)`;`useChallengeRunner.runStudentCode` 只在值為 true 時附加 `timed_out` key(顯式 undefined key 會讓整批反序列化失敗)。驗證:新增 `scripts/judge-wasm-boundary.test.ts`(落實 design 決策「D5:真 wasm 邊界整合測試(audit R1 新增)」)——真 wasm-pack 產物 + 真加密池,顯式 undefined key 批次不炸、TLE/RE/WA 各就各位,全綠。
- [x] 4.2 分類改 op-count 探測(落實 design 決策「D1:超時分類做在 worker 端,以 op counter 探測、非字串比對(audit R1 修訂)」與 spec「Student-raised TimeoutError is not a TLE」場景):worker 新增 `opLimitExceeded(opLimit)` 探測 `_op_count > limit`,`run_only` 與 dev `run` 的 catch 皆改用之——學生自拋 TimeoutError 維持 RE 且保留訊息。驗證:`pyodide-worker-run-only.spec.ts` 增 fake-tle 案例(mock `_op_count` 未超限 + TimeoutError 字樣 → RE),全綠。
- [x] 4.3 型別與規格同步:worker 匯出具名 `RunOnlyTestcaseResult` 型別、兩處 postMessage 以 satisfies 收斂,測試檔改 import 該型別;delta specs(wasm-pool-judge 的 undefined-key 場景、python-generator 的探測式分類重寫)與 design(D1/D2/D5、契約、Risks 含 Pyodide 冷啟吃預算的 margin 修正)同步。驗證:`spectra validate` 通過、`pnpm typecheck` 通過。
