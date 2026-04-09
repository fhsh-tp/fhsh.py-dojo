## 1. 結構建立（Structure Setup）

- [x] 1.1 建立 `docs/tutor/py/ch2/` 目錄（若不存在），並新增 `docs/tutor/py/ch2/2-2.md` 骨架檔案，確認 Section 2-2 file exists with correct frontmatter — `layout: doc`、`chapter: 2`、`section: "2-2"`、`createdTime` ISO 8601 +08:00
- [x] 1.2 建立 `challenges/017/`、`challenges/018/`、`challenges/019/` 目錄骨架，各放置空白 `challenge.yaml`，為後續關卡設計做準備

## 2. 關卡設計與建立（Challenge Design and Creation）

- [x] 2.1 設計並建立 Challenge ID 17 (Collatz 3N+1) exists with valid challenge.yaml：`layout: challenge`、`id: 17`、`difficulty: medium`、params（N: int, min 2, max 10000）、generator 計算 Collatz 步數、`starter_code` 提示 while 迴圈架構；以 N=6 驗證輸出 `8`，以 N=27 驗證輸出 `111`
- [x] 2.2 設計並建立 Challenge ID 18 (practice 1) exists with valid challenge.yaml：`layout: challenge`、`id: 18`、`difficulty: easy`、以 while 迴圈為核心、僅使用已教語法（while / if-else / 算術 / input / print），確認 generator 輸出正確
- [x] 2.3 設計並建立 Challenge ID 19 (practice 2) exists with valid challenge.yaml：`layout: challenge`、`id: 19`、`difficulty: easy`、以 while 迴圈為核心、僅使用已教語法，確認 generator 輸出正確

## 3. 教學內容撰寫（Content Writing）

- [x] 3.1 撰寫開場，確認 Section 2-2 opening connects from 2-1 with a clear motivation bridge：概念溯源段落說明人類討厭重複勞動、以 for+range 已知次數對比 while 未知次數，建立自 2-1 的銜接橋
- [x] 3.2 撰寫 while 迴圈語法教學，確認 Section 2-2 content covers while loops only within T-1 boundaries：含語法標注、條件判斷時機說明、最小可運作範例，並加入概念溯源段落
- [x] 3.3 建立基礎 while 迴圈追蹤表，確認 Section 2-2 while loop teaching includes syntax, semantics, and trace table：欄位含迭代次數、條件值（True/False）、關鍵變數數值；達成 M-1 逐步追蹤規則
- [x] 3.4 撰寫無窮迴圈防範段落，確認 Section 2-2 includes error prevention for infinite loops (E-1 compliance)：WARNING 容器緊接語法介紹後、含錯誤範例（缺少更新步驟）與修正版對比
- [x] 3.5 撰寫 Collatz Judge 解題實戰，確認 Section 2-2 Judge walkthrough uses Collatz Conjecture (3N+1) as example challenge (ID 17)：含題目說明、演算法邏輯先於程式碼、N=6 追蹤表（6→3→10→5→16→8→4→2→1，8 步）、完整 Python 解答、逐行解讀（W-1）
- [x] 3.6 加入 ChallengeLink 元件，確認 Section 2-2 includes challenge ID 17 (Collatz 3N+1) as example and IDs 18–19 as practice challenges：`<ChallengeLink id="17" />`、`<ChallengeLink id="18" />`、`<ChallengeLink id="19" />` 各附簡短提示
- [x] 3.7 撰寫章節收尾摘要段落，確認 H2 級別轉場符合 S-3 規則（2–4 句：回顧所學 + 指出缺口 + 引出下節 2-3）

## 4. 圖片佔位與附錄（Image Placeholders and Appendix）

- [x] 4.1 依 F-1 雙行格式在各 H2 段落加入圖片佔位：`![📷 **圖N**：description（AI 製圖）](/assets/tutor/py/ch2/2-2/figNN.png)` + `> 📷 **圖N**：...`，確認每個 H2 至少含一個視覺元素
- [x] 4.2 在檔案末尾建立 Section 2-2 includes Image Specification Appendix：含每張圖的完整 Nano Banana Pro 風格 prompt（美式火柴人漫畫、對話框、繁體中文對白、英文技術詞）

## 5. 體裁規則驗證（Editorial Rule Verification）

- [x] 5.1 完整審查 Section 2-2 follows all Ch1 editorial rules (P-1 through K-1)：依序逐條核查 P-1 至 K-1，記錄每條規則是否達成
- [x] 5.2 審查 P-1 punctuation style：掃描全文 `——` 用法，確認僅用於戲劇強調，一般子句改用 `，` 或 `：`
- [x] 5.3 審查 T-1 boundary，確認 Section 2-2 content covers while loops only within T-1 boundaries：`break`、`continue`、`list`、`dict`、`tuple` 未作為教學目標出現
- [x] 5.4 審查 S-1 analogy bridge、S-2 post-humor connector、S-3 section transition、C-1 conversational lead-in：每個類比前有元認知橋、笑點後有回扣句、H2 轉場 2–4 句、程式碼塊前有引導句
- [x] 5.5 審查 W-1 code-walkthrough correspondence：Collatz 逐行解讀與上方程式碼逐字對應
- [x] 5.6 審查 T-2 no residual TBD markers：確認無任何 `<!-- TBD ... -->` 或 `<!-- [START] TBD ... -->` 殘留
- [x] 5.7 審查 V-1 VitePress container syntax 與 T-3 no empty UI elements：所有容器使用 `> [!TYPE]` 格式，無空白 body 容器
- [x] 5.8 審查 K-1 emotional punctuation density：每 30 行散文至少一個顏文字/笑點，每 10 行不超過一個；確認至少兩種情感分類的顏文字出現於 2-2.md
- [x] 5.9 審查 M-1 mental model trace：確認 while 迴圈與 Collatz 各有獨立追蹤表（共至少 2 張）
