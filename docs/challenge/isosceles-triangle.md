---
layout: challenge
id: 40
title: 等腰三角形
difficulty: medium
tags: [nested-loop, pattern, for-loop, spacing]
algorithm: nested-loop
testcase_count: 6
params:
  n:
    type: int
    min: 1
    max: 20
generator: |
  n = int(input())
  for i in range(1, n + 1):
      print(" " * (n - i) + "*" * (2 * i - 1))
starter_code: |
  n = int(input())
  # 第 i 行：先印 n-i 個空格，再印 2*i-1 個 *
chapter: ch2
description: 輸入 N，印出高度為 N 的等腰三角形（每行置中對齊，含前導空格）
---
