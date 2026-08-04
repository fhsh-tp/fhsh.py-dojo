---
layout: challenge
id: apcs001
title: 撲克牌重排計數
difficulty: hard
category: apcs
type: competition
tags:
  - data structure
  - 計數
algorithm: card_restack_count
testcase_count: 20
description: 給定 N 張點數相異的牌,依「兩端抽牌疊成牌堆、再選定一側逐張發回」的規則重排,求最後可能產生的牌序總數
params:
  t:
    type: int
    min: 10
    max: 10
  n1:
    type: int
    min: 1
    max: 1
  n2:
    type: int
    min: 2
    max: 20
  n3:
    type: int
    min: 2
    max: 20
  n4:
    type: int
    min: 100
    max: 2000
  n5:
    type: int
    min: 100
    max: 2000
  n6:
    type: int
    min: 100
    max: 2000
  n7:
    type: int
    min: 5000
    max: 10000
  n8:
    type: int
    min: 5000
    max: 10000
  n9:
    type: int
    min: 5000
    max: 10000
  n10:
    type: int
    min: 5000
    max: 10000
generator: |
  t = int(input())
  for _ in range(t):
      n = int(input())
      print(1 if n == 1 else 2**n - 2)
reference_solution: |
  t = int(input())
  ans = []
  for _ in range(t):
      n = int(input())
      ans.append(1 if n == 1 else (1 << n) - 2)
  print('\n'.join(map(str, ans)))
starter_code: ""
---

## 撲克牌重排計數

桌上有一排 N 張牌,點數互不相同。你要把這排牌重新排列,規則分兩個階段:

1. **抽牌**:每次從這排牌的**最左端或最右端**任選一張抽走,疊到手中牌堆的**最上方**,直到桌面的牌抽完。
2. **發回**:從手中牌堆的**最上方**開始,一張一張放回桌面排成一排。放回前你要先**選定一側**(左或右),之後每一張都只能加在該側。

兩個階段中的每一次選擇都可以自由決定。請問:最後桌面上這排牌,總共有幾種**不同的**排列結果?

### 動手推演(N = 3)

假設桌上是 `1 2 3`。舉一種抽法:依序抽「左、右、左」,抽出順序是 1、3、2,牌堆由頂到底是 `2 3 1`。發回時選右側,結果是 `2 3 1`;若選左側,結果是 `1 3 2`。

把所有抽法與發回側都試過一遍,可以得到 6 種不同結果:

```
1 2 3   1 3 2   2 1 3   2 3 1   3 1 2   3 2 1
```

那 N 更大的時候呢?

### 輸入說明

- 第一行:整數 T,代表接下來有 T 筆測試資料
- 接下來 T 行:每行一個整數 N(1 ≤ N ≤ 10000),代表牌的張數

### 輸出說明

- 共 T 行,每行一個整數:對應該筆 N 的不同排列結果總數

### 範例

**輸入:**

```
2
3
5
```

**輸出:**

```
6
30
```
