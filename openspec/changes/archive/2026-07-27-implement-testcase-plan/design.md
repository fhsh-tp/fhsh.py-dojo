## Context

`upgrade-testcase-engine`(已 archive)為 `testcase_plan` 預留了 spec 物件化 API:`generate_pool_inputs(spec_json, count)` 遇到頂層 `testcase_plan` 鍵回報 "reserved, not yet implemented"。α 方案草案凍結於 `openspec/BACKLOG.md` §1。第一個消費者(deque 找最大最小值題)需求已收斂:前幾筆教學小值域、最後幾筆大值域(讓純 Python O(n²) 觸發 10M op 上限 TLE;實測門檻 n≈1600–2100)。

現況約束:
- 池為 200 筆 iid 測資,`pool.rs` 的 `select_testcases` 均勻 shuffle 後 truncate——沒有 band 結構,分區順序會被打散。
- 池 seed 只雜湊 `seed 字串 + params JSON`(不含 plan)。
- 預算估算只吃 base params(`estimate_input_bytes(&params)`)。
- dev 模式走 `generate_challenge(params_json, count)`(entropy 亂數),看不到 plan。
- 使用者已拍板:band + literal 一次做齊;dev 模式也要支援 plan;池層採 α 方案、block 數照 POOL_SIZE 換算;夾帶 verdict_detail 白名單與 BACKLOG 文件修正。

## Goals / Non-Goals

**Goals:**

- frontmatter 可宣告 `testcase_plan`(band + literal),每場測資順序 = 條目宣告順序。
- 正式池:block 結構 + 整塊選取,場次間仍有多樣性;非 plan 題池位元組不變(seed 雜湊向後相容)。
- dev 模式:plan 題預覽與正式池同形(一輪完整 plan,值隨機)。
- 全部驗證在 parse/建置期 fail-loud:並存禁止、override 合法性、逐 band 預算、literal 預算。
- 夾帶:`readChallenge` 的 verdict_detail 白名單;BACKLOG §1 錯誤定性修正與 §2.8 實測數據更新。

**Non-Goals:**

- 計分面(部分給分、band 加總、UI 標示)——「此區佔 XX 分」以題目敘述文字表達。
- deque 題本身(後續獨立 change)。
- `judge.rs` 任何變更;池加密容器格式(MAGIC/version byte)變更。
- 對既有非 plan 題目的任何行為或池內容改變。

## Decisions

**D1:plan 解析位於 pool-spec envelope 層(lib.rs),band 以 JSON 深層合併重用既有驗證。**
`testcase_plan` 是 JSON 陣列,每條目為 `{"count": N, "override": {...}}` 或 `{"literal": "..."}`。band 的 `override` 鏡射 params 形狀,與 base params 做深層合併(兩邊皆物件則遞迴,否則以 override 值取代);合併結果丟回 `parse_params_value` 跑**同一套**既有驗證(型別、min/max、引用、群組深度)。override 在每一層引用的鍵**必須存在於 base**(拼錯鍵名報 parse error,不靜默新增)。理由:重用驗證器、零重複邏輯;替代方案(獨立 band 驗證器)會複製整套規則。

**D2:預算逐 band 估算;literal 以實際位元組計。**
每個 band 以「合併後 params」各自跑 `estimate_input_bytes`,任何 band 超過 effective budget 即報錯(錯誤訊息標明第幾個 band);literal 條目以 UTF-8 位元組長度檢查同一預算。堵住「大 band 逃過 base params 估算」的已實證缺口。

**D3:seed 雜湊條件式納入 plan。**
plan 存在時,seed = FNV-1a(seed 字串 + 0x00 + params JSON + 0x00 + plan JSON);plan 不存在時維持現行雜湊輸入**位元組不變**。理由:改 plan 必重洗池;同時保證所有既有非 plan 題的池內容 byte-identical(部署零 diff 驗證可用)。

**D4:池 payload 加選填 `plan_block_size`,加密容器版本不動。**
`PoolPayload` 增 `plan_block_size: Option<usize>`(serde 預設 None);舊 payload 無此欄位 → None → 行為完全不變。不 bump 容器 version byte:池與 WASM 同一次建置產出、原子部署,不存在「舊 WASM 讀新池」的組合;`plan_block_size` 本身就是格式判別欄位。

**D5:`select_testcases` 對 plan 池改抽整塊,count 嚴格相等。**
池含 `plan_block_size = k` 時:驗證 `k > 0`、`testcases.len() % k == 0`、呼叫端 `count == k`(不等即報錯,不猜);隨機選一個 block,回傳該 block 切片**依序**(不 shuffle)。非 plan 池走既有 shuffle+truncate 路徑,一行不動。

**D6:`generate_pool_inputs` 對 plan spec 要求 count 為 plan 總數的整數倍。**
plan 總數 = Σ band count + literal 條目數(每條 literal 算 1)。建置端傳 `count = floor(POOL_SIZE ÷ plan_total) × plan_total`;WASM 依序產出 blocks,每 block 內按條目宣告順序(band 產 count 筆、literal 逐字放入)。count 非整數倍即報錯。TS 端 `inputs.length === count` 信任邊界檢查維持不變。

**D7:dev 模式經新 WASM 入口 `generate_dev_inputs(spec_json)`。**
吃 `{"params": {...}, "testcase_plan": [...]}`,entropy 亂數,回傳**一輪完整 plan**(順序照宣告)。`testcase_plan` 缺席即報錯(此入口專為 plan 題;非 plan 題 dev 沿用 `generate_challenge` 不動)。前端 dev 策略在 config 含 plan 時改走此入口,測資數 = plan 總數;prod 策略把 `select_testcases` 的 count 算成 plan 總數。`ChallengeConfig` 增 `testcasePlan?: unknown[]`,ChallengeView 由 frontmatter 傳入並據以推導 effective testcase count。

**D8:並存禁止在兩層都擋。**
frontmatter 同時宣告 `testcase_plan` 與 `testcase_count`:`readChallenge`(建置端)與 WASM envelope(引擎端)都報錯——引擎端規則為 spec 物件同時含 `testcase_plan` 與非整數倍 count 的保護,建置端規則為明確互斥訊息。dev 前端同理以 plan 優先並於 frontmatter 冒煙測試守門。

## Implementation Contract

**引擎(testcase-generator crate):**

- `pool_inputs_from_spec(spec_json, count)` 接受頂層 `testcase_plan`(JSON 陣列)。行為:
  - 條目形狀:`{"count": <正整數>, "override": <物件,可空>}` 或 `{"literal": <非空字串>}`;其他形狀、未知鍵、空陣列皆為描述性 parse error(訊息含條目索引)。
  - band 合併後跑既有 `parse_params_value` 全套驗證;override 引用 base 不存在的鍵 → error 指名鍵路徑。
  - 逐 band 預算:各 band 以合併後 params 估算,超標報 `budget_error` 且訊息標示 band 索引;literal 位元組超標同報。
  - `count % plan_total != 0` → error(訊息含兩數字)。
  - 產出順序:block 0 全部條目依序、block 1 依序、…;同 spec 兩次呼叫 byte-identical(seed 存在時)。
  - plan 缺席時:行為與現行完全一致,含 seed 雜湊輸入位元組(既有非 plan 題池 byte-identical)。
- 新 WASM 入口 `generate_dev_inputs(spec_json: &str) -> {inputs: string[]}`:entropy 亂數、一輪 plan、順序照宣告;`testcase_plan` 缺席或非法 → JsError。
- `pool.rs`:`PoolPayload.plan_block_size: Option<usize>`;`select_testcases` 對 Some(k) 池:`count != k` → Err、`len % k != 0` → Err、隨機整塊、塊內依序。非 plan 池行為與現行位元組級一致。
- `judge.rs`、`crypto.rs` 零變更。

**建置端(scripts/):**

- `readChallenge`:讀 `testcase_plan`(選填);與**明宣告的** `testcase_count` 並存 → throw;`verdict_detail` 非 `['hidden','actual','full']` → throw(訊息含檔名與合法值)。
- `generate-pools.ts` 主流程:plan 題 `count = floor(200 ÷ plan_total) × plan_total`,`encryptPool` payload 附 `plan_block_size: plan_total`;非 plan 題完全走現行路徑。plan_total 在 TS 端由 frontmatter 計算,與 WASM 端計算一致(冒煙測試守門)。
- `wasm-input-generator.ts`:`PoolSpec` 增 `testcase_plan?: unknown[]`;信任邊界檢查不變。
- `challenge-params.test.ts`:宣告 `testcase_plan` 的題目走「params + plan」整包驗證(至少 1 block 實際生成);並存宣告的題目必須被指名失敗。

**前端(.vitepress/):**

- `ChallengeConfig` 增 `testcasePlan?: unknown[]`;ChallengeView 傳入 frontmatter 值並推導 effective count(plan 總數,band count 相加 + literal 條數)。
- dev 策略:config 含 plan → `generate_dev_inputs`;否則現行 `generateChallenge`。
- prod 策略:`select_testcases(id, effectiveCount)`;WASM 對 plan 池要求 count == plan_block_size,前端算錯會 fail-loud 顯示錯誤訊息(不靜默降級)。
- `useWasm` composable 增對應 wrapper。

**文件:**

- `Usage.md`:新增「testcase_plan — 測資分區」章節:語法、順序保證、互斥規則、預算語意、dev/prod 行為差異、與 group 組合的完整範例。
- `openspec/BACKLOG.md`:§1 改為「已實作,剩計分面」並修正「2026-07-04 特地加固」錯誤定性;§2.8 更新實測 TLE 門檻(n≈1600–2100、C 內建不計 op)。

**驗收(全部須通過):**

1. `cargo test`(於 testcase-generator;含新 plan 測試)全綠。
2. `pnpm test --run` 全綠(challenge-params、content-regression、strip-generator、既有前端測試)。
3. `pnpm typecheck`、`pnpm lint` 全綠。
4. `pnpm build` 成功;既有非 plan 題池檔內容與 staging 基準 byte-identical(抽 3 題 sha256 比對)。
5. 樣本 plan 題(測試夾具,不進 docs/challenge/)可產池、block 結構正確(手動驗證塊內順序 = 宣告順序)。
6. agent-browser e2e(PR 前):dev 模式 plan 題預覽順序正確;prod 建置 plan 題判題 AC/WA 正常。

## Risks / Trade-offs

- [override 深層合併語意誤解(例如覆寫 type)] → override 引用鍵必須存在於 base;合併後全套重驗證;Usage.md 明文警告「override 只該補丁值域,不該改型別」。
- [plan 題池檔變大(TLE 級測資 ~60KB/筆 × 多 block)] → 已估算 deque 情境 ~5MB << CF 25MiB 上限;Usage.md 記載估算方式;不設額外硬限制。
- [`select_testcases` 是判題安全敏感檔案(與加密池同檔)] → plan 路徑完全新增分支、非 plan 路徑零改動;審查聚焦 diff;既有 pool.rs 測試全保留。
- [count 契約三處(前端/建置/引擎)各自計算 plan_total,可能漂移] → 引擎端嚴格相等/整數倍檢查為最終防線,任何漂移 fail-loud;冒煙測試涵蓋。
- [dev 入口擴大 WASM 面積] → `generate_dev_inputs` 只讀 spec 產輸入,不觸及池/judge 狀態;與 BACKLOG §2.7 同一威脅模型(公開資料可重現,邊際風險零)。

## Migration Plan

無資料遷移:池為建置產物,每次 build 全量重產;非 plan 題池 byte-identical(D3 保證)。部署即生效,失敗回滾 = revert merge commit。

## Open Questions

(無——需求已於 grilling 收斂,決策 4 項由使用者拍板,其餘為凍結草案與 review 實證。)
