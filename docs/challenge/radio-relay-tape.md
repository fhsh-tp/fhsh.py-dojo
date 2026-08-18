---
layout: challenge
id: apcs020
title: 午間廣播接力帶
difficulty: medium
category: apcs
type: competition
tags:
  - 滑動視窗
  - 雙指標
description: 從一整學期的點播序列裡剪一段完全不重播的接力帶，算出最長能剪多長
algorithm: radio_relay_tape
params:
  n:
    type: int
    min: 1
    max: 7000
  songs:
    type: int
    min: 1
    max: 4000000
    count:
      from: n
      separator: " "
input_budget: 60000
testcase_plan:
  - literal: |
      7
      4 9 4 7 1 9 1
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
      n: { min: 350, max: 350 }
  - count: 1
    override:
      n: { min: 700, max: 700 }
  - count: 1
    override:
      n: { min: 1100, max: 1100 }
  - count: 1
    override:
      n: { min: 1500, max: 1500 }
  - count: 1
    override:
      n: { min: 1900, max: 1900 }
  - count: 1
    override:
      n: { min: 2200, max: 2200 }
  - count: 1
    override:
      n: { min: 2500, max: 2500 }
  - count: 1
    override:
      n: { min: 4600, max: 4600 }
  - count: 1
    override:
      n: { min: 6700, max: 6700 }
  - count: 1
    override:
      n: { min: 6850, max: 6850 }
  - count: 1
    override:
      n: { min: 7000, max: 7000 }
  - count: 1
    override:
      n: { min: 7000, max: 7000 }
  - count: 1
    override:
      n: { min: 7000, max: 7000 }
generator: |
  n = int(input())
  songs = list(map(int, input().split()))
  last_seen = {}
  left = 0
  best = 0
  for right in range(n):
      song = songs[right]
      previous = last_seen.get(song, -1)
      if previous >= left:
          left = previous + 1
      last_seen[song] = right
      length = right - left + 1
      if length > best:
          best = length
  print(best)
reference_solution: |
  n = int(input())
  songs = list(map(int, input().split()))
  next_seen = {}
  limit = n
  best = 0
  for start in range(n - 1, -1, -1):
      song = songs[start]
      following = next_seen.get(song)
      if following is not None and following < limit:
          limit = following
      next_seen[song] = start
      span = limit - start
      if span > best:
          best = span
  print(best)
starter_code: |
  # CODE HERE...
---

## 午間廣播接力帶

廣播社累積了一整學期的午間點播紀錄：從開學第一天到期末，同學們依序點了 $n$ 首歌，每一首歌都有自己的編號。同一首歌可能被很多人點過，所以同一個編號在這串紀錄裡可以出現好幾次。

期末成果發表要放一條「接力帶」：從這串點播紀錄裡剪出**連續的一段**接在一起播。社長只有一個要求——整條帶子上不能有任何一首歌重播，也就是這一段裡的歌曲編號必須兩兩相異。剪短一點當然一定安全，但社長希望這條帶子愈長愈好。

社長想知道：在不重播的前提下，這條接力帶最長可以剪多長？

![📷 **圖 1**：上段是點播序列與其中最長的不重播區間，並用弧線連出三組重複的歌；下段逐步畫出右端往右推、撞見重複時左端如何跳到「上次出現位置的下一格」（程式繪製）](/assets/challenge/apcs020/圖一.png)

### 輸入說明

- 第一行：一個整數 $n$，代表點播紀錄的長度，$1 \le n \le 7000$
- 第二行：$n$ 個以一個空白分隔的整數，依點播順序給出每一首歌的編號，每個編號滿足 $1 \le$ 編號 $\le 4 \times 10^6$

### 輸出說明

- 輸出一行整數：最長的一段連續、而且歌曲編號兩兩相異的區段有多長。

### 範例

**輸入：**

```
7
4 9 4 7 1 9 1
```

**輸出：**

```
4
```

### 範例說明

這串點播紀錄有 7 首歌。把一段區間想成兩根手指：右手指 $r$ 一格一格往右推，左手指 $l$ 只在必要時往右跳，隨時保持 $l$ 到 $r$ 這一段裡沒有重複的編號。每推一格就記下當時的長度，最後取最大的那一個。

| 右手指推到 | 編號 | 這個編號上次出現在 | 左手指要不要跳 | 當時的區間 | 長度 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 第 1 個 | `4` | 沒出現過 | 不動，停在第 1 個 | `4` | 1 |
| 第 2 個 | `9` | 沒出現過 | 不動 | `4 9` | 2 |
| 第 3 個 | `4` | 第 1 個，在區間裡 | 跳到第 2 個 | `9 4` | 2 |
| 第 4 個 | `7` | 沒出現過 | 不動 | `9 4 7` | 3 |
| 第 5 個 | `1` | 沒出現過 | 不動 | `9 4 7 1` | 4 |
| 第 6 個 | `9` | 第 2 個，在區間裡 | 跳到第 3 個 | `4 7 1 9` | 4 |
| 第 7 個 | `1` | 第 5 個，在區間裡 | 跳到第 6 個 | `9 1` | 2 |

一路走下來最長的是 4，出現過兩次：第 2 個到第 5 個的 `9 4 7 1`，以及第 3 個到第 6 個的 `4 7 1 9`。所以答案是 4。

為什麼不是 5？長度 5 的連續段總共只有三段，逐一檢查就知道每一段都有重播：

| 這一段 | 編號 | 撞到哪裡 |
| :--- | :--- | :--- |
| 第 1 個到第 5 個 | `4 9 4 7 1` | 編號 4 出現兩次 |
| 第 2 個到第 6 個 | `9 4 7 1 9` | 編號 9 出現兩次 |
| 第 3 個到第 7 個 | `4 7 1 9 1` | 編號 1 出現兩次 |

三段全部不合格，長度 6 和 7 的段只會更糟，所以 4 就是上限。

注意左手指從頭到尾**只會往右走、不會往回退**：某個編號一旦造成重播，把左端往左退只會讓那次重播再回來。這代表兩根手指各自最多走 $n$ 格，整串紀錄掃一趟就夠了；反過來，若對每一個起點都重新往右延伸一次去試，同一段區間會被反覆重算很多遍。
