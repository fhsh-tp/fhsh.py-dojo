## Why

教學文件中需要使用 Mermaid 圖表（流程圖、心智圖等）取代 ASCII art，並使用 LaTeX 渲染數學公式。目前 VitePress 專案尚未安裝 Mermaid 或 Math 相關套件，也未啟用對應的 Markdown 擴充。此 change 建立基礎設施，讓後續 content change 能直接使用 ```` ```mermaid ```` 和 `$...$` 語法。

## What Changes

- 安裝 `vitepress-plugin-mermaid` 和 `mermaid` 套件，啟用 VitePress Mermaid 渲染
- 安裝 `markdown-it-mathjax3` 套件，啟用 VitePress Math/LaTeX 渲染
- 修改 `.vitepress/config.mts`：註冊 Mermaid plugin、設定 `markdown: { math: true }`
- CSP header 可能需要調整，因為 Mermaid 和 MathJax 可能需要 `unsafe-inline` 或額外 CSP 規則

## Non-Goals

- 不轉換任何教學內容中的 ASCII art 或數學文字（由後續 change 處理）
- 不自訂 Mermaid 主題或配色（由後續 change 搭配 `/ui-ux-pro-max` 處理）
- 不修改任何 `.md` 教學文件

## Capabilities

### New Capabilities

- `vitepress-mermaid-support`: VitePress 專案支援在 Markdown 中使用 ```` ```mermaid ```` code block 渲染 Mermaid 圖表
- `vitepress-math-support`: VitePress 專案支援在 Markdown 中使用 `$...$`（行內）和 `$$...$$`（區塊）語法渲染 LaTeX 數學公式

### Modified Capabilities

（無。現有 CSP 已包含 `style-src 'self' 'unsafe-inline'` 和 `img-src 'self' data:`，足以涵蓋 Mermaid 與 MathJax 的 inline style 和 SVG 渲染，不需要修改。）

## Impact

- 受影響的檔案：`.vitepress/config.mts`、`package.json`、`pnpm-lock.yaml`
- 受影響的套件：新增 `vitepress-plugin-mermaid`、`mermaid`、`markdown-it-mathjax3`
