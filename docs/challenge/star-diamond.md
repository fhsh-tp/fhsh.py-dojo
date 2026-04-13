---
layout: challenge
id: 42
title: 菱形圖案
difficulty: medium
tags: [nested-loop, pattern, for-loop, spacing]
algorithm: nested-loop
testcase_count: 5
params:
  n:
    type: int
    min: 1
    max: 10
generator: |
  n = int(input())
  for i in range(1, n + 1):
      print(" " * (n - i) + "*" * (2 * i - 1))
  for i in range(n - 1, 0, -1):
      print(" " * (n - i) + "*" * (2 * i - 1))
starter_code: |
  n = int(input())
  # 上半部：等腰三角形（1 到 n 行）
  # 下半部：倒等腰三角形（n-1 到 1 行）
chapter: ch2
description: 輸入 N，印出半高為 N 的菱形（上下各為等腰三角形）
---
