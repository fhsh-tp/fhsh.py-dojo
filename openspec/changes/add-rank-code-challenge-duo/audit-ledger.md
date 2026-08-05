# Audit 裁決帳本（add-rank-code-challenge-duo）

> 目的：每一條 audit finding 的**終局裁決**記錄。後續輪次的 finder 與統整者必須先對照本表 reconcile——已裁決項目（含「接受殘餘」）不得以相同理由復活；要推翻既有裁決必須引用新 evidence。
> 標尺（凍結）：must-fix＝會改變判題 verdict／建置測試失敗／違反 spec SHALL／誤導學生；should-fix＝文件不一致不影響上線行為；nit＝風格。收斂條件＝該輪無 must-fix。

| # | Round | 維度 | Finding 摘要 | 對抗驗證 | 終局裁決 | 處置（commit） |
|---|-------|------|--------------|----------|----------|----------------|
| 1 | R1 | semantics＋cliff | 10212 出貨 reference 在最貴角落 2.33~2.49M ops，超過 spec R4 自訂 ≤2M；設計期探針量的是分號單行精簡體（5.55 vs 7.75 ops/iter），量測對象≠出貨物 | 反駁 CONFIRMED（must-fix）×2、副作用 DOWNGRADED | **成立（must-fix）**：reference 瘦身（移除 %10 預剝層）＋門檻由上限/5 修正為上限/4（2.5M）＋全數據以出貨碼逐字重測（矩陣 F5/F10、design Context/D2、spec R4、notes 5.1） | R1 fix |
| 2 | R1 | semantics＋cliff | 568 正解記錄失真 1.49×（記 1.31M/7.6×，出貨碼實測 1.96M/5.1×） | 反駁 CONFIRMED（should-fix）×2 | 成立：與 #1 同根同修——568 reference 亦瘦身（移除逐步 cur+=1 結構），實測 1.556M（同值）/1.556M（異值），餘裕 6.4× | R1 fix |
| 3 | R1 | contract | design D4 只列暖身/壓力兩層 band，漏記中段層；且兩題中段角色不對稱（568 天真可過、10212 天真已 TLE） | 反駁 CONFIRMED、副作用 DOWNGRADED（指出原修法「過渡層」句對 10212 錯誤） | 成立：矩陣先增 F18／延伸 F12，再派生 design D4 三層不對稱敘述、tasks 2.1/3.1 band 清單 | R1 fix |
| 4 | R1 | semantics | spec R3 SHALL「separately」與出貨碼淨差簿記（568 gen twos、10212 ref bal）矛盾 | 反駁 CONFIRMED、副作用 DOWNGRADED | 成立：矩陣 F13 改為「符號三分支（分開計數或淨差皆可）」，spec R3 改以 balance b=c2−c5 敘述，design D5 同步——弱化過度指定而非加保證 | R1 fix |
| 5 | R1 | cliff | 矩陣 F1「大數運算完全隱形」對 CPython 3.12+ 巨數整除不成立（`_pylong` 落回 Python 層被計數） | 反駁 CONFIRMED、副作用 DOWNGRADED | 成立：F1 敘述收窄＋註明方向對獵殺有利；design Context #1 同步 | R1 fix |
| 6 | R1 | trace | 矩陣 F16 spec 欄誤標 R6（應為 R7 literacy statements） | 反駁 CONFIRMED、副作用 CONFIRMED | 成立：改 R7 | R1 fix |
| 7 | R1 | trace | 矩陣 F4/F14 proposal 欄誤標 Impact（實際內容在 Non-Goals） | 反駁 CONFIRMED、副作用 CONFIRMED | 成立：F4 改 Non-Goals、F14 改 Non-Goals、Impact | R1 fix |
| 8 | R1 | contract | spec R2 Scenario「GIVEN N_min=100000 and M_max=100000」誤導讀者以為有 band 同取兩極值 | 反駁 **REFUTED**（該句是保守上界論證的標準寫法，非存在性宣稱；band3 m_max 就是 base 的 100000） | **駁回**：不改 | — |
| 9 | R1 | cliff | 568 中段「天真必過」不成立（另一精簡天真體達 6.99M） | 反駁 **REFUTED**（6.99M 仍 < 10M，「必過」成立，僅餘裕較小 1.43×） | **駁回**：不改；餘裕數字屬既有記錄範圍 | — |
| 10 | R1 | cliff | D6 漏列 568 最強繞道「單次 factorial＋chunk 乘＋逐查詢大數除法」 | 反駁 DOWNGRADED（nit：實測貼兩道門檻刀鋒，未證實能存活） | 降級 nit：不改文件（避免為未證實攻擊加保證句）；如 R2 出現實測存活證據再開項 | — |
| 11 | R1 | trace | F6「前 20 筆破限」量測基準未固定（未綁定特定隨機序列） | 反駁 DOWNGRADED（nit：外推餘裕 16.6×，序列差異不影響結論） | 降級 nit：不改 | — |
| 12 | R1 | trace | F7 142s（設計期全套）與 notes 354s（壓力角落）未 reconcile | 反駁 **REFUTED**（兩數字量的是不同情境，notes 已標明角落法） | **駁回**：不改 | — |
| 13 | R1 | trace | 10212 input_budget 手算 56 bytes 是矩陣孤兒主張 | 反駁 **REFUTED**（F9 涵蓋 input_budget 主題，56 為其派生細節） | **駁回**：不改 | — |
| 14 | R1 | trace | design Context 正解數字與 notes 實測漂移（nit） | （nit 未進驗證） | 併入 #1/#2 修正後自然消失 | R1 fix |
| 15 | R1 | statement | （零 findings——題面維度乾淨） | — | 無缺陷 | — |

**R1 小結**：must-fix 1 根（#1/#2 同根）、should-fix 成立 5（#3~#7）、駁回 4、降級 nit 2。收斂條件（無 must-fix）尚未於本輪達成，R2 覆核修正後狀態。
