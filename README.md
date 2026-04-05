<div align="center">

# 🐍 Python 自學道場

**台北市立復興高級中學 Python 自學道場**

[![Version](https://img.shields.io/badge/version-v1.0.0-blue)](https://github.com/fhsh-tp/fhsh.py-dojo)
[![License](https://img.shields.io/badge/License-ECL--2.0-green)](./LICENSE)
[![VitePress](https://img.shields.io/badge/VitePress-2.x_alpha-646cff?logo=vite)](https://vitepress.dev)
[![Node](https://img.shields.io/badge/Node-22+-339933?logo=node.js)](https://nodejs.org)
[![pnpm](https://img.shields.io/badge/pnpm-10-f69220?logo=pnpm)](https://pnpm.io)

[快速開始](#快速開始) ❖ [新增題目](#新增題目) ❖ [部署](#部署)

</div>

---

## 簡介

Python 自學道場是一個完全運行於瀏覽器端的 Python 程式設計練習平台，無需後端伺服器。學生以 Python 撰寫解答，測試案例由 **Rust/WASM** 產生器即時生成，程式碼透過 **Pyodide**（WebAssembly Python）在 Web Worker 中執行與驗證。

```
學生撰寫 Python → Rust/WASM 產生測試輸入 → Pyodide 執行驗證 → 即時顯示結果
```

GitHub 倉庫：<https://github.com/fhsh-tp/fhsh.py-dojo>

## 功能特色

- **全瀏覽器執行** — 零後端依賴，Pyodide + WASM 處理所有運算
- **即時測試驗證** — 隨機產生測試案例，每次解題結果均不同
- **分割視窗 IDE** — 左側題目說明 / 右側 CodeMirror 6 編輯器（含 Python autocomplete）
- **難度分級篩選** — 簡單 / 中等 / 困難
- **frontmatter 定義題目** — 無需修改設定檔，一個 Markdown 檔即為一道題

## 技術架構

| 層次 | 技術 |
|------|------|
| 靜態站框架 | [VitePress](https://vitepress.dev) 2.x alpha |
| 前端 | [Vue 3](https://vuejs.org) + TypeScript |
| 樣式 | [Tailwind CSS 4](https://tailwindcss.com) + Typography |
| 狀態管理 | [Pinia](https://pinia.vuejs.org) |
| 程式碼編輯器 | [CodeMirror 6](https://codemirror.net) |
| Python 執行環境 | [Pyodide](https://pyodide.org) 0.29（WebAssembly） |
| 測試案例產生器 | Rust + [wasm-bindgen](https://rustwasm.github.io/wasm-bindgen/) |
| 測試框架 | [Vitest](https://vitest.dev) + Vue Test Utils |
| 套件管理 | [pnpm](https://pnpm.io) 10 |

## 快速開始

### 前置需求

- [Node.js](https://nodejs.org) 22+
- [pnpm](https://pnpm.io) 10+
- [Rust](https://rustup.rs) 工具鏈 + wasm-pack
- [Python](https://www.python.org) 3.10+（用於 pool generation）

```bash
cargo install wasm-pack
pip install -r requirements.txt
```

### 安裝

```bash
pnpm install
```

### 開發

```bash
pnpm dev
```

啟動後開啟 `http://localhost:5173`。首次執行會依序：

1. **編譯 Rust/WASM 模組**（`pnpm build:wasm`）
2. **下載 Pyodide 執行時期**（`pnpm build:pyodide`）

> [!NOTE]
> Pyodide 需要 `SharedArrayBuffer`，本地開發伺服器已自動設定 COOP / COEP 安全標頭。請使用 Chromium 系瀏覽器（Chrome / Edge）。

### 建置

```bash
pnpm build          # 建置完整靜態站（WASM + Pyodide + VitePress）
pnpm docs:preview   # 預覽建置結果
```

### 測試

```bash
pnpm test
```

## 新增題目

每道題目以一個 Markdown 檔案定義，位於 `docs/challenge/<slug>.md`。詳細格式說明請參閱 [Usage.md](./Usage.md)。

## 部署

### GitHub Actions Release

推送版本標籤（`v*`）或發佈 Release 時自動建置並打包為 `.tar.gz` 與 `.zip`。

### 靜態 Hosting

建置產物（`.vitepress/dist/`）可部署至任何靜態 hosting，但**必須設定以下 HTTP 安全標頭**：

| Header | 值 |
|--------|-----|
| `Cross-Origin-Opener-Policy` | `same-origin` |
| `Cross-Origin-Embedder-Policy` | `require-corp` |

## 專案結構

```
fhsh.py-dojo/
├── .vitepress/
│   ├── config.mts               # VitePress + Vite 設定
│   └── theme/
│       ├── components/          # challenge、editor、layout 元件
│       ├── views/               # ChallengeView、ChallengeListView
│       ├── stores/              # Pinia stores
│       ├── composables/         # useWasm、useExecutor、useApi 等
│       ├── workers/             # Pyodide Web Worker
│       └── __tests__/           # Vitest 測試
├── docs/
│   ├── index.md                 # 首頁
│   ├── challenge/               # 題目 Markdown（每檔即一道題）
│   └── public/                  # WASM / Pyodide 執行時期（gitignored）
├── testcase-generator/          # Rust crate（產生隨機測試輸入）
└── scripts/                     # 建置腳本
```

## 授權

Copyright 2026 MIS@FHSH（臺北市立復興高級中學資訊組）

本專案採用 [Educational Community License, Version 2.0 (ECL-2.0)](./LICENSE) 授權條款。
