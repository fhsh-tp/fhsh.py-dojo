---
layout: challenge
id: py026
title: 區間累加器
difficulty: medium
tags: [for, range, start, stop, 累加]
algorithm: range_sum
testcase_count: 5
params:
  a:
    type: int
    min: 1
    max: 500
  b:
    type: int
    min: 1
    max: 1000
generator: |
  a = int(input())
  b = int(input())
  total = 0
  for i in range(a, b + 1):
      total = total + i
  print(total)
starter_code: |
  # 讀取兩個正整數 A 和 B（A ≤ B），計算 A + (A+1) + ... + B
chapter: ch2
description: 計算 A 到 B 的區間累加總和
---

## 區間累加器

讀入兩個正整數 A 和 B（保證 A ≤ B），計算從 A 加到 B 的總和。

### 輸入說明

- 第一行：正整數 A
- 第二行：正整數 B（A ≤ B ≤ 1000）

### 輸出說明

- 一行：A + (A+1) + ... + B 的結果

### 範例

**輸入：**

```
3
7
```

**輸出：**

```
25
```
