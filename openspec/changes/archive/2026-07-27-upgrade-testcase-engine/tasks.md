## 1. Rust 引擎:schema 與驗證

- [x] 1.1 `testcase-generator/src/parser.rs`:`CountSpec` 新增選填 `from: Option<String>`(與 `min`/`max` 互斥);`ParamSpec` 新增 `Group { repeat: String, params: IndexMap<String, ParamSpec>, .. }` variant;所有 spec 結構加上 deny unknown fields。實作 parse 期驗證:值域反轉(`min > max`、`min_len > max_len`、`count.min > count.max`)、空 enum values(含群組內遞迴)、引用合法性(往回引用、單值 int、`min >= 0`、不得引用群組)、群組深度 1、`from` 與 `min`/`max` 互斥。每條違規回傳含規則名的可讀 `Err`。驗收:新增的 parser 單元測試涵蓋 design.md D5 邊界矩陣每一列的違規案例,全部以 `Err` 而非 panic 收場;修復既有 struct literal 編譯錯誤(`parser.rs` 與 `rng.rs` 內約 11 處 `CountSpec { .. }`)。(涵蓋 spec requirement:'Rust WASM generates random inputs only'、'Invalid specs fail at parse time instead of trapping at generation time';依 design「D5:群組與連動的引用語意(邊界矩陣)」)
- [x] 1.2 `testcase-generator/src/parser.rs`:實作 worst-case 輸入估算函式(int 位數含負號、字串型別 max_len、enum 最長值、count 上界含 from 引用之 max、separator、群組內部總和 × repeat 引用之 max),並在 `parse_params` 無條件強制 65536 bytes 硬上限。驗收:單元測試證明估算值 ≥ 多次實際產出 bytes,且超標規格得到列出逐參數估算的錯誤。(依 design「D4:輸入規模預算採兩層執行」的硬上限層)

## 2. Rust 引擎:產生邏輯與新入口

- [x] 2.1 `testcase-generator/src/rng.rs`:`generate_input` 改為依宣告序迭代並維護已抽值表(頂層一份、每次群組重複各一份,查找先群組層後頂層);實作 `from` 連動個數與群組重複渲染(重複間以換行銜接;repeat 為 0 時群組零輸出)。更新檔內「一參數一行」doc comment 與 `generate_input_joins_in_declaration_order` 等受影響測試。驗收:cargo test 綠;新增測試覆蓋 deque 式規格(t → 群組[n, nums(from=n, separator="\n")])的行數一致性與 repeat=0 邊界。(涵蓋 spec requirement:'Group construct repeats a nested param block';依 design「D6:產生器攜帶跨參數狀態」)
- [x] 2.2 `testcase-generator/src/lib.rs`:新增 `generate_pool_inputs(spec_json, count)` WASM 入口,吃 `{ params, seed?, input_budget? }`;seed 存在時以 FNV-1a 64(seed bytes + 0x00 + params 原始 JSON bytes)導出 `SmallRng::seed_from_u64`,否則 from_entropy;強制可調預算(預設 4096、宣告上限 65536,超過即錯);頂層 `testcase_plan` 鍵回報 reserved 錯誤,其他未知鍵回報 unknown-field 錯誤。既有 `generate_challenge` 簽名與行為不變(僅獲得 parse 期驗證與硬上限)。驗收:同 spec 兩次呼叫 byte-identical;params 內容變動則序列改變;reserved 鍵與超額預算得到指定錯誤。(涵蓋 spec requirement:'Pool input generation is deterministic and budget-enforced';依 design「D2:新 WASM 入口 generate_pool_inputs(spec_json, count),spec 物件化」「D3:seed 以 FNV-1a 64-bit 在 Rust 端導出」「D4:輸入規模預算採兩層執行」)
- [x] 2.3 [P] `testcase-generator/tests/param_conformance.rs`:配合 `generate_input` 新簽名重寫 `samples()` helper;新增 group/from/seed/budget 的 conformance 案例(含 D5 矩陣的合法案例)。驗收:cargo test 綠,新能力每項至少一個正向與一個違規案例。

## 3. 建置腳本:WASM 單一真相源

- [x] 3.1 新增 `scripts/wasm-input-generator.ts`:lazy 載入器(template-literal 動態 import glue、readFileSync 讀 wasm、`init({ module_or_path })` 一次性初始化),匯出 `generatePoolInputs(spec, count)` 與產物存在性檢查(缺產物時丟出含 `pnpm build:wasm` 的可讀錯誤)。驗收:在已建產物環境下 smoke 執行成功;無產物環境下 import 本身不觸發初始化。(依 design「D1:Node 端以 bytes init 載入 web-target WASM(不出第二個 build target)」)
- [x] 3.2 `scripts/generate-pools.ts`:刪除內嵌 Python 產生邏輯(`gen_value`/`gen_param_line` 等),`generateInputs` 改為呼叫 `wasm-input-generator`(spec 的 seed = challenge slug,`input_budget` 取自 frontmatter);preflight 新增 WASM 產物檢查;任何 WASM 錯誤中止建置並具名 challenge。frontmatter 解析與 generator 執行的 python3 路徑保持不變。驗收:`pnpm build:pools` 55 題全綠;連續兩次執行池 plaintext byte-identical(以解密比對或以 seed 重生比對)。(涵蓋 spec requirement:'Build script generates encrypted testcase pools')
- [x] 3.3 [P] 確認 `scripts/generate-pools.test.ts` 既有 24 個純單元測試在無 WASM 產物環境仍可執行(必要時調整 import 邊界,不得引入 top-level WASM 初始化)。驗收:暫時改名 `docs/public/wasm/` 後 `pnpm vitest run scripts/generate-pools.test.ts` 仍綠,改回後亦綠。

## 4. 測試守門汰換

- [x] 4.1 刪除 `scripts/generator-parity.test.ts`;新增 `scripts/challenge-params.test.ts`:枚舉 `docs/challenge/*.md`,每題 params 經 WASM parse 與預算檢查必須通過;題目數為 0 或 WASM 產物缺失時測試失敗(不 skip),錯誤訊息含 `pnpm build:wasm`。驗收:全題綠;人工注入一題 `type: str` 時測試紅並指名該檔。(涵蓋 spec requirement:'Every challenge params declaration passes the engine parser';同時完成除役 requirement 'Rust and Python input generators conform to identical ParamSpec constraints' 與 'The set of supported parameter types is kept in sync' 的守備交接;依 design「D7:建置鏈三段化與守門替代」)
- [x] 4.2 `scripts/content-regression.test.ts`:`generateInputs` 呼叫改走 WASM 路徑;覆蓋率地板斷言(至少一題宣告 reference_solution)移到 python3 skip guard 之前並改以 frontmatter 掃描計數,使 python3 缺席時地板仍生效。驗收:有 python3 環境全綠;模擬無 python3 時僅 generator 執行部分 skip、地板斷言仍執行。

## 5. 建置鏈與 CI

- [x] 5.1 `package.json`:`dev` 與 `build` 改為 `pnpm gen:keymaterial && pnpm build:wasm && pnpm build:pools && …`;新增 `engines: { "node": ">=22" }`。`.github/workflows/ci.yml`:verify job 於 vitest 之前加入 wasm-pack 安裝(jetli/wasm-pack-action)、`pnpm gen:keymaterial`、`pnpm build:wasm`,並更新三段已失真的解釋性註解(PyYAML 用途、wasm-pack 安裝理由、NOTE);`release.yml` 確認經由 `pnpm build` 繼承正確順序。驗收:本機乾淨環境(暫時移走產物)`pnpm build` 端到端成功;CI 綠。(涵蓋 spec requirement:'Build pipeline orders key material before WASM before pools';依 design「D7:建置鏈三段化與守門替代」)
- [x] 5.2 [P] 部署驗證清單寫入 change 目錄 `verification.md`:Cloudflare Pages dashboard build command 更新為三段順序、CF Node 版本 >= 22 確認、staging 部署綠燈與池檔大小抽查。此為人工項,完成後在檔內勾記。驗收:檔案存在且列出具體操作步驟與預期觀察值。

## 6. 文件與 future

- [x] 6.1 `Usage.md`:「一參數一行」契約改寫為「一參數一區塊」;新增 group/`count.from`/`input_budget` 規格段落(語法、D5 引用規則、預算與硬上限、deque 式完整範例);移除已不成立的敘述。驗收:文件內每個宣告範例可直接通過 `challenge-params` 等級的 parse 檢查。
- [x] 6.2 [P] 同步四份維護文件:`CLAUDE.md`、`AGENTS.md`、`GEMINI.md`、`.claude/skills/challenge-author/SKILL.md` 移除「Rust/Python 兩端同步 + generator-parity 守門」條目,改述「單一真相源 + challenge-params 冒煙守門」。驗收:四份文件對引擎守門的描述一致且無 parity 殘留。
- [x] 6.3 [P] 新增 `openspec/BACKLOG.md`:收錄 testcase_plan 原始構想(APCS 分區、band 覆寫、literal 測資、池層 block 選取的 α 方案草案與其風險)與 adversarial review 停車場(pool session 洩漏、IndexedDB 配額靜默失敗、dev generator 無逾時吞錯、池 params 指紋/CDN 快取、WASM 產物新鮮度殘餘風險)。驗收:每項含問題描述、證據位置、建議處理方向。

## 7. 端到端驗證

- [x] 7.1 全量驗證:`cargo test --manifest-path testcase-generator/Cargo.toml`、`pnpm build`(端到端三段順序)、`pnpm test --run`、`pnpm typecheck`、`pnpm lint` 全綠;以 node 腳本驗證 design.md Implementation Contract 五個觀察點(決定性重建比對、deque 式規格渲染、D5 違規可讀錯誤、既有 55 題 frontmatter 零修改、parity 檔案不存在)。驗收:五個觀察點逐項記錄實際輸出於 change 目錄 `verification.md`。
