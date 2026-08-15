---
layout: challenge
id: apcs015
title: 基地台佈點規劃
difficulty: easy
category: apcs
type: competition
tags:
  - 數學
description: 算出兩台基地台互不干擾的裝設方式共有幾種
algorithm: ap_layout_plan
params:
  n:
    type: int
    min: 1
    max: 1000
input_budget: 4096
testcase_plan:
  - literal: |
      8
  - literal: |
      1
  - literal: |
      2
  - literal: |
      3
  - literal: |
      4
  - literal: |
      6
  - literal: |
      21
  - literal: |
      72
  - literal: |
      249
  - literal: |
      250
  - literal: |
      325
  - literal: |
      400
  - literal: |
      475
  - literal: |
      550
  - literal: |
      625
  - literal: |
      700
  - literal: |
      775
  - literal: |
      850
  - literal: |
      925
  - literal: |
      1000
generator: |
  import sys

  n = int(sys.stdin.readline())
  lines = []
  for k in range(1, n + 1):
      cells = k * k
      total = cells * (cells - 1) // 2
      if k >= 3:
          total -= 4 * (k - 1) * (k - 2)
      lines.append(str(total))
  sys.stdout.write("\n".join(lines) + "\n")
reference_solution: |
  import sys


  def blocked(side):
      # 逐列累加：把「比較上面那一格」所在的列當主軸，一列一列加上去。
      bad = 0
      for _top in range(side - 1):
          bad += 2 * (side - 2)
      for _top in range(side - 2):
          bad += 2 * (side - 1)
      return bad


  def main():
      data = sys.stdin.read().split()
      n = int(data[0])
      out = []
      for side in range(1, n + 1):
          spots = side * side
          out.append(str(spots * (spots - 1) // 2 - blocked(side)))
      print("\n".join(out))


  main()
starter_code: ""
---

## 基地台佈點規劃

學校要在一間正方形的專科教室裝設無線基地台。教室地板鋪成 k 列 k 行的方格，每一台基地台就裝在某一個方格的正上方，**兩台不能裝在同一格**。

總務處實測後發現，兩台基地台若擺在某些相對位置上，訊號會互相干擾。把兩台的相對位置寫成一組數字（列差, 行差）：

- **列差**是「往下幾列」，負數就代表往上
- **行差**是「往右幾行」，負數就代表往左

只要兩台的相對位置落在下面這張表的其中一列，這兩台就會互相干擾：

| 列差（往下幾列） | 行差（往右幾行） |
| :--- | :--- |
| 1 | 2 |
| 1 | −2 |
| −1 | 2 |
| −1 | −2 |
| 2 | 1 |
| 2 | −1 |
| −2 | 1 |
| −2 | −1 |

舉例來說，一台裝好之後，另一台若裝在「往下 1 列、往右 2 行」的那一格，這組相對位置就在表裡，兩台會互相干擾；反過來說，如果另一台裝在正下方那一格（往下 1 列、同一行），這組相對位置不在表裡，兩台就相安無事。

兩台基地台**沒有編號、也不分主次**：把一台裝在甲格、另一台裝在乙格，跟反過來裝是**同一種裝法**，只能算一次。

教室要開多大還沒定案，所以總務處請你一次把所有可能的邊長都算好：對每個邊長 k，算出「兩台互不干擾」的裝法共有幾種。

### 輸入說明

- 一行一個整數 `n`，`1 <= n <= 1000`

### 輸出說明

- 輸出 `n` 行，第 k 行是邊長 k 的教室有幾種可行的裝法（k 由 1 數到 `n`）

### 範例

**輸入：**

```
8
```

**輸出：**

```
0
6
28
96
252
550
1056
1848
```

### 先手算幾個小的

下表是邊長比較小的幾間教室的答案，你可以先照著上面的規則自己算算看，確定題目讀懂了再往下想：

| 邊長 k | 可行的裝法數 |
| :--- | :--- |
| 1 | 0 |
| 2 | 6 |
| 3 | 28 |

幾個提示：邊長 1 的教室只有一格，另一台無處可放，所以答案是 0；邊長 2 的教室太小，表中每一種相對位置都會跨到教室外面，所以任兩格都能裝。從邊長 3 開始，才會有配對真的踩到表裡的相對位置。

> 提醒：後段測資的 `n` 會很大。經實測，「每個邊長都把所有方格兩兩湊成一對、逐對比對那張表」的寫法，在後段測資會超出單筆測資的執行量上限。請想想有沒有辦法不必真的把每一對方格都碰過一次。
