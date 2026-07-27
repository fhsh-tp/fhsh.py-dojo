## Why

平台需要出「效能感」題型(前幾筆教學小值域、最後幾筆大到讓純 Python O(n²) 解法 TLE),但現行引擎所有測資從同一組 params 分布 iid 抽樣,無法控制各筆測資的值域與順序。`testcase_plan` 在 upgrade-testcase-engine 時已預留 API 地基(reserved 鍵報錯)並凍結 α 草案於 `openspec/BACKLOG.md` §1;第一個消費者(deque 找最大最小值題)已收斂需求,現在實作。

## What Changes

- **frontmatter 新欄位 `testcase_plan`(opt-in)**:band 條目(`count` + `override` 值域補丁,鏡射 params 形狀)與 literal 條目(手工釘死的完整 stdin,期望輸出仍由 generator 計算)。條目宣告順序 = 每場測資順序(實現「前小後大」)。
- **parse 期驗證擴充**:`testcase_plan` 與 `testcase_count` 並存為 parse error;override 合併後跑既有整套驗證;每個 band 以「base params 合併 override 後」各自做 worst-case 預算估算;literal 以實際 bytes 過預算檢查;plan 內容納入池 seed 雜湊(改 plan 即重洗池)。
- **池格式與選取(α 方案)**:池格式加版本欄位與選填 `plan_block_size`;plan 題的池存「整組 block」(block 數 = floor(POOL_SIZE ÷ plan 總數),block 內順序 = 條目宣告順序);`select_testcases` 對 plan 題改抽一整個 block(保留場次間多樣性);`judge.rs` 不動。
- **dev 模式支援 plan**:瀏覽器 dev 策略對 plan 題產生「一輪完整 plan」(band 依 override 合併後隨機、literal 逐字採用、順序照宣告),WASM dev 入口與前端呼叫鏈同步擴充。**推翻** upgrade-testcase-engine 的「前端零改動」Non-Goal(使用者拍板)。
- **夾帶項 1**:`scripts/generate-pools.ts` 的 readChallenge 加 `verdict_detail` 白名單(`['hidden','actual','full']`,BACKLOG §2.11)。
- **夾帶項 2**:BACKLOG 文件修正——§1「2026-07-04 特地加固」錯誤定性改正(該 change 明文排除 pool.rs、git 歷史證實未動);§2.8 更新為實測 TLE 門檻數據(純 Python O(n²) 於 n≈1600–2100 觸發 10M op 上限;C 內建不計 op);§1 移除已實作內容、保留計分面等未實作部分。

## Capabilities

### New Capabilities

- `testcase-plan`: frontmatter `testcase_plan` 宣告契約——band/literal 條目語法、順序保證、與 testcase_count 互斥、逐 band 預算估算、seed 納入 plan 內容。

### Modified Capabilities

- `encrypted-pool-generation`: 建置期對 plan 題改產「block 結構池」(block 數換算、block 內順序、池 payload 加 plan_block_size 與格式版本)。
- `wasm-pool-judge`: `select_testcases` 對含 plan_block_size 的池改抽一整個 block(非 plan 池行為不變)。
- `challenge-runner-orchestration`: dev 策略對 plan 題產生一輪完整 plan 的測資(順序照宣告);非 plan 題行為不變。
- `verdict-detail-control`: 建置期 readChallenge 對 verdict_detail 加白名單驗證(非法值建置失敗)。

## Impact

- Affected specs: `testcase-plan`(new)、`encrypted-pool-generation`、`wasm-pool-judge`、`challenge-runner-orchestration`、`verdict-detail-control`(modified)
- Affected code:
  - Modified:
    - testcase-generator/src/lib.rs
    - testcase-generator/src/parser.rs
    - testcase-generator/src/rng.rs
    - testcase-generator/src/pool.rs
    - testcase-generator/tests/param_conformance.rs
    - scripts/generate-pools.ts
    - scripts/wasm-input-generator.ts
    - scripts/challenge-params.test.ts
    - .vitepress/theme/composables/useChallengeRunner.ts
    - Usage.md
    - openspec/BACKLOG.md
  - New: (none)
  - Removed: (none)
