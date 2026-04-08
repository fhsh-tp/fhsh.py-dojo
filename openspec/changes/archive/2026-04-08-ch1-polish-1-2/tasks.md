## 1. P-1 punctuation style rule 標點風格統一

- [x] 1.1 逐行掃描 `docs/tutor/py/ch1/1-2.md` 中所有 `——` 的使用。對「例行性子句銜接」的 `——` 改為逗號或冒號。保留 hook/笑話中用於戲劇效果的正當用法。記錄每處修改的行號與改法

## 2. C-1 conversational lead-in rule — Code Block 過場檢查

- [x] 2.1 檢查「實際操作」(L59) 的 `name = "小明"` code block 前是否有過場句。若從 `### 實際操作` 標題直接跳入 code，補上 1 句銜接
- [x] 2.2 檢查「等號不是等於」(L72) 的 `x = 5; x = 10` code block 前是否有足夠的 lead-in
- [x] 2.3 檢查「type()」(L121) 示範 code block 前是否有過場
- [x] 2.4 檢查「伏筆引爆」(L129) 的 `a + b` 型別陷阱 code block 前是否有過場。此段有豐富的敘事鋪陳，可能已足夠——若已足夠則跳過
- [x] 2.5 檢查「型別轉換」(L153) 的 `int(input())` code block 前是否有過場
- [x] 2.6 檢查「基本運算」(L188) 的四則運算 code block 前是否有過場
- [x] 2.7 檢查「整數除法與取餘數」(L206) 的 `//` 和 `%` code block 前是否有過場
- [x] 2.8 檢查「收銀機解題」(L274) 的解題 code block 前是否有過場

## 3. M-1 mental model rule — 求值模型顯性化

- [x] 3.1 確認 `int(input())` (L163-166) 的解說是否包含 step-by-step evaluation trace（先 `input()` 得到字串 → 再 `int()` 轉換為整數）。若只是一句帶過，補上明確的 2~3 步 trace。加上對 1-1 `print(1+1)` 「由內而外」模型的 callback

## 4. S-1 analogy bridge rule — 類比 meta-cognitive bridge

- [x] 4.1 檢查「置物櫃比喻」(L49-56) 前是否有一句 meta-cognitive bridge 說明為什麼要用這個比喻。`### 生活比喻：置物櫃` 前的段落 (L43-47) 描述了記憶體位址的不便，可能已自然構成 bridge——若已充分則跳過，若不夠明確則補一句
- [x] 4.2 檢查「分錢比喻」(L215-218) 前是否有 bridge 說明為什麼要用分錢來解釋 `//` 和 `%`

## 5. S-3 section transition rule — 段落過場密度

- [x] 5.1 檢查「變數→資料型別」過場 (L99)：`好，你會貼標籤了。但標籤上的東西，有分「種類」的⋯⋯` — 評估是否達到 2~4 句的標準。若只有一句，擴展為「摘要→缺口→動機」結構
- [x] 5.2 檢查「資料型別→四則運算」過場 (L182)：`型別搞懂了？來看看數字能玩什麼花樣。` — 同上標準
- [x] 5.3 檢查「四則運算→Judge 解題」過場 (L249)：`好，武器都齊了。來實戰看看！` — 同上標準

## 6. 其餘規則掃描

- [x] 6.1 T-1 terminology forward-reference rule：掃描全檔是否有使用 1-3 或更後面章節的術語（如 `if`、`bool`、迴圈等）。已知 L323 的 `f"{result:.1f}"` 為受控前向引用（標註「偷學一招」），不需修改
- [x] 6.2 S-2 post-humor connector rule：掃描所有 kaomoji/笑話後的下一句，確認有 callback connector
- [x] 6.3 E-1 error prevention rule：確認 `int()` 轉換非數字的情況 (L178)、字串 × 字串報錯 (L303) 的解說語氣充分
- [x] 6.4 最終校讀全檔，確認 prose 語氣一致，無遺漏修改
