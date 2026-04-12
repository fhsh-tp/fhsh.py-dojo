---
layout: challenge
id: 28
title: BMI 健康分級
difficulty: easy
tags: [if-elif-else, 運算, 公式]
algorithm: bmi_classifier
testcase_count: 10
params:
  weight:
    type: int
    min: 30
    max: 150
  height:
    type: int
    min: 130
    max: 200
generator: |
  weight = int(input())
  height = int(input())
  bmi = weight / (height / 100) / (height / 100)
  if bmi < 18.5:
      print("Underweight")
  elif bmi < 24:
      print("Normal")
  elif bmi < 27:
      print("Overweight")
  else:
      print("Obese")
starter_code: |
  # 讀取體重（公斤）和身高（公分），計算 BMI 並分級
chapter: ch1
description: 根據體重身高計算 BMI 並分級
---

## BMI 健康分級

給定體重和身高，計算 BMI 並根據衛福部標準分級。

### 計算公式

BMI = 體重(kg) / 身高(m)²

### 分級標準

| BMI 範圍 | 分級 |
|---------|------|
| < 18.5 | Underweight |
| 18.5 ~ 24（不含 24） | Normal |
| 24 ~ 27（不含 27） | Overweight |
| >= 27 | Obese |

### 輸入說明

- 兩行輸入：
  - 第一行：體重（公斤，整數，30 ~ 150）
  - 第二行：身高（公分，整數，130 ~ 200）

### 輸出說明

- 輸出 `Underweight`、`Normal`、`Overweight` 或 `Obese`

### 範例

**輸入：**

```
60
170
```

**輸出：**

```
Normal
```

---

**輸入：**

```
50
170
```

**輸出：**

```
Underweight
```
