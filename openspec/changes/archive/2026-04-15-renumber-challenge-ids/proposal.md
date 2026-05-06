## Summary

重新編號全部 challenge 的 `id` frontmatter 欄位，使 Ch1（20 題）占據 ID 1–20、Ch2（34 題）占據 ID 21–54，消除跨章 ID 不連續的問題。

## Motivation

`ch2-editorial-audit` 審計發現 Module 2 的 challenge ID 不連續：Ch2 使用 ID 11–25 和 36–54，中間 26–35 屬於 Ch1。原因是 Ch1 section 1-3 的 challenge 在 Ch2 開始編號之後才加入。此不連續違反 `ch2-cross-chapter-audit` spec 中「Challenge ID continuity across Module 2」的要求。

## Proposed Solution

僅修改 `docs/challenge/*.md` 檔案中的 `id:` frontmatter 欄位。Section 檔案使用 `<ChallengeLink slug="..." />` 引用 challenge（以 slug 而非數字 ID），因此不需要修改。

### 重新對應規則

**Ch1 後段 (10 檔)** — ID 下移 15：

| 現有 ID | 新 ID | slug |
|---------|-------|------|
| 26 | 11 | odd-even |
| 27 | 12 | sign-check |
| 28 | 13 | bmi-classifier |
| 29 | 14 | quadrant-classifier |
| 30 | 15 | triangle-classify |
| 31 | 16 | quadratic-discriminant |
| 32 | 17 | taxi-fare |
| 33 | 18 | movie-ticket |
| 34 | 19 | date-validator |
| 35 | 20 | vending-change |

**Ch2 前段 (15 檔)** — ID 上移 10：

| 現有 ID | 新 ID | slug |
|---------|-------|------|
| 11 | 21 | number-sum |
| 12 | 22 | repeat-greeting |
| 13 | 23 | factorial |
| 14 | 24 | countdown |
| 15 | 25 | odd-numbers |
| 16 | 26 | range-sum |
| 17 | 27 | collatz-steps |
| 18 | 28 | digit-counter |
| 19 | 29 | number-reverse |
| 20 | 30 | first-divisor |
| 21 | 31 | password-check |
| 22 | 32 | target-sum |
| 23 | 33 | skip-multiples |
| 24 | 34 | sum-skip-fives |
| 25 | 35 | digit-sum-skip |

**不需修改 (29 檔)**：Ch1 ID 1–10、Ch2 ID 36–54 維持不變。

### 最終結果

- Ch1：ID 1–20（連續）
- Ch2：ID 21–54（連續）
- 總計 54 題，無間隔、無重複

## Non-Goals

- 不修改 challenge 的 slug（路由不變）
- 不修改任何 section 教學檔案
- 不修改 `challenge.data.ts` 載入邏輯（它動態讀取 frontmatter）
- 不修改 challenge 題目內容

## Capabilities

### Modified Capabilities

- `ch2-cross-chapter-audit`: 修正 Challenge ID continuity 要求的違規狀態

### New Capabilities

（無）

## Impact

- 修改的檔案：`docs/challenge/*.md`（25 檔的 `id:` frontmatter 欄位）
- 驗證方式：重新編號後掃描全部 challenge 檔，確認 ID 1–54 無間隔無重複
