---
layout: challenge
id: apcs007
title: 每日榜單驗證碼回填
difficulty: medium
category: apcs
type: competition
tags:
  - 數學
  - 模擬
algorithm: rank_code_backfill
params:
  t:
    type: int
    min: 1
    max: 500
  days:
    type: group
    repeat: t
    params:
      n:
        type: int
        min: 1
        max: 200000
testcase_plan:
  - literal: |
      3
      5
      1
      10
  - count: 5
    override:
      t:
        min: 1
        max: 5
      days:
        params:
          n:
            min: 1
            max: 2000
  - count: 3
    override:
      t:
        min: 20
        max: 40
      days:
        params:
          n:
            min: 1000
            max: 20000
  - count: 6
    override:
      t:
        min: 400
        max: 500
      days:
        params:
          n:
            min: 150000
            max: 200000
  - literal: |
      1
      1
  - literal: |
      1
      200000
  - literal: |
      5
      137
      137
      137
      137
      137
  - literal: |
      10
      1
      2
      3
      4
      5
      6
      7
      8
      9
      10
  - literal: |
      2
      199999
      3
generator: |
  t = int(input())
  qs = [int(input()) for _ in range(t)]
  mx = max(qs)
  lnz = [1] * (mx + 1)
  r = 1
  twos = 0
  for i in range(2, mx + 1):
      x = i
      while x % 5 == 0:
          x //= 5
          twos -= 1
      while x % 2 == 0:
          x //= 2
          twos += 1
      r = (r * x) % 10
      lnz[i] = (r * pow(2, twos, 10)) % 10 if twos > 0 else r
  print('\n'.join(str(lnz[q]) for q in qs))
reference_solution: |
  import sys

  def main():
      data = sys.stdin.read().split()
      t = int(data[0])
      qs = [int(v) for v in data[1:1 + t]]
      order = sorted(range(t), key=lambda i: qs[i])
      ans = [1] * t
      r = 1
      bal = 0
      cur = 1
      cycle = [2, 4, 8, 6]
      for idx in order:
          n = qs[idx]
          for x in range(cur + 1, n + 1):
              while x % 2 == 0:
                  x //= 2
                  bal += 1
              while x % 5 == 0:
                  x //= 5
                  bal -= 1
              r = r * x % 10
          if n > cur:
              cur = n
          ans[idx] = r * cycle[(bal - 1) % 4] % 10 if bal > 0 else r
      print('\n'.join(str(v) for v in ans))

  main()
starter_code: ""
---

## 每日榜單驗證碼回填

你有沒有注意過，ISBN 書號和身分證字號的最後一碼都是「檢查碼」——一個從其他資料算出來的數字，用來驗證整串資料沒有被抄錯？手機遊戲《星海排位》的營運團隊也用同一個點子防偽：每天結算時，官方會在榜單頁面印上一個一位數的「榜單驗證碼」，讓玩家確認榜單沒有被竄改。

驗證碼的規則是：如果當天有 N 名玩家上榜，把「這 N 名玩家所有可能的名次排法總數」算出來——第一名有 N 種人選、第二名剩 N−1 種、依此類推，所以總數是 N×(N−1)×…×2×1。這個數字通常大得驚人，而且尾端拖著一長串 0，所以官方規定：**把尾端所有的 0 去掉之後，取最後一位數字**，就是當天的驗證碼。

資料庫搬遷時遺失了一批歷史驗證碼。你的任務是寫一支程式，一次回填 T 天的驗證碼。

### 任務說明

對每一天，計算 N×(N−1)×…×2×1 去掉尾端所有 0 之後的最後一位數字。

以 N=5 為例：5×4×3×2×1 = 120，去掉尾端的 0 得到 12，最後一位是 **2**，所以驗證碼是 2。

### 輸入說明

- 第一行：整數 T，代表要回填的天數（1 ≤ T ≤ 500）
- 接下來 T 行：每行一個整數 N，代表當天上榜的玩家數（1 ≤ N ≤ 200000）

### 輸出說明

- 輸出 T 行，第 i 行是第 i 天的驗證碼（一個 1~9 的數字）

> 提醒：部分測資的 T 與 N 都非常大。如果每一天都從頭把乘積重新算一遍，是來不及在時限內完成的。

### 範例

**輸入：**

```
3
5
1
10
```

**輸出：**

```
2
1
8
```

第一天 N=5：120 → 12 → 驗證碼 2。第二天 N=1：只有 1 種排法 → 驗證碼 1。第三天 N=10：3628800 → 36288 → 驗證碼 8。
