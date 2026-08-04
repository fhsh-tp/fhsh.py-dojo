---
layout: challenge
id: py042
title: 菱形圖案
difficulty: medium
tags: [nested-loop, pattern, for-loop, spacing]
algorithm: nested-loop
testcase_count: 5
params:
  n:
    type: int
    min: 1
    max: 10
generator: |
  n = int(input())
  for i in range(1, n + 1):
      print(" " * (n - i) + "*" * (2 * i - 1))
  for i in range(n - 1, 0, -1):
      print(" " * (n - i) + "*" * (2 * i - 1))
starter_code: |
  n = int(input())
  # 上半部：等腰三角形（1 到 n 行）
  # 下半部：倒等腰三角形（n-1 到 1 行）
chapter: ch2
description: 輸入 N，印出半高為 N 的菱形（上下各為等腰三角形）
---

## 菱形圖案

輸入 N，印出半高為 N 的菱形（上下各為等腰三角形）。

### 輸入說明

- 一行：一個正整數 N（1 ≤ N ≤ 10）

### 輸出說明

- 輸出 2*N-1 行，構成菱形圖案（包含前導空格）

### 範例

**輸入：**

```
2
```

**輸出：**

```
 *
***
 *
```
