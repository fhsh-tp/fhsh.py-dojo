## Context

fhsh.py-dojo 已建立完整的技術基礎設施（VitePress + Pyodide + WASM Judge），以及內容骨架（`tutor-article-structure`, `challenge-scaffold-script` 等 spec）。現在進入內容生產階段，需要以 Phoenix 科普寫作風格撰寫第一批教學文章。

大綱來源為 `refs/Python-self_learning-outline.md`，基於 108 課綱核心素養。

## Goals / Non-Goals

**Goals:**

- 產出可直接上線的模組一完整教學內容（4 個 section + 1 個 index 更新）
- 產出 10 個可正常運作的 Judge challenge（含 params、generator、starter_code）
- 每個 section 提供 Nano Banana Pro 圖片 prompt（美式火柴人四格漫畫）
- 建立可複製的內容生產模式，供後續 ch2-ch4 沿用

**Non-Goals:**

- 不修改任何平台功能或 spec
- 不實際生成圖片檔案
- 不處理模組二至四的內容

## Decisions

### 教學文結構：例題 walkthrough + 類題 ChallengeLink

每個 section 的教學流程：概念溯源 → step-by-step 教學 → 例題完整示範 → 類題自行練習。例題在教學文中提供完整解題思路；類題只給 `<ChallengeLink>` 和一句提示，不給解答。

**Why：** 零基礎學生需要完整的 walkthrough 建立信心，但也需要獨立練習驗證學習效果。

### 總結章節使用 1-4 編號

總結章節命名為 `1-4.md`（section: "1-4"），沿用數字序列而非 `1-conclusion`。

**Why：** 保持 sidebar 排序一致性，避免引入特殊命名規則。

### 圖片策略：統一 Visual Style Prefix + Image Specification Appendix

所有圖片使用統一的 style prefix，在 Markdown 中以 `[風格前綴]` placeholder 內嵌，文末 Appendix 展開完整 prompt。

**Why：** 方便批次生成；統一風格確保視覺一致性。

## Risks / Trade-offs

- **f-string 提前曝光**：`grade-average` 類題提示中使用了 `f"{result:.1f}"`，這在本章尚未教過。已加上「偷學一招」的標注降低困惑 → 可接受
- **change-calculator 測試多樣性有限**：price 上限 500、payment 下限 500，保證合法但找零金額偏大 → 不影響教學效果，可在未來迭代調整
