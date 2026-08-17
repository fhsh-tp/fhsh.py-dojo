---
layout: challenge
id: py019
title: 日期合法性檢查
difficulty: medium
tags: [if-elif-else, 巢狀判斷, 邏輯運算]
algorithm: date_validator
testcase_count: 10
params:
  year:
    type: int
    min: 1
    max: 9999
  month:
    type: int
    min: 0
    max: 15
  day:
    type: int
    min: 0
    max: 35
generator: |
  year = int(input())
  month = int(input())
  day = int(input())
  if month < 1 or month > 12 or day < 1:
      print("Invalid")
  elif month in (1, 3, 5, 7, 8, 10, 12):
      if day <= 31:
          print("Valid")
      else:
          print("Invalid")
  elif month in (4, 6, 9, 11):
      if day <= 30:
          print("Valid")
      else:
          print("Invalid")
  else:
      is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
      if is_leap and day <= 29:
          print("Valid")
      elif not is_leap and day <= 28:
          print("Valid")
      else:
          print("Invalid")
starter_code: |
  # 讀取年、月、日，判斷這個日期是否合法
chapter: ch1
description: 檢查日期的合法性
---

## 日期合法性檢查

給定年、月、日三個數字，判斷它是不是一個合法的日期。

### 規則

1. 月份必須在 1 ~ 12 之間
2. 日期必須 $\ge 1$
3. 大月（1, 3, 5, 7, 8, 10, 12）：最多 31 天
4. 小月（4, 6, 9, 11）：最多 30 天
5. 二月：
   - 閏年最多 29 天
   - 平年最多 28 天
6. 閏年規則：能被 4 整除但不能被 100 整除，或者能被 400 整除

### 輸入說明

- 三行輸入：
  - 第一行：年份（整數，1 ~ 9999）
  - 第二行：月份（整數，可能超出正常範圍）
  - 第三行：日期（整數，可能超出正常範圍）

### 輸出說明

- 如果日期合法，輸出 `Valid`
- 如果日期不合法，輸出 `Invalid`

### 範例

**輸入：**

```
2024
2
29
```

**輸出：**

```
Valid
```

---

**輸入：**

```
1900
2
29
```

**輸出：**

```
Invalid
```

---

**輸入：**

```
2024
13
1
```

**輸出：**

```
Invalid
```
