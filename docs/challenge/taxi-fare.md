---
layout: challenge
id: 32
title: 計程車費計算
difficulty: medium
tags: [if-else, 運算, 數學建模]
algorithm: taxi_fare
testcase_count: 10
params:
  distance:
    type: int
    min: 100
    max: 50000
generator: |
  distance = int(input())
  if distance <= 1250:
      fare = 85
  else:
      extra = (distance - 1250 + 199) // 200
      fare = 85 + extra * 5
  print(fare)
starter_code: |
  # 讀取搭乘距離（公尺），計算計程車車資
chapter: ch1
description: 根據搭乘距離計算計程車車資
---

## 計程車費計算

根據搭乘距離計算計程車車資。

### 計費規則

1. **起步價** 85 元，包含首 1250 公尺
2. 超過 1250 公尺後，每 200 公尺加收 5 元
3. 不足 200 公尺以 200 公尺計（無條件進位）

### 輸入說明

- 一行輸入：搭乘距離（公尺，正整數，100 ~ 50000）

### 輸出說明

- 輸出車資（正整數）

### 範例

**輸入：**

```
1000
```

**輸出：**

```
85
```

---

**輸入：**

```
1250
```

**輸出：**

```
85
```

---

**輸入：**

```
2000
```

**輸出：**

```
105
```
