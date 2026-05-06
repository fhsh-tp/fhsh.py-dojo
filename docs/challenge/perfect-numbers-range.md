---
layout: challenge
id: 53
title: 完美數搜尋
difficulty: medium
tags: [for-loop, factors, math, nested-logic]
algorithm: brute-force
testcase_count: 5
params:
  n:
    type: int
    min: 6
    max: 500
generator: |
  n = int(input())
  for num in range(2, n + 1):
      total = 0
      for d in range(1, num):
          if num % d == 0:
              total += d
      if total == num:
          print(num)
starter_code: |
  n = int(input())
  # 外層遍歷 2 到 N 的每個數
  # 內層計算每個數的真因數之和
  # 若因數和等於自身則輸出
chapter: ch2
description: 輸入 N（N≥6），找出 1 到 N 之間所有的完美數並依序輸出
---

## 完美數搜尋

輸入 N（N≥6），找出 1 到 N 之間所有的完美數並依序輸出。

### 輸入說明

- 一行：一個正整數 N（6 ≤ N ≤ 500）

### 輸出說明

- 依序輸出 1 到 N 之間的完美數，每個數字佔一行

### 範例

**輸入：**

```
30
```

**輸出：**

```
6
28
```
