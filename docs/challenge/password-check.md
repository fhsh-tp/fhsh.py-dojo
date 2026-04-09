---
layout: challenge
id: 21
title: 密碼驗證器
difficulty: easy
tags: [while, break, 迴圈控制, 字串比對]
algorithm: password_check
testcase_count: 5
params:
  password:
    type: str
    min_length: 1
    max_length: 20
  max_attempts:
    type: int
    min: 1
    max: 10
generator: |
  password = input()
  max_attempts = int(input())
  for i in range(max_attempts):
      guess = input()
      if guess == password:
          print("OK")
          break
  else:
      print("LOCKED")
starter_code: |
  # 第一行讀取正確密碼，第二行讀取最大嘗試次數 K
  # 接下來最多讀 K 行猜測，猜對印 OK 並結束；K 次都錯印 LOCKED
---

## 密碼驗證器

你有一組正確密碼和最大嘗試次數 K。接下來最多讀 K 次猜測，如果某次猜對了就印出 `OK` 並結束；如果 K 次都猜錯，印出 `LOCKED`。

### 輸入說明

- 第一行：正確密碼（字串）
- 第二行：最大嘗試次數 K（正整數）
- 接下來最多 K 行：每行一個猜測字串

### 輸出說明

- 猜對了：印出 `OK`
- K 次都錯：印出 `LOCKED`

### 範例

**輸入：**

```
abc123
3
wrong
abc123
```

**輸出：**

```
OK
```
