## Why

模組二（Chapter 2）在結構重組後聚焦於「迴圈與重複結構」，現有 2-1（for+range）、2-2（while）、2-3（break+continue）三節已完成撰寫，但缺少兩個關鍵內容：

1. **巢狀迴圈**（2-4）：雙重 for 迴圈是 APCS 初級實作題的核心技巧，也是學生理解排序演算法（Ch3）的前置知識
2. **模組總結**（2-5）：延續 Ch1 的 1-4 模式，提供知識地圖、自我檢查與下章預告

此外，現有三節的練習題量不足（2-1: 6題、2-2: 3題、2-3: 6題），需補充 APCS 初級風格的例題與類題，讓學生開始習慣 Judge 系統的正式輸入/輸出格式。

## What Changes

- 新增 `docs/tutor/py/ch2/2-4.md`：巢狀迴圈教學（2 個知識點 + 2 例題 + 6-8 類題）
- 新增 `docs/tutor/py/ch2/2-5.md`：模組二總結（知識地圖 + 自我檢查表 + 模組三預告）
- 新增 `docs/tutor/py/ch2/appendix.md`：Ch2 關鍵字補充表 + AI 圖片規格附錄
- 為既有 2-1 補充 2-4 道 APCS 風格 ChallengeLink 與對應 challenge 檔案
- 為既有 2-2 補充 3-5 道 APCS 風格 ChallengeLink 與對應 challenge 檔案
- 為既有 2-3 補充 2-4 道 APCS 風格 ChallengeLink 與對應 challenge 檔案
- 更新 `docs/tutor/py/ch2/index.md`：取消 2-4/2-5 的 HTML 註解

## Non-Goals

- 不修改 2-1/2-2/2-3 的教學內文（僅在「自己動手試試」區塊末尾追加新的 ChallengeLink）
- 不教授串列（list）、字典（dict）、tuple 等資料結構（留給 Ch3）
- 不教授函數（def）或遞迴（留給 Ch4）
- 不教授 list comprehension 或其他語法糖（留給 Ch5）
- 不產生 AI 圖片（僅撰寫圖片規格附錄中的生成 prompt）

## Capabilities

### New Capabilities

- `python-ch2-2-4-content`：第 2-4 節「巢狀迴圈」教學內容規格，包含兩個知識點（雙重 for 迴圈基礎、巢狀迴圈應用）、每個知識點的 trace table、4 張 AI 圖片規格、8-10 道 Judge 題目（2 例題 + 6-8 類題），題目格式採 APCS 初級過渡風格（明確輸入/輸出格式、多組範例、簡單限制）
- `python-ch2-2-5-content`：第 2-5 節「模組二總結」內容規格，包含 Mermaid mindmap 知識地圖（涵蓋 2-1 至 2-4 全部概念）、約 15 項自我檢查清單、模組三預告段落、2 張 AI 圖片規格，無 Judge 題目
- `python-ch2-enhanced-exercises`：為既有 2-1/2-2/2-3 補充的 APCS 風格練習題規格，每節新增 2-5 道題目，題目格式含明確「輸入格式」「輸出格式」區塊、2-3 組範例 I/O、簡單限制（N ≤ 100），並附解題思路提示

### Modified Capabilities

（無）

## Impact

- 新增檔案：
  - `docs/tutor/py/ch2/2-4.md`
  - `docs/tutor/py/ch2/2-5.md`
  - `docs/tutor/py/ch2/appendix.md`
  - `docs/tutor/py/ch2/reference.md`
  - 約 18-22 個新增 challenge 檔案（`docs/challenge/*.md`）
- 修改檔案：
  - `docs/tutor/py/ch2/index.md`（取消 2-4/2-5 註解）
  - `docs/tutor/py/ch2/2-1.md`（末尾追加 ChallengeLink）
  - `docs/tutor/py/ch2/2-2.md`（末尾追加 ChallengeLink）
  - `docs/tutor/py/ch2/2-3.md`（末尾追加 ChallengeLink）
- 依賴：`restructure-course-outline` change 須先 apply
- 遵循規範：phoenix-popular-science-article-style 全部 15 條編輯規則（P-1 ~ K-1）
- 編輯規則參考：全部 15 條編輯規則完整定義於 `/phoenix-popular-science-article-style-enhance.md`（規則定義、違規/合規對照、EAL 工作流程）。每條規則的 spec-level 定義另見 `openspec/specs/python-ch1-content/spec.md`（P-1 至 K-1 各 section）。實作者必須先讀取這兩個檔案後再開始撰寫。
