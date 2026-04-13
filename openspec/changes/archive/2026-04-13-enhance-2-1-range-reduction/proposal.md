## Why

Section 2-1 教完 `range()` 的三種寫法（`range(stop)`、`range(start, stop)`、`range(start, stop, step)`）後，直接跳到「常見錯誤：差一錯誤」，缺少一個統一認知的整理段落。學生容易把三種寫法當作三個獨立工具來死記，而非同一函式的預設值省略版。

同時，`range` 產生的數列在數學上就是等差數列（Python Tutorial 4.3: "It generates arithmetic progressions."），而 FHSH 高中生在國二下學期已學過等差數列。這是一個跨領域連結的教學機會，但目前 2-1 中完全沒有這層橋接。

## What Changes

在 `docs/tutor/py/ch2/2-1.md` 的 Knowledge Point B 區塊（`## range() 的完整用法`）中，於 `### range(start, stop, step)：指定步長` 之後、`### 常見錯誤：差一錯誤` 之前，插入：

1. **新增 H3 子節** `### range 的三種寫法，其實是同一招`
   - 用 peeling-off narrative（第一步：省略 step；第二步：省略 start）解釋預設值縮減邏輯
   - 附 ASCII flow diagram 視覺化「省略鏈」（`range(start, stop, step)` → `range(start, stop)` → `range(stop)`）
   - 兩個行內 code block 示範展開對照
2. **新增 `> [!TIP] 📌 數學小彩蛋` callout**
   - 連結 range 到等差數列（首項 = `start`、公差 = `step`）
   - 引用 Python 官方文件原文 "It generates arithmetic progressions."

不新增任何圖片、挑戰題或其他檔案。

## Non-Goals

- 不修改 2-1 的任何現有段落（不改寫罰寫比喻、不重排知識點順序、不調整現有 Trace Table）
- 不引入新的 CS 術語（「等差數列」是學生國二已知的數學概念，非新術語，T-1 合規）
- 不為此變更新增 challenge 題目或修改既有 challenge
- 不觸及 2-2 ~ 2-7 或任何其他章節檔案

## Capabilities

### New Capabilities

（none）

### Modified Capabilities

- `python-ch2-2-1-content`: 新增一條 requirement，要求 Knowledge Point B 包含參數縮減整理段落與等差數列 TIP callout

## Impact

- Affected specs: `python-ch2-2-1-content`（新增 1 個 requirement）
- Affected code: `docs/tutor/py/ch2/2-1.md`（唯一修改的檔案）
