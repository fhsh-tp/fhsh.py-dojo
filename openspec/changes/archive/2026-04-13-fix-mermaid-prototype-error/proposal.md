## Problem

Staging 站台（`staging.fhsh-py-dojo.pages.dev`）在所有頁面發生 client-side 崩潰：

```
Uncaught (in promise) TypeError: Cannot set properties of undefined (setting 'prototype')
    at Zo (app.4jdnPvUu.js:123:14406)
```

字體預載入警告（`inter-roman-latin.Di8DUHzh.woff2 was preloaded but not used`）為次要症狀——頁面在字體被使用前已崩潰。

## Root Cause

`vitepress-plugin-mermaid@2.0.17` 與 VitePress 2.0.0-alpha.16 **不相容**：

1. 該套件的 `peerDependencies` 宣告 `"vitepress": "^1.0.0 || ^1.0.0-alpha"`，明確排除 2.x
2. 套件使用 Vite `transform` hook 將 `import Mermaid from 'vitepress-plugin-mermaid/Mermaid.vue'` 注入 VitePress 的 client app 入口檔
3. 此注入導致 `mermaid@11.14.0` 在 bundle 初始化階段被立即載入，其模組初始化程式碼在 VitePress 2.x 模組結構中失敗
4. 該套件沒有支援 VitePress 2.x 的新版本（2.0.17 為最新版）

原始設計文件（`openspec/changes/archive/2026-04-10-setup-vitepress-mermaid-math/design.md` 第 52 行）已預見此風險，並記錄了緩解策略：「若不相容，改用手動 Mermaid client-side init」。

## Proposed Solution

移除 `vitepress-plugin-mermaid`，以自建整合方案取代（2 個新檔案、2 個修改檔案、1 個依賴移除）：

1. **自建 markdown-it 外掛**（`.vitepress/plugins/markdown-mermaid.ts`）：覆寫 `fence` renderer rule，將 ` ```mermaid ` 區塊轉換為 `<ClientOnly><MermaidDiagram>` 元件
2. **自建 Vue 元件**（`.vitepress/theme/components/MermaidDiagram.vue`）：在 `onMounted` 中動態 `import('mermaid')`，確保 mermaid 只在瀏覽器端載入、不在 SSR 中執行
3. **更新 VitePress 設定**（`.vitepress/config.mts`）：移除 `withMermaid()` wrapper，改用 `markdown.config` 註冊自建 markdown-it 外掛
4. **更新主題註冊**（`.vitepress/theme/index.ts`）：全域註冊 `MermaidDiagram` 元件

此方案完全遵循原始設計文件的緩解策略。

## Success Criteria

- `pnpm docs:build` 成功且無錯誤
- 所有頁面不再出現 TypeError
- `/tutor/py/ch1/1-3`（流程圖，含 `classDef` 自訂樣式）正常渲染
- `/tutor/py/ch1/1-4`（心智圖，含 `%%{init:...}%%` 指令）正常渲染
- 深色/淺色模式切換時圖表重新渲染
- `pnpm typecheck` 通過

## Capabilities

### New Capabilities

（無）

### Modified Capabilities

- `vitepress-mermaid-support`：將 Mermaid 整合方式從 `vitepress-plugin-mermaid` 套件改為自建的 markdown-it 外掛 + Vue 元件。修改「Mermaid plugin is registered via withMermaid wrapper」requirement 改用 `markdown.config` 機制。修改「Mermaid packages are installed as devDependencies」移除 `vitepress-plugin-mermaid`。修改「Mermaid code blocks render as SVG diagrams」新增 browser-only loading 和深色模式切換 scenarios。Mermaid 渲染行為維持不變。

## Impact

- 受影響程式碼：
  - `.vitepress/config.mts`（移除 withMermaid wrapper，新增 markdown.config）
  - `.vitepress/theme/index.ts`（新增 MermaidDiagram 元件註冊）
  - `.vitepress/plugins/markdown-mermaid.ts`（新增）
  - `.vitepress/theme/components/MermaidDiagram.vue`（新增）
- 受影響依賴：`vitepress-plugin-mermaid`（移除）、`mermaid`（保留）
- 受影響規格：`vitepress-mermaid-support`（更新整合方式相關 requirements）
