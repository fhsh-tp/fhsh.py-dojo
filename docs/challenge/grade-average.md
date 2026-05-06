---
layout: challenge
id: 6
title: 段考成績平均
difficulty: easy
tags: [變數, 運算, 除法]
algorithm: grade_average
testcase_count: 5
params:
  score1:
    type: int
    min: 0
    max: 100
  score2:
    type: int
    min: 0
    max: 100
  score3:
    type: int
    min: 0
    max: 100
generator: |
  a = int(input())
  b = int(input())
  c = int(input())
  avg = (a + b + c) / 3
  print(f"{avg:.1f}")
starter_code: |
  # 讀取三科成績，計算並輸出平均（保留一位小數）
chapter: ch1
description: 讀取三科成績，計算並輸出平均
---

## 段考成績平均

段考結束了，幫忙算一下三科的平均成績吧！

### 輸入說明

- 三行輸入，每行一個整數（0 ~ 100），分別代表三科成績

### 輸出說明

- 輸出一行：三科的平均成績，保留一位小數

### 範例

**輸入：**

```
80
90
70
```

**輸出：**

```
80.0
```
