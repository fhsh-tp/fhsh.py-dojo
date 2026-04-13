---
layout: challenge
id: 49
title: 最大公因數（GCD）
difficulty: medium
tags: [while-loop, euclidean-algorithm, math]
algorithm: euclidean-algorithm
testcase_count: 6
params:
  a:
    type: int
    min: 1
    max: 10000
  b:
    type: int
    min: 1
    max: 10000
generator: |
  a = int(input())
  b = int(input())
  while b != 0:
      a, b = b, a % b
  print(a)
starter_code: |
  a = int(input())
  b = int(input())
  # 輾轉相除法：while b != 0: a, b = b, a % b
  # 迴圈結束後 a 就是 GCD
  print(a)
chapter: ch2
description: 輸入 A 和 B，用輾轉相除法求最大公因數
---
