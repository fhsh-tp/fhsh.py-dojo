---
layout: challenge
id: 26
title: 奇偶數判斷
difficulty: easy
tags: [if-else, 取餘數]
algorithm: odd_even
testcase_count: 10
params:
  n:
    type: int
    min: -10000
    max: 10000
generator: |
  n = int(input())
  if n % 2 == 0:
      print("Even")
  else:
      print("Odd")
starter_code: |
  # 讀取一個整數，判斷是奇數還是偶數
chapter: ch1
description: 判斷整數是奇數還是偶數
---

## 奇偶數判斷

給定一個整數，判斷它是奇數還是偶數。

### 規則

- 如果整數能被 2 整除，輸出 `Even`
- 否則輸出 `Odd`

### 輸入說明

- 一行輸入：一個整數 n（-10000 ~ 10000）

### 輸出說明

- 如果是偶數，輸出 `Even`
- 如果是奇數，輸出 `Odd`

### 範例

**輸入：**

```
7
```

**輸出：**

```
Odd
```

---

**輸入：**

```
4
```

**輸出：**

```
Even
```

---

**輸入：**

```
0
```

**輸出：**

```
Even
```
