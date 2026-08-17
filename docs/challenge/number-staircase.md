---
layout: challenge
id: py045
title: 數字階梯
difficulty: easy
tags: [for-loop, range, output]
algorithm: for-loop
testcase_count: 5
params:
  n:
    type: int
    min: 1
    max: 50
generator: |
  n = int(input())
  for i in range(1, n + 1):
      print(i)
starter_code: |
  n = int(input())
  # 用 for i in range(1, n+1) 逐行印出數字
chapter: ch2
description: 輸入 N，印出 1 到 N 的數字，每行一個（數字階梯）
---

## 數字階梯

輸入 $N$，印出 1 到 $N$ 的數字，每行一個（數字階梯）。

### 輸入說明

- 一行：一個正整數 $N$（$1 \le N \le 50$）

### 輸出說明

- 輸出 $N$ 行，從 1 到 $N$ 逐行印出數字

### 範例

**輸入：**

```
3
```

**輸出：**

```
1
2
3
```
