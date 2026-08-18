---
layout: challenge
id: apcs019
title: 社團教室分配
difficulty: hard
category: apcs
type: competition
tags:
  - 排序
  - 排程
description: 依派房規則替一整週的社團借用申請分配教室，算出最少要開幾間以及每筆申請分到哪一間
algorithm: club_room_allocation
params:
  n:
    type: int
    min: 1
    max: 6000
  starts:
    type: int
    min: 1
    max: 9000
    count:
      from: n
      separator: " "
  durations:
    type: int
    min: 30
    max: 105
    count:
      from: n
      separator: " "
input_budget: 56000
testcase_plan:
  - literal: |
      4
      10 20 40 45
      30 30 10 10
  - count: 1
    override:
      n: { min: 1, max: 1 }
  - count: 1
    override:
      n: { min: 2, max: 2 }
  - count: 1
    override:
      n: { min: 3, max: 3 }
  - count: 1
    override:
      n: { min: 5, max: 5 }
  - count: 1
    override:
      n: { min: 10, max: 10 }
  - count: 1
    override:
      n: { min: 25, max: 25 }
  - count: 1
    override:
      n: { min: 60, max: 60 }
  - count: 1
    override:
      n: { min: 150, max: 150 }
  - count: 1
    override:
      n: { min: 400, max: 400 }
  - count: 1
    override:
      n: { min: 900, max: 900 }
  - count: 1
    override:
      n: { min: 1500, max: 1500 }
  - count: 1
    override:
      n: { min: 2200, max: 2200 }
  - count: 1
    override:
      n: { min: 2900, max: 2900 }
  - count: 1
    override:
      n: { min: 3500, max: 3500 }
  - count: 1
    override:
      n: { min: 4000, max: 4000 }
  - count: 1
    override:
      n: { min: 4500, max: 4500 }
  - count: 1
    override:
      n: { min: 5000, max: 5000 }
  - count: 1
    override:
      n: { min: 5500, max: 5500 }
  - count: 1
    override:
      n: { min: 6000, max: 6000 }
generator: |
  import heapq
  import sys


  def main():
      data = sys.stdin.read().split()
      n = int(data[0])
      starts = [int(v) for v in data[1:1 + n]]
      durations = [int(v) for v in data[1 + n:1 + 2 * n]]

      order = sorted(range(n), key=lambda i: (starts[i], i))
      busy = []          # (結束分鐘, 教室編號)，以結束分鐘為鍵的最小堆
      idle = []          # 目前空著的教室編號，最小堆
      opened = 0
      room = [0] * n

      for i in order:
          s = starts[i]
          while busy and busy[0][0] <= s:
              _, freed = heapq.heappop(busy)
              heapq.heappush(idle, freed)
          if idle:
              picked = heapq.heappop(idle)
          else:
              opened += 1
              picked = opened
          room[i] = picked
          heapq.heappush(busy, (s + durations[i], picked))

      out = [str(opened), ' '.join(str(v) for v in room)]
      sys.stdout.write('\n'.join(out) + '\n')


  main()
reference_solution: |
  import sys


  def main():
      data = sys.stdin.read().split()
      n = int(data[0])
      starts = [int(v) for v in data[1:1 + n]]
      durations = [int(v) for v in data[1 + n:1 + 2 * n]]

      order = sorted(range(n), key=lambda i: (starts[i], i))
      # last_end[r] = 第 r+1 號教室目前登記到的最後結束分鐘
      last_end = []
      room = [0] * n

      for i in order:
          s = starts[i]
          picked = -1
          for r in range(len(last_end)):
              if last_end[r] <= s:
                  picked = r
                  break
          if picked < 0:
              last_end.append(0)
              picked = len(last_end) - 1
          last_end[picked] = s + durations[i]
          room[i] = picked + 1

      print(len(last_end))
      print(' '.join(str(v) for v in room))


  main()
starter_code: |
  # CODE HERE...
---

## 社團教室分配

學務處每學期都要處理一大疊社團借用教室的申請單。這學期一共收到 $N$ 筆申請，申請單依收件先後編號為 1 到 $N$。

時間軸是某一週，以分鐘計；週一早上 08:00 算第 1 分鐘。第 $i$ 筆申請從第 $s_i$ 分鐘開始，借用 $d_i$ 分鐘，也就是占用「第 $s_i$ 分鐘到第 $s_i + d_i$ 分鐘」這一段，但**不含**第 $s_i + d_i$ 分鐘。因此，若某一筆申請在第 $t$ 分鐘把教室交還出來，另一筆申請就可以從第 $t$ 分鐘起借用同一間教室，兩者不算衝突。

教室不夠時就得再開一間。學務處的派房規則固定如下四條，依序套用：

1. 所有申請依**開始分鐘由早到晚**逐筆處理。
2. 開始分鐘相同的申請，依**申請編號由小到大**處理。
3. 每一筆申請發給「處理到它的那一刻，空著的教室中編號最小的一間」。
4. 若那一刻每一間已開的教室都被占用，就新開一間；新教室的編號是目前已開間數加一。

請寫一個程式，替學務處算出這學期最少要開幾間教室，以及每一筆申請各分到哪一間。

![📷 **圖 1**：上段是四筆借用申請在時間軸上的甘特圖，每條長條落在它分到的教室那一列，並標出 1 號教室被交還後立刻被下一筆申請取用的那一刻；下段條列派房規則的四層（程式繪製）](/assets/challenge/apcs019/圖一.png)

### 輸入說明

- 第一行：一個整數 $N$（$1 \le N \le 6000$），代表申請筆數
- 第二行：$N$ 個整數，以單一空白分隔；第 $i$ 個是第 $i$ 筆申請的開始分鐘 $s_i$（$1 \le s_i \le 9000$）
- 第三行：$N$ 個整數，以單一空白分隔；第 $i$ 個是第 $i$ 筆申請的借用時長 $d_i$（$30 \le d_i \le 105$），單位為分鐘

### 輸出說明

- 第一行：一個整數，最少要開的教室數
- 第二行：$N$ 個整數，以單一空白分隔；第 $i$ 個是**第 $i$ 筆申請**分到的教室編號

第二行請依**輸入順序**排列，不是依處理順序排列。

### 範例

**輸入：**

```
4
10 20 40 45
30 30 10 10
```

**輸出：**

```
3
1 2 1 3
```

### 範例說明

這四筆申請的開始分鐘剛好已經由早到晚排好，所以處理順序就是 1、2、3、4。先把每一筆占用的時段整理成表：

| 申請編號 | 開始分鐘 | 借用時長 | 占用時段 | 分到的教室 |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 10 | 30 | 第 10 分鐘到第 40 分鐘 | 1 |
| 2 | 20 | 30 | 第 20 分鐘到第 50 分鐘 | 2 |
| 3 | 40 | 10 | 第 40 分鐘到第 50 分鐘 | 1 |
| 4 | 45 | 10 | 第 45 分鐘到第 55 分鐘 | 3 |

- **第 1 筆**：一間教室都還沒開，於是新開 1 號教室。
- **第 2 筆**：第 20 分鐘時，1 號教室還被第 1 筆占著（要到第 40 分鐘才交還），已開的教室全滿，於是新開 2 號教室。
- **第 3 筆**：關鍵的一刻就在第 40 分鐘。第 1 筆的占用時段不含第 40 分鐘，也就是它在這一刻剛好把 1 號教室交還出來；而 2 號教室還被第 2 筆占到第 50 分鐘。此時空著的只有 1 號教室，它同時也是編號最小的一間，所以第 3 筆**拿回 1 號教室**，不必新開。
- **第 4 筆**：第 45 分鐘時，1 號教室被第 3 筆占到第 50 分鐘、2 號教室被第 2 筆占到第 50 分鐘，兩間都滿，於是新開 3 號教室。

全程總共開了 3 間教室，四筆申請依輸入順序分到的編號依序是 `1 2 1 3`。
