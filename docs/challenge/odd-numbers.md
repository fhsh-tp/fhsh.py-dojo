---
layout: challenge
id: 25
title: 奇數列印機
difficulty: easy
tags: [for, range, step, 奇數]
algorithm: odd_numbers
testcase_count: 5
params:
  n:
    type: int
    min: 1
    max: 100
generator: |
  n = int(input())
  for i in range(1, n + 1, 2):
      print(i)
starter_code: |
  # 讀取正整數 N，印出 1 到 N 之間的所有奇數（每行一個）
chapter: ch2
description: 印出 1 到 N 之間所有的奇數
---

## 奇數列印機

讀入一個正整數 N，印出 1 到 N 之間所有的奇數（包含 1，若 N 本身是奇數也包含 N），每行一個。

### 輸入說明

- 一行：一個正整數 N（1 ≤ N ≤ 100）

### 輸出說明

- 每行一個奇數，從 1 開始遞增，不超過 N

### 範例

**輸入：**

```
7
```

**輸出：**

```
1
3
5
7
```
