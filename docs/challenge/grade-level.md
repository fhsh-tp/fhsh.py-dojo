---
layout: challenge
id: py009
title: 成績等第
difficulty: easy
tags: [if-elif-else, 流程控制]
algorithm: grade_level
testcase_count: 10
params:
  score:
    type: int
    min: 0
    max: 100
generator: |
  score = int(input())
  if score >= 90:
      print("A")
  elif score >= 80:
      print("B")
  elif score >= 70:
      print("C")
  elif score >= 60:
      print("D")
  else:
      print("F")
starter_code: |
  # 讀取一個成績，根據分數輸出對應的等第
chapter: ch1
description: 根據分數輸出對應的成績等第
---

## 成績等第

老師需要把分數轉換成等第。寫一個程式幫忙判斷吧！

### 等第規則

| 分數範圍 | 等第 |
|---------|------|
| 90 ~ 100 | A |
| 80 ~ 89 | B |
| 70 ~ 79 | C |
| 60 ~ 69 | D |
| 0 ~ 59 | F |

### 輸入說明

- 一行輸入：一個整數（0 ~ 100），代表成績

### 輸出說明

- 輸出一行：對應的等第（A、B、C、D 或 F）

### 範例

**輸入：**

```
85
```

**輸出：**

```
B
```
