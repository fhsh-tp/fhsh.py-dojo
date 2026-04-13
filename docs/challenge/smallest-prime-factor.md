---
layout: challenge
id: 54
title: 最小質因數
difficulty: easy
tags: [for-loop, break, prime, factorization]
algorithm: trial-division
testcase_count: 6
params:
  n:
    type: int
    min: 2
    max: 1000000
generator: |
  n = int(input())
  result = n
  for i in range(2, n):
      if n % i == 0:
          result = i
          break
  print(result)
starter_code: |
  n = int(input())
  result = n
  # 從 2 到 n-1 嘗試整除
  # 第一個能整除的數就是最小質因數，找到就 break
  print(result)
chapter: ch2
description: 輸入 N，找出 N 的最小質因數（若 N 是質數則輸出 N 本身）
---
