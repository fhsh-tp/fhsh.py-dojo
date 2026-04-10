## 1. 安裝套件（D4: 套件安裝方式 → pnpm devDependencies）

- [x] [P] 1.1 執行 `pnpm add -D vitepress-plugin-mermaid mermaid` 安裝 Mermaid packages（對應 spec: Mermaid packages are installed as devDependencies）
- [x] [P] 1.2 執行 `pnpm add -D markdown-it-mathjax3@^4` 安裝 MathJax package（對應 spec: MathJax package is installed as devDependency）

## 2. 設定 VitePress Config

- [x] 2.1 D1: Mermaid plugin 選擇 → `vitepress-plugin-mermaid`：修改 `.vitepress/config.mts`，import `withMermaid` from `vitepress-plugin-mermaid`，並將 `defineConfig()` 的 `export default` 包裹為 `withMermaid(defineConfig({...}))`（對應 spec: Mermaid plugin is registered via withMermaid wrapper）
- [x] 2.2 D2: Math 啟用方式 → `markdown: { math: true }`：修改 `.vitepress/config.mts`，在 `defineConfig()` 內新增 `markdown: { math: true }` 設定（對應 spec: Math support is enabled via markdown config）

## 3. 驗證

- [x] 3.1 建立臨時測試頁面 `docs/test-mermaid-math.md`，包含一個 mermaid flowchart code block 和一個 `$E=mc^2$` inline math，啟動 dev server 確認兩者均正確渲染（對應 spec: Mermaid code blocks render as SVG diagrams、LaTeX math expressions render in Markdown）
- [x] 3.2 D3: CSP 調整策略：確認 dev server console 無 CSP violation 錯誤，驗證現有 CSP policy 與 Mermaid/MathJax 相容
- [x] 3.3 刪除臨時測試頁面 `docs/test-mermaid-math.md`
