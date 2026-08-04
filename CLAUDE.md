<!-- SPECTRA:START v1.0.2 -->

# Spectra Instructions

This project uses Spectra for Spec-Driven Development(SDD). Specs live in `openspec/specs/`, change proposals in `openspec/changes/`.

## Use `/spectra-*` skills when:

- A discussion needs structure before coding → `/spectra-discuss`
- User wants to plan, propose, or design a change → `/spectra-propose`
- Tasks are ready to implement → `/spectra-apply`
- There's an in-progress change to continue → `/spectra-ingest`
- User asks about specs or how something works → `/spectra-ask`
- Implementation is done → `/spectra-archive`
- Commit only files related to a specific change → `/spectra-commit`

## Workflow

discuss? → propose → apply ⇄ ingest → archive

- `discuss` is optional — skip if requirements are clear
- Requirements change mid-work? Plan mode → `ingest` → resume `apply`

## Parked Changes

Changes can be parked（暫存）— temporarily moved out of `openspec/changes/`. Parked changes won't appear in `spectra list` but can be found with `spectra list --parked`. To restore: `spectra unpark <name>`. The `/spectra-apply` and `/spectra-ingest` skills handle parked changes automatically.

<!-- SPECTRA:END -->

---

# 專案領域指南（fhsh.py-dojo）

> 本段落位於 Spectra 受管區塊之外，不會被模板升級覆蓋。任何 AI agent 或維護者接手前，請先讀完本段與下方「維護前必讀」清單。

## 專案定位

「台北市立復興高級中學 Python 自學道場」——給高中生的互動式 Python 自學與自動評測平台。題目於瀏覽器內以 Pyodide 執行、由 Rust/WASM 產生測資並判題，無需後端伺服器。

## 技術棧

- **文件站台**：VitePress 2（alpha）+ Vue 3 + Pinia
- **Python 執行環境**：Pyodide（瀏覽器內 CPython）
- **測資產生 / 判題**：Rust crate `testcase-generator`，以 wasm-pack 編為 WASM
- **套件管理**：pnpm（請勿改用 npm / yarn）
- **程式編輯器**：CodeMirror 6

## 建置指令總表

| 指令 | 用途 |
|------|------|
| `pnpm dev` | 產測資池 + 建 WASM + 下載 Pyodide + 起本機開發站 |
| `pnpm build` | 完整生產建置（pools + WASM + Pyodide + VitePress） |
| `pnpm build:pools` | 產生加密測資池（需 python3 + PyYAML；部分密碼學題型另需 pycryptodome，非標準相依） |
| `pnpm build:wasm` | 用 wasm-pack 將 `testcase-generator` 建為 WASM |
| `pnpm build:pyodide` | 下載自架 Pyodide 執行環境 |
| `pnpm gen:keymaterial` | 單獨產生 `testcase-generator/src/key_material.rs`（cargo test 前置步驟） |
| `pnpm typecheck` | vue-tsc + tsc 型別檢查（含 `scripts/`） |
| `pnpm lint` | ESLint + prettier 檢查 |
| `pnpm test` | vitest（本機請加 `--run` 避免進 watch） |
| `pnpm new-challenge` | 互動式 scaffold 新題目（新增題目的首選方式） |
| `pnpm new-tutor` | scaffold 新教學文章 |

## 題目 frontmatter 契約（摘要）

題目為 `docs/challenge/*.md`，主要 frontmatter 欄位：

- `layout: challenge`（固定）、`id`（字串，格式 `<category 前綴><3 位零填充序號>`，例 `py001`／`apcs005`，全站唯一，由 scaffold 自動配號，勿手填）、`title`、`difficulty`（easy | medium | hard）
- `algorithm`（snake_case，WASM 產生測資的識別鍵）、`testcase_count`（選填，預設 5）
- `params`（必填，輸入參數規格）、`generator`（必填，Python 正解，輸出期望答案）、`starter_code`（必填，使用者初始程式碼）
- `reference_solution`（**選填**）：宣告後，`content-regression` 測試會驗證此正解在正式測資下與 generator 的期望輸出一致
- 完整規格見 `Usage.md`。**注意**：測資輸入產生邏輯只有一份（Rust crate `testcase-generator`，建置期與瀏覽器共用同一份 WASM）；全部題目的 params 宣告由 `scripts/challenge-params.test.ts` 冒煙守門，任何引擎不認識的型別／欄位會指名該題失敗。

## 維護前必讀

1. `CONTRIBUTE.md` — 貢獻流程與新增題目 / 教學文章的 SOP
2. `README.md` — 專案總覽與環境需求（Node.js 22+、pnpm）
3. `Usage.md` — 題目 frontmatter 完整欄位規格

## 禁區

- 勿 commit gitignored 產物：`docs/public/pools/`、`testcase-generator/src/key_material.rs`、`.env.pool`、`.understand-anything/`。
- 建置順序固定為 gen:keymaterial → build:wasm → build:pools（build:pools 依賴 WASM 產物；順序寫在 package.json 的 dev/build，勿手動跳步）。
