---
layout: challenge
id: 58
title: 智慧藥盒提醒
difficulty: hard
type: competition
tags:
  - 模擬
  - 排程
algorithm: pillbox_reminder
description: 智慧藥盒依登記順序為藥品編號,各藥品照固定週期發出提醒,預告接下來 K 次提醒的藥品編號
params:
  q:
    type: int
    min: 2
    max: 5
  periods:
    type: int
    min: 2
    max: 50000
    count:
      from: q
      separator: " "
  k:
    type: int
    min: 1
    max: 400
testcase_plan:
  - count: 3
    override:
      periods: { max: 30 }
      k: { min: 5, max: 20 }
  - count: 2
    override:
      q: { min: 3 }
      periods: { min: 30000 }
      k: { min: 300 }
  - literal: |
      3
      2 3 6
      12
generator: |
  q = int(input())
  periods = list(map(int, input().split()))
  k = int(input())
  nxt = periods[:]
  out = []
  for _ in range(k):
      best = 0
      for i in range(1, q):
          if nxt[i] < nxt[best]:
              best = i
      out.append(best + 1)
      nxt[best] += periods[best]
  print('\n'.join(map(str, out)))
reference_solution: |
  import heapq
  q = int(input())
  periods = list(map(int, input().split()))
  k = int(input())
  h = [(periods[i], i + 1, periods[i]) for i in range(q)]
  heapq.heapify(h)
  out = []
  for _ in range(k):
      t, idx, p = heapq.heappop(h)
      out.append(idx)
      heapq.heappush(h, (t + p, idx, p))
  print('\n'.join(map(str, out)))
starter_code: ""
---

## 智慧藥盒提醒

家中長輩每天要吃好幾種藥,你幫他準備了一台智慧藥盒。藥盒裡登記了 Q 種藥,並依登記順序把藥品編號為 1、2、…、Q(輸入不會另外給編號)。第 i 種藥有自己的提醒「週期」:登記完成後,藥盒會在第 週期、週期×2、週期×3、…分鐘各響一次,提醒長輩吃這種藥。

藥盒的螢幕有個貼心功能:預告「接下來 K 次提醒」分別輪到哪種藥。同一分鐘有多種藥同時到點時,先登記的藥品會先顯示在前面。請寫一個程式,替藥盒算出這份預告。

### 動手推演(2 種藥)

週期依序為 `3 5`,K = 6。把每次提醒發生的分鐘逐一列出:

1. t=3:藥 1 到點(3×1)→ 第 1 次提醒:藥 1
2. t=5:藥 2 到點(5×1)→ 第 2 次提醒:藥 2
3. t=6:藥 1 到點(3×2)→ 第 3 次提醒:藥 1
4. t=9:藥 1 到點(3×3)→ 第 4 次提醒:藥 1
5. t=10:藥 2 到點(5×2)→ 第 5 次提醒:藥 2
6. t=12:藥 1 到點(3×4)→ 第 6 次提醒:藥 1

湊滿 K = 6 次,螢幕上的預告依序就是 `1 2 1 1 2 1`(每個編號一行)。

### 同一分鐘同時到點怎麼辦?

以週期依序 `2 3`、K = 7 推演一次:

- t=2:藥 1 到點 → 藥 1
- t=3:藥 2 到點 → 藥 2
- t=4:藥 1 到點 → 藥 1
- t=6:藥 1(2×3)與藥 2(3×2)**同時到點** → 先登記的藥 1 先顯示,藥 2 接著顯示
- t=8:藥 1 到點 → 藥 1
- t=9:藥 2 到點 → 藥 2

前 K = 7 次提醒依序是 `1 2 1 1 2 1 2`(每個編號一行)。

### 輸入說明

- 第一行:整數 Q(2 ≤ Q ≤ 5),代表登記的藥品種類數
- 第二行:Q 個整數,以單一空白分隔,第 i 個整數就是藥品 i 的提醒週期(2 ≤ 週期 ≤ 50000,單位:分鐘)
- 第三行:整數 K(1 ≤ K ≤ 400),代表螢幕要預告的提醒次數

### 輸出說明

- 共 K 行,每行一個藥品編號
- 依提醒發生的先後,列出接下來 K 次提醒各輪到哪種藥
- 同一分鐘有多筆提醒時,編號小(先登記)的排前面

### 範例

**範例一**

**輸入:**

```
2
3 5
6
```

**輸出:**

```
1
2
1
1
2
1
```

**範例二(同一分鐘同時到點)**

**輸入:**

```
3
2 3 6
12
```

**輸出:**

```
1
2
1
1
2
3
1
2
1
1
2
3
```

範例二中,t=6 與 t=12 時三種藥同時到點,依登記順序 1、2、3 顯示。
