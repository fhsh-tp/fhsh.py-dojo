---
layout: challenge
id: 30
title: 三角形分類器
difficulty: medium
tags: [if-elif-else, 邏輯運算, 幾何]
algorithm: triangle_classify
testcase_count: 10
params:
  a:
    type: int
    min: 1
    max: 100
  b:
    type: int
    min: 1
    max: 100
  c:
    type: int
    min: 1
    max: 100
generator: |
  a = int(input())
  b = int(input())
  c = int(input())
  if a + b > c and a + c > b and b + c > a:
      if a == b == c:
          print("Equilateral")
      elif a == b or b == c or a == c:
          print("Isosceles")
      else:
          print("Scalene")
  else:
      print("Not a Triangle")
starter_code: |
  # 讀取三個邊長，判斷能否構成三角形，若可以則分類
---

## 三角形分類器

給定三個正整數代表邊長，先判斷能否構成三角形，再進行分類。

### 規則

1. 先檢查**三角不等式**：任意兩邊之和必須大於第三邊
2. 通過後分類：
   - 三邊相等 → `Equilateral`（等邊三角形）
   - 恰好兩邊相等 → `Isosceles`（等腰三角形）
   - 三邊都不同 → `Scalene`（不等邊三角形）
3. 不符合三角不等式 → `Not a Triangle`

### 輸入說明

- 三行輸入：三個正整數 a, b, c（1 ~ 100）

### 輸出說明

- 輸出 `Not a Triangle`、`Equilateral`、`Isosceles` 或 `Scalene`

### 範例

**輸入：**

```
3
3
3
```

**輸出：**

```
Equilateral
```

---

**輸入：**

```
3
4
5
```

**輸出：**

```
Scalene
```

---

**輸入：**

```
1
2
10
```

**輸出：**

```
Not a Triangle
```
