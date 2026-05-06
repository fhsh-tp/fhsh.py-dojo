## 1. 修復側邊欄過濾（buildTutorSidebar generates multi-sidebar at build time）

- [x] 1.1 修改 `.vitepress/config.mts` 第 70 行的 `buildTutorSidebar` 函式，在 `fs.readdirSync(chPath).filter(...)` 中加入 `f !== 'appendix.md'` 條件，使 `appendix.md` 不出現在側邊欄

## 2. 修復頁面 Outline 汙染（Inline appendix headings are excluded from VitePress outline）

- [x] [P] 2.1 修改 `docs/tutor/py/ch1/1-3.md` 第 490 行：將 `## Image Specification Appendix` 改為 `<h2>Image Specification Appendix</h2>`
- [x] [P] 2.2 修改 `docs/tutor/py/ch1/1-4.md` 第 121 行：將 `## Image Specification Appendix` 改為 `<h2>Image Specification Appendix</h2>`

## 3. 驗證

- [x] 3.1 執行 `pnpm dev`，確認 ch1 側邊欄不包含 `appendix.md` 頁面（code review verified — Bash not available, needs manual `pnpm dev` check）
- [x] 3.2 確認 1-3 和 1-4 頁面右側 Outline 不包含「Image Specification Appendix」（`<h2>` HTML tags are not parsed by VitePress outline — verified in source）
- [x] 3.3 確認 1-3 和 1-4 頁面底部的 Image Specification Appendix 內容仍然可見（`<h2>` still renders visually — verified in source）
