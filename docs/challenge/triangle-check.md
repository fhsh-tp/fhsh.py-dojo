---
layout: challenge
id: 10
title: 三角形判斷
difficulty: easy
tags: [if-else, 邏輯運算, and]
algorithm: triangle_check
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
      print("YES")
  else:
      print("NO")
starter_code: |
  # 讀取三個正整數，判斷能否構成三角形
---

## 三角形判斷

給定三個正整數，判斷它們能不能構成一個三角形。

### 三角形規則

任意兩邊之和必須大於第三邊。

### 輸入說明

- 三行輸入，每行一個正整數（1 ~ 100），代表三邊長度

### 輸出說明

- 如果能構成三角形，輸出 `YES`
- 如果不能，輸出 `NO`

### 範例

**輸入：**

```
3
4
5
```

**輸出：**

```
YES
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
NO
```
