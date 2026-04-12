## Why

第二章第三節（2-3）教授 `break` 與 `continue` 兩種迴圈控制語法，讓學生在學完 `for` 與 `while` 之後，進一步掌握在迴圈執行中途改變流程的能力。這是循序漸進課程設計的必要環節，也是後續演算法題目的基礎技能。

## What Changes

- 新增教學文件 `docs/tutor/py/ch2/2-3.md`，涵蓋 `break`（提早離開迴圈）與 `continue`（跳過本次迭代）兩個知識點
- 新增 6 道挑戰題（ID 20–25），每個知識點各配 1 道範例題（example）與 2 道練習題（practice）
- 挑戰題可同時示範 `break`／`continue` 在 `for` 與 `while` 迴圈中的應用
- 教學文件包含執行追蹤表（trace table），幫助學生理解迴圈中途控制的行為

## Non-Goals (optional)

- 不涵蓋 `break` 的巢狀迴圈（nested loop）脫出行為，留待後續章節
- 不引入 `list`、`dict`、`tuple` 等尚未教授的資料結構
- 不修改 Ch1 或 Ch2 其他節的任何現有內容

## Capabilities

### New Capabilities

- `python-ch2-2-3-content`: 第二章第三節「迴圈控制：break 與 continue」的教學內容與配套挑戰題（ID 20–25）

### Modified Capabilities

(none)

## Impact

- Affected specs: `python-ch2-2-3-content`（新建）
- Affected code:
  - `docs/tutor/py/ch2/2-3.md`（新建教學文件）
  - `docs/challenges/ch2/20.yaml`（新建挑戰題）
  - `docs/challenges/ch2/21.yaml`
  - `docs/challenges/ch2/22.yaml`
  - `docs/challenges/ch2/23.yaml`
  - `docs/challenges/ch2/24.yaml`
  - `docs/challenges/ch2/25.yaml`
