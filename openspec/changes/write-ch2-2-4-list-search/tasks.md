## 1. 結構建立（Structure Setup）

- [ ] 1.1 在 `docs/tutor/py/ch2/` 建立 `2-4.md` 骨架，加入正確 frontmatter（`layout: doc`、`chapter: 2`、`section: "2-4"`、`createdTime`），確認「Section 2-4 file exists with correct frontmatter」需求
- [ ] 1.2 確認 VitePress sidebar 設定包含 2-4 章節連結，使頁面出現在導覽列


## 2. 題目設計與建立（Challenge Design and Creation）

- [ ] 2.1 設計並建立 `docs/challenge/py/26.md`：List 基礎範例題（`layout: challenge`、`id: 26`、`algorithm`、`testcase_count: 5`、`params`、`generator`、`starter_code`），確認「Six challenge files exist for section 2-4」需求
- [ ] 2.2 設計並建立 `docs/challenge/py/27.md`：List 基礎練習題 1（`id: 27`，難度適中，符合 T-1 邊界）
- [ ] 2.3 設計並建立 `docs/challenge/py/28.md`：List 基礎練習題 2（`id: 28`，難度適中，符合 T-1 邊界）
- [ ] 2.4 設計並建立 `docs/challenge/py/29.md`：線性搜尋範例題「尋找最大值與位置」（`id: 29`，為主 Judge 範例）
- [ ] 2.5 設計並建立 `docs/challenge/py/30.md`：線性搜尋練習題 1（`id: 30`，符合 T-1 邊界）
- [ ] 2.6 設計並建立 `docs/challenge/py/31.md`：線性搜尋練習題 2（`id: 31`，符合 T-1 邊界）
- [ ] 2.7 執行所有六個 generator 驗證輸出正確性，確認「Challenge generators produce correct output」需求


## 3. 知識點一：List 基礎內容撰寫

- [ ] 3.1 撰寫概念溯源段落：說明 100 個成績需要宣告 100 個變數的問題，引出 List 解決「同類別大量資料統一管理」的動機；確認「Section 2-4 covers two knowledge points」需求（List basics knowledge point is present）
- [ ] 3.2 撰寫 List 建立語法、零索引（zero-based indexing）說明與索引越界警告，確認「Section 2-4 follows error prevention rule E-1」需求（Index error pitfall is warned at introduction）
- [ ] 3.3 撰寫 `len()` 與 `append()` 操作說明，附帶 conversational lead-in，確認「Section 2-4 code blocks follow conversational lead-in rule C-1」需求
- [ ] 3.4 撰寫 `for item in list` 過渡說明：與 `for i in range()` 比較，解釋直接迭代值 vs 迭代索引的差異，確認「Section 2-4 introduces for-item-in-list as natural transition from range-based for」需求
- [ ] 3.5 加入 `for item in list` 的步驟追蹤（step-by-step trace），確認「Section 2-4 follows mental model rule M-1」需求（List iteration is traced step-by-step）
- [ ] 3.6 插入類比前的後設認知橋接句，確認「Section 2-4 follows analogy bridge rule S-1」需求
- [ ] 3.7 插入 `<ChallengeLink id="26">` 至 List 基礎範例題走讀區，確認「Section 2-4 challenges are linked with ChallengeLink components」需求（Example ChallengeLink is embedded in walkthrough）
- [ ] 3.8 插入 `<ChallengeLink id="27">` 與 `<ChallengeLink id="28">` 至練習區（附簡短提示，不提供完整解法），確認「Practice ChallengeLinks appear with hints only」需求


## 4. 知識點二：線性搜尋內容撰寫

- [ ] 4.1 撰寫線性搜尋概念導入：說明為什麼需要搜尋資料、線性搜尋是最直觀的方法，確認「Section 2-4 covers two knowledge points」需求（Linear Search knowledge point is present）
- [ ] 4.2 撰寫主範例「尋找最大值與位置」：包含完整走讀（step-by-step trace 展示 running maximum 如何更新），確認「Running-maximum update is traced」需求（Section 2-4 follows mental model rule M-1）
- [ ] 4.3 加入線性搜尋的索引 vs 值混淆警告，確認「Section 2-4 follows error prevention rule E-1」需求（Linear search pitfall is warned at introduction）
- [ ] 4.4 插入 H2 層次的段落轉換（2–4 句：總結 → 缺口 → 動機），確認「Section 2-4 follows section transition rule S-3」需求
- [ ] 4.5 插入 `<ChallengeLink id="29">` 至線性搜尋範例題走讀區
- [ ] 4.6 插入 `<ChallengeLink id="30">` 與 `<ChallengeLink id="31">` 至練習區（附簡短提示）


## 5. 圖片佔位符與附錄（Image Placeholders and Appendix）

- [ ] 5.1 在每個 H2 區塊加入至少一個圖片佔位符，使用雙行格式（`![📷 **圖 N**：...](path)` + `> 📷 **圖 N**：...`），確認「Section 2-4 includes image placeholders and Image Specification Appendix」需求（Image placeholders use dual-line format）
- [ ] 5.2 確認整節無超過五段連續純文字段落，確認視覺節奏規則（Visual rhythm rule is satisfied）
- [ ] 5.3 在檔案末尾撰寫 Image Specification Appendix，包含每張圖的完整 Nano Banana Pro prompt（美式火柴人漫畫風格、對話框為繁體中文、技術詞彙用英文），確認「Image Specification Appendix exists」需求


## 6. 編輯規則驗證（Editorial Rule Verification）

- [ ] 6.1 掃描 2-4.md 中所有 `——` 符號，依 P-1 決策清單逐一判斷並修正，確認「Section 2-4 follows punctuation style rule P-1」需求
- [ ] 6.2 確認未教術語未在教學點之前使用；檢查 `dict`、`tuple`、巢狀迴圈、bubble sort、list comprehension、二維串列皆未出現，確認「Section 2-4 respects T-1 boundary constraints」與「Section 2-4 follows terminology forward-reference rule T-1」需求
- [ ] 6.3 在幽默元素（顏文字、括弧玩笑）後加入明確的接續語，確認「Section 2-4 follows post-humor connector rule S-2」需求
- [ ] 6.4 確認所有 VitePress custom container 使用 `> [!TYPE]` 語法（帶驚嘆號），確認「Section 2-4 VitePress custom containers use correct syntax per rule V-1」需求
- [ ] 6.5 確認所有 custom container 內容非空白，確認「Section 2-4 contains no empty UI elements per rule T-3」需求
- [ ] 6.6 統計顏文字出現位置，確認每 30 行至少一個、每 10 行不超過一個、同一顏文字不重複超過兩次、涵蓋至少兩種情緒類別，確認「Section 2-4 follows emotional punctuation density rule K-1」需求
