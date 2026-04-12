## 1. Tier 1 暖身題（Tier 1 warm-up challenges exist）

- [x] [P] 1.1 建立 `docs/challenge/odd-even.md`（ID: 26）— 奇偶數判斷，params: n (int, -10000~10000)，generator 使用 `n % 2 == 0` 判斷，輸出 `Even` 或 `Odd`
- [x] [P] 1.2 建立 `docs/challenge/sign-check.md`（ID: 27）— 正負零判斷，params: n (int, -10000~10000)，generator 使用 if-elif-else 判斷，輸出 `Positive`/`Negative`/`Zero`

## 2. Tier 2 基礎應用（Tier 2 application challenges exist）

- [x] [P] 2.1 建立 `docs/challenge/bmi-classifier.md`（ID: 28）— BMI 健康分級，params: weight (30~150), height (130~200)，generator 計算 `weight / (height/100) / (height/100)` 並分級為 `Underweight`/`Normal`/`Overweight`/`Obese`（衛福部標準：18.5/24/27）
- [x] [P] 2.2 建立 `docs/challenge/quadrant-classifier.md`（ID: 29）— 座標象限判斷，params: x (-100~100), y (-100~100)，generator 判斷 7 種 case：`Origin`/`X-axis`/`Y-axis`/`Quadrant 1`~`Quadrant 4`

## 3. Tier 3 數學建模（Tier 3 mathematical modeling challenges exist）

- [x] [P] 3.1 建立 `docs/challenge/triangle-classify.md`（ID: 30）— 三角形分類器，params: a,b,c (1~100)，generator 先檢查三角不等式再分類 `Not a Triangle`/`Equilateral`/`Isosceles`/`Scalene`
- [x] [P] 3.2 建立 `docs/challenge/quadratic-discriminant.md`（ID: 31）— 二次方程式判別式，params: a (1~20), b (-50~50), c (-50~50)，generator 計算 `D = b*b - 4*a*c` 並輸出 `Two Real Roots`/`One Repeated Root`/`No Real Roots`
- [x] [P] 3.3 建立 `docs/challenge/taxi-fare.md`（ID: 32）— 計程車費計算，params: distance (100~50000)，generator 基礎價 85 含首 1250m，超出每 200m 加 5（無條件進位），輸出整數車資
- [x] [P] 3.4 建立 `docs/challenge/movie-ticket.md`（ID: 33）— 電影票價，params: age (3~90), hour (8~22)，generator 依年齡分級（兒童150/學生250/成人350/敬老150）+ 早場(hour<12)減50

## 4. Tier 4 + 模組一綜合題（Tier 4 comprehensive challenge exists + Module 1 comprehensive challenge exists for section 1-4）

- [x] [P] 4.1 建立 `docs/challenge/date-validator.md`（ID: 34）— 日期合法性檢查，params: year (1~9999), month (0~15), day (0~35)，generator 驗證月份 1-12、各月天數、2 月閏年邏輯，輸出 `Valid`/`Invalid`
- [x] [P] 4.2 建立 `docs/challenge/vending-change.md`（ID: 35）— 自動販賣機找零，params: price (10~200), payment (10~500)，generator 若 payment < price 輸出 `Insufficient`，否則用 `//` 和 `%` 依序拆解 50/10/5/1 並輸出四個空格分隔的整數

## 5. 驗證（All challenges use only Module 1 Python constructs）

- [x] 5.1 對每個 generator 手動測試至少 2 組 sample input，驗證輸出正確
- [x] 5.2 確認所有 challenge 的 `starter_code` 註解只描述 Module 1 可用的語法構造
- [x] 5.3 執行 `pnpm dev` 確認所有新 challenge 頁面正常渲染
