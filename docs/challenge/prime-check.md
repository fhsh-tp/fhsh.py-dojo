---
layout: challenge
id: py052
title: 質數判斷
difficulty: easy
tags: [for-loop, break, prime, math]
algorithm: trial-division
testcase_count: 6
params:
  n:
    type: int
    min: 2
    max: 100000
generator: |
  n = int(input())
  is_prime = True
  for i in range(2, n):
      if n % i == 0:
          is_prime = False
          break
  if is_prime:
      print("Yes")
  else:
      print("No")
reference_solution: |
  n = int(input())
  def is_prime(x):
      if x < 2:
          return False
      i = 2
      while i * i <= x:
          if x % i == 0:
              return False
          i += 1
      return True
  print("Yes" if is_prime(n) else "No")
starter_code: |
  n = int(input())
  is_prime = True
  # 從 2 到 n-1，遇到能整除的就 break 並標記為非質數
  if is_prime:
      print("Yes")
  else:
      print("No")
chapter: ch2
description: 輸入 N，判斷 N 是否為質數，輸出 Yes 或 No
---

## 質數判斷

輸入 $N$，判斷 $N$ 是否為質數，輸出 Yes 或 No。

### 輸入說明

- 一行：一個正整數 $N$（$2 \le N \le 100000$）

### 輸出說明

- 一行：若是質數輸出 `Yes`，否則輸出 `No`

### 範例

**輸入：**

```
7
```

**輸出：**

```
Yes
```

---

**輸入：**

```
8
```

**輸出：**

```
No
```
