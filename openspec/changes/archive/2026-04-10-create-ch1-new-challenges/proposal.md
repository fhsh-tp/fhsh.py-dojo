## Why

模組一目前僅有 3 道 Judge 題（閏年、成績等第、三角形判斷），題目數量不足以支撐鷹架式自學。根據 PISA 數學素養框架與運算思維四大支柱的研究，需要新增融合數學素養與 CT 的多層次題目，讓學生透過刷題逐步內化 if-elif-else、布林邏輯與數學建模能力。

## What Changes

新增 10 個 Judge challenge 定義檔（`docs/challenge/*.md`），涵蓋四個難度層級：

**★☆☆ Tier 1 暖身**（ID 26–27）
- `odd-even`: 奇偶數判斷 — 整除概念 + 基本 if-else
- `sign-check`: 正負零判斷 — 數線概念 + if-elif-else 三路分支

**★★☆ Tier 2 基礎應用**（ID 28–29）
- `bmi-classifier`: BMI 健康分級 — 公式代入 + 分段分類（衛福部標準）
- `quadrant-classifier`: 座標象限判斷 — 直角座標系 + 7 case 系統列舉

**★★★ Tier 3 數學建模**（ID 30–33）
- `triangle-classify`: 三角形分類器 — 三角不等式 + 等邊/等腰/不等邊分類（升級版）
- `quadratic-discriminant`: 二次方程式判別式 — D = b²−4ac 公式轉程式
- `taxi-fare`: 計程車費計算 — 分段函數數學建模（無公式提示）
- `movie-ticket`: 電影票價 — 年齡×時段雙變數交叉條件

**★★★★ Tier 4 綜合挑戰**（ID 34）
- `date-validator`: 日期合法性檢查 — 閏年整合 + 月份天數系統分解

**模組一綜合題**（ID 35，用於 1-4）
- `vending-change`: 自動販賣機找零 — I/O + 運算 + if-else 全整合

每個 challenge 包含：YAML frontmatter（params + generator）、題目說明、範例 I/O。

## Non-Goals

- 不修改教學正文（1-3.md、1-4.md 的內容修改由 Change D/E 處理）
- 不修改現有 challenge 檔案（`triangle-check.md` 保留，新增 `triangle-classify.md`）
- 不執行 `pnpm generate-pools`（等所有 challenge 建完後統一生成）

## Capabilities

### New Capabilities

- `ch1-exercise-challenges`: 模組一練習題 Judge challenge 定義檔集合（10 個 challenge）

### Modified Capabilities

（無）

## Impact

- 新增檔案：`docs/challenge/odd-even.md`（ID: 26）
- 新增檔案：`docs/challenge/sign-check.md`（ID: 27）
- 新增檔案：`docs/challenge/bmi-classifier.md`（ID: 28）
- 新增檔案：`docs/challenge/quadrant-classifier.md`（ID: 29）
- 新增檔案：`docs/challenge/triangle-classify.md`（ID: 30）
- 新增檔案：`docs/challenge/quadratic-discriminant.md`（ID: 31）
- 新增檔案：`docs/challenge/taxi-fare.md`（ID: 32）
- 新增檔案：`docs/challenge/movie-ticket.md`（ID: 33）
- 新增檔案：`docs/challenge/date-validator.md`（ID: 34）
- 新增檔案：`docs/challenge/vending-change.md`（ID: 35）
