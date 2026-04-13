---
layout: challenge
id: 51
title: 完美數判斷
difficulty: medium
tags: [for-loop, factors, math]
algorithm: brute-force
testcase_count: 6
params:
  n:
    type: int
    min: 2
    max: 10000
generator: |
  n = int(input())
  total = 0
  for d in range(1, n):
      if n % d == 0:
          total += d
  if total == n:
      print("Yes")
  else:
      print("No")
starter_code: |
  n = int(input())
  total = 0
  # 從 1 到 n-1，累加所有能整除 n 的數
  # 比較 total 是否等於 n
chapter: ch2
description: 輸入 N，判斷 N 是否為完美數（真因數之和等於自身）
---
