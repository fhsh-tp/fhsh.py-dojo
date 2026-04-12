## Why

模組二（Chapter 2）的第 2-4 節需要教授「串列（List）」與「線性搜尋（Linear Search）」，使學生能夠管理大量同類資料並學習最直觀的搜尋演算法，為後續章節奠定資料結構基礎。

## What Changes

- 新增教學文件 `docs/tutor/py/ch2/2-4.md`，涵蓋兩個知識點：List 基礎操作、線性搜尋演算法
- 新增 6 道 Judge 練習題（ID 26–31），每個知識點各含 1 道範例題與 2 道練習題

## Non-Goals

- 不教授二維（巢狀）串列
- 不教授串列推導式（list comprehension）——保留至模組四
- 不教授 `dict`、`tuple` 等其他容器型別
- 不教授氣泡排序（bubble sort）或其他排序演算法
- 不教授巢狀迴圈

## Capabilities

### New Capabilities

- `python-ch2-2-4-content`: 模組二第 2-4 節的教學內容——串列基礎（含 `for item in list` 迭代）與線性搜尋演算法，包含對應的 6 道 Judge 題目（ID 26–31）

### Modified Capabilities

(none)

## Impact

- Affected specs: `python-ch2-2-4-content` (new)
- Affected code:
  - `docs/tutor/py/ch2/2-4.md` (new section file)
  - `docs/challenge/py/26.md` (new — List basics example)
  - `docs/challenge/py/27.md` (new — List basics practice 1)
  - `docs/challenge/py/28.md` (new — List basics practice 2)
  - `docs/challenge/py/29.md` (new — Linear Search example: 尋找最大值與位置)
  - `docs/challenge/py/30.md` (new — Linear Search practice 1)
  - `docs/challenge/py/31.md` (new — Linear Search practice 2)
