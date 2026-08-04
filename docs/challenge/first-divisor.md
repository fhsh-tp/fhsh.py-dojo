---
layout: challenge
id: py030
title: 第一個因數
difficulty: easy
tags: [for, break, 迴圈控制, 因數]
algorithm: first_divisor
testcase_count: 5
params:
  n:
    type: int
    min: 4
    max: 10000
generator: |
  n = int(input())
  for i in range(2, n):
      if n % i == 0:
          print(i)
          break
starter_code: |
  # 讀取正整數 N（N ≥ 4），找出 N 的最小因數（不含 1 和 N 本身）
  # 提示：用 for 迴圈從 2 開始找，找到第一個就用 break 停下
chapter: ch2
description: 找出正整數的最小因數
---

## 第一個因數

給定一個正整數 N（N ≥ 4），找出 N 最小的因數（不含 1 和 N 本身）。

### 輸入說明

- 一行：一個正整數 N（4 ≤ N ≤ 10000）

### 輸出說明

- 一行：N 的最小因數（不含 1 和 N 本身）

### 範例

**輸入：**

```
12
```

**輸出：**

```
2
```
