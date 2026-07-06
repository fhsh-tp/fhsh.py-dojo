# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [1.1.0] - 2026-07-06

補齊純前端道場的核心能力（學生作答持久化），完成模組一、二完整課程內容，並導入自動化品質守門與測資安全強化。

### Added

- **學生作答情形本機持久化（IndexedDB）**：完成度追蹤（`ChallengeCard` ✓ 徽章 + 題庫頁「已完成 X/54」計數）、作答軌跡錄製（edit｜run｜submit）、可下載作答紀錄 Markdown（含給 LLM 的提示前言）與 JSON
- 模組一、二完整教學內容與互動練習：迴圈與重複課程、數學素養 × 運算思維鷹架、APCS 素養導向題型、畢業考綜合題，以及 19 題程式挑戰的完整說明與範例
- 挑戰題庫搜尋功能與 `Challenge` 型別統一
- 自動化品質守門 CI（`.github/workflows/ci.yml`）：typecheck、lint、vitest、cargo test；雙測資產生器一致性測試（Rust `rng.rs` ↔ Python `generate-pools.ts`）與內容層回歸測試
- 可擴充題型 taxonomy 與領域 skill；挑戰 frontmatter 新增選填 `reference_solution` 欄位
- Ch1 Appendix Python 關鍵字完整參考表；`lit-fetcher` / `ref-verifier` 學術文獻管理工具；`pnpm gen:keymaterial` 指令

### Changed

- 測資池改用 challenge slug 隔離：同 `algorithm` 的不同題目不再共用池檔，避免互相覆寫測資
- Release 產物名由 `crypto-challenge-*` 改為 `fhsh-py-dojo-*`；預設挑戰題名 fallback 由「密碼學挑戰 #N」改為中性的「挑戰 #N」
- AI agent 指令檔（`CLAUDE.md` / `AGENTS.md` / `GEMINI.md`）領域化並補上專案領域指南；統一文件標示 Node.js 22+、新增題目 SOP 以 `pnpm new-challenge` 為首選

### Fixed

- 移除壞掉且有害的 npm `wasm-pack` 相依，改由 PATH 提供（本機 cargo、release CI 用 `jetli/wasm-pack-action`）；並修正 CI 因 wasm-pack postinstall 404 而安裝失敗
- 以自建整合取代 `vitepress-plugin-mermaid`，修復頁面崩潰；修復 `password-check` 測資池生成失敗
- 修正乘法表 generator 的對齊格式

### Security

- 答案金鑰零外洩：作答紀錄於寫入與匯出時皆依測資池 `verdict_detail` 雙重過濾，隱藏題的期望輸出絕不進入下載檔；匯出 Markdown 以變動長度 code fence 與 table／inline 逸出，防止學生輸出偽造報告結構或注入 LLM

### Removed

- 移除無呼叫端的 `useApi` / `useWsApi` composable 死碼與 `.gitignore` 指向已更名 crate 的失效規則

## [1.0.0] - 2026-04-05

### Added

- 初始化「台北市立復興高級中學 Python 自學道場」專案
- 基於 crypto-challenge 架構建立 Python Judge 系統（Rust/WASM + Pyodide）
- 新增 `useApi` / `useWsApi` composable（VueUse useFetch / useWebSocket wrapper）
