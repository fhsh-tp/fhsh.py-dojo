---
layout: challenge
id: py039
title: 星號倒三角形
difficulty: easy
tags: [nested-loop, pattern, for-loop]
algorithm: nested-loop
testcase_count: 6
params:
  n:
    type: int
    min: 1
    max: 20
generator: |
  n = int(input())
  for i in range(1, n + 1):
      print("*" * (n - i + 1))
starter_code: |
  n = int(input())
  # 第 i 行印 n-i+1 個 *
  # 第 1 行最多，逐行遞減到 1
chapter: ch2
description: 輸入 N，印出高度為 N 的倒三角形（第 1 行 N 個星號，逐行遞減）
---

## 星號倒三角形

輸入 N，印出高度為 N 的倒三角形（第 1 行 N 個星號，逐行遞減）。

### 輸入說明

- 一行：一個正整數 N（1 ≤ N ≤ 20）

### 輸出說明

- 輸出 N 行，第 i 行印出 N-i+1 個星號（`*`）

### 範例

**輸入：**

```
3
```

**輸出：**

```
***
**
*
```
