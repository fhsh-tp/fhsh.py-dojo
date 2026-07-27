## 1. 引擎:plan 解析與驗證(testcase-generator crate)

- [x] 1.1 plan 條目解析 + band 深層合併 + 全套重驗證。先寫紅測試(TDD):合法 band+literal plan 通過並算出 plan_total;`{"count":0}`、`{"literal":""}`、band+literal 混合條目、未知鍵、空陣列、非陣列各報含條目索引的錯誤;override 引用 base 不存在的鍵報含鍵路徑的錯誤;合併後違反既有驗證(如 min>max)沿用既有錯誤訊息。實作於 `testcase-generator/src/lib.rs`(envelope 層,移除 reserved 拒收)與必要的 `testcase-generator/src/parser.rs` 輔助;深層合併規則:兩邊皆 JSON 物件則遞迴、否則以 override 取代。驗收:`cargo test` 新增測試全綠。(涵蓋 spec requirement:'testcase_plan frontmatter declaration'、'Band override merges into base params and is fully re-validated')
- [x] 1.2 逐 band 與 literal 預算檢查。紅測試:base params 過預算但某 band 合併後超標 → budget error 且訊息含該 band 條目索引;literal 位元組超標 → 同報索引;全部 band/literal 在預算內 → 通過。實作:每 band 以合併後 params 跑 `estimate_input_bytes`,literal 以 UTF-8 位元組長度比對 effective budget。驗收:`cargo test` 全綠。(涵蓋 spec requirement:'Per-band and literal budget enforcement')
- [x] 1.3 plan-aware seed 與 blocked 生成 + count 整數倍契約。紅測試:(a) 同 spec+seed 兩次呼叫 byte-identical;(b) 改 band 值域即重洗;(c) **無 plan spec 的 seed 雜湊輸入位元組不變**(以既有 DEQUE_SPEC 輸出快照比對——先在改動前記錄輸出,改動後斷言相同);(d) count 非 plan_total 整數倍 → 錯誤訊息含兩數;(e) 產出順序 = block 0 條目依序、block 1 條目依序,literal 位置逐字相符。實作:seed 雜湊在 plan 存在時追加 `0x00 + plan JSON`;生成迴圈按 block × 條目順序。驗收:`cargo test` 全綠。(涵蓋 spec requirement:'Plan-aware deterministic seeding'、'Blocked generation order and count contract')
- [x] 1.4 `generate_dev_inputs(spec_json)` WASM 入口。紅測試(native 層 `dev_inputs_from_spec`):band(3)+band(2)+literal 回傳恰 6 筆、位置 1-3/4-5 落在各自 band 值域、位置 6 逐字等於 literal;無 `testcase_plan` → 錯誤訊息導向 `generate_challenge`;非法 plan 沿用 1.1 錯誤。實作:entropy 亂數、一輪 plan、與 pool 入口共用解析/預算程式碼。驗收:`cargo test` 全綠。(涵蓋 spec requirement:'Dev-mode plan generation entry')

## 2. 引擎:池層 block 選取(testcase-generator crate)

- [x] 2.1 `PoolPayload.plan_block_size: Option<usize>` + `select_testcases` 整塊選取。紅測試:(a) 200 筆 + `plan_block_size:5` 的池,`select_testcases(id,5)` 回傳的 5 筆恰為某個儲存 block 且依序;(b) count≠k → 錯誤訊息含 k;(c) 池筆數非 k 整數倍 → 描述性錯誤;(d) k=0 → 錯誤;(e) 無 `plan_block_size` 的池走既有 shuffle+truncate(既有測試全保留不動)。實作於 `testcase-generator/src/pool.rs`;plan 路徑為全新分支,非 plan 路徑零 diff;`judge.rs`、`crypto.rs` 不動。驗收:`cargo test` 全綠。(涵蓋 spec requirement:'Block selection for plan pools')

## 3. 建置端(scripts/)

- [x] 3.1 `readChallenge` 擴充:讀選填 `testcase_plan`、`testcase_plan` 與 `testcase_count` 並存即 throw(訊息含檔名)、`verdict_detail` 白名單 `['hidden','actual','full']`(非法值 throw 訊息含檔名與合法值;缺席預設 hidden 不變)。紅測試加在 `scripts/generate-pools.test.ts`(既有 readChallenge 測試同檔)。實作於 `scripts/generate-pools.ts`。驗收:`pnpm test --run scripts/generate-pools.test.ts` 全綠。(涵蓋 spec requirement:'readChallenge validates testcase_plan usage'、'Mutual exclusion with testcase_count'、'Build-time verdict_detail whitelist')
- [x] 3.2 池建置 plan 路徑:`scripts/wasm-input-generator.ts` 的 `PoolSpec` 增 `testcase_plan?: unknown[]`;`scripts/generate-pools.ts` 主流程對 plan 題計算 `plan_total`(band count 相加 + literal 條數)與 `count = floor(200 ÷ plan_total) × plan_total`,並在 `encryptPool` payload 附 `plan_block_size`(非 plan 題 payload 無此欄位、路徑零改動)。`encryptPool` 簽名擴充的紅測試加在 `generate-pools.test.ts`(解密驗 payload 欄位)。驗收:`pnpm test --run scripts/generate-pools.test.ts` 全綠。(涵蓋 spec requirement:'Plan challenges produce blocked pools')
- [x] 3.3 冒煙守門:`scripts/challenge-params.test.ts` 對宣告 `testcase_plan` 的題目改送「params + plan」整包給 WASM 實際生成 1 個 block(驗證解析+預算+plan_total 一致);並存宣告的題目必須被指名失敗。同步確認 TS 端 plan_total 計算與 WASM 端一致(1 block 生成回傳筆數 = TS 算出的 plan_total)。驗收:`pnpm test --run scripts/challenge-params.test.ts` 全綠(現庫無 plan 題,守門邏輯以測試夾具驗證)。

## 4. 前端(.vitepress/)

- [x] 4.1 [P] `useWasm` 增 `generateDevInputs` wrapper(呼叫 WASM `generate_dev_inputs`,錯誤回 null 並保留 console.error 慣例);單元測試加在 `.vitepress/theme/__tests__/useWasm.spec.ts`。
- [x] 4.2 `ChallengeConfig` 增 `testcasePlan?: unknown[]`;ChallengeView 從 frontmatter 傳入並推導 effective count(plan 總數;與 `testcaseCount` 的取捨:plan 存在即用 plan 總數)。dev 策略:config 含 plan → `generateDevInputs` 取一輪(取代 `generateChallenge`),其餘流程(generator 產期望輸出、store)不變;prod 策略:`select_testcases(id, effectiveCount)`;引擎錯誤走既有 `errorMessage` 呈現(不靜默降級)。紅測試:`useChallengeRunner-dev.spec.ts` 增 plan 題走 dev 入口與順序斷言;`useChallengeRunner-prod.spec.ts` 增 plan 題 count 傳遞與錯誤浮出斷言;非 plan 題既有測試不動。驗收:`pnpm test --run` 前端測試全綠。(涵蓋 spec requirement:'Runner supports testcase_plan challenges')

## 5. 文件

- [x] 5.1 [P] `Usage.md` 新增「testcase_plan — 測資分區」章節:條目語法(band/literal)、順序保證(宣告順序 = 每場順序)、與 `testcase_count` 互斥、逐 band 預算語意、seed 重洗規則、dev/prod 行為、override 警告(只補丁值域勿改型別)、與 group 組合的完整 YAML 範例(標明數字為語法示範)。
- [x] 5.2 [P] `openspec/BACKLOG.md` 修正:§1 改記「資料面已實作(implement-testcase-plan),計分面(部分給分/UI)仍凍結」;刪除「2026-07-04 isolate-testcase-pools 特地加固」錯誤定性(該 change Non-Goals 明文排除 pool.rs、git 歷史證實未動),改為「與加密判題引擎同檔的敏感邏輯」;§2.8 更新實測數據(settrace op 計數下純 Python O(n²) 於 n≈1600–2100 觸發 10M 上限;C 內建不計 op;`while lst: lst.pop(0)` 於 n=12000 僅約 24k ops)。

## 6. 整體驗證

- [x] 6.1 全鏈驗證:`pnpm gen:keymaterial && pnpm build:wasm` 後 `cargo test`(testcase-generator)全綠;`pnpm test --run`、`pnpm typecheck`、`pnpm lint` 全綠;`pnpm build:pools` 成功。既有非 plan 題池 byte-identical 驗證:改動前後各產一次池,抽 `repeat-greeting`、`card-restack-count`、任一 ch1 題共 3 題 sha256 比對相同(建置前記錄基準)。樣本 plan 題夾具(不進 docs/challenge/)產池後解密驗證 block 結構:塊內順序 = 宣告順序、`plan_block_size` 正確。
