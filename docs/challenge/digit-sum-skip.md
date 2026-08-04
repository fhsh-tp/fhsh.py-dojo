---
layout: challenge
id: py035
title: 跳零位數和
difficulty: medium
tags: [while, continue, 迴圈控制, 位數]
algorithm: digit_sum_skip
testcase_count: 5
params:
  n:
    type: int
    min: 10
    max: 1000000000
generator: |
  n = int(input())
  total = 0
  while n > 0:
      digit = n % 10
      n = n // 10
      if digit == 0:
          continue
      total = total + digit
  print(total)
starter_code: |
  # 讀取正整數 N，計算各位數字的總和，但跳過數字 0
  # 提示：用 while 迴圈搭配 % 和 //，遇到 0 就 continue
chapter: ch2
description: 計算各位數字總和但跳過 0
---

## 跳零位數和

讀入一個正整數 N，計算 N 各位數字的總和，但遇到數字 0 就跳過不加。

### 輸入說明

- 一行：正整數 N（10 ≤ N ≤ 1000000000）

### 輸出說明

- 一行：N 各位非零數字的和

### 範例

**輸入：**

```
10203
```

**輸出：**

```
6
```
