---
layout: challenge
id: 48
title: 加總達標步數
difficulty: easy
tags: [while-loop, accumulation, counting]
algorithm: while-loop
testcase_count: 6
params:
  s:
    type: int
    min: 1
    max: 5000
generator: |
  s = int(input())
  total = 0
  count = 0
  n = 1
  while total < s:
      total += n
      count += 1
      n += 1
  print(count)
starter_code: |
  s = int(input())
  total = 0
  count = 0
  # 用 while 迴圈不斷累加連續整數（1, 2, 3...）
  # 直到 total >= s 為止，輸出加了幾個數
  print(count)
chapter: ch2
description: 輸入 S，計算從 1 開始連續整數累加，需要加幾個數才能讓總和達到或超過 S
---

## 加總達標步數

輸入 S，計算從 1 開始連續整數累加，需要加幾個數才能讓總和達到或超過 S。

### 輸入說明

- 一行：一個正整數 S（1 ≤ S ≤ 5000）

### 輸出說明

- 一行：需要的連續整數個數

### 範例

**輸入：**

```
10
```

**輸出：**

```
4
```
