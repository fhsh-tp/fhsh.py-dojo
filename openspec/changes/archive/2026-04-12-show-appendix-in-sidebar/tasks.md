## 1. 修改 buildTutorSidebar — appendix 納入側邊欄

- [x] [P] 1.1 在 `.vitepress/config.mts` 的 `buildTutorSidebar` 函式中，找到第 71 行的 `.filter(f => f.endsWith('.md') && f !== 'appendix.md')`，移除 `&& f !== 'appendix.md'` 條件（即移除「appendix.md is excluded from sidebar」的舊行為），使 appendix.md 依字母順序（a < r）自然排在 reference.md 之前，滿足「buildTutorSidebar generates multi-sidebar at build time」與「appendix appears in sidebar before reference」規格

## 2. 重新格式化 appendix.md 的圖片規格清單

- [x] [P] 2.1 開啟 `docs/tutor/py/ch1/appendix.md`，在「Image Specification Appendix」區塊中，將每個圖片條目的四項屬性（`- **類型**`、`- **意圖**`、`- **完整 Prompt**`、`- **備註**`）由無序清單改為有序清單（`1. **類型**`、`2. **意圖**`、`3. **完整 Prompt**`、`4. **備註**`），滿足「Chapter 1 appendix image specifications use ordered lists」規格；格式為標準 Markdown 有序清單，無需任何 Slidev 專屬語法即可在 VitePress 與 Slidev 中正確渲染，滿足「Ordered list is valid Slidev-compatible Markdown」規格
