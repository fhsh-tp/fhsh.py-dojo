---
layout: challenge
id: apcs018
title: 禮堂吊扇風域
difficulty: medium
category: apcs
type: competition
tags:
  - 二維陣列
  - 差分
description: 天花板上每台吊扇各吹地板上的一塊矩形，算出被最多台吊扇吹到的那一格被幾台吹到
algorithm: hall_fan_coverage
params:
  rc:
    type: int
    min: 300
    max: 300
    count:
      min: 2
      max: 2
      separator: " "
  f:
    type: int
    min: 1
    max: 3000
  tops:
    type: int
    min: 1
    max: 151
    count:
      from: f
      separator: " "
  lefts:
    type: int
    min: 1
    max: 151
    count:
      from: f
      separator: " "
  heights:
    type: int
    min: 1
    max: 150
    count:
      from: f
      separator: " "
  widths:
    type: int
    min: 1
    max: 150
    count:
      from: f
      separator: " "
input_budget: 51200
testcase_plan:
  - literal: |
      4 5
      3
      1 2 1
      1 2 3
      2 2 3
      3 3 2
  - count: 1
    override:
      f: { min: 1, max: 1 }
  - count: 1
    override:
      f: { min: 2, max: 2 }
  - count: 1
    override:
      f: { min: 3, max: 3 }
  - count: 1
    override:
      f: { min: 5, max: 5 }
  - count: 1
    override:
      f: { min: 10, max: 10 }
  - count: 1
    override:
      f: { min: 25, max: 25 }
  - count: 1
    override:
      f: { min: 60, max: 60 }
  - count: 1
    override:
      f: { min: 140, max: 140 }
  - count: 1
    override:
      f: { min: 300, max: 300 }
  - count: 1
    override:
      f: { min: 500, max: 500 }
  - count: 1
    override:
      f: { min: 750, max: 750 }
  - count: 1
    override:
      f: { min: 1000, max: 1000 }
  - count: 1
    override:
      f: { min: 1300, max: 1300 }
  - count: 1
    override:
      f: { min: 1600, max: 1600 }
  - count: 1
    override:
      f: { min: 1900, max: 1900 }
  - count: 1
    override:
      f: { min: 2200, max: 2200 }
  - count: 1
    override:
      f: { min: 2500, max: 2500 }
  - count: 1
    override:
      f: { min: 2750, max: 2750 }
  - count: 1
    override:
      f: { min: 3000, max: 3000 }
generator: |
  rows, cols = map(int, input().split())
  f = int(input())
  tops = list(map(int, input().split()))
  lefts = list(map(int, input().split()))
  heights = list(map(int, input().split()))
  widths = list(map(int, input().split()))
  diff = [[0] * (cols + 2) for _ in range(rows + 2)]
  for i in range(f):
      top = tops[i]
      left = lefts[i]
      bottom = top + heights[i]
      right = left + widths[i]
      diff[top][left] += 1
      diff[top][right] -= 1
      diff[bottom][left] -= 1
      diff[bottom][right] += 1
  best = 0
  for i in range(1, rows + 1):
      row = diff[i]
      above = diff[i - 1]
      for j in range(1, cols + 1):
          row[j] += row[j - 1] + above[j] - above[j - 1]
          if row[j] > best:
              best = row[j]
  print(best)
reference_solution: |
  rows, cols = map(int, input().split())
  f = int(input())
  tops = list(map(int, input().split()))
  lefts = list(map(int, input().split()))
  heights = list(map(int, input().split()))
  widths = list(map(int, input().split()))
  mark = [[0] * (cols + 2) for _ in range(rows + 2)]
  for i in range(f):
      left = lefts[i]
      right = left + widths[i]
      for r in range(tops[i], tops[i] + heights[i]):
          line = mark[r]
          line[left] += 1
          line[right] -= 1
  best = 0
  for r in range(1, rows + 1):
      line = mark[r]
      running = 0
      for c in range(1, cols + 1):
          running += line[c]
          if running > best:
              best = running
  print(best)
starter_code: |
  # CODE HERE...
---

## 禮堂吊扇風域

學校禮堂要重新規劃天花板的吊扇。總務處先把禮堂地板畫成一張格點圖：由前往後共 $R$ 列、由左往右共 $C$ 行，每一格大約 10 公分見方。

天花板上一共裝了 $F$ 台吊扇，每一台吹得到的地板範圍都是一塊矩形。第 $i$ 台的風域左上角落在第 $r_i$ 列第 $c_i$ 行，從那一格往下蓋住 $h_i$ 列、往右蓋住 $w_i$ 行。矩形裡的每一格都吹得到，矩形外的每一格都吹不到。不同吊扇的風域可以互相重疊，重疊處的那一格就同時被好幾台吹到。

畢業典禮當天，校長想把講台擺在全場最涼的位置。請寫一個程式，算出被最多台吊扇吹到的那一格，總共被幾台吊扇吹到。

![📷 **圖 1**：上段是地板格點上三台吊扇的風域矩形，重疊處標出該格被幾台吹到；中段示範只在每個矩形的四個角落做記號；下段示範沿著列與行各累加一次，還原出上段那張表（程式繪製）](/assets/challenge/apcs018/圖一.png)

### 輸入說明

- 第一行：兩個整數 $R$ 與 $C$，以一個空白分隔，代表地板共 $R$ 列 $C$ 行，$1 \le R \le 300$、$1 \le C \le 300$
- 第二行：一個整數 $F$，代表吊扇台數，$1 \le F \le 3000$
- 第三行：$F$ 個以一個空白分隔的整數，第 $i$ 個是第 $i$ 台吊扇風域最上面那一列 $r_i$，$1 \le r_i \le 151$
- 第四行：$F$ 個以一個空白分隔的整數，第 $i$ 個是第 $i$ 台吊扇風域最左邊那一行 $c_i$，$1 \le c_i \le 151$
- 第五行：$F$ 個以一個空白分隔的整數，第 $i$ 個是第 $i$ 台吊扇風域的高 $h_i$，也就是往下蓋住幾列，$1 \le h_i \le 150$
- 第六行：$F$ 個以一個空白分隔的整數，第 $i$ 個是第 $i$ 台吊扇風域的寬 $w_i$，也就是往右蓋住幾行，$1 \le w_i \le 150$

每一台吊扇的風域保證完全落在地板範圍內，也就是 $1 \le r_i$ 且 $r_i + h_i - 1 \le R$，同時 $1 \le c_i$ 且 $c_i + w_i - 1 \le C$。

### 輸出說明

- 輸出一行整數：被最多台吊扇吹到的那一格，被幾台吊扇吹到。
- 每一台吊扇至少蓋住一格，所以答案至少是 `1`。

### 範例

**輸入：**

```
4 5
3
1 2 1
1 2 3
2 2 3
3 3 2
```

**輸出：**

```
3
```

### 範例說明

地板有 4 列 5 行，天花板上有 3 台吊扇。四行資料直的看，就是每一台吊扇自己的四個數字：

| 吊扇 | 最上面那一列 | 最左邊那一行 | 高 | 寬 | 蓋住的範圍 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 第 1 台 | 1 | 1 | 2 | 3 | 第 1~2 列、第 1~3 行 |
| 第 2 台 | 2 | 2 | 2 | 3 | 第 2~3 列、第 2~4 行 |
| 第 3 台 | 1 | 3 | 3 | 2 | 第 1~3 列、第 3~4 行 |

把三台的風域疊起來，每一格被吹到的台數如下（表格裡的數字就是該格被幾台吊扇吹到）：

```
      行1 行2 行3 行4 行5
列1     1   1   2   1   0
列2     1   2   3   2   0
列3     0   1   2   2   0
列4     0   0   0   0   0
```

第 2 列第 3 行那一格三塊矩形都含到：第 1 台蓋住第 1~2 列第 1~3 行、第 2 台蓋住第 2~3 列第 2~4 行、第 3 台蓋住第 1~3 列第 3~4 行。全場沒有任何一格被超過 3 台吹到，所以輸出 `3`。
