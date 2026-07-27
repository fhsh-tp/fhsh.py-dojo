---
layout: challenge
id: 22
title: 重複問候
difficulty: easy
tags: [for, range, 迴圈, print]
algorithm: repeat_greeting
testcase_count: 5
params:
  name:
    type: alpha_mixed
    min_len: 1
    max_len: 20
  n:
    type: int
    min: 1
    max: 50
generator: |
  name = input()
  n = int(input())
  for i in range(n):
      print("Hello,", name)
starter_code: |
  # 讀取名字和次數 N，輸出 N 行 "Hello, 名字"
chapter: ch2
description: 讀取名字和次數，輸出 N 行問候
---

## 重複問候

讀入一個名字和一個正整數 N，輸出 N 行 `Hello, 名字`。

### 輸入說明

- 第一行：一個字串（名字）
- 第二行：一個正整數 N（1 ≤ N ≤ 50）

### 輸出說明

- 輸出 N 行，每行為 `Hello, 名字`（逗號後有空格）

### 範例

**輸入：**

```
Alice
3
```

**輸出：**

```
Hello, Alice
Hello, Alice
Hello, Alice
```
