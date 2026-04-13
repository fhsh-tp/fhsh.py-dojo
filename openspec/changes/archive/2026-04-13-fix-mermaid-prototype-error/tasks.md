## 1. 建立自建 Mermaid 整合元件

- [x] [P] 1.1 建立 `.vitepress/plugins/markdown-mermaid.ts`：實作 D5: markdown-it fence rule 覆寫策略——保存原始 `fence` rule 引用（使用 `.bind(md.renderer.rules)`），覆寫為自訂函式。若 `token.info.trim() === 'mermaid'`（或 `'mmd'`），輸出 `<ClientOnly><MermaidDiagram id="mermaid-${idx}" graph="${encodeURIComponent(content)}" /></ClientOnly>`（D3: 使用 `<ClientOnly>` 包裝而非 `<Suspense>`）；否則委派給原始 renderer。函式簽名：`(md: any) => void`（D7：VitePress 2.x 不公開導出 MarkdownItAsync，參考 strip-generator.ts 的 inline type 模式）。確保「Mermaid code blocks render as SVG diagrams」spec 中 fence 轉換的部分
- [x] [P] 1.2 建立 `.vitepress/theme/components/MermaidDiagram.vue`：依據 D7: 元件 Props 介面與 mermaid 安全設定，Props 為 `graph: string`（URI 編碼的 mermaid 原始碼）和 `id: string`（唯一識別碼）。實作 D2: 使用動態 `import('mermaid')` 而非靜態 import，在 `onMounted` 中載入 mermaid 庫。呼叫 `mermaid.initialize({ startOnLoad: false, securityLevel: 'loose', theme })` 後以 `mermaid.render(id, decodeURIComponent(graph))` 渲染。實作 D4: MutationObserver 監聽深色/淺色模式切換（`attributeFilter: ['class']`）。在 `onUnmounted` 中 `observer.disconnect()`。Error handling：catch `mermaid.render()` 失敗並顯示 `<pre>` 錯誤訊息，以滿足「Invalid Mermaid syntax shows error gracefully」scenario。使用 salt trick 強制 v-html 更新

## 2. 更新設定與註冊

- [x] [P] 2.1 更新 `.vitepress/config.mts`：D1: 移除 `vitepress-plugin-mermaid`，以自建整合取代——移除 `import { withMermaid }` 和 `withMermaid()` wrapper，新增 `import { mermaidPlugin }` 從 `'./plugins/markdown-mermaid'` 並在 `markdown.config` callback 中呼叫。D6: 不複製 `withMermaid()` 的 `optimizeDeps.include` 與 `resolve.alias`（動態 import 使 Vite 自動處理依賴預打包）。確保「Mermaid plugin is registered via withMermaid wrapper」modified requirement 中「Config uses markdown.config with mermaid plugin」scenario
- [x] [P] 2.2 更新 `.vitepress/theme/index.ts`：import 並全域註冊 `MermaidDiagram` 元件，確保「MermaidDiagram component is registered globally」scenario 與「Mermaid plugin is registered via withMermaid wrapper」modified requirement

## 3. 依賴清理

- [x] 3.1 執行 `pnpm remove vitepress-plugin-mermaid` 移除不相容套件，確保「Mermaid packages are installed as devDependencies」spec 中 `vitepress-plugin-mermaid` SHALL NOT be present 的要求

## 4. 驗證

- [x] 4.1 執行 `pnpm docs:build` 確認建置成功且無 TypeError 或 mermaid 相關錯誤（驗證「Mermaid loads only in browser context」scenario）
- [x] 4.2 執行 `pnpm typecheck` 確認型別檢查通過
- [x] 4.3 使用 `pnpm docs:preview` 手動驗證 `/tutor/py/ch1/1-3`（flowchart，含 classDef）和 `/tutor/py/ch1/1-4`（mindmap，含 `%%{init:...}%%`）正常渲染（驗證「Mermaid code blocks render as SVG diagrams」spec）。注意：1-4.md 的 `%%{init:...}%%` 指令會覆蓋深色模式主題設定，此為 mermaid 原生行為，非 regression。確認 1-3.md 的深色/淺色模式切換正常重新渲染（驗證「Dark mode toggle re-renders diagrams」scenario）
