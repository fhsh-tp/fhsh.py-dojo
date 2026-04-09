## Why

`appendix.md`（AI 圖片提示詞揭露）目前被側邊欄當作一般教學頁面顯示，誤導學生。此外，1-3.md 和 1-4.md 中的 `## Image Specification Appendix` 標題會出現在頁面右側目錄（TOC/Outline），干擾閱讀體驗。

## What Changes

- 修改 `.vitepress/config.mts` 的 `buildTutorSidebar()`，過濾 `appendix.md` 使其不出現在側邊欄
- 將 `1-3.md` 和 `1-4.md` 中的 `## Image Specification Appendix` 改為 HTML `<h2>` 標籤，使 VitePress 不將其納入頁面 Outline

## Non-Goals

- 不刪除 appendix.md（內容仍需保留供 AI 圖片生成參考）
- 不修改 appendix.md 的內容本身
- 不影響未來新增的 reference.md 的側邊欄顯示

## Capabilities

### New Capabilities

（無）

### Modified Capabilities

- `site-nav-sidebar`: 側邊欄建構邏輯新增 `appendix.md` 過濾規則

## Impact

- 修改檔案：`.vitepress/config.mts`（`buildTutorSidebar` 函式第 70 行）
- 修改檔案：`docs/tutor/py/ch1/1-3.md`（第 490 行，`##` → `<h2>`）
- 修改檔案：`docs/tutor/py/ch1/1-4.md`（第 121 行，`##` → `<h2>`）
