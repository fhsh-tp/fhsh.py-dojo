---
layout: challenge
id: 11
title: 數字累加器
difficulty: easy
tags: [for, range, 迴圈, 累加]
algorithm: number_sum
testcase_count: 5
params:
  n:
    type: int
    min: 1
    max: 1000
generator: |
  n = int(input())
  print(sum(range(1, n + 1)))
starter_code: |
  # 讀取正整數 N，計算並輸出 1 + 2 + ... + N 的結果
chapter: ch2
description: 計算從 1 加到 N 的總和
---

## 數字累加器

你拿到一個正整數 N，請計算從 1 加到 N 的總和。

### 輸入說明

- 一行：一個正整數 N（1 ≤ N ≤ 1000）

### 輸出說明

- 一行：1 + 2 + ... + N 的結果

### 範例

**輸入：**

```
5
```

**輸出：**

```
15
```
