## Why

六題 stack／tree 批次的 change B：以「運算式求值」雙題訓練學生對運算子優先序與結合性的真正理解（矩陣 C8——本雙題得分階梯以語義鑑別為軸心，而非 TLE）。翻轉的優先序規則（加減先於乘除）讓「直接丟給 Python eval」結構性失效（矩陣 A4／B5：標準優先序 eval 上界 2/20 與 1/20），逼出自行剖析與求值的核心能力；012 再疊加右結合與括弧，對照 011 形成「同一式子、兩種世界」的教學設計（矩陣 A2／B2：`10 - 4 - 3 + 2 * 6` 在兩題分別為 30 與 66）。

## What Changes

- 新增挑戰題 apcs011「福利社老收銀機」（medium、competition）：加減先於乘除、加減與乘除皆左結合、無括弧（矩陣 A1）
- 新增挑戰題 apcs012「折價券疊加試算」（hard、competition）：同翻轉優先序、加減改右結合、乘除左結合、括弧可覆寫且自第 9 筆起出現（矩陣 B1）
- 兩題各 20 筆全 literal 策展測資（矩陣 C5：關聯輸入無法由 8 型別引擎原生生成），除法保證整除（矩陣 C4）
- 兩題各附獨立異構 reference_solution（矩陣 B10）
- 題面採兩個獨立生活情境，全站禁資料結構術語（矩陣 C11）

## Capabilities

### New Capabilities

- `expression-eval-challenges`: apcs011／apcs012 運算式求值雙題的題目內容、語義規則、測資策展與判分階梯要求

### Modified Capabilities

（無——純新增題目內容，不動平台功能）

## Impact

- Affected specs: 新增 `expression-eval-challenges`
- Affected code:
  - New: docs/challenge/snack-bar-register.md、docs/challenge/coupon-combo-quote.md
  - Modified: （無平台程式碼變更；題庫頁由 frontmatter 自動聚合）
  - Removed: （無）
- 測資池：pnpm build:pools 重建（literal 內容參與池 seed，矩陣 C9）
