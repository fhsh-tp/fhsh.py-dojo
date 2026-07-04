## Why

專案已累積 28 個 TS/Vue 測試與 67 個 Rust 單元測試，但 `.github/workflows/` 只有 release 打包，沒有任何在 push/PR 時執行測試、型別檢查或 lint 的守門機制——所有測試靠本機手動，無自動化保障。此外，測資產生邏輯在 Rust 端（`testcase-generator` crate）與 build 腳本內嵌的 Python 版各有一份、需手動同步；且題目缺「範例正解」欄位，無法驗證正解在正式加密池下真的能得 AC（`isolate-testcase-pools-per-challenge` 那類「悄悄誤判 WA」的 bug 正源於此結構性缺口）。

## What Changes

- 新增 GitHub Actions CI（於 `.github/workflows/` 下），在 push/PR 到 `staging` 與 `main` 時執行 `pnpm typecheck`、`pnpm test`（vitest）、`cargo test`（testcase-generator）與 lint，任一失敗即擋下合併。
- 導入 lint 設定：ESLint（TS/Vue，flat config）、`prettier --check`、`cargo clippy -D warnings`；於 `package.json` 新增 `lint` script。
- 新增**雙測資產生器一致性測試**：以共用的 ParamSpec fixtures，驗證 Rust 產生器與 build 腳本的 Python 複寫版對相同規格產出的結果皆符合**相同約束**（型別、字元集、長度／數量範圍、separator、multiple_of、值域），且兩端支援的 `type` 集合一致。因 Rust `SmallRng` 與 Python `random` 演算法不同，故驗證的是「約束一致性 + 型別覆蓋一致性」而非位元組相同。
- 為 challenge frontmatter 新增**選填 `reference_solution` 欄位**（Python 參考解答），並新增**內容層回歸測試 harness**：對有 `reference_solution` 的題目，跑正解對正式加密測資池 judge 應全數 AC；未標註者 skip。先為 3–5 題種子驗證此 harness。

## Non-Goals

- 不強制所有 54 題立即補上 `reference_solution`（採漸進式；本變更僅種子數題並讓測試 skip 未標註者）。
- 不導入 e2e（Playwright／Cypress）測試。
- 不改動 dev／prod runner 的判題邏輯本身，也不改測資池加密格式。
- 不處理部署（Cloudflare Pages）設定，CI 僅做驗證不做 deploy。

## Capabilities

### New Capabilities

- `ci-quality-gate`: push／PR 觸發的 GitHub Actions CI，執行 typecheck、vitest、cargo test、lint 作為合併前的自動守門。
- `generator-parity-test`: 自動化測試，保證 Rust 與 Python 兩套測資產生邏輯對相同 ParamSpec 產出符合相同約束、且支援型別集合一致，避免只改一端造成 prod 池悄悄產出錯誤測資。

### Modified Capabilities

- `python-generator`: challenge frontmatter 新增選填 `reference_solution` 欄位，並定義內容層回歸測試（有標註者，正解對正式加密池 judge 須全數 AC）。

## Impact

- Affected specs: ci-quality-gate (new), generator-parity-test (new), python-generator (modified)
- Affected code:
  - New: .github/workflows/ci.yml, eslint.config.mjs, scripts/generator-parity.test.ts, scripts/content-regression.test.ts, testcase-generator/tests/param_conformance.rs
  - Modified: package.json, Usage.md, scripts/new-challenge.ts
  - Removed: (none)
