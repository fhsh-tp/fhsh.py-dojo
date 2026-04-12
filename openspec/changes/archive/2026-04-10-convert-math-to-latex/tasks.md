## 1. 轉換 ch1/1-3.md 中的數學公式（Mathematical expressions in section 1-3 use LaTeX syntax）

- [x] 1.1 確保 Mathematical expressions in section 1-3 use LaTeX syntax：將 `docs/tutor/py/ch1/1-3.md` 第 518 行的 `ax² + bx + c = 0` 改為 `$ax^2 + bx + c = 0$`，`D = b² − 4ac` 改為 `$D = b^2 - 4ac$`，`D > 0`/`D = 0`/`D < 0` 改為 `$D > 0$`/`$D = 0$`/`$D < 0$`
- [x] 1.2 將 `docs/tutor/py/ch1/1-3.md` 第 520 行的 `b²` 改為 `$b^2$`，`b * b` 保留不動（它在 code context 中是 Python 語法，不是數學公式）

## 2. 轉換 challenge 題目中的數學公式

- [x] 2.1 將 `docs/challenge/quadratic-discriminant.md` 第 34 行的 `ax²`、`D = b²` 等數學表達改為 LaTeX 語法（注意：第 34 行在 YAML frontmatter starter_code 內，是 Python comment，無法渲染 LaTeX，已跳過）
- [x] 2.2 將 `docs/challenge/quadratic-discriminant.md` 第 39 行的 `ax² + bx + c = 0` 和 `D = b² - 4ac` 改為 LaTeX 語法（同時也轉換了第 43-45 行的 D > 0 / D = 0 / D < 0）

## 3. 驗證

- [x] 3.1 啟動 dev server，瀏覽 1-3 頁面確認數學公式正確渲染為 LaTeX 格式
