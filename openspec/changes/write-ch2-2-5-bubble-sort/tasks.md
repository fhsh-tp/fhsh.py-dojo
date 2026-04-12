## 1. 結構準備（Structure Setup）

- [ ] 1.1 確認 `docs/tutor/py/ch2/` 目錄存在，必要時建立；確認 `docs/challenge/` 目錄存在
- [ ] 1.2 建立 `docs/tutor/py/ch2/2-5.md`，填入正確 frontmatter（layout: doc, chapter: 2, section: "2-5", title, description, createdTime），滿足「Section 2-5 file exists with correct frontmatter」規格

## 2. 題目設計與建立（Challenge Design and Creation，IDs 32–40）

- [ ] 2.1 建立 `docs/challenge/variable-swap.md`（id: 32，difficulty: easy）——變數交換例題，generator 使用 `a, b = b, a`，testcase_count ≥ 5；滿足「Nine challenge files exist with correct structure (IDs 32–40)」與「Variable swap knowledge point has one example and two practice challenges」
- [ ] 2.2 建立 `docs/challenge/swap-practice-1.md`（id: 33，difficulty: easy）——變數交換練習一，params/generator/starter_code 完整；滿足「Nine challenge files exist with correct structure (IDs 32–40)」與「Variable swap knowledge point has one example and two practice challenges」
- [ ] 2.3 建立 `docs/challenge/swap-practice-2.md`（id: 34，difficulty: easy）——變數交換練習二，params/generator/starter_code 完整；滿足「Nine challenge files exist with correct structure (IDs 32–40)」與「Variable swap knowledge point has one example and two practice challenges」
- [ ] 2.4 建立 `docs/challenge/nested-loop-example.md`（id: 35，difficulty: easy）——雙重迴圈例題，generator 展示巢狀 for 迴圈，顯示迭代次數或矩陣輸出；滿足「Nine challenge files exist with correct structure (IDs 32–40)」與「Nested loop knowledge point has one example and two practice challenges」
- [ ] 2.5 建立 `docs/challenge/nested-loop-practice-1.md`（id: 36，difficulty: easy）——雙重迴圈練習一；滿足「Nine challenge files exist with correct structure (IDs 32–40)」與「Nested loop knowledge point has one example and two practice challenges」
- [ ] 2.6 建立 `docs/challenge/nested-loop-practice-2.md`（id: 37，difficulty: medium）——雙重迴圈練習二；滿足「Nine challenge files exist with correct structure (IDs 32–40)」與「Nested loop knowledge point has one example and two practice challenges」
- [ ] 2.7 建立 `docs/challenge/award-ceremony.md`（id: 38，difficulty: medium）——頒獎典禮，降序氣泡排序，params 含 n（min: 3, max: 8）和多個 scores（0–100），generator 使用 explicit bubble sort 邏輯（禁用 .sort()/sorted()），題目描述含「嚴禁使用內建 .sort()」；滿足「Nine challenge files exist with correct structure (IDs 32–40)」、「Bubble sort knowledge point has one example and two practice challenges」及「頒獎典禮 challenge (id: 38) uses descending bubble sort with list input」
- [ ] 2.8 建立 `docs/challenge/bubble-sort-practice-1.md`（id: 39，difficulty: medium）——氣泡排序練習一（升序或統計類）；滿足「Nine challenge files exist with correct structure (IDs 32–40)」與「Bubble sort knowledge point has one example and two practice challenges」
- [ ] 2.9 建立 `docs/challenge/bubble-sort-practice-2.md`（id: 40，difficulty: medium）——氣泡排序練習二（進階排序應用）；滿足「Nine challenge files exist with correct structure (IDs 32–40)」與「Bubble sort knowledge point has one example and two practice challenges」
- [ ] 2.10 驗證全部 9 道題目的 generator 輸出正確（手動或腳本執行確認）；滿足「Challenge generators produce correct output」
- [ ] 2.11 確認所有題目 frontmatter 欄位完整（layout, id, title, difficulty, tags, algorithm, testcase_count, params, generator, starter_code）；滿足「Challenge files have required frontmatter fields」

## 3. 內容撰寫：變數交換（Content Writing for Variable Swap）

- [ ] 3.1 撰寫 2-5.md「概念溯源」引言：說明為何需要學排序（亂序資料沒有價值），建立學習動機；引言需符合 S-1 類比橋規則（每個類比前先說明為何比喻）
- [ ] 3.2 撰寫變數交換（`a, b = b, a`）知識點：說明三步驟暫存法 vs. Pythonic 寫法，在語法首次介紹處立即警示常見錯誤（如順序寫反）；滿足「Section 2-5 follows error prevention rule E-1」與「Section 2-5 respects T-1 terminology boundary constraints」
- [ ] 3.3 在變數交換段落新增逐步推導 trace（例：`a=3, b=7` → 執行 `a, b = b, a` → 結果），符合 M-1 步驟追蹤規則；滿足「Section 2-5 follows mental model trace rule M-1」
- [ ] 3.4 插入變數交換圖片佔位符（雙行格式：image link + caption），符合 F-1 規則；滿足「Section 2-5 contains image placeholders with dual-line format (F-1)」
- [ ] 3.5 插入 `<ChallengeLink>` 連結（id: 32 例題，id: 33、34 練習），滿足「Variable swap knowledge point has one example and two practice challenges」
- [ ] 3.6 確認變數交換段落中未出現「氣泡排序」術語，符合術語邊界規則；滿足「Variable swap subsection does not mention bubble sort by name」（T-1 forward reference）

## 4. 內容撰寫：雙重迴圈（Content Writing for Nested Loops）

- [ ] 4.1 撰寫雙重迴圈（nested loops）知識點：從單層 for 延伸，展示外層 × 內層迭代次數計算，提示 range() off-by-one 常見錯誤；滿足「Section 2-5 follows error prevention rule E-1」
- [ ] 4.2 確保雙重迴圈段落符合 C-1 規則：每個 code block 前至少有一句口語鋪墊；滿足「Section 2-5 code blocks follow conversational lead-in rule C-1」
- [ ] 4.3 插入雙重迴圈圖片佔位符（雙行格式），符合 F-1 與視覺節奏規則；滿足「Section 2-5 has visual rhythm」與「Section 2-5 contains image placeholders with dual-line format (F-1)」
- [ ] 4.4 插入 `<ChallengeLink>` 連結（id: 35 例題，id: 36、37 練習），滿足「Nested loop knowledge point has one example and two practice challenges」
- [ ] 4.5 在雙重迴圈段落結尾撰寫過渡語（2–4 句）：總結已學、點出單層迴圈的限制、引入氣泡排序；滿足「Section 2-5 follows section transition rule S-3」

## 5. 內容撰寫：氣泡排序（Content Writing for Bubble Sort）

- [ ] 5.1 撰寫氣泡排序（bubble sort）知識點引言：先設定情境（頒獎典禮需要排名），再引入演算法概念，所有類比需有 S-1 橋接句
- [ ] 5.2 撰寫完整氣泡排序逐步 trace（pass-by-pass），至少 2 輪完整追蹤，每步驟標明「第幾輪、比較哪兩個值、是否交換、陣列現況」；滿足「Bubble sort section contains step-by-step swap trace (M-1)」與「Section 2-5 follows mental model trace rule M-1」
- [ ] 5.3 Trace 中明確回呼「a, b = b, a」交換語法，建立前後知識點的連結；滿足「Trace uses the same swap idiom taught earlier」
- [ ] 5.4 在氣泡排序程式碼範例介紹處立即警示 inner loop 縮小範圍優化（減少不必要的比較），符合 E-1；滿足「Section 2-5 follows error prevention rule E-1」
- [ ] 5.5 確認氣泡排序內容完全不使用 `.sort()`、`sorted()`、`dict`、`tuple`、list comprehension；滿足「Section 2-5 respects T-1 terminology boundary constraints」
- [ ] 5.6 確保每個 code block 前有口語鋪墊（C-1），VitePress 自訂容器使用 `> [!TYPE]` 格式（V-1）；滿足「Section 2-5 code blocks follow conversational lead-in rule C-1」與「Section 2-5 follows VitePress custom container syntax rule V-1」
- [ ] 5.7 插入氣泡排序圖片佔位符（雙行格式，至少一張說明排序過程），符合 F-1 與視覺節奏規則；滿足「Section 2-5 has visual rhythm」
- [ ] 5.8 插入 `<ChallengeLink>` 連結（id: 38 例題，id: 39、40 練習），滿足「Bubble sort knowledge point has one example and two practice challenges」
- [ ] 5.9 確認氣泡排序段落的幽默元素後有 S-2 回呼連接詞；滿足「Section 2-5 follows post-humor connector rule S-2」

## 6. 圖片佔位符與附錄（Image Placeholders and Appendix）

- [ ] 6.1 檢查全文：確保每個 H2 段落至少有一個圖片佔位符，且連續純文字段落不超過 5 段；滿足「Section 2-5 has visual rhythm — at least one visual per H2 section (visual rhythm rule)」
- [ ] 6.2 在 2-5.md 末尾新增「圖片規格附錄 (Image Specification Appendix)」，列出每張圖片的完整 Nano Banana Pro 提示詞（美式火柴人漫畫風格，對話框用繁體中文台灣，技術術語用英文）；滿足「Section 2-5 ends with Image Specification Appendix」

## 7. 編輯規則驗證（Editorial Rule Verification）

- [ ] 7.1 全文逐句審查 P-1 標點規則：確認「——」只用於戲劇性強調，改正所有說明性、原因性破折號為「：」或「，」；滿足「Section 2-5 follows punctuation style rule P-1」
- [ ] 7.2 全文審查 S-1（類比橋接）：確認每個類比或比喻前都有一句「為什麼要這樣比喻」的導引句；滿足「Section 2-5 follows analogy bridge rule S-1」
- [ ] 7.3 全文審查 S-2（幽默後回呼）：確認每個 kaomoji 或括號笑點後的下一句有明確的「回到主題」連接語；滿足「Section 2-5 follows post-humor connector rule S-2」
- [ ] 7.4 全文審查 S-3（段落過渡）：確認三個知識點之間的 H2 級過渡含 2–4 句（總結、缺口、引導）；滿足「Section 2-5 follows section transition rule S-3」
- [ ] 7.5 全文審查 K-1（情緒標點密度）：確認每 30 行純文字至少有 1 個情緒元素、每 10 行不超過 1 個；確認同一 kaomoji 在單一文件中不超過 2 次；確認使用至少 2 種情緒分類的 kaomoji；滿足「Section 2-5 follows emotional punctuation density rule K-1」
- [ ] 7.6 掃描全文確認無 `<!-- TBD -->` 或 `<!-- [START] TBD -->` 殘留；滿足「Section 2-5 contains no residual TBD markers (T-2)」
- [ ] 7.7 掃描全文確認無空的 VitePress 自訂容器（T-3）；滿足「Section 2-5 contains no empty UI elements (T-3)」
- [ ] 7.8 確認圖片佔位符全部使用雙行格式（image link + caption），無遺漏；滿足「Section 2-5 contains image placeholders with dual-line format (F-1)」
- [ ] 7.9 最終確認三個知識點的教學順序為：「變數交換 → 雙重迴圈 → 氣泡排序」，符合先備知識依序；滿足「Section 2-5 teaches three knowledge points in prerequisite order」
- [ ] 7.10 全文通讀確認無術語前向引用問題：變數交換段不提「氣泡排序」，雙重迴圈段不預設讀者已懂排序；滿足「Section 2-5 follows terminology boundary rule T-1 (no forward references)」
