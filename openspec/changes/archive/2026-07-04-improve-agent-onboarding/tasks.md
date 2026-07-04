## 1. 指令檔領域段落（agent-onboarding-docs）

- [x] 1.1 於 `CLAUDE.md` 的 `<!-- SPECTRA:END -->` 之後新增「專案領域指南」canonical section，涵蓋技術棧、建置指令總表（`pnpm dev`/`build:pools`/`build:wasm`/`build:pyodide`/`gen:keymaterial`/`typecheck`/`lint`/`test` 用途）、題目 frontmatter 契約摘要（含選填 `reference_solution`）、必讀清單（`CONTRIBUTE.md`/`README.md`/`Usage.md`），滿足規格需求 Agent instruction files carry project domain content outside managed blocks。驗證：`grep -n "SPECTRA:END" CLAUDE.md` 確認新 section 行號在其後，且四項子內容可辨識。
- [x] 1.2 將 1.1 的領域內容鏡像進 `AGENTS.md`（受管區塊外），引用 skill 時改用 Codex `$spectra-*` 語法慣例、不加「Plan mode →」行。驗證：section 在 `<!-- SPECTRA:END -->` 之後、內容與 1.1 對齊、skill 引用為 `$spectra-*`。
- [x] 1.3 將 1.1 的領域內容鏡像進 `GEMINI.md`（受管區塊外），沿用該檔既有語法慣例。驗證：section 在 `<!-- SPECTRA:END -->` 之後、內容與 1.1 對齊。

## 2. fork 遺留文件一致化（Fork-legacy documentation is consistent）

- [x] 2.1 修正 `CONTRIBUTE.md`：Node.js 版本由 v20+ 改為 22+（對齊 README badge），並修正 Phase 章節跳號（1→2→3→5 缺 4）為連續編號，滿足規格需求 Fork-legacy documentation is consistent。驗證：`grep -n "Phase\|22" CONTRIBUTE.md` 確認版本 22+、Phase 連號無缺。
- [x] 2.2 統一 `Usage.md` 新增題目 SOP：以 `pnpm new-challenge` 為首選路徑並與 `CONTRIBUTE.md` 一致（不再教純手動 frontmatter 為唯一途徑）。驗證：`grep -n "new-challenge" Usage.md` 有結果、內文不與 `CONTRIBUTE.md` 矛盾。
- [x] 2.3 於 `CHANGELOG.md` 新增 `## [Unreleased]` section，收錄 1.0.0（2026-04-05）之後重大變更（Ch1/Ch2 內容、測資池隔離、quality-gates、agent onboarding）。驗證：`grep -n "Unreleased" CHANGELOG.md` 有結果且列出重大變更。
- [x] 2.4 將 `docs/shared/challenge.data.ts` 預設題名 fallback「密碼學挑戰 #N」改為中性字樣「挑戰 #N」，僅改字串常值不動型別。驗證：`pnpm typecheck` 綠且 `grep "密碼學挑戰" docs/shared/challenge.data.ts` 無結果。
- [x] 2.5 更新 `.gitignore`：移除失效規則 `challenge-generator/target`（crate 已更名 testcase-generator），保留分析階段新增的 `.understand-anything/` 忽略。驗證：`grep -n "challenge-generator\|understand-anything" .gitignore` 確認舊規則消失、新規則存在。
- [x] 2.6 於 `testcase-generator/Cargo.toml` 為未啟用的 `faker` feature 加註解說明其保留意圖與現況（`default = []` 未啟用），依 design D4 不移除宣告。驗證：`cargo metadata` 可解析且 `grep -n "faker" testcase-generator/Cargo.toml` 附有說明註解。

## 3. release 產物改名（Dist packaging in dual formats／Asset upload to GitHub Release）

- [x] 3.1 修改 `.github/workflows/release.yml`：打包與上傳的產物名由 `crypto-challenge-<ref>.tar.gz`/`.zip` 改為 `fhsh-py-dojo-<ref>.tar.gz`/`.zip`（tar/zip/upload 三處一致），滿足規格需求 Dist packaging in dual formats 與 Asset upload to GitHub Release。驗證：`grep -n "crypto-challenge" .github/workflows/release.yml` 無結果，且 `python3 -c "import yaml,sys;yaml.safe_load(open('.github/workflows/release.yml'))"` 不報錯。

## 4. useApi 死碼移除（vueuse-api-composable removal）

- [x] 4.1 移除無呼叫端的 useApi 死碼：刪除 `.vitepress/theme/composables/useApi.ts`、測試 `.vitepress/theme/__tests__/useApi.spec.ts`，並自 `.vitepress/theme/composables/index.ts` 移除 useApi/useWsApi re-export（其餘 composable re-export 保留不變）。此舉正式下線規格需求 useApi composable provides useFetch wrapper、useApi composable provides useWebSocket wrapper、useApi composable is exported from theme composables index（由 delta spec 的 REMOVED Requirements 處理）。驗證：`grep -rn "useApi\|useWsApi" .vitepress docs` 於原始碼無結果、`pnpm typecheck` 綠、`node_modules/.bin/vitest --run` 全綠（少掉 useApi.spec 測試）。

## 5. 整體驗證

- [x] 5.1 跑四道 gate 確認全綠：`pnpm typecheck`、`pnpm lint`、`node_modules/.bin/vitest --run`、`pnpm gen:keymaterial && cargo test --manifest-path testcase-generator/Cargo.toml`。驗證：typecheck/lint 綠、vitest 全 passed（預期約 248 passed）、cargo 73 passed。
