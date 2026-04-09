## Why

`ch1-polish-1-2` change 的 tasks 全部標記完成，但實際 1-2.md 仍有 11 個 TBD、6 處 P-1 違規、6 處 C-1 違規未修正。1-3.md 和 1-4.md 完全未經任何規則審計。審計發現現有 8 條規則存在定義盲點（S-2 跨 H3 邊界、P-1 判定灰色地帶），且缺少 4 條規則來覆蓋已發現但無規則可依的問題（圖片格式不一致、VitePress 語法錯誤、空 UI 元素、顏文字密度）。

此外，缺乏一個「反覆驗證」的工作流程機制，導致單輪檢查後即宣告完成，是品質逸脫的根本原因。

## What Changes

### 規則修改（2 條）

- **P-1 增補判定清單**：在現有規則下方新增 4 條具體判定條件，消除「這算不算戲劇效果」的灰色地帶
- **S-2 增補跨 H3 邊界條件**：明確定義笑話位於 H3 末尾、下一個是新 H3 heading 時，connector 的放置位置

### 規則新增（4 條）

- **F-1 圖片佔位符格式一致性**：統一所有圖片的 `![](path)` + `> 📷` 雙行格式
- **V-1 VitePress container 語法正確性**：強制 `> [!TYPE]` 語法，掃描缺少 `!` 的寫法
- **T-3 無空白 UI 元素**：禁止標題存在但內容為空的 container / callout / TIP 框
- **K-1 顏文字語氣密度**：每 30 行正文至少 1 個語氣元素，每 10 行不超過 1 個

### 工作流程新增

- **Editorial Audit Loop（EAL）**：建立迭代驗證流程——每輪逐規則掃描所有 ch1 檔案，記錄違規，修正，然後重新掃描。最多 3 輪，或違規歸零時提前終止。

### Skill 參考文件

- 撰寫 `phoenix-popular-science-article-style-enhance.md`，整合所有規則定義、判定清單、EAL 工作流程，供 Phoenix 更新其 `phoenix-popular-science-article-style` skill。

## Non-Goals

- 不在此 change 中實際執行 1-2 ~ 1-4 的內容修正（那是下一個 change 的工作）
- 不修改 challenge 題目檔案
- 不修改 VitePress 系統配置
- 不更新 `phoenix-popular-science-article-style` skill 本身（只產出參考文件）

## Capabilities

### New Capabilities

- `editorial-audit-loop`: 定義 Chapter 1 教材的迭代驗證工作流程（EAL），包含輪次上限、逐規則掃描清單、違規記錄格式、終止條件

### Modified Capabilities

- `python-ch1-content`: 新增 4 條規則（F-1, V-1, T-3, K-1）、修改 2 條規則（P-1, S-2）

## Impact

- 受影響的 spec：`openspec/specs/python-ch1-content/spec.md`（修改）、`openspec/specs/editorial-audit-loop/spec.md`（新增）
- 新增檔案：`phoenix-popular-science-article-style-enhance.md`（skill 參考文件，放置於專案根目錄）
- 不影響任何應用程式碼
