## 1. Lint 設定

> 對應規格需求：Lint is runnable locally and in CI

- [x] 1.1 新增 `eslint.config.mjs`（flat config，`@typescript-eslint` + `eslint-plugin-vue` 保守推薦集，涵蓋 `.vitepress/**` 與 `scripts/**` 的 `.ts`／`.vue`），並於 `package.json` devDependencies 加入對應套件。驗證：`pnpm install` 成功、`pnpm exec eslint .vitepress scripts` 可執行（回傳結果不 crash）。
- [x] 1.2 於 `package.json` 新增 `lint` script（eslint 涵蓋 `.vitepress`／`scripts` + `prettier --check`）。驗證：`pnpm lint` 可執行完成並回傳明確 pass／fail；若既有告警過多，以 `--max-warnings <N>` 緩衝並在 design/tasks 記錄該 N 值與理由。滿足規格需求 Lint is runnable locally and in CI。

## 2. CI workflow

> 對應規格需求：Continuous integration verifies pushes and pull requests

- [x] 2.1 新增 `.github/workflows/ci.yml`：`on: push` 與 `pull_request` 針對 `staging`、`main`；單一 job `verify` 依序 setup Node 22 + pnpm、Rust toolchain(含 clippy)、Python 3.12、`pnpm install --frozen-lockfile`、`pnpm typecheck`、`pnpm lint`、`pnpm test`、`cargo test --manifest-path testcase-generator/Cargo.toml`；**不**執行 `build:wasm`／`build:pyodide`／`build:pools`。驗證：YAML 通過 `node -e "require('js-yaml').load(...)"` 或 `yq` 解析無誤；推上分支後 GitHub Actions 對本 PR 出現 `verify` job。滿足規格需求 Continuous integration verifies pushes and pull requests。

## 3. generate-pools 可測試重構

- [x] 3.1 將 `scripts/generate-pools.ts` 的 input 產生邏輯抽出為可匯入的純函式（例如 `export function generateInputsForSpec(params, count, rng?)`），`generate-pools.ts` 改呼叫該函式，行為不變。驗證：既有 `scripts/generate-pools.test.ts` 全綠、`pnpm build:pools` 仍能寫出 54 個 `.bin`。

## 4. 雙產生器一致性測試

> 對應規格需求：Rust and Python input generators conform to identical ParamSpec constraints；The set of supported parameter types is kept in sync

- [x] 4.1 [P] 新增 `testcase-generator/tests/param_conformance.rs`：對共用 ParamSpec fixtures（涵蓋 int／alpha_upper／alpha_lower／alpha_mixed／hex_string／printable_ascii／enum，及 count／multiple_of 變體）各產 N≥100 筆，斷言每筆符合該規格約束（字元集、長度範圍、count 範圍、separator、multiple_of、值域）。驗證：`cargo test --manifest-path testcase-generator/Cargo.toml` 通過含此測試。滿足規格需求 Rust and Python input generators conform to identical ParamSpec constraints。
- [x] 4.2 [P] 新增 `scripts/generator-parity.test.ts`（vitest）：對同一組 fixtures 呼叫 3.1 匯出的函式產 N≥100 筆、以相同 oracle 斷言約束；並斷言「Rust 支援 type 集合 == Python 支援 type 集合」，已知差異（如 `faker` 僅 Rust）以明確 allow-list 常數記錄。驗證：`pnpm test` 通過含此測試。滿足規格需求 The set of supported parameter types is kept in sync。
- [x] 4.3 人工反向驗證：暫時於 Python 端移除一種 type 支援 → `pnpm test` 之 parity 測試失敗並指出該 type；還原後通過。驗證：於本任務描述記錄失敗訊息片段與還原後綠燈。

## 5. reference_solution 欄位與內容層回歸

> 對應規格需求：Frontmatter supports an optional reference solution field；Content-layer regression verifies reference solutions pass

- [x] 5.1 [P] 於 `Usage.md` 文件化選填 `reference_solution` 欄位（用途、Python 格式、與 `generator` 的關係、與內容回歸測試的關聯）；於 `scripts/new-challenge.ts` 樣板加入註解形式的 `reference_solution`（預設註解、選填）。驗證：`Usage.md` 含該段落；`pnpm new-challenge` 產出的樣板含註解式欄位、`new-challenge.test.ts` 全綠。滿足規格需求 Frontmatter supports an optional reference solution field。
- [x] 5.2 [P] 新增 `scripts/content-regression.test.ts`（vitest node 環境）：讀 `docs/challenge/*.md`，對有 `reference_solution` 者以 3.1 方式產 M≥20 組 inputs，分別以 `generator` 與 `reference_solution` 計算輸出、斷言 `trimEnd` 後相等；未標註者 skip 並計數輸出；缺 python3／PyYAML 時整體 skip 並印警告。驗證：`pnpm test` 通過含此測試、輸出顯示 skip 計數。滿足規格需求 Content-layer regression verifies reference solutions pass。
- [x] 5.3 為至少 3 題（如 hello-world、multiplication-table、一題質數／GCD 類）補上正確 `reference_solution`。驗證：`pnpm test` 之 content-regression 對這些題全數通過（非 skip）。

## 6. 全套驗證

- [x] 6.1 全套本機驗證並記錄結果：`pnpm typecheck`、`pnpm lint`、`pnpm test`、`cargo test --manifest-path testcase-generator/Cargo.toml` 皆通過。驗證：四項指令輸出貼於本任務或 commit 訊息。
