---
layout: challenge
id: py047
title: 倒數偶數
difficulty: easy
tags: [for-loop, range, negative-step, even-numbers]
algorithm: for-loop
testcase_count: 6
params:
  n:
    type: int
    min: 2
    max: 100
generator: |
  n = int(input())
  if n % 2 != 0:
      n -= 1
  for i in range(n, 0, -2):
      print(i)
starter_code: |
  n = int(input())
  # 用 range(n, 0, -2) 產生從 n 倒數的偶數序列
chapter: ch2
description: 輸入偶數 N，從 N 倒數到 2，每次減 2，每個數字獨立一行
---

## 倒數偶數

輸入偶數 N，從 N 倒數到 2，每次減 2，每個數字獨立一行。

### 輸入說明

- 一行：一個正整數 N（2 ≤ N ≤ 100）

### 輸出說明

- 輸出倒數的偶數序列，每個數字一行，直到 2 結束

### 範例

**輸入：**

```
6
```

**輸出：**

```
6
4
2
```
