## 1. 結構建立

- [ ] 1.1 建立 `docs/tutor/py/ch2/2-6.md`，加入正確 frontmatter（layout: doc, chapter: 2, section: "2-6", createdTime），確認「Section 2-6 file exists with correct frontmatter」規格
- [ ] 1.2 確認 `docs/tutor/py/ch2/index.md` 已包含 2-6 的連結，使 section 2-6 出現在 ch2 sidebar navigation

## 2. 挑戰題設計與建立：Dict KV 結構（ID 41–43）

- [ ] 2.1 設計 id 41「字母頻率統計」挑戰題（medium，Dict KV 結構範例）：設計 params（輸入字串）、generator（用 dict 統計各字母出現次數，忽略非字母字元，按字母排序輸出），確認「Six challenge files exist for section 2-6 (IDs 41–46)」與「Example challenges (id 41, 44) use dict-based solutions in generator」規格
- [ ] 2.2 建立 `docs/challenge/letter-frequency.md`（id: 41），包含 layout、id、title、difficulty、tags（含字典/dict）、algorithm、testcase_count（≥5）、params、generator、starter_code，確認「Challenge generators produce correct output」規格
- [ ] 2.3 設計 id 42 練習題（easy，Dict KV 查找）：例如「單字翻譯」— 給定一個小字典（幾對 key-value）和一個查詢字，回傳對應的中文意思（若無則輸出 "Not Found"），設計 params 與 generator
- [ ] 2.4 建立 `docs/challenge/<id42-name>.md`（id: 42），符合「All six challenge files exist」規格
- [ ] 2.5 設計 id 43 練習題（medium，Dict 累積/聚合）：例如「學生成績平均」— 多行輸入「名字 分數」，用 dict 累積後輸出每人平均（可能出現同名多筆），設計 params 與 generator
- [ ] 2.6 建立 `docs/challenge/<id43-name>.md`（id: 43），符合「All six challenge files exist」規格

## 3. 挑戰題設計與建立：雜湊查找 vs 線性搜尋（ID 44–46）

- [ ] 3.1 設計 id 44「落單的數字」挑戰題（medium，雜湊查找範例）：輸入一組數字（每個數字除了一個以外都出現兩次），用 dict/Counter 找出只出現一次的數字，設計 params 與 generator，確認「Example challenges (id 41, 44) use dict-based solutions in generator」規格
- [ ] 3.2 建立 `docs/challenge/single-number.md`（id: 44），包含完整 YAML frontmatter 與正確 generator，確認「Six challenge files exist for section 2-6 (IDs 41–46)」規格
- [ ] 3.3 設計 id 45 練習題（easy，成員查詢 O(1) 優勢示範）：例如「黑名單查詢」— 給定一個黑名單 set/dict 和一組查詢，判斷每個查詢是否在黑名單中（強調用 dict/set 比 list 快），設計 params 與 generator
- [ ] 3.4 建立 `docs/challenge/<id45-name>.md`（id: 45），符合「All six challenge files exist」規格
- [ ] 3.5 設計 id 46 練習題（medium，頻率計算/去重）：例如「找到出現最多次的元素」— 給定一串數字，用 dict 計算頻率後找出出現最多次的那個，設計 params 與 generator
- [ ] 3.6 建立 `docs/challenge/<id46-name>.md`（id: 46），符合「All six challenge files exist」規格

## 4. 教學內容撰寫：Dict Key-Value 結構知識點

- [ ] 4.1 撰寫 `docs/tutor/py/ch2/2-6.md` 的開頭引入段落（概念溯源）：說明當資料量達到百萬筆時，從頭找起會讓程式卡死，引出字典（Dict）的發明動機，確認「Section 2-6 follows section transition rule S-3」規格
- [ ] 4.2 撰寫 Dict KV 結構知識點的核心教學內容：建立字典（`{}`、`dict()`）、用 `d[key]` 存取值、新增與修改鍵值，確認「Section 2-6 covers Dict Key-Value structure as first knowledge point」規格
- [ ] 4.3 緊接 `d[key]` 語法後加入 `KeyError` 警告與 `.get()` 替代方案，確認「Section 2-6 follows error prevention rule E-1」規格
- [ ] 4.4 為 Dict KV 結構段落加入至少一張圖片佔位符（雙行格式：image link + caption），確認「Section 2-6 image placeholders follow dual-line format rule F-1」規格
- [ ] 4.5 加入 `<ChallengeLink>` 指向 id 41（字母頻率統計）並撰寫完整解題示範走讀（逐行解讀），確認「Dict KV structure example is present and linked」規格
- [ ] 4.6 加入 `<ChallengeLink>` 指向 id 42 與 id 43，各附簡短提示但不提供完整步驟，確認「Dict KV practice challenges are present and linked」規格

## 5. 教學內容撰寫：Tuple 旁白

- [ ] 5.1 在 Dict KV 知識點之後（或內部）加入 Tuple 旁白 callout（使用 `> [!NOTE]` 語法）：說明 Tuple 是不可變的有序序列、語法 `t = (1, 2, 3)` 與 list 的對比、可作為 dict key 使用，確認「Section 2-6 introduces Tuple as an aside (no dedicated challenges)」規格
- [ ] 5.2 確認旁白 callout 有實質內容（非空白），確認「Section 2-6 contains no empty UI elements (rule T-3)」規格，並且 VitePress 語法使用 `> [!NOTE]`（含驚嘆號），確認「Section 2-6 VitePress custom containers use correct syntax rule V-1」規格

## 6. 教學內容撰寫：雜湊查找 vs 線性搜尋知識點

- [ ] 6.1 撰寫 H2 section 之間的過渡段落（2–4 句），總結 Dict KV 知識點並帶出線性搜尋 vs 雜湊查找的速度差異主題，確認「Section 2-6 follows section transition rule S-3」規格
- [ ] 6.2 撰寫雜湊查找 vs 線性搜尋知識點的核心教學內容：明確引用 2-4 節介紹的線性搜尋為基準、說明 Hash Map 的發明動機（百萬筆資料的效能問題）、解釋 O(1) vs O(n) 的直覺差異，確認「Section 2-6 covers Hash lookup vs Linear Search as second knowledge point」與「Hash vs Linear Search references section 2-4」規格
- [ ] 6.3 加入計時對比程式碼範例（`in list` vs `in dict` 在大量資料上的速度差異），並在說明中逐步追蹤執行邏輯，確認「Section 2-6 code examples follow mental model rule M-1」與「Hash lookup O(1) is traced or demonstrated」規格
- [ ] 6.4 在每個程式碼區塊前加入對話式引言，確認「Section 2-6 code blocks follow conversational lead-in rule C-1」規格
- [ ] 6.5 為雜湊查找段落加入至少一張圖片佔位符（雙行格式），確認「Section 2-6 image placeholders follow dual-line format rule F-1」規格
- [ ] 6.6 加入 `<ChallengeLink>` 指向 id 44（落單的數字）並撰寫完整解題示範走讀，確認「Hash vs Linear Search example is present and linked」規格
- [ ] 6.7 加入 `<ChallengeLink>` 指向 id 45 與 id 46，各附簡短提示，確認「Hash vs Linear Search practice challenges are present and linked」規格

## 7. 圖片佔位符與附錄

- [ ] 7.1 在 `docs/tutor/py/ch2/2-6.md` 結尾加入 `## 圖片規格附錄`，為每個圖片佔位符提供完整 AI 生成 prompt（美式火柴人漫畫風格、對話框驅動、繁體中文對話、英文技術術語），確認「Image Specification Appendix exists」規格

## 8. 編輯規則驗證

- [ ] 8.1 全文掃描標點符號規則 P-1：確認所有 `——` 只用於戲劇性強調，非解釋性或延續性子句，確認「Section 2-6 follows punctuation style rule P-1」規格
- [ ] 8.2 全文掃描術語前向引用規則 T-1：確認所有已教過的概念（for、while、list 等）可自由使用，新術語有平語解釋，確認「Section 2-6 follows terminology forward-reference rule T-1」規格
- [ ] 8.3 全文掃描類比橋接規則 S-1：確認每個比喻前有一句說明為何要做此比喻，確認「Section 2-6 follows analogy bridge rule S-1」規格
- [ ] 8.4 全文掃描幽默後連接詞規則 S-2：確認顏文字或括弧笑話後有明確引回敘述的連接詞，確認「Section 2-6 follows post-humor connector rule S-2」規格
- [ ] 8.5 全文掃描節次過渡規則 S-3：確認每個 H2 邊界有 2–4 句包含摘要、缺口識別、引出下文的過渡段，確認「Section 2-6 follows section transition rule S-3」規格
- [ ] 8.6 全文掃描代碼前導語規則 C-1：確認所有程式碼區塊前有至少一句對話式引言，確認「Section 2-6 code blocks follow conversational lead-in rule C-1」規格
- [ ] 8.7 全文掃描即時警告規則 E-1：確認 KeyError 及 dict key 不可為 mutable 等常見錯誤已在語法介紹處就提醒，確認「Section 2-6 follows error prevention rule E-1」規格
- [ ] 8.8 全文掃描心智模型規則 M-1：確認計時對比或步驟追蹤已清楚說明 O(1) vs O(n) 差異，確認「Section 2-6 code examples follow mental model rule M-1」規格
- [ ] 8.9 全文掃描 VitePress 容器語法規則 V-1：確認所有 callout 使用 `> [!TYPE]`（含 !），確認「Section 2-6 VitePress custom containers use correct syntax rule V-1」規格
- [ ] 8.10 全文掃描空白 UI 元素規則 T-3：確認所有 callout 區塊都有實質內容，確認「Section 2-6 contains no empty UI elements (rule T-3)」規格
- [ ] 8.11 掃描 TBD 標記規則 T-2：確認全文無 `<!-- TBD -->` 或 `<!-- [START] TBD -->` 殘留，確認「Section 2-6 contains no residual TBD markers (rule T-2)」規格
- [ ] 8.12 全文掃描情感標點密度規則 K-1：確認每 30 行散文至少一個顏文字/括弧笑話，每 10 行散文不超過一個；確認顏文字不重複超過兩次，且使用至少兩種情感類別，確認「Section 2-6 follows emotional punctuation density rule K-1」規格
