---
layout: challenge
id: 23
title: 跳過倍數
difficulty: easy
tags: [for, continue, 迴圈控制, 倍數]
algorithm: skip_multiples
testcase_count: 5
params:
  n:
    type: int
    min: 5
    max: 100
  k:
    type: int
    min: 2
    max: 9
generator: |
  n = int(input())
  k = int(input())
  for i in range(1, n + 1):
      if i % k == 0:
          continue
      print(i)
starter_code: |
  # 讀取 N 和 K，印出 1 到 N 中所有「不是 K 的倍數」的數字
---

## 跳過倍數

讀入兩個正整數 N 和 K，印出 1 到 N 之間所有「不是 K 的倍數」的數字，每行一個。

### 輸入說明

- 第一行：正整數 N（5 ≤ N ≤ 100）
- 第二行：正整數 K（2 ≤ K ≤ 9）

### 輸出說明

- 每行一個數字，為 1 到 N 中不是 K 倍數的數

### 範例

**輸入：**

```
10
3
```

**輸出：**

```
1
2
4
5
7
8
10
```
