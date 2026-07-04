# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- Python 自學課程內容：第一、二章教學文章與互動練習題
- APCS 素養導向題型範本與相關規格
- 自動化品質守門 CI（`.github/workflows/ci.yml`）：typecheck、lint、vitest、cargo test
- 雙測資產生器一致性測試（Rust `rng.rs` ↔ Python `generate-pools.ts`）與內容層回歸測試
- 挑戰 frontmatter 新增選填 `reference_solution` 欄位（供正解對正式測資池回歸驗證）
- `pnpm gen:keymaterial` 指令：獨立產生 `testcase-generator/src/key_material.rs`
- AI agent 指令檔（`CLAUDE.md` / `AGENTS.md` / `GEMINI.md`）新增專案領域指南段落

### Changed

- Release 產物名由 `crypto-challenge-*` 改為 `fhsh-py-dojo-*`
- 統一文件：Node.js 版本標示為 22+、新增題目 SOP 以 `pnpm new-challenge` 為首選
- 預設挑戰題名 fallback 由「密碼學挑戰 #N」改為中性字樣「挑戰 #N」

### Removed

- 移除無呼叫端的 `useApi` / `useWsApi` composable 死碼
- 移除 `.gitignore` 指向已更名 crate 的失效規則

### Fixed

- 修正測資池命名碰撞：改用 challenge slug 隔離各題目的測資池檔，避免同 `algorithm` 題目互相覆寫測資
- 修正乘法表 generator 的對齊格式

## [1.0.0] - 2026-04-05

### Added

- 初始化「台北市立復興高級中學 Python 自學道場」專案
- 基於 crypto-challenge 架構建立 Python Judge 系統（Rust/WASM + Pyodide）
- 新增 `useApi` / `useWsApi` composable（VueUse useFetch / useWebSocket wrapper）
