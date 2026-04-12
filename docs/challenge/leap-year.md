---
layout: challenge
id: 3
title: 閏年判斷器
difficulty: easy
tags: [if-else, 布林, 邏輯運算]
algorithm: leap_year
testcase_count: 10
params:
  year:
    type: int
    min: 1
    max: 9999
generator: |
  year = int(input())
  if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
      print("Leap Year")
  else:
      print("Common Year")
starter_code: |
  # 讀取一個西元年份，判斷是否為閏年
  # 閏年規則：能被 4 整除但不能被 100 整除，或者能被 400 整除
chapter: ch1
description: 給定西元年份，判斷是否為閏年
---

## 閏年判斷器

給定一個西元年份，判斷它是不是閏年。

### 閏年規則

1. 能被 4 整除，**且**不能被 100 整除 → 閏年
2. 能被 400 整除 → 閏年
3. 其他情況 → 平年

### 輸入說明

- 一行輸入：一個正整數 Y（西元年份，1 ~ 9999）

### 輸出說明

- 如果是閏年，輸出 `Leap Year`
- 如果不是閏年，輸出 `Common Year`

### 範例

**輸入：**

```
2024
```

**輸出：**

```
Leap Year
```

---

**輸入：**

```
1900
```

**輸出：**

```
Common Year
```
