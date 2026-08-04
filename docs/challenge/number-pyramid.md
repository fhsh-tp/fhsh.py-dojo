---
layout: challenge
id: py041
title: 數字金字塔
difficulty: easy
tags: [nested-loop, pattern, for-loop, numbers]
algorithm: nested-loop
testcase_count: 6
params:
  n:
    type: int
    min: 1
    max: 15
generator: |
  n = int(input())
  for i in range(1, n + 1):
      row = ""
      for j in range(1, i + 1):
          if j > 1:
              row += " "
          row += str(j)
      print(row)
starter_code: |
  n = int(input())
  # 第 i 行印 1 到 i 的數字，數字間用空格分隔
chapter: ch2
description: 輸入 N，印出數字金字塔（第 i 行為 1 2 3 ... i，數字間空格分隔）
---

## 數字金字塔

輸入 N，印出數字金字塔（第 i 行為 1 2 3 ... i，數字間空格分隔）。

### 輸入說明

- 一行：一個正整數 N（1 ≤ N ≤ 15）

### 輸出說明

- 輸出 N 行，第 i 行印出從 1 到 i 的數字，數字之間以一個空格分隔

### 範例

**輸入：**

```
4
```

**輸出：**

```
1
1 2
1 2 3
1 2 3 4
```
