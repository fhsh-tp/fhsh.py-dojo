---
layout: challenge
id: py031
title: 密碼驗證器
difficulty: easy
tags: [while, break, 迴圈控制, 字串比對]
algorithm: password_check
testcase_count: 5
params:
  password:
    type: printable_ascii
    min_len: 1
    max_len: 20
  max_attempts:
    type: int
    min: 1
    max: 10
generator: |
  import json, random, string
  password = input()
  max_attempts = int(input())
  # Decide which round (0-based) the correct guess appears, or -1 for all wrong
  correct_round = random.choice(list(range(max_attempts)) + [-1])
  def rand_wrong(pw):
      while True:
          length = random.randint(1, 20)
          chars = [chr(c) for c in range(0x21, 0x7f)]
          g = ''.join(random.choices(chars, k=length))
          if g != pw:
              return g
  guesses = []
  for i in range(max_attempts):
      if i == correct_round:
          guesses.append(password)
          break
      else:
          guesses.append(rand_wrong(password))
  num_guesses = len(guesses)
  lines = [password, str(max_attempts)] + guesses
  full_input = '\n'.join(lines)
  expected_output = 'OK' if correct_round >= 0 else 'LOCKED'
  print(json.dumps({"input": full_input, "expected_output": expected_output}))
reference_solution: |
  password = input()
  k = int(input())
  for _ in range(k):
      if input() == password:
          print('OK')
          break
  else:
      print('LOCKED')
starter_code: |
  # 第一行讀取正確密碼，第二行讀取最大嘗試次數 K
  # 接下來最多讀 K 行猜測，猜對印 OK 並結束；K 次都錯印 LOCKED
chapter: ch2
description: 模擬密碼驗證，限制嘗試次數
---

## 密碼驗證器

你有一組正確密碼和最大嘗試次數 $K$。接下來最多讀 $K$ 次猜測，如果某次猜對了就印出 `OK` 並結束；如果 $K$ 次都猜錯，印出 `LOCKED`。

### 輸入說明

- 第一行：正確密碼（字串）
- 第二行：最大嘗試次數 $K$（正整數）
- 接下來最多 $K$ 行：每行一個猜測字串

### 輸出說明

- 猜對了：印出 `OK`
- $K$ 次都錯：印出 `LOCKED`

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
