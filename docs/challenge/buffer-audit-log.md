---
layout: challenge
id: apcs002
title: 緩衝區稽核日誌
difficulty: medium
category: apcs
type: competition
tags:
  - data structure
  - 模擬
algorithm: buffer_audit_log
description: 記憶體受限的裝置只能檢視與移除資料緩衝區最早與最新兩端的讀數,模擬峰值與谷值稽核並輸出逐步移除日誌
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
        max: 400
      nums:
        type: int
        min: -999
        max: 999
        count:
          from: n
          separator: "\n"
input_budget: 8192
testcase_plan:
  - count: 3
    override:
      cases: { params: { n: { max: 20 } } }
  - count: 2
    override:
      cases: { params: { n: { min: 200 } } }
  - count: 1
    override:
      cases: { params: { n: { min: 1, max: 1 } } }
generator: |
  t = int(input())
  for _ in range(t):
      n = int(input())
      nums = [int(input()) for _ in range(n)]
      lines = []
      for peak_round in (True, False):
          l, r = 0, n - 1
          log = []
          while l < r:
              if peak_round:
                  drop_newest = nums[l] >= nums[r]
              else:
                  drop_newest = nums[l] <= nums[r]
              if drop_newest:
                  log.append(nums[r])
                  r -= 1
              else:
                  log.append(nums[l])
                  l += 1
          log.append(nums[l])
          lines.append(' '.join(map(str, log)))
      print('\n'.join(lines))
reference_solution: |
  from collections import deque
  t = int(input())
  for _ in range(t):
      n = int(input())
      readings = [int(input()) for _ in range(n)]
      for peak_round in (True, False):
          buf = deque(readings)
          log = []
          while len(buf) > 1:
              if peak_round:
                  remove_newest = buf[0] >= buf[-1]
              else:
                  remove_newest = buf[0] <= buf[-1]
              if remove_newest:
                  log.append(buf.pop())
              else:
                  log.append(buf.popleft())
          log.append(buf[0])
          print(' '.join(map(str, log)))
starter_code: ""
---

## 緩衝區稽核日誌

一台記憶體有限的邊緣裝置,把感測器傳來的讀數依收到的順序存進緩衝區。受限於硬體,裝置**每次只能檢視緩衝區「最早」與「最新」兩端各一筆讀數,並移除其中一筆**;而管理規範要求:每移除一筆讀數,都必須立刻寫進稽核日誌。

裝置要對每一批讀數執行兩輪稽核:

1. **峰值稽核**:重複「比較兩端讀數、移除數值**較小**的那筆並記入日誌」;若兩端數值相同,移除**最新**的那筆。直到緩衝區只剩一筆——留下的就是這批讀數的峰值(最大值)。這一輪的日誌,就是依序被移除的讀數,最後補上留下的峰值。
2. **谷值稽核**:把同一批讀數重新載入緩衝區,再跑一次,但方向相反:每次移除數值**較大**的那筆(相同時同樣移除最新那筆),最後留下的就是谷值(最小值)。

請寫一個程式,替裝置產生每一批讀數的兩行稽核日誌。

### 動手推演(4 筆讀數)

讀數依序為 `3 -5 8 1`(最早的是 3,最新的是 1)。

**峰值稽核**(移除較小端):

1. 比較最早端 `3` 與最新端 `1`:`1` 較小,移除並記入日誌 → 日誌:`1`
2. 比較 `3` 與 `8`:`3` 較小,移除 → 日誌:`1 3`
3. 比較 `-5` 與 `8`:`-5` 較小,移除 → 日誌:`1 3 -5`
4. 只剩 `8`,它就是峰值 → 第一行日誌:`1 3 -5 8`

**谷值稽核**(重新載入,移除較大端):

1. 比較 `3` 與 `1`:`3` 較大,移除 → 日誌:`3`
2. 比較 `-5` 與 `1`:`1` 較大,移除 → 日誌:`3 1`
3. 比較 `-5` 與 `8`:`8` 較大,移除 → 日誌:`3 1 8`
4. 只剩 `-5`,它就是谷值 → 第二行日誌:`3 1 8 -5`

**兩端數值相同時怎麼辦?** 以讀數 `5 2 5` 為例(最早與最新都是 5):

- 峰值稽核:兩端都是 `5` → 移除**最新**那筆 → 日誌 `5`;接著 `5` 與 `2`:`2` 較小,移除 → `5 2`;剩下 `5` 是峰值 → `5 2 5`
- 谷值稽核:兩端都是 `5` → 移除最新那筆 → `5`;接著 `5` 與 `2`:`5` 較大,移除最早那筆 → `5 5`;剩下 `2` 是谷值 → `5 5 2`

### 輸入說明

- 第一行:整數 T(2 ≤ T ≤ 3),代表接下來有 T 批讀數
- 每批讀數:
  - 第一行:整數 Ni(1 ≤ Ni ≤ 400),代表這批讀數的筆數
  - 接下來 Ni 行:每行一個整數讀數(-999 ≤ 讀數 ≤ 999,可能為負)

### 輸出說明

- 每批讀數輸出**兩行**,共 2 × T 行
- 第一行:峰值稽核日誌——依序被移除的讀數,最後接上留下的峰值,以單一空白分隔(共 Ni 個數)
- 第二行:谷值稽核日誌——同樣格式,最後一個數是谷值
- **比較規則**:峰值稽核每次移除數值較小的那端;谷值稽核每次移除數值較大的那端;**兩端數值相同時,一律移除最新(較晚存入)的那筆**
- 該批只有一筆讀數時,沒有任何移除,兩行都只有那個讀數本身

### 範例

**輸入:**

```
2
4
3
-5
8
1
1
64
```

**輸出:**

```
1 3 -5 8
3 1 8 -5
64
64
```
