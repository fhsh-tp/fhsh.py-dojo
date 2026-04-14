---
layout: challenge
id: 14
title: 座標象限判斷
difficulty: easy
tags: [if-elif-else, 邏輯運算, 座標]
algorithm: quadrant_classifier
testcase_count: 10
params:
  x:
    type: int
    min: -100
    max: 100
  y:
    type: int
    min: -100
    max: 100
generator: |
  x = int(input())
  y = int(input())
  if x == 0 and y == 0:
      print("Origin")
  elif y == 0:
      print("X-axis")
  elif x == 0:
      print("Y-axis")
  elif x > 0 and y > 0:
      print("Quadrant 1")
  elif x < 0 and y > 0:
      print("Quadrant 2")
  elif x < 0 and y < 0:
      print("Quadrant 3")
  else:
      print("Quadrant 4")
starter_code: |
  # 讀取座標 (x, y)，判斷它在哪個象限、哪條軸上、或是原點
chapter: ch1
description: 判斷座標點所在的象限
---

## 座標象限判斷

給定一個座標點 (x, y)，判斷它在第幾象限、在哪條軸上、或是原點。

### 七種情況

1. 原點：x = 0 且 y = 0 → `Origin`
2. X 軸上：y = 0（且 x != 0）→ `X-axis`
3. Y 軸上：x = 0（且 y != 0）→ `Y-axis`
4. 第一象限：x > 0 且 y > 0 → `Quadrant 1`
5. 第二象限：x < 0 且 y > 0 → `Quadrant 2`
6. 第三象限：x < 0 且 y < 0 → `Quadrant 3`
7. 第四象限：x > 0 且 y < 0 → `Quadrant 4`

### 輸入說明

- 兩行輸入：
  - 第一行：整數 x（-100 ~ 100）
  - 第二行：整數 y（-100 ~ 100）

### 輸出說明

- 輸出 `Origin`、`X-axis`、`Y-axis`、`Quadrant 1`、`Quadrant 2`、`Quadrant 3` 或 `Quadrant 4`

### 範例

**輸入：**

```
3
4
```

**輸出：**

```
Quadrant 1
```

---

**輸入：**

```
0
0
```

**輸出：**

```
Origin
```

---

**輸入：**

```
-5
0
```

**輸出：**

```
X-axis
```
