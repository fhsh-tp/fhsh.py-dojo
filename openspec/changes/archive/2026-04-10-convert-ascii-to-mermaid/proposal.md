## Why

教學文件中有 2 處 ASCII art 圖形（閏年流程圖、模組一知識地圖），在不同裝置和字型下顯示效果不一，也無法在暗色模式下自動適配。將它們轉換為 Mermaid 圖表可以提供更好的視覺效果、互動性和主題適配能力，提升學生的學習體驗。

## What Changes

- 將 `docs/tutor/py/ch1/1-3.md`（line 280-306）的閏年判斷 ASCII 流程圖轉換為 Mermaid `flowchart TD` 語法
- 將 `docs/tutor/py/ch1/1-4.md`（line 35-56）的模組一知識地圖 ASCII 樹狀圖轉換為 Mermaid `mindmap` 語法
- 使用 `/ui-ux-pro-max` 技能設計適合高中生的 Mermaid 主題配色
- 建立 Mermaid 圖表配色規範，供後續所有教學內容使用

## Non-Goals

- 不修改 Markdown 表格（Trace Table、運算子表格等）——GFM table 已是最佳呈現方式
- 不修改 VitePress 設定或安裝套件（已由 `setup-vitepress-mermaid-math` 處理）
- 不修改 AI 生成的插圖（`![image]()` 引用）

## Capabilities

### New Capabilities

（無。）

### Modified Capabilities

- `python-ch1-content`: 1-3 節的閏年流程圖和 1-4 節的知識地圖從 ASCII art 改為 Mermaid 圖表

## Impact

- 受影響的檔案：`docs/tutor/py/ch1/1-3.md`（line 280-306）、`docs/tutor/py/ch1/1-4.md`（line 35-56）
- 前置依賴：`setup-vitepress-mermaid-math` change 必須先完成；`convert-math-to-latex` 建議先完成（因同樣修改 1-3.md，避免衝突）
