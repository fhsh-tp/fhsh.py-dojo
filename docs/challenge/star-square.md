---
layout: challenge
id: 46
title: 星星正方形
difficulty: easy
tags: [for-loop, pattern, string-multiplication]
algorithm: for-loop
testcase_count: 5
params:
  n:
    type: int
    min: 1
    max: 20
generator: |
  n = int(input())
  for i in range(n):
      print("*" * n)
starter_code: |
  n = int(input())
  # 用 for 迴圈跑 n 次
  # 每次 print("*" * n)
chapter: ch2
description: 輸入 N，印出 N×N 的星號正方形
---
