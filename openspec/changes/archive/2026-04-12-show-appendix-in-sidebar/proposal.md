## Why

`appendix.md` 目前被 `buildTutorSidebar` 刻意排除在側邊欄之外，導致學生必須知道直接 URL 才能瀏覽關鍵字表與圖片規格揭露內容。同時，圖片規格揭露區塊以無序清單呈現，不利於逐項索引對照；改為有序清單後，學生可用編號快速定位特定圖片的規格說明，且格式與 Slidev 有序清單語法（標準 Markdown `1. 2. 3.`）完全相容，未來製作投影片時可直接引用。

## What Changes

- **`config.mts`**：移除 `buildTutorSidebar` 對 `appendix.md` 的排除過濾（`f !== 'appendix.md'`），使 appendix 依字母順序自然排在 `reference.md` 之前（`a < r`）出現於側邊欄
- **`docs/tutor/py/ch1/appendix.md`**：將「Image Specification Appendix」區塊中各圖片的屬性清單（`- **類型**`、`- **意圖**`、`- **完整 Prompt**`、`- **備註**`）從無序清單改為有序清單（`1. 2. 3. 4.`）
- **`openspec/specs/site-nav-sidebar/spec.md`**：移除「appendix.md is excluded from sidebar」情境，新增「appendix appears before reference in sidebar」情境

## Non-Goals

- 不修改 `appendix.md` 的內容或章節標題
- 不修改 Python Keywords Table 的表格格式（該區塊已是表格，不涉及清單格式）
- 不新增其他章節的 appendix 檔案
- 不引入 Slidev 專案或投影片檔案至此 repo

## Capabilities

### New Capabilities

（無）

### Modified Capabilities

- `site-nav-sidebar`：移除 appendix.md 的側邊欄排除規則；新增 appendix 必須出現且位於 reference 之前的情境
- `python-ch1-content`：appendix 的 Image Specification Appendix 區塊格式由無序清單改為有序清單

## Impact

- Affected specs: `site-nav-sidebar`、`python-ch1-content`
- Affected code: `.vitepress/config.mts`、`docs/tutor/py/ch1/appendix.md`
