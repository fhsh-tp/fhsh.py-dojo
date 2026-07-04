## Context

現況：`.github/workflows/` 僅有 release 打包（推 tag 建 dist），**無測試型 CI**。95 個既有測試（28 TS/Vue + 67 Rust）全靠本機手動執行。測資產生邏輯存在兩份實作：Rust `testcase-generator` crate（dev 即時、prod 判題）與 `scripts/generate-pools.ts` 內嵌的 Python 複寫版（build 時產池、刻意避免載入 WASM）。題目 frontmatter 目前只有 `generator`（算 expected）與 `starter_code`，無「已知正解」，故無法端到端驗證「正解在正式加密池下得 AC」。

## Goals / Non-Goals

**Goals:**

- push／PR 自動守門：typecheck + vitest + cargo test + lint 綠燈才可合併。
- 偵測雙產生器漂移：任一端新增／修改 ParamSpec 型別或約束而未同步另一端時，測試失敗。
- 提供內容層回歸能力：讓有標註正解的題目能自動驗證「正解對正式池得 AC」。

**Non-Goals:**

- 不要求 54 題全數補正解（漸進導入）。
- 不導入 e2e（Playwright／Cypress）。
- 不改判題／加密邏輯或測資池格式。
- 不做部署設定；CI 僅驗證不 deploy，也不清零全部既有 lint 告警。

## Decisions

1. **CI 平台與觸發**：GitHub Actions，`on: push` 與 `pull_request` 針對 `staging`、`main`。單一 job `verify`：checkout → setup Node 22 + pnpm → Rust toolchain(含 clippy) → Python 3.12 → `pnpm install --frozen-lockfile` → `pnpm typecheck` → `pnpm lint` → `pnpm test` → `cargo test --manifest-path testcase-generator/Cargo.toml`。CI 只驗證不建站，故**略過** `build:wasm`／`build:pyodide`／`build:pools` 以縮短時間（vitest 用 jsdom、cargo test 為純單元測試，皆不需 WASM/Pyodide 產物）。
2. **Lint 範圍**：ESLint flat config（`eslint.config.mjs`）涵蓋 `.vitepress/**` 與 `scripts/**` 的 `.ts`／`.vue`，用 `@typescript-eslint` + `eslint-plugin-vue` 之**保守推薦集**；`prettier --check`（沿用 `.prettierrc.json`）；`cargo clippy -- -D warnings`。新增 `package.json` script `lint`。決策：首版採保守規則集、只擋明顯錯誤，必要時以 `--max-warnings` 緩衝，避免既有告警一次湧入擋死 CI。
3. **雙產生器一致性（generator-parity）**：定義一組共用 ParamSpec fixtures（涵蓋每種 type：int／alpha_upper／alpha_lower／alpha_mixed／hex_string／printable_ascii／enum，及 count／multiple_of 變體）。Rust 端 `testcase-generator/tests/param_conformance.rs` 對每 fixture 產 N 筆並斷言符合該規格約束；TS 端 `scripts/generator-parity.test.ts` 呼叫 `generate-pools.ts` 匯出的 input 產生函式，對同組 fixtures 以**相同 oracle** 斷言。另斷言「Rust 支援 type 集合 == Python 支援 type 集合」，已知差異（如 `faker` 僅 Rust）以明確 allow-list 記錄，逼使新增型別時同步兩端。**非位元組相同**：Rust `SmallRng` 與 Python `random` 序列不同，golden-file 不可行；一致性定義為「約束一致性 + 型別覆蓋一致性」。
4. **內容層回歸（content-regression）**：Frontmatter 新增選填 `reference_solution`（Python 區塊純量）。`scripts/content-regression.test.ts`（vitest node 環境）讀每個 `docs/challenge/*.md`，若有 `reference_solution`：以與 `generate-pools.ts` 相同方式對該題產 M 組 inputs → 用 `generator` 算 expected → 用 `reference_solution` 算 actual → 斷言 `actual === expected`（trimEnd 後）。因正式 judge 就是比對 generator 的 expected，此為「正解得 AC」的離線等價驗證。未標註者 skip 並計數。先為 3–5 題（hello-world 等）補正解證明 harness。此測試併入 `pnpm test`、於 CI 執行。

## Implementation Contract

- **Behavior**：開 PR／推 commit 到 staging／main → GitHub Actions 跑 typecheck／lint／vitest／cargo test，任一失敗 PR 顯示紅燈。本機 `pnpm lint` 可重現 lint。
- **Interface／data**：CI workflow（job 名 `verify`）；`package.json` 新增 `lint` script；challenge frontmatter 新增選填 `reference_solution:`（Python）；`generate-pools.ts` 匯出可重用的 input 產生函式（供測試 import，行為不變）；新測試檔 `scripts/generator-parity.test.ts`、`scripts/content-regression.test.ts`、`testcase-generator/tests/param_conformance.rs`。
- **Failure modes**：parity 在型別集合不一致或約束違反時失敗並指出 type／約束；content-regression 對「有正解但 actual≠expected」的題目失敗並指名 slug；缺 python3／PyYAML 時 content-regression skip 並印警告（與 build:pools preflight 一致），不卡死無 Python 者，CI 有 Python 照跑。
- **Acceptance criteria**：CI 對本 PR 顯示綠燈；`pnpm test` 本機通過含新兩測試；`cargo test` 通過含 `param_conformance`；≥3 題有 `reference_solution` 且通過 content-regression；故意在 `generate-pools.ts` 移除一種 type 支援 → parity 測試失敗（人工驗證一次）。
- **Scope boundaries**：In — CI yaml、lint 設定與 script、parity 測試(Rust+TS)、content-regression harness + 3–5 題種子、`reference_solution` 欄位與 Usage.md 文件、`generate-pools.ts` 匯出重構(純重構行為不變)。Out — 補齊全部 54 題正解、e2e、部署、判題／加密變更、清零全部既有 lint 告警。

## Risks / Trade-offs

- Lint 首次導入可能揭露大量既有告警：以保守規則集 + 必要時 `--max-warnings` 緩衝，不追求一次清零。
- `generate-pools.ts` 的 input 產生邏輯目前內嵌 build 流程；抽出為可匯入函式的重構須以既有 `generate-pools.test.ts` 保護、確保 build 行為不變。
- content-regression 依賴 python3 + PyYAML；以 skip + 警告降級避免無 Python 環境卡死。
- parity 的型別集合一致以 allow-list 記錄已知差異（faker 僅 Rust），需維護——但這正是逼使同步的機制。
