---
layout: challenge
id: 24
title: 跳五累加器
difficulty: easy
tags: [for, continue, 迴圈控制, 累加]
algorithm: sum_skip_fives
testcase_count: 5
params:
  n:
    type: int
    min: 5
    max: 1000
generator: |
  n = int(input())
  total = 0
  for i in range(1, n + 1):
      if i % 5 == 0:
          continue
      total = total + i
  print(total)
starter_code: |
  # 讀取正整數 N，計算 1 到 N 的總和，但跳過所有 5 的倍數
---

## 跳五累加器

計算 1 到 N 的總和，但跳過所有 5 的倍數。

### 輸入說明

- 一行：正整數 N（5 ≤ N ≤ 1000）

### 輸出說明

- 一行：1 到 N 中跳過 5 的倍數後的累加結果

### 範例

**輸入：**

```
10
```

**輸出：**

```
40
```
