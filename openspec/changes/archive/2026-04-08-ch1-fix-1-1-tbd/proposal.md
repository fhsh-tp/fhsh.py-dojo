## Why

`docs/tutor/py/ch1/1-1.md` 有殘留的 TBD 區塊與教學一致性問題：

1. **開場白動機不足**（已修正）：原本的 Hook 直接講人機溝通鴻溝，沒有先回答零基礎學生最根本的問題——「為什麼要學程式」。已改成以 Phoenix 親身經歷（為了零用錢學程式）為錨點的動機段落。
2. **解題程式碼使用了尚未教過的語法**：解題實戰原本用字串串接 `+`（`print("Hello, " + name + "!")`），但 1-1 尚未教字串串接，違反 T-1 規則（不得在教學點之前使用正式術語/語法）。同時 hello-world challenge 的輸出格式 `Hello, Alice!` 強迫使用 `+` 才能把 `!` 接在名字後面。
3. **殘留 TBD 標記**：L287 的 TBD 註解未被清除。

## What Changes

- **重寫開場白**（已完成）：將開場白替換為「為什麼要學程式」段落。
- **改用逗號分隔取代字串串接**：解題程式碼改為 `print("Hello,", name)`，完全使用 `print()` 的逗號分隔功能，不引入 `+` 字串串接。逐行解讀與常見錯誤排查段落同步更新。
- **簡化 hello-world challenge 輸出格式**：從 `Hello, Alice!` 改為 `Hello, Alice`（移除 `!`），使解法不需要字串串接。challenge 定義檔（`docs/challenge/hello-world.md`）的 generator、輸出說明、範例一併更新。
- **更新類題提示**：類題一（self-introduction）的提示從「字串串接（`+`）」改為「逗號分隔」。
- **移除所有 TBD 標記**：清除殘留的 `<!-- TBD ... -->` 註解。
- **重新生成 test pool**：hello-world challenge 輸出格式改變，pool 需重新生成。

## Capabilities

### New Capabilities

（無）

### Modified Capabilities

- `python-ch1-content`：修正 1-1.md 中殘留 TBD 區塊的內容缺陷——開場白重寫、解題程式碼改用逗號分隔、challenge 輸出格式簡化

## Impact

- 受影響檔案：`docs/tutor/py/ch1/1-1.md`、`docs/challenge/hello-world.md`、`docs/public/pools/hello_world.bin`
- 受影響 spec：`python-ch1-content`（delta spec 更新輸出格式要求）
