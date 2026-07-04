---
layout: challenge
id: 1
title: 哈囉，世界！
difficulty: easy
tags: [print, input, 字串]
algorithm: hello_world
testcase_count: 5
params:
  name:
    type: alpha_mixed
    min_len: 2
    max_len: 10
generator: |
  name = input()
  print("Hello,", name)
reference_solution: |
  name = input()
  print(f"Hello, {name}")
starter_code: |
  # 讀取輸入的名字，然後輸出 Hello, [名字]
chapter: ch1
description: 讀取使用者的名字，然後跟他打招呼
---

## 哈囉，世界！

你的第一個程式挑戰！讀取使用者的名字，然後跟他打招呼。

### 輸入說明

- 一行輸入：一個字串 S（使用者的名字，由英文字母組成）

### 輸出說明

- 輸出一行：`Hello, S`（注意逗號後有一個空格）

### 範例

**輸入：**

```
Alice
```

**輸出：**

```
Hello, Alice
```
