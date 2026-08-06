---
layout: challenge
id: apcs008
title: 頒獎順位驗證碼
difficulty: hard
category: apcs
type: competition
tags:
  - 數學
  - 模擬
algorithm: prize_order_code
params:
  t:
    type: int
    min: 1
    max: 3
  rounds:
    type: group
    repeat: t
    params:
      n:
        type: int
        min: 100000
        max: 1000000000
      m:
        type: int
        min: 0
        max: 100000
testcase_plan:
  - literal: |
      3
      10
      2
      25
      1
      7
      0
  - count: 5
    override:
      t:
        min: 1
        max: 2
      rounds:
        params:
          n:
            min: 100000
            max: 150000
          m:
            min: 0
            max: 1000
  - count: 3
    override:
      t:
        min: 2
        max: 3
      rounds:
        params:
          n:
            min: 10000000
            max: 100000000
          m:
            min: 1000
            max: 50000
  - count: 6
    override:
      t:
        min: 2
        max: 3
      rounds:
        params:
          n:
            min: 100000000
            max: 1000000000
          m:
            min: 80000
            max: 100000
  - literal: |
      1
      999999999
      0
  - literal: |
      1
      100000
      100000
  - literal: |
      3
      26
      2
      24
      2
      10
      1
  - literal: |
      2
      1
      1
      2
      2
  - literal: |
      3
      1000000000
      1
      999999937
      3
      123456789
      0
generator: |
  t = int(input())
  out = []
  for _ in range(t):
      n = int(input())
      m = int(input())
      r = 1
      c2 = 0
      c5 = 0
      for i in range(n - m + 1, n + 1):
          x = i
          while x % 2 == 0:
              x //= 2
              c2 += 1
          while x % 5 == 0:
              x //= 5
              c5 += 1
          r = (r * x) % 10
      if m == 0:
          out.append(1)
      elif c2 > c5:
          out.append((r * pow(2, c2 - c5, 10)) % 10)
      elif c5 > c2:
          out.append(5)
      else:
          out.append(r)
  print('\n'.join(str(v) for v in out))
reference_solution: |
  import sys

  def code_of(n, m):
      if m == 0:
          return 1
      r = 1
      bal = 0
      for x in range(n - m + 1, n + 1):
          while x % 2 == 0:
              x //= 2
              bal += 1
          while x % 5 == 0:
              x //= 5
              bal -= 1
          r = r * x % 10
      if bal > 0:
          return r * [2, 4, 8, 6][(bal - 1) % 4] % 10
      if bal < 0:
          return 5
      return r

  data = sys.stdin.read().split()
  t = int(data[0])
  res = []
  p = 1
  for _ in range(t):
      n = int(data[p])
      m = int(data[p + 1])
      p += 2
      res.append(code_of(n, m))
  print('\n'.join(str(v) for v in res))
starter_code: ""
---

## 頒獎順位驗證碼

ISBN 書號、商品條碼、身分證字號的最後一碼都是「檢查碼」——從其他資料算出來的一位數字，用來驗證整串資料沒有出錯。手機遊戲《星海排位》的全球賽季也採用這套做法：每一輪頒獎典禮的公告上，都印著一個一位數的「頒獎順位驗證碼」。

驗證碼的規則是：這一輪全球共有 N 個帳號參賽，要依序頒發第 1 名到第 M 名共 M 個獎項。第 1 名有 N 種可能人選、第 2 名剩 N−1 種、……、第 M 名剩 N−M+1 種，所以「頒獎順位的所有可能總數」是 N×(N−1)×…×(N−M+1)，一共 M 個數相乘。這個乘積大得無法想像，尾端還拖著一串 0，所以官方規定：**把尾端所有的 0 去掉之後，取最後一位數字**，就是這一輪的驗證碼。

有些輪次因故停辦頒獎（M=0）：此時規定驗證碼為 1。

審計部門要重新核對 T 輪頒獎紀錄，請寫一支程式算出每一輪的驗證碼。

### 任務說明

對每一輪，計算 N×(N−1)×…×(N−M+1)（共 M 項）去掉尾端所有 0 之後的最後一位數字；M=0 時輸出 1。

以 N=10、M=2 為例：10×9 = 90，去掉尾端的 0 得到 9，驗證碼是 **9**。再以 N=25、M=1 為例：乘積就是 25，沒有尾端的 0，驗證碼是 **5**。

### 輸入說明

- 第一行：整數 T，代表要核對的輪數（1 ≤ T ≤ 3）
- 接下來每一輪兩行：第一行整數 N（1 ≤ N ≤ 1000000000），第二行整數 M（0 ≤ M ≤ 100000，且 M ≤ N）

### 輸出說明

- 輸出 T 行，第 i 行是第 i 輪的驗證碼（一個 1~9 的數字）

> 提醒：部分測資的 N 接近 10 億、M 接近 10 萬，乘積本身可能有幾十萬位數。如果你用迴圈一項一項把它完整乘出來、再從結果裡找答案，是來不及在時限內完成的；把它整個轉成字串取尾巴，也會撞上 Python 的轉換位數上限。動手前先想清楚：答案真正需要的是哪些資訊？

### 範例

**輸入：**

```
3
10
2
25
1
7
0
```

**輸出：**

```
9
5
1
```

第一輪 10×9=90 → 9 → 驗證碼 9。第二輪乘積為 25 → 驗證碼 5。第三輪 M=0（停辦）→ 驗證碼 1。
