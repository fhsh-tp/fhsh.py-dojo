---
layout: challenge
id: py032
title: 累加到目標
difficulty: medium
tags: [while, break, 迴圈控制, 累加]
algorithm: target_sum
testcase_count: 5
params:
  target:
    type: int
    min: 1
    max: 10000
generator: |
  target = int(input())
  total = 0
  i = 1
  while True:
      total = total + i
      if total >= target:
          print(i)
          break
      i = i + 1
starter_code: |
  # 讀取目標值 T，從 1 開始累加（1+2+3+...），找出讓累加和 ≥ T 的最小數字
chapter: ch2
description: 從 1 累加找出讓總和首次達到目標的數字
---

## 累加到目標

從 1 開始一個一個往上加（1, 1+2, 1+2+3, ...），請問加到哪個數字時，總和首次 ≥ T？

### 輸入說明

- 一行：目標值 T（正整數，1 ≤ T ≤ 10000）

### 輸出說明

- 一行：讓 1+2+...+N ≥ T 的最小 N

### 範例

**輸入：**

```
10
```

**輸出：**

```
4
```
