# Audit 裁決帳本（add-rank-code-challenge-duo）

> 目的：每一條 audit finding 的**終局裁決**記錄。後續輪次的 finder 與統整者必須先對照本表 reconcile——已裁決項目（含「接受殘餘」）不得以相同理由復活；要推翻既有裁決必須引用新 evidence。
> 標尺（凍結）：must-fix＝會改變判題 verdict／建置測試失敗／違反 spec SHALL／誤導學生；should-fix＝文件不一致不影響上線行為；nit＝風格。收斂條件＝該輪無 must-fix。
> 合法終局裁決類別（RCA 補充）：成立→修正／駁回／降級 nit／**聰明解（accepted alternative）**——實測存活且經裁決收編的繞道，不構成缺陷，記錄於 design D6.b 與 notes 5.2b。

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

| # | Round | 維度 | Finding 摘要 | 對抗驗證 | 終局裁決 | 處置（commit） |
|---|-------|------|--------------|----------|----------|----------------|
| 16 | R2 | fixverify＋sidefx＋freshcliff（三 finder 同報） | proposal.md What Changes 殘留作廢舊數字（1.31M/7.6×、1.67M/6.0×）——#1/#2 修正漏改矩陣 F5/F10 指名的同步位置 | 反駁 CONFIRMED×3、副作用 CONFIRMED×3 | 成立：改為出貨實測 1.56M/6.4×、2.33M/4.3× | R2 fix |
| 17 | R2 | fixverify＋sidefx | tasks.md 5.1 驗收條件殘留「≤2M」舊門檻，與已勾選 [x]＋notes 實測 2.33M 自相矛盾 | 反駁 CONFIRMED×2、副作用 CONFIRMED×2 | 成立：改「≤2.5M（上限/4）」 | R2 fix |
| 18 | R2 | fixverify＋sidefx | spec R3 末句「the table SHALL be built incrementally」與瘦身後 568 reference（排序單趟掃描、無具體表）主詞不相容 | 反駁 DOWNGRADED（nit）×2、副作用 DOWNGRADED | 成立（採副作用鏡頭建議）：改為「incrementally in a single ascending pass (whether or not an explicit table is materialized)」——弱化過度指定 | R2 fix |
| 19 | R2 | fixverify | spec R4 Scenario 的「the intended solution」缺「出貨 reference 逐字」限定，與 requirement 散文不對齊 | 反駁 DOWNGRADED（nit） | 成立（低成本對齊）：Scenario 改「the shipped reference_solution (the measured intended-solution proxy)」 | R2 fix |
| 20 | R2 | fixverify | 矩陣 F9 proposal 欄誤標 Impact（應 What Changes）；F14 修一半仍留錯誤 Impact 指向 | 反駁 CONFIRMED、副作用 CONFIRMED | 成立：F9→What Changes、F14→Non-Goals | R2 fix |
| 21 | R2 | sidefx | 568 reference 瘦身後與 generator 同用淨差簿記，spec R6「different bookkeeping style」宣稱弱化 | 反駁 DOWNGRADED（nit）、副作用 DOWNGRADED | 成立（弱化宣告）：R6 改「a materially different implementation strategy」（table+pow vs 排序掃描+cycle 表、input() vs stdin.read 仍實質不同） | R2 fix |
| 22 | R2 | sidefx | 矩陣 F8/F13/F15 spec 欄誤指「R3 example」（R3 無 Example 區塊；錨點實在 R1/R2 的 Example 表） | 反駁 DOWNGRADED（nit）、副作用 DOWNGRADED | 成立：F8→R1 example、F13→R3 scenario＋R2 example、F15→R2 example | R2 fix |
| 23 | R2 | freshcliff | design D4 把 P(25,1)=5 歸入 10212 邊界 literal 組，實際它在第 1 筆範例 literal；邊界組清單不完整（R2-SE-6 nit 同題） | 反駁 CONFIRMED、副作用 DOWNGRADED | 成立：D4 邊界 literal 逐筆列舉並註明 P(25,1) 歸屬範例 literal | R2 fix |
| 24 | R2 | fixverify | （nit）568 異值角落 1,555,807 不可重現且方向記反（異值最壞應比同值貴 +499） | nit 未進驗證、但採納 | 併修：F5／design／notes 改「同值最貴 1,555,994；異值最壞加成 +499 → ≤1,556,493」 | R2 fix |
| 25 | R2 | freshcontract | （clean）引擎契約＋題面維度全查零 findings；#8 以新驗證複核後維持駁回不變 | — | 無缺陷 | — |

**R2 小結**：**零 must-fix**（收斂條件本輪達成）；should-fix 成立 8（#16~#23，全屬 R1 修正的同步殘留與措辭對齊）、nit 併修 1（#24）。R3 為終局確認輪：驗證 R2 修正落地＋無新 must-fix 即 CLEAN。

| # | Round | 維度 | Finding 摘要 | 對抗驗證 | 終局裁決 | 處置（commit） |
|---|-------|------|--------------|----------|----------|----------------|
| 26 | R3 | mustfixhunt | R3-MF-1：apcs008 存在存活繞道 math.perm＋Legendre 尾零計數（正式池 20/20 AC、池最貴 ~108k ops、全套 8.8s native）——D6 清單漏列的 C 內建 API 路線 | 主控親手復刻 CONFIRMED（114,386 ops／1.93s）；RCA 三位 opus 分析官獨立覆核一致 | **成立（must-fix）→ 處置 A：收編為聰明解（accepted alternative）**：矩陣 F19/F20 先行、D6 分流 a 必死/b 接受殘餘、spec R5 存活例外句、notes 5.2b、題面提示句改為經實測為真的成本警語（去除不可能性承諾）；帳本 #10 的降級規則（未證實存活→nit）經 RCA 認定為本缺陷遲到的直接誘因，廢止 | R4 fix |
| 27 | R3/RCA | — | 「調測資獵殺 math.perm」已量化評估並駁回：reference 7.75 ops/元素、門檻 2.5M ⇒ 元素上限 ~322k；math.perm(10⁹,322k)≈3.2s×20 筆×2＝128s 對 120s 僅 6% 餘裕且正解零餘裕 ⇒ 加壓先死正解（F20） | RCA 裁決輪量測 | **駁回獵殺路線**：不得以相同理由復活；推翻須提出新量測 evidence | — |
| 28 | R3/RCA | — | 「改問末兩位殺繞道」變體無效：繞道持有精確整數，(p//10**k)%100 同樣一步可得；只有非連續／跳項結構才殺得掉，但毀掉素養敘事，屬另開 change 的題型重設計 | RCA 結構論證 | **駁回變體**：本 change 不採 | — |
| 29 | R3 | r2landed＋xdoc | 四條 should-fix 同步殘留：tasks 2.2/design D5「不同簿記」舊敘述（#21 漏同步）；spec R4 散文 corner 數字未上界化；矩陣 F12 Evidence 欄 5.5 舊值；tasks 2.2/3.2「spec R3 範例」誤引（應 R1/R2 Example） | 反駁 CONFIRMED×2、DOWNGRADED×2（均採副作用鏡頭修法） | 成立：R4 一併修正（含 F10 +63 上界，兩次獨立重測吻合） | R4 fix |

**R3／RCA 小結**：R3 出現 1 條 must-fix（#26）→ 依協定觸發 multi-opus 乾淨上下文 RCA。裁決＝收編（教學價值：寫得出此解需 Legendre＋min(v₂,v₅) 數論理解，嚴格高於正解；且同款路線在 007 必死，雙題並置本身在教「C 內建不是萬靈丹」）。R4 為 doc-diff 落地輪：F19/F20 → 四份文件＋題面＋BACKLOG §2.8 案例回寫，機械驗證（grep＋validate＋測試）後 CLEAN 收案。root causes 與流程建議全文見 session RCA 報告（wuohycagh）。
