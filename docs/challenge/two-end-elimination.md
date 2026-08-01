---
layout: challenge
id: 56
title: 兩端淘汰賽
difficulty: medium
type: competition
tags:
  - data structure
  - deque
algorithm: two_end_elimination
description: 給定多筆整數序列,用 deque 從兩端比較淘汰,找出每筆序列的最大值與最小值
params:
  t:
    type: int
    min: 2
    max: 3
  cases:
    type: group
    repeat: t
    params:
      n:
        type: int
        min: 1
        max: 4000
      nums:
        type: int
        min: -999
        max: 999
        count:
          from: n
          separator: "\n"
input_budget: 65535
testcase_plan:
  - count: 3
    override:
      cases: { params: { n: { max: 20 } } }
  - count: 2
    override:
      cases: { params: { n: { min: 2500 } } }
  - count: 1
    override:
      cases: { params: { n: { min: 1, max: 1 } } }
generator: |
  t = int(input())
  for _ in range(t):
      n = int(input())
      nums = [int(input()) for _ in range(n)]
      print(max(nums), min(nums))
reference_solution: |
  from collections import deque
  t = int(input())
  for _ in range(t):
      n = int(input())
      d = deque(int(input()) for _ in range(n))
      dmax = deque(d)
      while len(dmax) > 1:
          if dmax[0] >= dmax[-1]:
              dmax.pop()
          else:
              dmax.popleft()
      dmin = deque(d)
      while len(dmin) > 1:
          if dmin[0] <= dmin[-1]:
              dmin.pop()
          else:
              dmin.popleft()
      print(dmax[0], dmin[0])
starter_code: ""
---

## 兩端淘汰賽

一排整數要選出「最大值」與「最小值」,但比較的方式像淘汰賽:每一輪只能比較這排數字的**最前端**與**最後端**,把「輸」的那一端淘汰出列;不斷重複,直到只剩一個數字,它就是這場淘汰賽的優勝者。

- 找**最大值**時:兩端比較,**較小**的一端輸、被淘汰。
- 找**最小值**時:兩端比較,**較大**的一端輸、被淘汰。
- 若兩端數字相同,淘汰任一端都不影響最後結果。

這種「兩端都要拿取」的操作,正是 Python `collections.deque`(雙端佇列)的拿手好戲:`d[0]` 看最前端、`d[-1]` 看最後端,`popleft()` 淘汰最前端、`pop()` 淘汰最後端。請對每筆資料**各複製一份 deque**,分別跑一輪「找最大值」與「找最小值」的淘汰賽,輸出兩位優勝者。

> **效能提醒**:測資中包含長度很大的序列。若改用「每個數字都和其他所有數字逐一比較」這類雙重迴圈的過慢寫法,將超出運算量限制而無法通過;兩端淘汰賽每輪淘汰一個數字,只需一次走訪就能完賽。

### 動手推演(4 個數字)

以數列 `3 -5 8 1` 為例。

**找最大值**(較小端被淘汰):

1. 比較前端 `3` 與後端 `1`:`1` 較小,淘汰 → 剩 `3 -5 8`
2. 比較 `3` 與 `8`:`3` 較小,淘汰 → 剩 `-5 8`
3. 比較 `-5` 與 `8`:`-5` 較小,淘汰 → 剩 `8`,最大值是 **8**

**找最小值**(用原數列的另一份複本,較大端被淘汰):

1. 比較 `3` 與 `1`:`3` 較大,淘汰 → 剩 `-5 8 1`
2. 比較 `-5` 與 `1`:`1` 較大,淘汰 → 剩 `-5 8`
3. 比較 `-5` 與 `8`:`8` 較大,淘汰 → 剩 `-5`,最小值是 **-5**

所以這筆資料的答案是 `8 -5`。

### 輸入說明

- 第一行:整數 T(2 ≤ T ≤ 3),代表接下來有 T 筆測試資料
- 每筆測試資料:
  - 第一行:整數 Ni(1 ≤ Ni ≤ 4000),代表該筆序列的數字個數
  - 接下來 Ni 行:每行一個整數(-999 ≤ 值 ≤ 999)

### 輸出說明

- 共 T 行:每筆測試資料輸出一行,依序為該筆序列的**最大值**與**最小值**,以一個空格分隔(先最大、後最小)
- 序列只有一個數字時,最大值與最小值都是它自己

### 範例

**輸入:**

```
2
3
-52
817
-3
1
64
```

**輸出:**

```
817 -52
64 64
```
