---
layout: challenge
id: py028
title: 位數計算器
difficulty: easy
tags: [while, 迴圈, 位數]
algorithm: digit_counter
testcase_count: 5
params:
  n:
    type: int
    min: 0
    max: 1000000000
generator: |
  n = int(input())
  if n == 0:
      print(1)
  else:
      count = 0
      while n > 0:
          n = n // 10
          count = count + 1
      print(count)
starter_code: |
  # 讀取非負整數 N，計算 N 有幾位數
  # 提示：用 while 迴圈不斷除以 10
chapter: ch2
description: 計算非負整數的位數
---

## 位數計算器

讀入一個非負整數 N，計算 N 有幾位數。

### 輸入說明

- 一行：一個非負整數 N（0 ≤ N ≤ 1000000000）

### 輸出說明

- 一行：N 的位數

### 範例

**輸入：**

```
12345
```

**輸出：**

```
5
```
