---
name: phoenix-sci-writing
description: "Phoenix 科普寫作 15 條編輯規則（P-1~K-1）的可操作摘要，用於撰寫/修訂 fhsh.py-dojo 教學文章。"
license: MIT
metadata:
  author: fhsh-py-dojo
  version: "1.0"
---

# phoenix-sci-writing

Phoenix 科普寫作風格的 15 條編輯規則摘要，用於撰寫或修訂教學文章（`docs/tutor/py/**`）。**正本**在 `phoenix-popular-science-article-style-enhance.md`（含每條規則的判定清單與違規/合規對照），本 skill 為可操作摘要；逐檔系統性稽核請用 `eal-editorial-audit` skill。

## 何時使用

- 撰寫或修訂教學文章、章節內容。
- 需要檢查文章是否符合 Phoenix 科普寫作風格時。

## 15 條規則

| ID | 規則 | 判定要點 |
|----|------|----------|
| P-1 | 標點風格（破折號控制） | 破折號不用於解釋子句；解釋改用冒號或另起句。依正本 5 條判定清單。 |
| T-1 | 術語前向引用控制 | 術語在首次出現處即定義，不先用後解釋。 |
| S-1 | 類比的後設認知橋 | 類比後要有一句「後設認知橋」點明類比對應到的概念。 |
| S-2 | 笑話後的回歸連接詞 | 玩笑/離題後用回歸連接詞把讀者拉回主線（注意 H3 邊界條件）。 |
| S-3 | 段落層級過場 | 段落之間要有過場句，避免主題硬切。 |
| C-1 | 程式碼區塊的對話式前導 | 程式碼區塊前要有一句對話式前導，說明「接下來要看什麼」。 |
| E-1 | 錯誤預防（即時提醒） | 在容易犯錯處即時插入提醒，而非事後才提。 |
| M-1 | 心智模型顯式化 | 把隱含的心智模型講明白，不假設讀者自行腦補。 |
| O-1 | 開場動機建立 | 章節開場先建立「為什麼要學這個」的動機。 |
| W-1 | 程式碼與解說一致性 | 內文解說與實際程式碼一致（變數名、行為、輸出）。 |
| T-2 | 無殘留 TBD 標記 | 全文無 TBD / TODO / 待補等殘留標記。 |
| F-1 | 圖片佔位符雙行格式 | 圖片佔位符採雙行格式（正本定義）。 |
| V-1 | VitePress container 語法正確性 | 自訂 container 一律用 `> [!TYPE]` callout 語法（TYPE ∈ NOTE/TIP/WARNING/DANGER/DETAILS）；`!` 為必要字元，`> [TYPE]`（缺 `!`）不會正確渲染。 |
| T-3 | 無空白 UI 元素 | 無空白的 UI 元素（空按鈕/空區塊/空連結）。 |
| K-1 | 顏文字語氣密度 | 顏文字密度適中且多樣，不過度、不重複同一款。 |

## 用法

1. 撰寫時對照上表逐條自檢；細節與違規/合規範例查正本文件。
2. 修訂既有文章時，優先跑 `eal-editorial-audit` 做多輪系統性稽核。

## 參照

- `phoenix-popular-science-article-style-enhance.md` — 15 規則正本（判定清單、違規/合規對照、規則演化指南）
- `eal-editorial-audit` skill — 迭代編審工作流程
- `openspec/specs/editorial-audit-loop/spec.md` — EAL 正式規格
