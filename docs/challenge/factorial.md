---
layout: challenge
id: 13
title: 階乘計算機
difficulty: easy
tags: [for, range, 迴圈, 累乘]
algorithm: factorial
testcase_count: 5
params:
  n:
    type: int
    min: 0
    max: 12
generator: |
  n = int(input())
  result = 1
  for i in range(1, n + 1):
      result = result * i
  print(result)
starter_code: |
  # 讀取非負整數 N，計算並輸出 N!（N 的階乘）
  # 提示：0! = 1
---

## 階乘計算機

讀入一個非負整數 N，計算並輸出 N!（N 的階乘）。

### 輸入說明

- 一行：一個非負整數 N（0 ≤ N ≤ 12）

### 輸出說明

- 一行：N! 的值

### 範例

**輸入：**

```
5
```

**輸出：**

```
120
```
