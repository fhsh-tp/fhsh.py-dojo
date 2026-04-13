---
layout: challenge
id: 36
title: 星星直角三角形
difficulty: easy
tags: [nested-loop, pattern, for-loop]
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
      for j in range(1, i + 1):
          print("*", end="")
      print()
starter_code: |
  n = int(input())
  # 用巢狀迴圈印出直角三角形
  # 第 i 行印 i 個 *
chapter: ch2
description: 輸入 N，用雙重 for 迴圈印出高度為 N 的星號直角三角形
---
