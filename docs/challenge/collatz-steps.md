---
layout: challenge
id: py027
title: 3N+1 猜想
difficulty: medium
tags: [while, 迴圈, Collatz, 條件判斷]
algorithm: collatz_steps
testcase_count: 5
params:
  n:
    type: int
    min: 2
    max: 10000
generator: |
  n = int(input())
  steps = 0
  while n != 1:
      if n % 2 == 0:
          n = n // 2
      else:
          n = 3 * n + 1
      steps = steps + 1
  print(steps)
starter_code: |
  # 讀取正整數 N，根據 3N+1 規則不斷變換，直到 N 變成 1
  # 偶數 → N // 2；奇數 → 3 * N + 1
  # 輸出總共需要幾步
chapter: ch2
description: 根據 3N+1 規則計算到達 1 的步數
---

## 3N+1 猜想

這是一個數學界的著名猜想：給定任意正整數 N，按以下規則不斷變換：

- 如果 N 是偶數 → N = N ÷ 2
- 如果 N 是奇數 → N = 3 × N + 1

不管 N 是多少，最終都會變成 1（至少到目前為止沒有人找到反例）。請問：從 N 出發，要經過幾步才能到達 1？

### 輸入說明

- 一行：一個正整數 N（2 ≤ N ≤ 10000）

### 輸出說明

- 一行：從 N 到 1 所需的步數

### 範例

**輸入：**

```
6
```

**輸出：**

```
8
```
