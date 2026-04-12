## Why

第 2-5 節涵蓋串列進階操作與氣泡排序法，是第二章的核心演算法單元。學生在前四節學會了 `for`、`while`、`list` 的基本用法，現在需要結合「變數交換」、「雙重迴圈」兩個前置技術，才能理解氣泡排序的精髓。這是整個高中 Python 課程中第一次正式教導排序演算法，建立從亂序到有序的思維模式。

## What Changes

- 新增教材文章 `docs/tutor/py/ch2/2-5.md`，涵蓋三個知識點：變數交換、雙重迴圈、氣泡排序法
- 新增 9 道 Judge 題目（ID 32–40）：每個知識點各 1 道例題 + 2 道練習題
- 例題主軸：「頒獎典禮」，要求學生以降序排列成績，嚴禁使用內建 `.sort()` / `sorted()`
- 氣泡排序教學必須包含逐步交換的 trace（符合 M-1 規則）

## Non-Goals (optional)

- 本節不教 `dict`、`tuple`、list comprehension、lambda 或任何其他排序演算法（選擇排序、插入排序等）
- 不教 `.sort()` 或 `sorted()` 的用法（這些將在更後期章節介紹）
- 不涵蓋多維陣列（二維列表）的完整應用，雙重迴圈僅作為氣泡排序的工具介紹

## Capabilities

### New Capabilities

- `python-ch2-2-5-content`: 第 2-5 節「串列進階與氣泡排序」的完整教材，包含三知識點文章（變數交換 → 雙重迴圈 → 氣泡排序）及 9 道對應的 Judge 題目（IDs 32–40）

### Modified Capabilities

(none)

## Impact

- Affected specs: `python-ch2-2-5-content` (new)
- Affected code:
  - `docs/tutor/py/ch2/2-5.md` (new tutorial section)
  - `docs/challenge/variable-swap.md` (id: 32, example)
  - `docs/challenge/swap-practice-1.md` (id: 33, practice)
  - `docs/challenge/swap-practice-2.md` (id: 34, practice)
  - `docs/challenge/nested-loop-example.md` (id: 35, example)
  - `docs/challenge/nested-loop-practice-1.md` (id: 36, practice)
  - `docs/challenge/nested-loop-practice-2.md` (id: 37, practice)
  - `docs/challenge/award-ceremony.md` (id: 38, bubble sort example)
  - `docs/challenge/bubble-sort-practice-1.md` (id: 39, practice)
  - `docs/challenge/bubble-sort-practice-2.md` (id: 40, practice)
