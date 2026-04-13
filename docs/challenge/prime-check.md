---
layout: challenge
id: 52
title: 質數判斷
difficulty: easy
tags: [for-loop, break, prime, math]
algorithm: trial-division
testcase_count: 6
params:
  n:
    type: int
    min: 2
    max: 100000
generator: |
  n = int(input())
  is_prime = True
  for i in range(2, n):
      if n % i == 0:
          is_prime = False
          break
  if is_prime:
      print("Yes")
  else:
      print("No")
starter_code: |
  n = int(input())
  is_prime = True
  # 從 2 到 n-1，遇到能整除的就 break 並標記為非質數
  if is_prime:
      print("Yes")
  else:
      print("No")
chapter: ch2
description: 輸入 N，判斷 N 是否為質數，輸出 Yes 或 No
---
