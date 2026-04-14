---
layout: challenge
id: 20
title: 自動販賣機找零
difficulty: medium
tags: [if-else, 整除, 取餘數, 綜合]
algorithm: vending_change
testcase_count: 10
params:
  price:
    type: int
    min: 10
    max: 200
  payment:
    type: int
    min: 10
    max: 500
generator: |
  price = int(input())
  payment = int(input())
  if payment < price:
      print("Insufficient")
  else:
      change = payment - price
      c50 = change // 50
      change = change % 50
      c10 = change // 10
      change = change % 10
      c5 = change // 5
      c1 = change % 5
      print(c50, c10, c5, c1)
starter_code: |
  # 讀取商品價格和投入金額，計算找零的硬幣組合
chapter: ch1
description: 計算自動販賣機的找零硬幣數量
---

## 自動販賣機找零

自動販賣機收到付款後，需要找零。用最少的硬幣組合找零給顧客。

### 規則

1. 若付款金額**不足**（付款 < 價格），輸出 `Insufficient`
2. 否則，依序使用以下面額找零：
   - 50 元硬幣
   - 10 元硬幣
   - 5 元硬幣
   - 1 元硬幣
3. 輸出各面額的枚數

### 輸入說明

- 兩行輸入：
  - 第一行：商品價格（正整數，10 ~ 200）
  - 第二行：投入金額（正整數，10 ~ 500）

### 輸出說明

- 若付款不足，輸出 `Insufficient`
- 否則輸出四個以空格分隔的整數，分別代表 50 元、10 元、5 元、1 元硬幣的枚數

### 範例

**輸入：**

```
30
100
```

**輸出：**

```
1 2 0 0
```

---

**輸入：**

```
200
100
```

**輸出：**

```
Insufficient
```

---

**輸入：**

```
100
100
```

**輸出：**

```
0 0 0 0
```
