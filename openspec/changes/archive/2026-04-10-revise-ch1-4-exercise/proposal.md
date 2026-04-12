## Why

1-4.md（模組一總結）目前沒有任何 Judge 練習題，只有知識地圖和自我檢查表。缺少一道「畢業考」綜合題來驗證學生是否真正掌握了模組一所有技能（I/O、運算、型別轉換、if-else）。自動販賣機找零題完美整合三節所學，且引入貪心演算法直覺，為模組二的迴圈預埋伏筆。

## What Changes

- 在 `docs/tutor/py/ch1/1-4.md` 的自我檢查表之後、模組二預告之前，插入「模組一畢業考」區段
- 包含自動販賣機找零題的情境描述、技能交叉引用、提示與 `<ChallengeLink slug="vending-change">`
- 用慶祝式語氣（畢業考 = 里程碑），明確指出這題如何串聯 1-1（I/O）、1-2（// 和 %）、1-3（if-else）

## Non-Goals

- 不修改知識地圖和自我檢查表
- 不修改模組二預告
- 不修改 Image Specification Appendix（由 Change B 處理）

## Capabilities

### New Capabilities

（無——此變更修改教學文章內容，不引入新的技術能力）

### Modified Capabilities

- `python-ch1-content`: 1-4 節新增模組一綜合 Judge 練習題

## Impact

- 修改檔案：`docs/tutor/py/ch1/1-4.md`（插入新區段，約第 84–90 行之間）
- 依賴：Change C（`create-ch1-new-challenges`）必須先完成，提供 `vending-change` challenge
