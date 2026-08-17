---
layout: challenge
id: py005
title: 鸚鵡學舌
difficulty: easy
tags: [print, input, 字串]
algorithm: parrot_echo
testcase_count: 5
params:
  word:
    type: alpha_mixed
    min_len: 1
    max_len: 20
generator: |
  word = input()
  print(word)
  print(word)
  print(word)
starter_code: |
  # 讀取一行字串，連續輸出三次（每次一行）
chapter: ch1
description: 讀取一行字串，連續輸出三次
---

## 鸚鵡學舌

你養了一隻鸚鵡，牠會把你說的話重複三遍。寫一個模擬鸚鵡的程式吧！

### 輸入說明

- 一行輸入：一個字串 $S$

### 輸出說明

- 將 $S$ 連續輸出三次，每次各佔一行

### 範例

**輸入：**

```
Hello
```

**輸出：**

```
Hello
Hello
Hello
```
