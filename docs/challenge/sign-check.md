---
layout: challenge
id: 27
title: 正負零判斷
difficulty: easy
tags: [if-elif-else, 比較運算]
algorithm: sign_check
testcase_count: 10
params:
  n:
    type: int
    min: -10000
    max: 10000
generator: |
  n = int(input())
  if n > 0:
      print("Positive")
  elif n < 0:
      print("Negative")
  else:
      print("Zero")
starter_code: |
  # 讀取一個整數，判斷它是正數、負數還是零
chapter: ch1
description: 判斷整數是正數、負數還是零
---

## 正負零判斷

給定一個整數，判斷它是正數、負數還是零。

### 輸入說明

- 一行輸入：一個整數 n（-10000 ~ 10000）

### 輸出說明

- 如果是正數，輸出 `Positive`
- 如果是負數，輸出 `Negative`
- 如果是零，輸出 `Zero`

### 範例

**輸入：**

```
5
```

**輸出：**

```
Positive
```

---

**輸入：**

```
-3
```

**輸出：**

```
Negative
```

---

**輸入：**

```
0
```

**輸出：**

```
Zero
```
