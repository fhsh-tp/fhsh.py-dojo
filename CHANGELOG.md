# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [1.2.0] - 2026-07-25

新增可持久化的編輯器設定與資料結構挑戰題系列首題，並修復下載紀錄面板被裁切等多項 UI 問題。

### Added

- **編輯器設定**：齒輪選單可切換「自動完成」與「括號自動閉合」，設定存於瀏覽器並即時生效
- **編輯器字型大小調整**：設定選單內以步進器調整程式編輯器字級（10–24px），即時套用且保留游標與復原歷史
- **新挑戰題「撲克牌重排計數」**（id 55，hard／競賽題型）：資料結構系列首題，採 APCS 多筆資料輸入格式與空白起始程式碼；極限測資讓暴力模擬必然逾時，引導以找規律推導公式作答

### Fixed

- 下載紀錄面板被編輯器下方區域裁切、預設高度下看不到欄位與按鈕：面板改為向上開啟並完整可見（抽出 `useAnchoredPopover` 共用 composable），同時補上點擊外部／Escape 關閉、與設定選單互斥、關閉重開保留已填資料、鍵盤 Tab 可達與焦點歸還等行為
- 編輯器設定選單在拖曳結果區分隔線時與齒輪按鈕脫離的問題
- 字型步進器在達到字級上下限時焦點脫離選單的問題
- 測資池建置在大整數答案題型（如 2^N）下因子行程輸出緩衝不足而以 ENOBUFS 失敗的問題

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
