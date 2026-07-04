---
name: eal-editorial-audit
description: "Editorial Audit Loop（EAL）：以固定掃描順序逐輪稽核教學文章 15 條規則、輪間修正、≤3 輪或零違規終止。"
license: MIT
metadata:
  author: fhsh-py-dojo
  version: "1.0"
---

# eal-editorial-audit

Editorial Audit Loop（EAL）是一個**迭代驗證流程**，系統性檢查教學內容是否符合全部編輯規則。每輪逐規則掃描所有目標檔案、記錄違規、修正，再重新掃描。規則內容見 `phoenix-sci-writing` skill；**正式規格**見 `openspec/specs/editorial-audit-loop/spec.md`。

## 何時使用

- 對一批教學文章（如 `docs/tutor/py/ch1/`）做整體編輯稽核。
- 章節內容完成後、發布前的品質把關。

## 固定掃描順序（每輪相同）

```
P-1 → T-1 → S-1 → S-2 → S-3 → C-1 → E-1 → M-1 → F-1 → V-1 → T-3 → K-1 → O-1 → W-1 → T-2
```

順序邏輯：標點/術語（P-1, T-1）→ 鷹架（S-1~S-3）→ 程式碼/錯誤預防（C-1, E-1, M-1）→ 格式（F-1, V-1, T-3）→ 密度（K-1，需在其他修正後評估）→ 全域檢查（O-1, W-1, T-2）。

## Violation Log 格式

每筆違規記錄：`file`（檔案路徑）、`line`（行號或範圍）、`rule`（規則 ID）、`desc`（違規描述）、`fix`（具體建議修正）。

## 輪次流程

```
Round N 掃描（依上序）→ 產生 violation log
        ↓
   修正所有違規（直接改目標檔案）
        ↓
   Round N+1 從頭重新掃描全檔（非只檢查修改處）
```

**重新掃描全檔**的原因：修正一個違規可能引入新違規（例如改 P-1 動到行數，影響 K-1 密度計算），也可能連鎖解決其他問題。

## 終止條件

- **提前終止**：某輪掃描完成後違規數為 0 → 立即終止（clean pass）。
- **最大輪次**：完成 **3 輪**後無論是否仍有違規 → 強制終止。

## Summary Report

終止後產出摘要：目標目錄、掃描規則清單、每輪違規數與修正數、最終結果（PASS / 幾輪 / 是否 clean）。

## 可重用性（參數化）

- **目標目錄**：預設 `docs/tutor/py/ch1/`，可換 `ch2/` 等。
- **規則子集**：預設 15 條全掃，可指定子集（如僅 P-1、C-1）做焦點審計。
- **流程邏輯不變**：掃描順序、violation log 格式、終止條件皆通用。

## 參照

- `openspec/specs/editorial-audit-loop/spec.md` — EAL 正式規格（normative）
- `phoenix-sci-writing` skill — 15 條規則摘要
- `phoenix-popular-science-article-style-enhance.md` — 規則與 EAL 正本（含規則演化指南）
