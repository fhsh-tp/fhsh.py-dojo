---
layout: challenge
id: py016
title: 二次方程式判別式
difficulty: medium
tags: [if-elif-else, 運算, 數學公式]
algorithm: quadratic_discriminant
testcase_count: 10
params:
  a:
    type: int
    min: 1
    max: 20
  b:
    type: int
    min: -50
    max: 50
  c:
    type: int
    min: -50
    max: 50
generator: |
  a = int(input())
  b = int(input())
  c = int(input())
  d = b * b - 4 * a * c
  if d > 0:
      print("Two Real Roots")
  elif d == 0:
      print("One Repeated Root")
  else:
      print("No Real Roots")
starter_code: |
  # 讀取二次方程式 ax² + bx + c = 0 的係數，用判別式判斷根的情況
chapter: ch1
description: 用判別式判斷二次方程式的根的類型
---

## 二次方程式判別式

給定二次方程式 $ax^2 + bx + c = 0$ 的三個係數，計算判別式 $D = b^2 - 4ac$，判斷根的情況。

### 規則

- $D > 0$ → `Two Real Roots`（兩個相異實根）
- $D = 0$ → `One Repeated Root`（一個重根）
- $D < 0$ → `No Real Roots`（無實根）

### 輸入說明

- 三行輸入：
  - 第一行：整數 a（1 ~ 20）
  - 第二行：整數 b（-50 ~ 50）
  - 第三行：整數 c（-50 ~ 50）

### 輸出說明

- 輸出 `Two Real Roots`、`One Repeated Root` 或 `No Real Roots`

### 範例

**輸入：**

```
1
-5
6
```

**輸出：**

```
Two Real Roots
```

---

**輸入：**

```
1
2
1
```

**輸出：**

```
One Repeated Root
```

---

**輸入：**

```
1
0
1
```

**輸出：**

```
No Real Roots
```
