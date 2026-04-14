---
layout: challenge
id: 38
title: 星號長方形
difficulty: easy
tags: [nested-loop, pattern, for-loop]
algorithm: nested-loop
testcase_count: 6
params:
  r:
    type: int
    min: 1
    max: 20
  c:
    type: int
    min: 1
    max: 20
generator: |
  r = int(input())
  c = int(input())
  for i in range(r):
      print("*" * c)
starter_code: |
  r = int(input())
  c = int(input())
  # 用巢狀迴圈印出 R 行、每行 C 個 * 的長方形
chapter: ch2
description: 輸入 R 和 C，印出 R 行、每行 C 個星號的長方形
---

## 星號長方形

輸入 R 和 C，印出 R 行、每行 C 個星號的長方形。

### 輸入說明

- 第一行：正整數 R（1 ≤ R ≤ 20）
- 第二行：正整數 C（1 ≤ C ≤ 20）

### 輸出說明

- 輸出 R 行，每行 C 個星號（`*`）

### 範例

**輸入：**

```
2
4
```

**輸出：**

```
****
****
```
