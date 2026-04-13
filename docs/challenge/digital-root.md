---
layout: challenge
id: 50
title: 數位根
difficulty: medium
tags: [while-loop, digit-operations, math]
algorithm: while-loop
testcase_count: 6
params:
  n:
    type: int
    min: 1
    max: 1000000
generator: |
  n = int(input())
  while n >= 10:
      total = 0
      while n > 0:
          total += n % 10
          n //= 10
      n = total
  print(n)
starter_code: |
  n = int(input())
  # 反覆對 n 求各位數總和，直到 n < 10 為止
  print(n)
chapter: ch2
description: 輸入 N，反覆將各位數字加總直到結果是個位數，輸出數位根
---
