---
layout: challenge
id: 8
title: 秒數轉換器
difficulty: easy
tags: [運算, 整數除法, 取餘數]
algorithm: seconds_converter
testcase_count: 5
params:
  total_seconds:
    type: int
    min: 0
    max: 3599
generator: |
  s = int(input())
  minutes = s // 60
  seconds = s % 60
  print(f"{minutes} {seconds}")
starter_code: |
  # 讀取總秒數，轉換成幾分幾秒並輸出
chapter: ch1
description: 將總秒數轉換成幾分幾秒
---

## 秒數轉換器

體育課計時器壞了，只會顯示總秒數。寫一個程式把它轉換成「幾分幾秒」吧！

### 輸入說明

- 一行輸入：一個非負整數 S（總秒數，0 ~ 3599）

### 輸出說明

- 輸出一行：兩個整數，以空格分隔，分別為分鐘數和剩餘秒數

### 範例

**輸入：**

```
135
```

**輸出：**

```
2 15
```
