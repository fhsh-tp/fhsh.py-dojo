---
layout: challenge
id: apcs017
title: 園遊會代幣兌換
difficulty: medium
category: apcs
type: competition
tags:
  - 數學
description: 代幣每 12 枚整批換上一級，求最多能成功換幾次
algorithm: fair_token_exchange
params:
  n:
    type: int
    min: 1
    max: 1000000000
input_budget: 4096
testcase_plan:
  - literal: |
      9
  - literal: |
      1
  - literal: |
      3
  - literal: |
      8
  - literal: |
      11
  - literal: |
      15
  - literal: |
      32
  - literal: |
      39
  - literal: |
      116
  - literal: |
      243
  - literal: |
      1024
  - literal: |
      4374
  - literal: |
      20276
  - literal: |
      65610
  - literal: |
      987654
  - literal: |
      100000089
  - literal: |
      123456789
  - literal: |
      777777777
  - literal: |
      999999968
  - literal: |
      1000000000
generator: |
  n = int(input())

  two = 0
  q = 2
  while q <= n:
      two += n // q
      q *= 2

  three = 0
  q = 3
  while q <= n:
      three += n // q
      q *= 3

  print(min(two // 2, three))
reference_solution: |
  import sys


  def share(value, unit):
      total = 0
      current = value
      while current >= unit:
          current, _ = divmod(current, unit)
          total += current
      return total


  amount = int(sys.stdin.read().split()[0])
  threes = share(amount, 3)
  twos = share(amount, 2)
  print(threes if threes * 2 <= twos else twos // 2)
starter_code: ""
---

## 園遊會代幣兌換

園遊會這天，你們班的攤位不收現金，改發**代幣**。代幣分等級：第 1 級、第 2 級、第 3 級……數字愈大愈稀有。

開場時攤位手上只有第 1 級代幣，枚數是這樣決定的：班上有 $n$ 位同學要排成一列拍紀念照，**所有不同的排隊順序總共有幾種**，攤位就發幾枚第 1 級代幣。

接著攤位開始往上兌換，兌換規則只有一條：

> **每 12 枚同一級的代幣，剛好整批換成 1 枚上一級的代幣。**

這條規則要一字一句照著做：

1. 兌換是**一級一級往上**做的：先拿第 1 級的換第 2 級，再拿換到的第 2 級換第 3 級，依此類推，不能跳級。
2. 換某一級時，必須把手上**這一級的代幣全部剛好用完**——12 枚一批、12 枚一批地換，換到最後一枚都不剩。
3. 只要分完之後還剩下零頭（湊不滿一整批），這一次兌換就**不算成功**，整個兌換活動到此為止。不能把零頭丟掉硬換，也不能留著零頭繼續往上換。

請問攤位最後總共**成功往上換了幾次**。

### 輸入說明

- 一行一個整數 $n$，表示排隊拍照的同學人數
- $1 \le n \le 10^9$

### 輸出說明

- 一行一個整數：總共成功往上換了幾次（第一次就換不成的話，輸出 `0`）

### 範例

**輸入：**

```
9
```

**輸出：**

```
3
```

範例說明：9 位同學排成一列，不同的排隊順序共有 362880 種，所以攤位開場時有 362880 枚第 1 級代幣。接下來一步一步換：

| 第幾次兌換 | 手上這一級的枚數 | 12 枚一批分下去 | 結果 |
|---|---|---|---|
| 第 1 次 | 362880 | $362880 \div 12 = 30240$，沒有剩下 | 成功，換到 30240 枚第 2 級代幣 |
| 第 2 次 | 30240 | $30240 \div 12 = 2520$，沒有剩下 | 成功，換到 2520 枚第 3 級代幣 |
| 第 3 次 | 2520 | $2520 \div 12 = 210$，沒有剩下 | 成功，換到 210 枚第 4 級代幣 |
| 第 4 次 | 210 | 210 分成 12 枚一批之後還剩 6 枚 | 失敗，兌換活動結束 |

前三次都把手上的代幣剛好用完，第四次湊不滿整批。總共成功往上換了 3 次（最高換到第 4 級），所以輸出 `3`。

> 提醒：$n$ 最大會到 $10^9$。人數一多，「不同的排隊順序有幾種」這個數字漲得非常快——才 9 個人就已經有 362880 種；人數到十億時，光是把那個數字完整寫在紙上，大概沿著跑道貼滿整個操場都還寫不完。所以「先把那個數字整個算出來，再一次一次除以 12」並不是個實際的做法。不妨換個角度想想：要判斷 12 能一批一批整批換掉幾次，有沒有辦法不必先把那個數字本身寫出來？
