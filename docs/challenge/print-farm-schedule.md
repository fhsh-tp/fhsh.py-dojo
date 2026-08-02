---
layout: challenge
id: 57
title: 列印工坊排程
difficulty: medium
type: competition
tags:
  - 模擬
  - 排程
algorithm: print_farm_schedule
description: 自動派單系統把工單依序交給最早空閒的列印機台,計算全部工單完工的總時數
params:
  m:
    type: int
    min: 2
    max: 5
  n:
    type: int
    min: 1
    max: 400
  times:
    type: int
    min: 1
    max: 5000
    count:
      from: n
      separator: " "
testcase_plan:
  - count: 3
    override:
      m: { max: 3 }
      n: { min: 3, max: 8 }
      times: { max: 20 }
  - count: 2
    override:
      n: { min: 200 }
  - literal: |
      3
      2
      5 9
generator: |
  m = int(input())
  n = int(input())
  times = list(map(int, input().split()))
  free = [0] * m
  for t in times:
      best = 0
      for i in range(1, m):
          if free[i] < free[best]:
              best = i
      free[best] += t
  print(max(free))
reference_solution: |
  import heapq
  m = int(input())
  n = int(input())
  times = list(map(int, input().split()))
  h = [(0, i) for i in range(m)]
  heapq.heapify(h)
  for t in times:
      ft, i = heapq.heappop(h)
      heapq.heappush(h, (ft + t, i))
  print(max(ft for ft, _ in h))
starter_code: ""
---

## 列印工坊排程

創客社的列印工坊有 m 台 3D 列印機,編號 1 到 m。同學送來的工單依送件順序排隊,派單系統全自動運作,規則只有一條:下一張工單,交給「下次空閒時刻最早」的機台;若有多台機台同時最早空閒,就由編號最小的那台接手。機台接下工單後,會從自己的空閒時刻起連續列印,直到這張工單完成為止。

請寫一個程式,替工坊算出:從時刻 0 開工起算,所有工單全部完工的時刻。

### 動手推演(2 台機台、4 張工單)

工時依序為 `2 3 5 7`(單位:小時)。

1. **工單 1**(工時 2):兩台機台都在時刻 0 空閒,同時最早 → 編號最小的機台 1 接手,於 0~2 列印;機台 1 的下次空閒時刻變成 2。
2. **工單 2**(工時 3):機台 1 要到時刻 2 才空閒,機台 2 在時刻 0 就空閒 → 機台 2 接手,於 0~3 列印;機台 2 的下次空閒時刻變成 3。
3. **工單 3**(工時 5):機台 1 於時刻 2 空閒、機台 2 於時刻 3 空閒 → 機台 1 較早,於 2~7 列印;下次空閒時刻變成 7。
4. **工單 4**(工時 7):機台 1 於時刻 7 空閒、機台 2 於時刻 3 空閒 → 機台 2 較早,於 3~10 列印;下次空閒時刻變成 10。

把過程畫成甘特圖(每格 1 小時,格中的數字是該小時正在列印的工單編號,`·` 表示該機台已印完手上的工單):

```
時刻    0 1 2 3 4 5 6 7 8 9 10
機台1  |1|1|3|3|3|3|3|·|·|·|
機台2  |2|2|2|4|4|4|4|4|4|4|
```

機台 1 於時刻 7 印完手上最後一張工單,機台 2 於時刻 10 印完 → **全部完工時刻 = 10**。

### 輸入說明

- 第一行:整數 m(2 ≤ m ≤ 5),機台數
- 第二行:整數 n(1 ≤ n ≤ 400),工單數
- 第三行:n 個整數,依送件順序列出每張工單的工時(1 ≤ 工時 ≤ 5000,單位:小時),以單一空白分隔

### 輸出說明

- 單獨一行,一個整數:自時刻 0 開工起算,所有工單全部完工的時刻
- 注意:機台多於工單時,每張工單都能立刻開工,答案就是最長的單一工時

### 範例

**輸入:**

```
2
4
2 3 5 7
```

**輸出:**

```
10
```

---

**輸入:**

```
3
2
5 9
```

**輸出:**

```
9
```
