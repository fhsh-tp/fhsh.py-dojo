---
layout: challenge
id: 2
title: 飲料店的收銀機
difficulty: easy
tags: [變數, 運算, input, int]
algorithm: beverage_cashier
testcase_count: 5
params:
  quantity:
    type: int
    min: 1
    max: 20
  price:
    type: int
    min: 20
    max: 80
generator: |
  quantity = int(input())
  price = int(input())
  print(quantity * price)
starter_code: |
  # 讀取珍珠奶茶的數量和每杯單價，計算並輸出總金額
---

## 飲料店的收銀機

學校旁邊的飲料店需要一台自動收銀機，幫忙計算客人買珍珠奶茶的總金額。

### 輸入說明

- 第一行：珍珠奶茶的數量（正整數，1 ~ 20）
- 第二行：每杯的單價（正整數，20 ~ 80）

### 輸出說明

- 輸出一行：總金額（數量 × 單價）

### 範例

**輸入：**

```
3
55
```

**輸出：**

```
165
```
