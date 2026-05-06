## Context

VitePress 2.0.0-alpha.16 專案使用 `vitepress-plugin-mermaid@2.0.17` 整合 Mermaid 圖表渲染。該套件的 `peerDependencies` 宣告 `"vitepress": "^1.0.0 || ^1.0.0-alpha"`，明確不支援 VitePress 2.x。套件透過 Vite `transform` hook 將 Mermaid 元件的 import 注入 VitePress client app 入口檔，導致 `mermaid@11.14.0` 在 bundle 初始化時被立即載入並崩潰。

目前有 2 個 Markdown 檔案使用 Mermaid 圖表：
- `docs/tutor/py/ch1/1-3.md:280`：flowchart（含 `classDef` 自訂樣式）
- `docs/tutor/py/ch1/1-4.md:33`：mindmap（含 `%%{init:...}%%` 主題指令）

現有架構：`withMermaid()` wrapper → Vite transform hook → 立即載入 mermaid → 崩潰。

## Goals / Non-Goals

**Goals:**

- 修復 TypeError，使所有頁面正常載入
- Mermaid 圖表（flowchart、mindmap）在 dev server 和 production build 中正常渲染為 SVG
- 支援深色/淺色模式切換時重新渲染
- 維持 `classDef` 自訂樣式和 `%%{init:...}%%` 指令的支援
- 維持 CSP policy 相容性

**Non-Goals:**

- 不處理 Mermaid SSR/SSG 預渲染（維持 client-side 渲染）
- 不清理 mermaid 的 transitive dependencies（`cytoscape`、`dayjs` 等，留待後續處理）
- 不處理 `inter-roman-latin.woff2` 字體預載入警告（預期為 TypeError 的次要症狀，修復後自動消失）
- 不自訂 Mermaid 主題（超出修復範圍）

## Decisions

### D1: 移除 `vitepress-plugin-mermaid`，以自建整合取代

**選擇**：移除套件，自建 markdown-it 外掛 + Vue 元件。

**替代方案考量**：
- 降級 VitePress 至 1.x → 功能退化、影響範圍過大
- Fork 並修補該套件 → 維護負擔高，且套件架構本身使用不穩定的 Vite transform hack
- 等待套件更新 → 該套件無 VitePress 2.x 支援的跡象

**理由**：原設計文件已預見此風險並指定此為緩解策略。自建整合僅需 2 個檔案，邏輯簡單可控。

### D2: 使用動態 `import('mermaid')` 而非靜態 import

**選擇**：在 Vue 元件的 `onMounted` 中使用 `const { default: mermaid } = await import('mermaid')`。

**理由**：
- 確保 mermaid 只在瀏覽器端載入、不在 SSR/build 階段執行
- 避免 mermaid 模組初始化程式碼在不適當的環境中執行
- 瀏覽器端 lazy loading，僅在有 Mermaid 圖表的頁面才載入 800KB+ 的 mermaid 庫

### D3: 使用 `<ClientOnly>` 包裝而非 `<Suspense>`

**選擇**：markdown-it 外掛輸出 `<ClientOnly><MermaidDiagram .../></ClientOnly>`。

**理由**：`ClientOnly` 是 VitePress 內建元件，保證跳過 SSR。原套件使用 `<Suspense>` 是因為元件有 async setup，但我們的元件使用 `onMounted` + 動態 import，不需要 `<Suspense>`。

### D4: MutationObserver 監聽深色/淺色模式切換

**選擇**：在 `onMounted` 中建立 `MutationObserver`，監聽 `document.documentElement` 的 `class` attribute 變化。

**理由**：VitePress 透過在 `<html>` 上切換 `.dark` class 來實現深色模式。MutationObserver 是最可靠的偵測方式，與 VitePress 的實作解耦。使用 `attributeFilter: ['class']` 限縮觸發範圍。

### D5: markdown-it fence rule 覆寫策略

**選擇**：保存原始 `fence` rule 的引用，覆寫為自訂函式。若 `token.info.trim() === 'mermaid'`，輸出元件 HTML；否則委派給原始 renderer。

**理由**：與原套件相同的策略，但更簡潔。`encodeURIComponent()` 編碼圖表內容作為 prop 傳遞，安全處理特殊字元和換行。

### D6: 不複製 `withMermaid()` 的 `optimizeDeps.include` 與 `resolve.alias`

**選擇**：移除 `withMermaid()` 後，不在 `config.mts` 中手動加回 `optimizeDeps.include`（`@braintree/sanitize-url`、`dayjs`、`debug`、`cytoscape-cose-bilkent`、`cytoscape`）和 `resolve.alias`（`dayjs/plugin/*.js` → ESM、`cytoscape/dist/cytoscape.umd.js` → ESM）。

**理由**：
- 原套件需要這些設定是因為它透過 Vite `transform` hook 在建置時注入靜態 import，Vite 的依賴掃描器無法偵測到這些注入的 import，因此需要手動指定 `optimizeDeps.include` 強制預打包
- 我們的方案改用 `import('mermaid')` 動態 import，Vite 的依賴掃描器**可以**偵測到動態 import 並自動處理預打包
- `resolve.alias`（CJS → ESM 路徑映射）同樣不需要，因為 Vite 在處理動態 import 的 chunk 時會正確解析 mermaid 的內部 import
- 目前僅使用 flowchart 和 mindmap 圖表類型，不觸及 gantt（使用 dayjs CJS 路徑的主要場景）

**風險**：若未來新增 gantt 圖表時出現 CJS 解析問題，可於該時再加入對應的 `resolve.alias`。此為已知且可控的風險。

### D7: 元件 Props 介面與 mermaid 安全設定

**元件 Props**：
- `graph`（`string`，必要）：以 `encodeURIComponent()` 編碼的 mermaid 圖表原始碼
- `id`（`string`，必要）：每個圖表的唯一識別碼（如 `mermaid-0`、`mermaid-1`），由 markdown-it 外掛根據 token index 自動生成

**mermaid.initialize() 設定**：
- `startOnLoad: false`：防止 mermaid 自動掃描 DOM 尋找 `.mermaid` 元素，避免與 Vue 的渲染產生競爭條件
- `securityLevel: 'loose'`：與原套件保持一致。此設定跳過 DOMPurify sanitization，允許 SVG 中的 inline event handler 和 embedded HTML。在本專案中可接受，因為 mermaid 圖表內容來自開發者自己編寫的 Markdown 檔案，非使用者輸入。若未來需要處理使用者提供的圖表，須改為 `'strict'`

**markdown-it 外掛類型**：
- VitePress 2.x 不公開導出 `MarkdownItAsync` 類型，僅導出 `MarkdownRenderer`（為 `MarkdownItAsync` 的 alias）
- 外掛函式簽名應為 `(md: any) => void`，或使用 `import type MarkdownIt from 'markdown-it'` 搭配 `(md: MarkdownIt) => void`
- 參考 `.vitepress/plugins/strip-generator.ts` 的 inline type 模式

## Risks / Trade-offs

| 風險 | 影響 | 緩解 |
|------|------|------|
| mermaid 動態載入造成圖表短暫不可見 | 使用者在頁面載入時看到 "Loading..." | 影響極短暫（mermaid 會被 Vite 打包），可接受 |
| `mermaid.render()` 使用相同 ID 重新渲染 | 切換主題時可能閃爍 | mermaid 11.x 原生支援同 ID 重新渲染，使用 salt trick 強制 v-html 更新 |
| 未來新增的 Mermaid 圖表類型未測試 | 新圖表類型可能有未預期的行為 | mermaid 庫原生支援所有圖表類型，自建整合不限制圖表類型 |
