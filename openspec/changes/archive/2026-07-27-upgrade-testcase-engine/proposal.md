## Why

競賽式多筆測資格式(第一行 T,每筆測資第一行 Ni、接著 Ni 行資料)無法以現行 params 模型宣告:`count` 的實際數量獨立隨機、與其他參數不連動,也沒有群組重複構件。同時輸入產生邏輯存在雙實作(Rust WASM 供瀏覽器、`scripts/generate-pools.ts` 內嵌 Python 供建置期),每個引擎級新功能需在 5 處描述且「加欄位」級變更無自動守門——id 22 的 `type: str` 靜默產出 `UNKNOWN_TYPE` 測資即為此缺口的實證。

## What Changes

- **建置期整併(單一真相源)**:`scripts/generate-pools.ts` 改為在 Node 載入 web-target WASM 產生輸入(lazy dynamic import + bytes init);python3 職責縮減為 frontmatter 解析與 generator 期望輸出計算。**BREAKING(內部管線)**:建置順序改為 gen:keymaterial → build:wasm → build:pools,`package.json`、`.github/workflows/ci.yml`、`.github/workflows/release.yml` 與 Cloudflare Pages build command 同步修正。
- **除債**:刪除內嵌 Python 產生邏輯與 `scripts/generator-parity.test.ts`;`generator-parity-test` capability 除役;4 份維護文件(CLAUDE.md/AGENTS.md/GEMINI.md/challenge-author skill)的「兩端同步」禁區條目移除。
- **params 新能力(全部 opt-in,既有題目 frontmatter 一字不改)**:
  - 群組 `repeat`:params 可宣告群組(巢狀 params),重複次數由先前宣告的單值 int 參數決定;深度限制 1。
  - `count.from`:參數的產生個數由先前宣告的單值 int 參數的抽出值決定;與 `min`/`max` 互斥。
  - seed 決定性:建置期產池走新 WASM 入口,seed 由 slug + params 內容以穩定雜湊導出;同規格必產同池。瀏覽器 dev 模式維持非決定性(練習多樣性)。
  - 輸入規模預算:parse 期以宣告值做 worst-case 估算;預設 4096 bytes/筆,frontmatter `input_budget` 可調高,硬上限 65536 bytes 不可覆寫;超標建置失敗並輸出估算式。
- **parse 期驗證強化**:未知欄位拒收(deny unknown fields)、min>max 等非法值域、群組內巢狀參數遞迴驗證(含空 enum)、`from`/`repeat` 引用合法性(往回引用、單值 int、非負),全部在 parse 期以可讀錯誤失敗,不再進入產生期 panic(WASM trap)。
- **守門替代與強化**:新增「全題目 params 冒煙測試」(所有 docs/challenge/*.md 的 params 必須通過 WASM parse 與預算檢查);`scripts/content-regression.test.ts` 改用 WASM 產輸入,skip guard 不得繞過覆蓋率地板。
- **spec 物件化 API(testcase_plan 地基)**:建置端新入口吃整包 spec 物件(params + seed + input_budget),欄位形狀為未來 `testcase_plan` 預留;本次不實作 plan。
- **文件**:Usage.md 重寫「一鍵一行」契約並補新構件規格;新增 future/backlog 文件收錄 testcase_plan 原始構想(APCS 分區)與 adversarial review 停車場清單。

## Non-Goals

- `testcase_plan`(APCS 式測資分區)的實作:池層選取邏輯、band 覆寫、literal 測資皆不做;完整構想寫入 future 文件。
- lib(vp-wasm-coding)合流:dojo 的 crate 本次維持獨立演化。
- 前端程式碼:dev 模式沿用既有 `generate_challenge` API,前端零改動。
- 池加密格式、`testcase-generator/src/pool.rs`、`testcase-generator/src/judge.rs`:不動。
- `faker` 型別常駐啟用、既有題目改寫為新格式、單筆超過 65536 bytes 的大測資支援:不做。
- 停車場項目(pool session 洩漏、IndexedDB 配額靜默失敗、dev generator 無逾時吞錯、池 params 指紋):記入 future 文件,本次不修。

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `python-generator`:ParamSpec 擴充(群組 repeat、count.from、seed 決定性、輸入規模預算、parse 期驗證強化、全題目 params 冒煙守門);「一參數一行」契約由「一參數一區塊」取代。
- `encrypted-pool-generation`:建置期輸入產生改由 WASM 單一真相源執行;建置順序三段化;python3 職責縮減;池產出決定性化。
- `generator-parity-test`:capability 除役(雙實作消滅後守門標的不存在),由全題目 params 冒煙測試接手守備。

## Impact

- Affected specs: `python-generator`(modified)、`encrypted-pool-generation`(modified)、`generator-parity-test`(removed)
- Affected code:
  - New:
    - scripts/wasm-input-generator.ts
    - scripts/challenge-params.test.ts
    - openspec/BACKLOG.md
  - Modified:
    - testcase-generator/src/parser.rs
    - testcase-generator/src/rng.rs
    - testcase-generator/src/lib.rs
    - testcase-generator/tests/param_conformance.rs
    - scripts/generate-pools.ts
    - scripts/content-regression.test.ts
    - package.json
    - .github/workflows/ci.yml
    - .github/workflows/release.yml
    - Usage.md
    - CLAUDE.md
    - AGENTS.md
    - GEMINI.md
    - .claude/skills/challenge-author/SKILL.md
  - Removed:
    - scripts/generator-parity.test.ts
