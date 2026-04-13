---
layout: challenge
id: 37
title: 九九乘法表
difficulty: easy
tags: [nested-loop, multiplication, for-loop, formatting]
algorithm: nested-loop
testcase_count: 5
params:
  n:
    type: int
    min: 1
    max: 9
generator: |
  n = int(input())
  for i in range(1, n + 1):
      for j in range(1, n + 1):
          print(f"{i * j:4}", end="")
      print()
starter_code: |
  n = int(input())
  # 用雙重 for 迴圈印出 N×N 乘法表
  # 每個數字右對齊佔 4 個字元
chapter: ch2
description: 輸入 N（1≤N≤9），印出 1 到 N 的乘法表，每格右對齊佔 4 字元
---
