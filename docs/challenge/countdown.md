---
layout: challenge
id: py024
title: 倒數計時器
difficulty: easy
tags: [for, range, step, 倒數]
algorithm: countdown
testcase_count: 5
params:
  n:
    type: int
    min: 1
    max: 100
generator: |
  n = int(input())
  for i in range(n, 0, -1):
      print(i)
  print("Go!")
starter_code: |
  # 讀取正整數 N，從 N 倒數到 1，每行印一個數字，最後印 "Go!"
chapter: ch2
description: 從 N 倒數到 1，最後印出 Go!
---

## 倒數計時器

讀入一個正整數 N，從 N 倒數到 1（每行一個數字），最後印出 `Go!`。

### 輸入說明

- 一行：一個正整數 N（1 ≤ N ≤ 100）

### 輸出說明

- 前 N 行：從 N 倒數到 1
- 最後一行：`Go!`

### 範例

**輸入：**

```
3
```

**輸出：**

```
3
2
1
Go!
```
