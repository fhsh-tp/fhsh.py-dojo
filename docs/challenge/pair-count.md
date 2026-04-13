---
layout: challenge
id: 43
title: 配對計數
difficulty: easy
tags: [nested-loop, counting, for-loop, conditional]
algorithm: nested-loop
testcase_count: 6
params:
  n:
    type: int
    min: 5
    max: 100
  s:
    type: int
    min: 5
    max: 100
generator: |
  n = int(input())
  s = int(input())
  count = 0
  for i in range(1, n + 1):
      for j in range(i, n + 1):
          if i + j == s:
              count += 1
  print(count)
starter_code: |
  n = int(input())
  s = int(input())
  count = 0
  # 用巢狀迴圈遍歷所有 i <= j 的整數對
  # 計算 i + j == s 的對數
  print(count)
chapter: ch2
description: 輸入 N 和 S，計算 1≤i≤j≤N 且 i+j==S 的整數對個數
---
