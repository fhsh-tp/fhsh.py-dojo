## 1. 填補 TBD：Code Block 過場 — Chapter 1 code blocks follow conversational lead-in rule C-1

- [x] 1.1 [Chapter 1 code blocks follow conversational lead-in rule C-1] 在 `### 第一步：印出一段文字`（L134）的 `<!-- TBD 加一個過場 -->` 位置，補上 1~2 句過場。方向：從前面的 `print()` 總論銜接到「來試試最簡單的——印一段固定文字」。移除 TBD 註解
- [x] 1.2 在 `### 第二步：印出計算結果`（L161）的 `<!-- TBD 再加一個過場 -->` 位置，補上 1~2 句過場。方向：「你會印固定文字了。但如果 print() 只能印寫死的東西，那跟在螢幕上貼便利貼有什麼差別？」引出 print 能做計算。移除 TBD 註解
- [x] 1.3 在 `### 第三步：印出多個東西`（L181）的 `<!-- TBD 加一個過場 -->` 位置，補上 1~2 句過場。方向：「印一個東西會了。但如果我想同時印名字和成績呢？」引出 print 多參數。移除 TBD 註解

## 2. 填補 TBD：引號混用警告 — Chapter 1 sections follow error prevention rule E-1

- [x] 2.1 [Chapter 1 sections follow error prevention rule E-1] 在 L155-156 的 `[!WARNING] 想想英文文法` 區塊中，補上完整的說明內容。用英文文法的「opening/closing quotes must match」類比 Python 的 `"..."` 和 `'...'` 規則，明確指出 `"Hello'` 是語法錯誤。包含一個正確/錯誤的 code 對比範例。移除 TBD 註解

## 3. 填補 TBD：求值模型 — Chapter 1 code examples follow mental model rule M-1

- [x] 3.1 [Chapter 1 code examples follow mental model rule M-1] 在 L174 的 `<!-- TBD 說明 print(1+1) 時電腦中發生什麼事 -->` 位置，補上 `print(1+1)` 的 step-by-step evaluation trace。格式：Step 1: Python 看到 `print(...)` → Step 2: 先算括號裡的 `1+1` 得到 `2` → Step 3: 把 `2` 交給 `print()` → 印出 `2`。以「由內而外」作為記憶口訣。加上 forward reference：「這個『由內而外』的規則，下一節的 `int(input())` 也是同一個道理。」移除 TBD 註解

## 4. 填補 TBD：print → input 過場 — Chapter 1 sections follow section transition rule S-3

- [x] 4.1 [Chapter 1 sections follow section transition rule S-3] 將 L202-206 之間 `<!-- [START] TBD -->` 和 `<!-- [END] TBD -->` 包裹的一句話過場，擴展為 2~4 句。結構：(a) 摘要「你已經學會讓電腦說話了」 (b) 指出缺口「但它只能自言自語——它不知道你是誰、你要什麼」 (c) 引出動機「如果程式能『聽』你說話，就能根據你的回答做出不同的事」。保持 Phoenix 的對話語氣。移除 `[START]/[END]` TBD 註解

## 5. 全檔審計：其餘規則

- [x] 5.1 Chapter 1 sections follow punctuation style rule P-1：掃描全檔，確認 Phoenix 已完成的修改（4 處破折號→逗號/冒號）之外，是否還有其他 `——` 需要修正。保留 hook/笑話中的正當用法（如 L17 的 `第一步——讓電腦聽你的話` 屬於標題式強調，可保留）
- [x] 5.2 Chapter 1 sections follow terminology forward-reference rule T-1：掃描全檔，確認 Phoenix 已完成 2 處修改之外，是否還有其他前向引用。特別檢查 `input()` 段落（L208-248）使用「變數」時是否符合受控前向引用的標準
- [x] 5.3 Chapter 1 sections follow analogy bridge rule S-1：掃描全檔，確認 Phoenix 已加的計算機比喻 bridge 之外，Google 搜尋框比喻（L214-215）前是否有 meta-cognitive bridge。若無，補上
- [x] 5.4 Chapter 1 sections follow post-humor connector rule S-2：掃描全檔，確認 Phoenix 已加的「沒錯！」之外，其他笑話/kaomoji 後是否有 callback connector。重點檢查 L106 的 `_(´ཀ`」 ∠)_` 後的銜接
- [x] 5.5 最終校讀全檔，確認所有 TBD/TODO 註解已移除，prose 語氣一致，無遺漏
