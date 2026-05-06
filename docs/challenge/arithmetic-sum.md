---
layout: challenge
id: 44
title: 等差數列求和
difficulty: easy
tags: [for-loop, range, arithmetic-sequence, accumulation]
algorithm: for-loop
testcase_count: 6
params:
  a:
    type: int
    min: 1
    max: 100
  d:
    type: int
    min: 1
    max: 50
  n:
    type: int
    min: 1
    max: 100
generator: |
  a = int(input())
  d = int(input())
  n = int(input())
  total = 0
  for i in range(n):
      total += a + i * d
  print(total)
starter_code: |
  a = int(input())
  d = int(input())
  n = int(input())
  total = 0
  # 用 range(n) 計算各項並累加
  print(total)
chapter: ch2
description: 輸入首項 a、公差 d、項數 n，計算等差數列所有項的總和
---

## 等差數列求和

輸入首項 a、公差 d、項數 n，計算等差數列所有項的總和。

### 輸入說明

- 第一行：首項 a（1 ≤ a ≤ 100）
- 第二行：公差 d（1 ≤ d ≤ 50）
- 第三行：項數 n（1 ≤ n ≤ 100）

### 輸出說明

- 一行：等差數列的總和

### 範例

**輸入：**

```
2
3
4
```

**輸出：**

```
26
```
