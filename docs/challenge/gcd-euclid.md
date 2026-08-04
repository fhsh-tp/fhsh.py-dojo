---
layout: challenge
id: py049
title: 最大公因數（GCD）
difficulty: medium
tags: [while-loop, euclidean-algorithm, math]
algorithm: euclidean-algorithm
testcase_count: 6
params:
  a:
    type: int
    min: 1
    max: 10000
  b:
    type: int
    min: 1
    max: 10000
generator: |
  a = int(input())
  b = int(input())
  while b != 0:
      a, b = b, a % b
  print(a)
starter_code: |
  a = int(input())
  b = int(input())
  # 輾轉相除法：while b != 0: a, b = b, a % b
  # 迴圈結束後 a 就是 GCD
  print(a)
chapter: ch2
description: 輸入 A 和 B，用輾轉相除法求最大公因數
---

## 最大公因數（GCD）

輸入 A 和 B，用輾轉相除法求最大公因數。

### 輸入說明

- 第一行：正整數 A（1 ≤ A ≤ 10000）
- 第二行：正整數 B（1 ≤ B ≤ 10000）

### 輸出說明

- 一行：A 和 B 的最大公因數

### 範例

**輸入：**

```
12
18
```

**輸出：**

```
6
```
