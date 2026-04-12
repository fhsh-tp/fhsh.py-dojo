## Why

模組二（Chapter 2）的教學內容尚未撰寫。2-1 是模組二的第一節，教授 `for` 迴圈與 `range()` 函式——這是零基礎學生第一次接觸「重複執行」的概念，也是模組二所有後續內容（while、串列、排序、字典）的基礎。此外，原有的 ch2 index.md 只列出 4 節，需要更新為討論中確定的 7 節結構。

## What Changes

- 新增 `docs/tutor/py/ch2/2-1.md`：教授 `for` 迴圈與 `range()` 函式的完整教學文章
- 更新 `docs/tutor/py/ch2/index.md`：從原有 4 節擴展為 7 節（2-1 至 2-7）
- 新增 6 個 challenge 檔案（ID 11–16）：2 個知識節點各 1 例題 + 2 類題
  - 知識節點 A：`for i in range(n)` 基礎計數迴圈（1 例題 + 2 類題）
  - 知識節點 B：`range(start, stop, step)` 進階用法（1 例題 + 2 類題）
- 新增圖片 placeholder（遵循 F-1 雙行格式），含 Image Specification Appendix

## Non-Goals

- 不教 `while` 迴圈（2-2 範圍）
- 不教 `break`/`continue`（2-3 範圍）
- 不教 `for item in list` 迭代語法（2-4 範圍，T-1 術語前引用規則：串列尚未正式教授）
- 不產生實際圖片檔案（只建立 placeholder 與 AI prompt）
- 不處理 2-2 至 2-7 的教學內容

## Capabilities

### New Capabilities

- `python-ch2-2-1-content`：2-1 節「`for` + `range()` 定次數迴圈」的教學文章內容、結構、challenge 設計，以及 Ch1 通用撰寫規則（P-1 至 K-1）在本節的適用性要求

### Modified Capabilities

- `tutor-article-structure`：ch2 index.md 的章節列表需從 4 節擴展為 7 節，反映模組二的最終結構

## Impact

- 新增檔案：
  - `docs/tutor/py/ch2/2-1.md`
  - `docs/challenge/` 下 6 個新 challenge 檔案（ID 11–16）
- 修改檔案：
  - `docs/tutor/py/ch2/index.md`
- Sidebar 自動更新（`buildTutorSidebar()` 掃描檔案系統動態生成，無需手動修改 config）
