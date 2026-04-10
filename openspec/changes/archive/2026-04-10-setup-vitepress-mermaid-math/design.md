## Context

VitePress 2.0.0-alpha.16 不內建 Mermaid 渲染。社群標準做法是使用 `vitepress-plugin-mermaid`（wraps `mermaid` library）。LaTeX 數學則透過 VitePress 官方支援的 `markdown-it-mathjax3` 套件啟用。

目前 `.vitepress/config.mts` 有嚴格的 CSP policy（`script-src 'self' 'unsafe-inline' 'wasm-unsafe-eval'`），Mermaid 和 MathJax 均在 client-side 渲染 SVG/CSS，可能與 CSP 衝突。

## Goals / Non-Goals

**Goals:**

- 讓 ```` ```mermaid ```` code block 在 VitePress dev server 和 build output 中正確渲染為 SVG 圖表
- 讓 `$...$` 和 `$$...$$` 語法正確渲染為數學公式
- 維持 CSP 安全性，僅放寬必要的規則

**Non-Goals:**

- 不自訂 Mermaid 主題（後續 change 處理）
- 不修改任何教學 Markdown 內容
- 不處理 Mermaid 的 SSR/SSG 預渲染（client-side 渲染即可）

## Decisions

### D1: Mermaid plugin 選擇 → `vitepress-plugin-mermaid`

唯一成熟的 VitePress Mermaid 整合方案。它在 theme `enhanceApp` 中註冊 Mermaid 元件，將 ```` ```mermaid ```` code block 自動替換為渲染後的 SVG。

**整合方式**：在 `.vitepress/config.mts` 中使用 `withMermaid()` wrapper 包裹 `defineConfig()`。

### D2: Math 啟用方式 → `markdown: { math: true }`

VitePress 官方支援。安裝 `markdown-it-mathjax3` 後，在 config 中設定 `markdown: { math: true }` 即可。不需要額外的 theme 設定。

### D3: CSP 調整策略

Mermaid 使用 inline `<style>` 和動態建立 SVG，MathJax 同樣注入 inline style。目前 CSP 已有 `style-src 'self' 'unsafe-inline'`，應足以涵蓋兩者。

**策略**：先不修改 CSP，安裝後在 dev server 測試。若 console 出現 CSP violation，再針對性放寬 `img-src`（加入 `data:` 已有）或 `font-src`。

### D4: 套件安裝方式 → pnpm devDependencies

三個套件均為建置時依賴：
- `vitepress-plugin-mermaid`
- `mermaid`
- `markdown-it-mathjax3@^4`

使用 `pnpm add -D` 安裝。

## Risks / Trade-offs

| 風險 | 影響 | 緩解 |
|------|------|------|
| `vitepress-plugin-mermaid` 與 VitePress 2.0.0-alpha.16 不相容 | Mermaid 無法渲染 | 安裝後立即測試；若不相容，改用手動 Mermaid client-side init |
| CSP violation 阻擋 Mermaid/MathJax 渲染 | 圖表/公式顯示為空白 | dev server 測試時檢查 console，按需調整 CSP |
| `markdown-it-mathjax3` 與其他 markdown-it plugin 衝突 | 數學公式渲染異常 | 目前專案無自訂 markdown-it plugin，風險低 |
