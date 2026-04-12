---
layout: doc
title: Appendix
description: 產生圖片的 AI 提示詞負責任揭露
chapter: 1
---

# Python Keywords Table

Python 有一組**保留字**（又叫「關鍵字」，Reserved Words / Keywords），它們是 Python 直譯器為了辨識語法而預先「掛牌」的詞彙。簡單講就是：這些字是 Python 內建的 VIP，你不能拿它們當變數名，否則直譯器會翻桌給你看。

例如你如果興沖沖地寫：

```python
if = 3   # ❌ 這會炸
```

Python 會立刻回你這個錯誤訊息：

```
  File "<stdin>", line 1
    if = 3
       ^
SyntaxError: invalid syntax
```

> [!WARNING]
> **避雷提示**：只要你拿底下 39 個字中的任何一個當變數名，都會得到 `SyntaxError`。如果 VS Code / Google Colab 幫你把某個字自動上色（紫色或藍色粗體），那就是保留字了，別碰。

截至本章為止（1-1 ～ 1-4），你其實只學到 8 個關鍵字：`True`、`False`、`and`、`or`、`not`、`if`、`elif`、`else`。剩下的 27 個硬關鍵字和 4 個軟關鍵字會在接下來的章節陸續登場；下面的表格會告訴你每個字「什麼時候會遇到」，方便你自我檢查學習進度。

> [!TIP]
> **硬 vs 軟關鍵字**：Python 把關鍵字分成兩種：
>
> - **硬關鍵字（Hard Keywords）**：永遠不能當變數名，共 35 個。
> - **軟關鍵字（Soft Keywords）**：只在特定語境（例如 `match` / `case` 語句裡）才算關鍵字，其他場合可以當變數名使用，共 4 個。
>
> 高中 APCS 考試不會考你「背出全部 39 個」，但認得它們、知道「這是 Python 的內建語法詞」就夠了。「首次登場章節」欄位標示 `1-3 ✅` 代表你已經在本章學過；標示 `2-1`、`3-1` 等代表會在未來章節登場；標示 `—` 代表本課綱四個模組內不會正式教，通常是進階主題或 APCS 不常考的語法。

## 硬關鍵字（Hard Keywords）

### 常數值

| 關鍵字  | 中文簡述               | 首次登場章節 | 示例                 |
| ------- | ---------------------- | ------------ | -------------------- |
| `False` | 布林假值（邏輯 0）     | 1-3 ✅        | `is_raining = False` |
| `None`  | 「什麼都沒有」的特殊值 | —            | `result = None`      |
| `True`  | 布林真值（邏輯 1）     | 1-3 ✅        | `is_student = True`  |

### 邏輯運算

| 關鍵字 | 中文簡述                   | 首次登場章節 | 示例                       |
| ------ | -------------------------- | ------------ | -------------------------- |
| `and`  | 邏輯「且」，兩邊都真才真   | 1-3 ✅        | `age >= 18 and has_id`     |
| `not`  | 邏輯「否」，把真假顛倒     | 1-3 ✅        | `not is_raining`           |
| `or`   | 邏輯「或」，任一邊為真即真 | 1-3 ✅        | `is_weekend or is_holiday` |

### 條件判斷

| 關鍵字 | 中文簡述                     | 首次登場章節 | 示例                |
| ------ | ---------------------------- | ------------ | ------------------- |
| `if`   | 「如果」：條件成立就執行     | 1-3 ✅        | `if score >= 60:`   |
| `elif` | 「否則如果」：再試下一個條件 | 1-3 ✅        | `elif score >= 40:` |
| `else` | 「否則」：以上都不成立時執行 | 1-3 ✅        | `else:`             |

### 迴圈控制

| 關鍵字     | 中文簡述                             | 首次登場章節 | 示例                      |
| ---------- | ------------------------------------ | ------------ | ------------------------- |
| `for`      | 固定次數或逐一取元素的迴圈           | 2-1          | `for i in range(10):`     |
| `while`    | 條件成立就一直重複的迴圈             | 2-1          | `while n > 0:`            |
| `break`    | 立刻跳出目前的迴圈                   | 2-1          | `if found: break`         |
| `continue` | 跳過這一圈剩下的部分，直接進入下一圈 | 2-1          | `if n % 2 == 0: continue` |

### 函式與類別

| 關鍵字   | 中文簡述                 | 首次登場章節 | 示例                 |
| -------- | ------------------------ | ------------ | -------------------- |
| `def`    | 定義一個函式             | 3-1          | `def add(a, b):`     |
| `return` | 從函式把結果交回呼叫者   | 3-1          | `return a + b`       |
| `lambda` | 一行寫完的匿名函式       | 4-1          | `key=lambda x: x[1]` |
| `class`  | 定義一個類別（物件模版） | —            | `class Dog:`         |

### 例外處理

| 關鍵字    | 中文簡述                         | 首次登場章節 | 示例                      |
| --------- | -------------------------------- | ------------ | ------------------------- |
| `try`     | 嘗試執行可能會出錯的程式區塊     | 3-3          | `try:`                    |
| `except`  | 攔截 `try` 區塊裡的錯誤並處理    | 3-3          | `except ValueError:`      |
| `finally` | 不論成功或失敗都會執行的收尾區塊 | —            | `finally: file.close()`   |
| `raise`   | 主動丟出一個錯誤                 | —            | `raise ValueError("bad")` |
| `assert`  | 斷言條件為真，否則直接丟出錯誤   | —            | `assert n > 0`            |

### 匯入

| 關鍵字   | 中文簡述                     | 首次登場章節 | 示例                   |
| -------- | ---------------------------- | ------------ | ---------------------- |
| `import` | 匯入整個模組                 | 4-2          | `import math`          |
| `from`   | 從模組挑特定東西來匯入       | 4-2          | `from math import gcd` |
| `as`     | 給匯入的東西（或變數）取別名 | 4-2          | `import numpy as np`   |

### 範圍與作用域

| 關鍵字     | 中文簡述                       | 首次登場章節 | 示例             |
| ---------- | ------------------------------ | ------------ | ---------------- |
| `global`   | 宣告變數來自全域範圍           | —            | `global counter` |
| `nonlocal` | 宣告變數來自外層（非全域）函式 | —            | `nonlocal total` |

### 非同步

| 關鍵字  | 中文簡述                   | 首次登場章節 | 示例                   |
| ------- | -------------------------- | ------------ | ---------------------- |
| `async` | 宣告一個非同步（協程）函式 | —            | `async def fetch():`   |
| `await` | 等待一個非同步結果         | —            | `data = await fetch()` |

### 其他

| 關鍵字  | 中文簡述                          | 首次登場章節 | 示例                 |
| ------- | --------------------------------- | ------------ | -------------------- |
| `in`    | 成員判斷，也是 `for` 迴圈的搭配詞 | 2-1          | `for x in items:`    |
| `is`    | 身份比較（是否為同一個物件）      | —            | `x is None`          |
| `del`   | 刪除變數或容器中的元素            | —            | `del my_list[0]`     |
| `pass`  | 什麼都不做的佔位符                | —            | `def todo(): pass`   |
| `with`  | 自動管理資源開關的區塊            | —            | `with open(f) as x:` |
| `yield` | 產生器函式產出一個值              | —            | `yield n`            |

## 軟關鍵字（Soft Keywords）

軟關鍵字是 Python 的彈性設計：它們只在**特定語境**才算關鍵字，其他場合可以當變數名使用（但為了可讀性，不建議這麼做）。

| 關鍵字  | 中文簡述                                | 首次登場章節 | 示例                        |
| ------- | --------------------------------------- | ------------ | --------------------------- |
| `match` | 模式匹配（Python 3.10+ 的 Switch Case） | 4-1          | `match shape:`              |
| `case`  | 搭配 `match` 的單一分支                 | 4-1          | `case "circle":`            |
| `_`     | 通配符（Wildcard），匹配任何東西        | —            | `case _:`                   |
| `type`  | 定義型別別名（Python 3.12+）            | —            | `type Vector = list[float]` |

> [!TIP]
> **學習建議**：高中課綱和 APCS 檢定**不會**考你「寫出所有 39 個 Python 關鍵字」，所以不要硬背。你只要記住一件事：「這些字是 Python 內建的 VIP，不要拿它們當自己的變數名」。等到遇到哪個字再回來查表就好，表格會陪你一整個學期 (＾◡＾)。
>
> 另外，現在的 IDE（VS Code、Google Colab 等）都會自動把關鍵字上色標記，所以萬一你不小心打錯把關鍵字當變數名用，編輯器通常會在第一時間提醒你。

# Image Specification Appendix

## 1-1

### 圖 1
1. **類型**：四格漫畫（Hook）
2. **意圖**：以學生對電腦大喊卻得到 0101 回應的反差，吸引讀者進入「人機溝通」主題
3. **完整 Prompt**：American stick figure comic strip, clean black ink on white background, minimalist line art, 4-panel horizontal layout, numbered panels 1-4, expressive stick figures with simple dot eyes and line mouths, humorous tone, dialogue-driven narrative with speech bubbles only and no narration boxes, speech bubble text in Traditional Chinese Taiwan usage with technical terms in English, consistent character design across all panels, panel 1: a student stick figure sitting at desk facing a computer monitor with a confident expression and speech bubble saying 我要學 Python, panel 2: student typing furiously on keyboard with speech bubble saying 幫我寫作業, panel 3: computer monitor displaying confused binary 01010011 with a question mark speech bubble saying 啥？, panel 4: student slumping in chair with defeated expression and computer showing speech bubble saying 請說我聽得懂的話 with a smug expression on the monitor face
4. **備註**：四格分鏡需有明確敘事弧線，電腦螢幕要有擬人化的簡單臉部表情

### 圖 2
1. **類型**：四格漫畫（Explanation）
2. **意圖**：用擬人化角色說明 IPO 流程，讓學生直覺理解 Input → Process → Output 的概念
3. **完整 Prompt**：American stick figure comic strip, clean black ink on white background, minimalist line art, 4-panel horizontal layout, numbered panels 1-4, expressive stick figures with simple dot eyes and line mouths, humorous tone, dialogue-driven narrative with speech bubbles only and no narration boxes, speech bubble text in Traditional Chinese Taiwan usage with technical terms in English, consistent character design across all panels, panel 1: stick figure labeled 題目 handing a paper scroll to another stick figure labeled 你的程式 with speech bubble saying 這是 Input, panel 2: 你的程式 stick figure thinking hard with gears above head and speech bubble saying 讓我 Process 一下, panel 3: 你的程式 stick figure proudly holding up a result paper with speech bubble saying Output 完成, panel 4: a robot judge stick figure with glasses comparing the result to an answer sheet with speech bubble saying 答對了 and a checkmark
4. **備註**：四個角色要有不同的視覺特徵（標籤、道具），讓學生一眼看出誰是誰

### 圖 3
1. **類型**：四格漫畫（Hook）
2. **意圖**：以電腦第一次「開口說話」的驚喜感，強化 print() 的功能印象
3. **完整 Prompt**：American stick figure comic strip, clean black ink on white background, minimalist line art, 4-panel horizontal layout, numbered panels 1-4, expressive stick figures with simple dot eyes and line mouths, humorous tone, dialogue-driven narrative with speech bubbles only and no narration boxes, speech bubble text in Traditional Chinese Taiwan usage with technical terms in English, consistent character design across all panels, panel 1: student stick figure typing print Hello on keyboard with nervous expression and speech bubble saying 拜託動一下, panel 2: computer monitor suddenly displaying Hello with a speech bubble saying Hello and the monitor has a smiling face, panel 3: student jumping back in shock with speech bubble saying 你...你會說話, panel 4: student hugging the monitor with tears of joy and speech bubble saying 我的電腦終於理我了 while computer speech bubble says 別這樣很噁心
4. **備註**：第四格的「擁抱電腦」需要有適度誇張的喜劇效果

### 圖 4
1. **類型**：四格漫畫（Analogy）
2. **意圖**：用 input() 的互動過程，展示「電腦也能聽你說話」的雙向溝通
3. **完整 Prompt**：American stick figure comic strip, clean black ink on white background, minimalist line art, 4-panel horizontal layout, numbered panels 1-4, expressive stick figures with simple dot eyes and line mouths, humorous tone, dialogue-driven narrative with speech bubbles only and no narration boxes, speech bubble text in Traditional Chinese Taiwan usage with technical terms in English, consistent character design across all panels, panel 1: computer monitor stick figure with a curious face and speech bubble saying input 啟動 你叫什麼名字, panel 2: student stick figure typing on keyboard with confident expression and speech bubble saying 我叫小明, panel 3: computer processing with sparkle effects and speech bubble saying 收到 name 等於 小明, panel 4: computer and student both happy with computer speech bubble saying Hello 小明 and student speech bubble saying 你終於聽懂我說話了
4. **備註**：強調互動的雙向性，電腦和學生的表情都要有變化

## 1-2

### 圖 5
1. **類型**：四格漫畫（Hook）
2. **意圖**：以「記電話號碼」的日常痛點引出變數的必要性
3. **完整 Prompt**：American stick figure comic strip, clean black ink on white background, minimalist line art, 4-panel horizontal layout, numbered panels 1-4, expressive stick figures with simple dot eyes and line mouths, humorous tone, dialogue-driven narrative with speech bubbles only and no narration boxes, speech bubble text in Traditional Chinese Taiwan usage with technical terms in English, consistent character design across all panels, panel 1: teacher stick figure pointing at blackboard with speech bubble saying 來 背下全班40個電話號碼, panel 2: student stick figure trying to memorize with numbers floating around head and speech bubble saying 0912...0935...等等第一個是什麼, panel 3: student head literally exploding with numbers flying everywhere and speech bubble saying 腦容量不足, panel 4: a computer stick figure calmly organizing papers into labeled folders with speech bubble saying 我用 variable 就好了 輕鬆
4. **備註**：第三格的「爆炸」用漫畫誇飾法，數字從頭部噴出；第四格電腦的從容對比強烈

### 圖 6
1. **類型**：四格漫畫（Explanation）
2. **意圖**：用置物櫃的比喻視覺化「變數 = 記憶體標籤」的概念
3. **完整 Prompt**：American stick figure comic strip, clean black ink on white background, minimalist line art, 4-panel horizontal layout, numbered panels 1-4, expressive stick figures with simple dot eyes and line mouths, humorous tone, dialogue-driven narrative with speech bubbles only and no narration boxes, speech bubble text in Traditional Chinese Taiwan usage with technical terms in English, consistent character design across all panels, panel 1: stick figure pointing at a row of school lockers with speech bubble saying 每個櫃子都有編號 0x7FFF, panel 2: stick figure sticking a label that says name on one locker with speech bubble saying 但我叫它 name 比較好記, panel 3: stick figure opening the locker revealing 小明 text inside with speech bubble saying 裡面放的就是資料, panel 4: another stick figure asking with speech bubble saying name 在哪 and first stick figure pointing at the labeled locker with speech bubble saying 就在那 不用背編號
4. **備註**：置物櫃要畫出格子感，標籤要清楚可辨

### 圖 7
1. **類型**：四格漫畫（Hook）
2. **意圖**：以「1+2=12」的經典初學者陷阱製造驚愕效果，強化型別意識
3. **完整 Prompt**：American stick figure comic strip, clean black ink on white background, minimalist line art, 4-panel horizontal layout, numbered panels 1-4, expressive stick figures with simple dot eyes and line mouths, humorous tone, dialogue-driven narrative with speech bubbles only and no narration boxes, speech bubble text in Traditional Chinese Taiwan usage with technical terms in English, consistent character design across all panels, panel 1: student stick figure confidently writing code on screen with speech bubble saying a 等於 input 然後 b 等於 input 再 print a加b 穩了, panel 2: student typing input values 1 and 2 with speech bubble saying 1 加 2 等於 3 easy, panel 3: screen showing output 12 in large text with student having shocked frozen face and speech bubble saying 什麼...12, panel 4: Python logo stick figure wearing sunglasses with speech bubble saying 字串的加法是串接哦 while student has tears streaming down face
4. **備註**：第三格的 12 要用大字體凸顯衝擊感，Python 的擬人角色可以用蛇的簡單圖案

### 圖 8
1. **類型**：四格漫畫（Explanation）
2. **意圖**：用分錢的生活場景直覺解釋 // 和 % 的差別
3. **完整 Prompt**：American stick figure comic strip, clean black ink on white background, minimalist line art, 4-panel horizontal layout, numbered panels 1-4, expressive stick figures with simple dot eyes and line mouths, humorous tone, dialogue-driven narrative with speech bubbles only and no narration boxes, speech bubble text in Traditional Chinese Taiwan usage with technical terms in English, consistent character design across all panels, panel 1: stick figure holding 100 dollar bill with speech bubble saying 100元要分給3個人, panel 2: three stick figures each receiving 33 with a division symbol and speech bubble from first figure saying 100 整除 3 每人33元, panel 3: first stick figure holding a single coin with speech bubble saying 100 取餘 3 剩下1元, panel 4: all four stick figures together with the three each holding 33 and one person holding the leftover 1 coin with speech bubble saying 所以整除給你商 取餘給你剩的
4. **備註**：金額用簡單的圓形硬幣或鈔票符號表示