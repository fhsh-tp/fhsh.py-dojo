---
layout: challenge
id: 4
title: 自我介紹產生器
difficulty: easy
tags: [print, input, 字串]
algorithm: self_introduction
testcase_count: 5
params:
  name:
    type: alpha_mixed
    min_len: 2
    max_len: 8
  age:
    type: int
    min: 14
    max: 18
generator: |
  name = input()
  age = input()
  print(f"Hi, I'm {name} and I'm {age} years old.")
starter_code: |
  # 讀取名字和年齡，輸出自我介紹
chapter: ch1
description: 讀取名字和年齡，輸出英文自我介紹
---

## 自我介紹產生器

幫新同學寫一個自動產生英文自我介紹的程式。

### 輸入說明

- 第一行：名字（英文字母組成）
- 第二行：年齡（正整數）

### 輸出說明

- 輸出一行：`Hi, I'm [名字] and I'm [年齡] years old.`

### 範例

**輸入：**

```
Bob
16
```

**輸出：**

```
Hi, I'm Bob and I'm 16 years old.
```
