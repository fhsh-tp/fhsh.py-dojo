---
layout: challenge
id: 7
title: 便利商店找零
difficulty: easy
tags: [變數, 運算, 減法]
algorithm: change_calculator
testcase_count: 5
params:
  price:
    type: int
    min: 10
    max: 500
  payment:
    type: int
    min: 500
    max: 1000
generator: |
  price = int(input())
  payment = int(input())
  print(payment - price)
starter_code: |
  # 讀取商品金額和付款金額，計算並輸出找零
chapter: ch1
description: 讀取商品金額和付款金額，計算找零
---

## 便利商店找零

你在便利商店買東西，店員需要算找零給你。寫一個程式幫忙計算吧！

### 輸入說明

- 第一行：商品金額（正整數）
- 第二行：付款金額（正整數，保證大於等於商品金額）

### 輸出說明

- 輸出一行：找零金額（付款金額 − 商品金額）

### 範例

**輸入：**

```
87
100
```

**輸出：**

```
13
```
