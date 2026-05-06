## 1. Mermaid 主題配色設計

- [x] 1.1 使用 `/ui-ux-pro-max` 技能，為教學用 Mermaid 圖表設計一套適合高中生的主題配色方案（需考慮 light/dark mode、色彩對比度、可讀性），產出 Mermaid `%%{init: {'theme': '...', 'themeVariables': {...}}}%%` 配置

## 2. 閏年流程圖轉換（Section 1-3 uses Mermaid flowchart for leap year logic）

- [x] 2.1 實作 Section 1-3 uses Mermaid flowchart for leap year logic：將 `docs/tutor/py/ch1/1-3.md` line 280-306 的 ASCII art 流程圖替換為 Mermaid `flowchart TD` 語法，保留三個菱形判斷節點（`year % 400 == 0`、`year % 100 == 0`、`year % 4 == 0`）、Yes/No 分支標籤、以及「閏年」「平年」終端節點
- [x] 2.2 將 Task 1.1 產出的主題配色套用至閏年流程圖

## 3. 知識地圖轉換（Section 1-4 uses Mermaid mindmap for knowledge map）

- [x] 3.1 實作 Section 1-4 uses Mermaid mindmap for knowledge map：將 `docs/tutor/py/ch1/1-4.md` line 35-56 的 ASCII art 樹狀圖替換為 Mermaid `mindmap` 語法，保留根節點「程式語言（Python）」、三個分支節點（1-1 I/O 基礎、1-2 資料與運算、1-3 流程控制）及各自的技能子節點
- [x] 3.2 將 Task 1.1 產出的主題配色套用至知識地圖

## 4. 驗證

- [x] 4.1 啟動 dev server，瀏覽 1-3 頁面確認閏年流程圖正確渲染為 Mermaid SVG，邏輯結構與原 ASCII art 一致
- [x] 4.2 瀏覽 1-4 頁面確認知識地圖正確渲染為 Mermaid mindmap SVG，所有技能節點完整保留
