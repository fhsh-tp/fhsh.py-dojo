# 題目建立指南

本文說明如何在本專案新增一道 Python 自學道場題目。

---

## 目錄

- [快速流程](#快速流程)
- [命名規則](#命名規則)
- [Frontmatter 欄位說明](#frontmatter-欄位說明)
  - [基本欄位](#基本欄位)
  - [params 參數型別](#params-參數型別)
  - [generator 產生器程式碼](#generator-產生器程式碼)
  - [starter\_code 起始程式碼](#starter_code-起始程式碼)
- [Markdown 內文結構](#markdown-內文結構)
- [完整範本](#完整範本)
- [現有難度參考](#現有難度參考)
- [開發與測試](#開發與測試)

---

## 快速流程

1. 執行 `pnpm new-challenge <name> --title "題目名稱" --difficulty easy` 產生題目骨架（`<name>` 為小寫 kebab-case；腳本會自動分配唯一的 `id`，並將檔案建立於 `docs/challenge/<name>.md`）
   - **請勿手動建立題目檔**：手動建立容易造成 `id` 衝突。此為新增題目的首選方式，與 `CONTRIBUTE.md` 的 Phase 2 SOP 一致。
2. 依下方「Frontmatter 欄位說明」編輯 `params`、`generator`、`starter_code` 等核心欄位
3. 撰寫題目說明、輸入輸出規格與範例
4. 執行 `pnpm build:pools` 重新編譯加密測資池，再執行 `pnpm dev` 在瀏覽器確認題目與測資，並親自跑過一次確認可以通過（Accepted）

> 所有題目資料皆定義在 Markdown 的 frontmatter 中，**不需要** 額外修改設定檔或 TOML 檔。

---

## 命名規則

| 欄位 | 格式 | 範例 |
|------|------|------|
| 檔案名稱 | `kebab-case.md` | `bubble-sort.md` |
| `algorithm` | `snake_case` | `bubble_sort` |
| `id` | 遞增整數 | `16`（由 `pnpm new-challenge` 自動分配，接續現有最大值） |

**演算法名稱與檔名的對應：**

```
algorithm: bubble_sort    →  docs/challenge/bubble-sort.md
algorithm: binary_search  →  docs/challenge/binary-search.md
```

規則：`algorithm` 欄位的底線（`_`）全部替換為連字號（`-`），即為檔名（不含 `.md`）。

---

## Frontmatter 欄位說明

### 基本欄位

```yaml
---
layout: challenge          # 固定值，觸發 ChallengeView 元件
id: 16                     # 題目 ID，整數，全站唯一，依序遞增
title: 題目名稱             # 顯示於題目清單的中文名稱
difficulty: easy           # 難度：easy | medium | hard
type: basic                # 選填，題型，預設 basic（見下方「題型 type」）
tags:                      # 選填：分類標籤陣列
  - 排序
  - 基礎演算法
algorithm: my_algorithm    # snake_case，用於 WASM 產生測資的識別鍵
testcase_count: 5          # 選填，預設 5，測試案例數量
editor_capture_debounce_ms: 1000  # 選填，卡關紀錄的 editor 快照 debounce 間隔（見下方）
params: ...                # 必填，定義 WASM 產生測資的參數規格（見下方）
generator: |               # 必填，Python 程式，讀入參數並輸出正確答案
  ...
starter_code: |            # 必填，使用者初始程式碼範本
  ...
---
```

---

### 題型 type

`type` 為選填欄位，標示題目的「題型」，預設 `basic`。省略時視同 `basic`，故既有題目無須修改。

| `type` 值 | 說明 | 狀態 |
|-----------|------|------|
| `basic` | 基礎練習題 | ✅ 已實作（預設） |
| `competition` | 競賽題 | ✅ 已實作 |
| `fill_in_blank` | 填空題 | ⏳ deferred（下一版） |
| `gamified` | 遊戲化題型 | ⏳ deferred（下一版） |
| `guided` | 引導題型 | 🔮 future（設計中，placeholder） |

`pnpm new-challenge` 以 `--type basic|competition` 指定題型；目前僅接受已實作的 `basic` 與 `competition`，其餘值會被拒絕（避免產出無樣板的半成品題）。出題流程可搭配 `.claude/skills/challenge-author/` skill 一鍵引導。

> **注意**：此處的頂層 `type`（題型）與下方「params 參數型別」表格中每個參數各自的 `type`（如 `int`、`alpha_upper`）是**不同欄位、不同用途**，位於 frontmatter 的不同層級，請勿混淆。

---

### params 參數型別

`params` 是一個 YAML 物件，**每個鍵代表一個輸入參數**，順序即為 stdin 的行順序。

WASM 產生的每筆測資為多行字串，每行對應一個參數，`generator` 程式碼用 `input()` 依序讀取。

#### 型別一覽

| `type` | 說明 | 必要欄位 |
|--------|------|----------|
| `int` | 整數 | `min`, `max` |
| `alpha_upper` | 大寫英文字母（A–Z） | `min_len`, `max_len` |
| `alpha_lower` | 小寫英文字母（a–z） | `min_len`, `max_len` |
| `alpha_mixed` | 大小寫混合英文字母（A–Za–z） | `min_len`, `max_len` |
| `hex_string` | 十六進位字串（0–9a–f） | `min_len`, `max_len` |
| `printable_ascii` | 可列印 ASCII 字元（空格至 ~） | `min_len`, `max_len` |
| `enum` | 從固定清單中隨機挑選一個值 | `values`（非空字串陣列） |

#### 範例

```yaml
params:
  n:
    type: int
    min: 5
    max: 20
  numbers:
    type: int
    min: 1
    max: 100
    count:
      min: 5
      max: 20
      separator: " "
```

以上定義產生的測資格式（兩行）：

```
10
42 7 88 15 3 61 29 47 5 90
```

#### 固定值參數

若某個參數需要固定值（不隨機），使用 `min == max`：

```yaml
params:
  base:
    type: int
    min: 2
    max: 2
  n:
    type: int
    min: 1
    max: 50
```

#### count — 產生多個值

所有型別都支援 `count` 欄位，用於在**同一行**產生多個值：

```yaml
params:
  numbers:
    type: int
    min: 1
    max: 100
    count:
      min: 3    # 最少產生 3 個
      max: 8    # 最多產生 8 個
      separator: " "  # 值之間的分隔符，預設為空格
```

產生的測資範例（該行包含 5 個整數）：

```
42 7 88 15 3
```

省略 `count` 時等同於 `count: { min: 1, max: 1 }`，即只產生一個值。

---

### generator 產生器程式碼

`generator` 是一段 Python 程式碼，由後端（Pyodide Worker）執行，用於**產生正確答案**。

**規範：**

- 用 `input()` 依照 `params` 的宣告順序讀取每個參數
- 將最終答案 `print()` 到 stdout（只輸出一行結果）
- 數值型態需自行轉換（`int(input())`）
- 避免使用外部套件（Pyodide 環境，可用標準函式庫）

**範例（氣泡排序）：**

```yaml
generator: |
  n = int(input())
  nums = list(map(int, input().split()))
  for i in range(n):
      for j in range(n - i - 1):
          if nums[j] > nums[j + 1]:
              nums[j], nums[j + 1] = nums[j + 1], nums[j]
  print(' '.join(map(str, nums)))
```

---

### reference_solution 參考解答（選填）

`reference_solution` 是一段**獨立於 `generator`** 的正確 Python 解法（完整程式，讀 `input()`、`print()` 出正解）。它**不影響題目在網站上的行為**，僅供**內容層回歸測試**（`scripts/content-regression.test.ts`）使用。

**用途：** 測試會對有標註 `reference_solution` 的題目，用學生實際會拿到的輸入分別跑 `generator` 與 `reference_solution`，斷言兩者輸出一致——這等同於「正解在正式加密測資池下能得 AC」的離線驗證。若兩者輸出不一致，代表 `generator` 或參考解其中之一有誤，測試會指名該題失敗。

**規範：**

- 選填。未提供時，該題會被回歸測試 skip。
- 建議刻意用**與 `generator` 不同的寫法**（例如質數判斷用 `sqrt` 上界、`generator` 用完整試除），才能同時抓出 `generator` 與參考解各自的錯誤。
- 與 `generator` 同樣避免使用外部套件（Pyodide／標準函式庫）。

**範例（氣泡排序）：**

```yaml
generator: |
  n = int(input())
  nums = list(map(int, input().split()))
  for i in range(n):
      for j in range(n - i - 1):
          if nums[j] > nums[j + 1]:
              nums[j], nums[j + 1] = nums[j + 1], nums[j]
  print(' '.join(map(str, nums)))
reference_solution: |
  n = int(input())
  nums = list(map(int, input().split()))
  print(' '.join(map(str, sorted(nums))))
```

---

### starter_code 起始程式碼

`starter_code` 是使用者在編輯器中看到的**初始程式碼範本**。

**規範：**

- 提供函式骨架，使用者填入實作
- 通常包含讀取 `input()` 的提示程式碼

**範例：**

```yaml
starter_code: |
  def bubble_sort(nums):
      # 在此實作氣泡排序
      pass

  n = int(input())
  nums = list(map(int, input().split()))
  print(' '.join(map(str, bubble_sort(nums))))
```

---

### editor_capture_debounce_ms 編輯捕捉間隔（選填）

「卡關紀錄」功能會把學生在編輯器裡的作答歷程（編輯快照、執行、提交）記到瀏覽器本機（IndexedDB），供學生下載後交給 LLM／教師分析盲點。`editor_capture_debounce_ms` 控制**編輯快照的 debounce 間隔**：學生停止打字達此毫秒數才拍一張全文快照。

- **預設 1000**（未設此欄位時）。
- **有效範圍 100–10000**；非整數或超出範圍的值會**回退預設 1000**。
- 可**逐題覆寫**：例如某題想更細地捕捉試錯過程可設 `editor_capture_debounce_ms: 500`。

此紀錄純本機、匿名、可由學生主動清除；不含任何隱藏的期望輸出（答案金鑰）。

## Markdown 內文結構

frontmatter 之後的 Markdown 內文會顯示於題目說明面板（左側）。建議依照以下結構撰寫：

```markdown
## 題目名稱

一段簡短的演算法說明，讓學生了解這道題目在練習什麼。

### 演算法說明

詳細說明演算法的步驟（可選）。

### 輸入說明

- 第一行：`n`，整數 5~20，代表數字個數
- 第二行：`numbers`，n 個以空格分隔的整數（1~100）

### 輸出說明

- 輸出排序後的整數，以空格分隔

### 範例

**輸入：**

```
5
42 7 88 15 3
```

**輸出：**

```
3 7 15 42 88
```
```

---

## 完整範本

以下是一道新題目的完整 Markdown 範本，複製後修改即可：

```markdown
---
layout: challenge
id: 16
title: 你的題目名稱
difficulty: easy
tags:
  - 標籤一
  - 標籤二
algorithm: my_algorithm
testcase_count: 5
params:
  n:
    type: int
    min: 5
    max: 20
  numbers:
    type: int
    min: 1
    max: 100
    count:
      min: 5
      max: 20
      separator: " "
generator: |
  n = int(input())
  nums = list(map(int, input().split()))
  # 在此實作正確的演算法邏輯
  result = sorted(nums)  # 替換為實際計算
  print(' '.join(map(str, result)))
starter_code: |
  def my_algorithm(nums):
      # 在此實作你的解法
      pass

  n = int(input())
  nums = list(map(int, input().split()))
  print(' '.join(map(str, my_algorithm(nums))))
---

## 你的題目名稱

簡短說明此演算法的用途與背景。

### 演算法說明

說明演算法的操作步驟。

### 輸入說明

- 第一行：`n`，整數 5~20，代表數字個數
- 第二行：`numbers`，n 個以空格分隔的整數（1~100）

### 輸出說明

- 輸出一行結果

### 範例

**輸入：**

\`\`\`
5
42 7 88 15 3
\`\`\`

**輸出：**

\`\`\`
3 7 15 42 88
\`\`\`
```

---

## 現有難度參考

| 難度 | 題目範例 | 特徵 |
|------|----------|------|
| `easy` | 費氏數列、反轉字串、判斷質數 | 單一簡單邏輯，參數少 |
| `medium` | 氣泡排序、二分搜尋、字串處理 | 需要迴圈或條件組合 |
| `hard` | 動態規劃、圖論、遞迴 | 多步驟演算法，需理解資料結構 |

---

## 開發與測試

```bash
# 安裝依賴
pnpm install

# 啟動開發伺服器（會先重新編譯 WASM，再啟動 VitePress）
pnpm dev

# 執行單元測試
pnpm test

# 正式建置
pnpm build
```

> **注意：** WASM 僅在第一次啟動或修改 `testcase-generator/` Rust 程式碼後需要重新編譯。若只新增題目 Markdown 檔，直接執行 `pnpm docs:dev` 即可跳過 WASM 編譯步驟。

### 驗證新題目是否正常

1. 執行 `pnpm dev`，開啟瀏覽器
2. 前往首頁確認新題目出現在清單中
3. 點入題目，確認測資正常產生（左側顯示測試案例）
4. 在編輯器貼入正確解法，確認所有測資通過
5. 故意送出錯誤解法，確認失敗案例正確顯示
