---
layout: challenge
id: 33
title: 電影票價
difficulty: medium
tags: [if-elif-else, 邏輯運算, 多條件]
algorithm: movie_ticket
testcase_count: 10
params:
  age:
    type: int
    min: 3
    max: 90
  hour:
    type: int
    min: 8
    max: 22
generator: |
  age = int(input())
  hour = int(input())
  if age < 12:
      price = 150
  elif age <= 25:
      price = 250
  elif age <= 64:
      price = 350
  else:
      price = 150
  if hour < 12:
      price = price - 50
  print(price)
starter_code: |
  # 讀取年齡和場次時間，計算電影票價
chapter: ch1
description: 根據年齡和場次計算電影票價
---

## 電影票價

根據觀眾年齡和場次時間計算電影票價。

### 票價規則

**依年齡分級：**

| 類別 | 年齡範圍 | 票價 |
|------|---------|------|
| 兒童 | < 12 歲 | $150 |
| 學生 | 12 ~ 25 歲 | $250 |
| 成人 | 26 ~ 64 歲 | $350 |
| 敬老 | >= 65 歲 | $150 |

**早場優惠：**

- 場次時間 < 12 點：所有票價減 $50

### 輸入說明

- 兩行輸入：
  - 第一行：年齡（整數，3 ~ 90）
  - 第二行：場次時間（整數，8 ~ 22，24 小時制）

### 輸出說明

- 輸出票價（正整數）

### 範例

**輸入：**

```
15
10
```

**輸出：**

```
200
```

---

**輸入：**

```
30
20
```

**輸出：**

```
350
```

---

**輸入：**

```
8
9
```

**輸出：**

```
100
```
