---
layout: challenge
id: 19
title: 數字反轉器
difficulty: easy
tags: [while, 迴圈, 取餘數]
algorithm: number_reverse
testcase_count: 5
params:
  n:
    type: int
    min: 1
    max: 1000000000
generator: |
  n = int(input())
  result = 0
  while n > 0:
      result = result * 10 + n % 10
      n = n // 10
  print(result)
starter_code: |
  # 讀取正整數 N，將 N 的數字反轉後輸出
  # 提示：用 while 迴圈搭配 % 和 //
chapter: ch2
description: 將正整數的數字反轉後輸出
---

## 數字反轉器

讀入一個正整數 N，將 N 的各位數反轉後輸出。例如 12345 → 54321。

### 輸入說明

- 一行：一個正整數 N（1 ≤ N ≤ 1000000000，保證不含前導零）

### 輸出說明

- 一行：反轉後的數字（反轉後的前導零不需輸出，例如 1200 → 21）

### 範例

**輸入：**

```
12345
```

**輸出：**

```
54321
```
