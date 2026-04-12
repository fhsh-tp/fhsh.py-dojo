## 1. 結構建立

- [ ] 1.1 建立 `docs/tutor/py/ch2/2-7.md` 骨架，填入符合「Section 2-7 file exists with correct frontmatter」要求的 frontmatter（layout: doc、chapter: 2、section: "2-7"、createdTime、title、description；不含 challenge 欄位）
- [ ] 1.2 確認 Chapter 2 側邊欄導航中已包含 2-7 連結（驗證「Section 2-7 file exists with correct frontmatter」的導航情境）

## 2. 知識地圖

- [ ] 2.1 撰寫「模組二知識地圖」區塊：建立文字樹狀圖（fenced plain-text code block），涵蓋 2-1（for/range）、2-2（while）、2-3（break/continue）、2-4（List + 線性搜尋）、2-5（進階 List + 泡沫排序）、2-6（Dictionary + hash table）所有分支與葉節點，滿足「Section 2-7 contains a Module 2 knowledge map」要求
- [ ] 2.2 在文字樹狀圖之前插入圖片佔位符（dual-line 格式），符合「Section 2-7 contains a Module 2 knowledge map」的圖片佔位符情境，並依 F-1 規則（image placeholder dual-line format）使用 `![📷 **圖 N**...](path)` + `> 📷 **圖 N**...` 雙行格式

## 3. 自我檢查表

- [ ] 3.1 撰寫「自我檢查表」區塊：建立 Markdown 表格，包含表頭 `| # | 能力 | 你會了嗎？ |` 及至少 15 行技能條目（含 2-1 至 2-6 各節至少一條）、每行第三欄填入 `☐`，滿足「Section 2-7 contains a self-check table」要求
- [ ] 3.2 確認表格技能條目涵蓋以下核心技能：for+range、while 終止條件、break 早退、continue 跳過、list 建立與索引、append 與 len、線性搜尋、泡沫排序邏輯、dict 建立與查找、hash table 概念說明（依「Section 2-7 contains a self-check table」的覆蓋情境）

## 4. 模組三預告

- [ ] 4.1 撰寫「模組三預告」區塊，介紹函式（函式）、二元搜尋（binary search）、遞迴（recursion）三個主題，並說明與模組二技能的連結，滿足「Section 2-7 contains a Module 3 preview」要求
- [ ] 4.2 在模組三預告區塊結尾插入圖片佔位符（dual-line 格式），符合「Section 2-7 contains a Module 3 preview」的圖片佔位符情境，並依 F-1 規則使用雙行格式

## 5. Image Specification Appendix

- [ ] 5.1 在 `2-7.md` 結尾新增 `## Image Specification Appendix`，為每張圖片佔位符建立對應的 `### 圖 N` 條目（含 類型、意圖、完整 Prompt、備註），滿足「Section 2-7 contains an Image Specification Appendix」要求
- [ ] 5.2 確認所有圖片 Prompt 以 American stick figure comic strip 視覺風格前綴開頭（與 Ch1/Ch2 其他章節一致），滿足「Section 2-7 contains an Image Specification Appendix」的 Prompt 風格情境

## 6. 編輯規則驗證

- [ ] 6.1 執行 P-1 規則（punctuation）檢查：掃描 `2-7.md` 中所有 `——` 用法，確認僅用於戲劇性強調；說明性子句改用冒號或逗號，符合「Section 2-7 follows all Ch1 editorial rules (P-1 through K-1)」的 P-1 情境
- [ ] 6.2 執行 F-1 規則（image placeholder dual-line format）驗證：確認每個 `> 📷 **圖 N**` 說明行前均有對應的 `![📷 **圖 N**...](path)` 圖片連結行，符合「Section 2-7 follows all Ch1 editorial rules (P-1 through K-1)」的 F-1 情境
- [ ] 6.3 執行 V-1 規則（VitePress container syntax）驗證：確認所有自訂容器開頭使用 `> [!TYPE]`（含驚嘆號），符合「Section 2-7 follows all Ch1 editorial rules (P-1 through K-1)」的 V-1 情境
- [ ] 6.4 執行 K-1 規則（emotional punctuation density）驗證：確認每 30 行連續散文中至少有一個情感標點元素（顏文字 / 括號笑話 / 學生對話插入語），且每 10 行不超過一個；顏文字不重複超過兩次且涵蓋至少兩種情感類別，符合「Section 2-7 follows all Ch1 editorial rules (P-1 through K-1)」的 K-1 情境
- [ ] 6.5 執行 S-3 規則（section transition）驗證：確認各 H2 邊界的過渡段落包含 2–4 句（總結 + 缺口 + 動機），符合「Section 2-7 follows all Ch1 editorial rules (P-1 through K-1)」的 S-3 要求
- [ ] 6.6 執行 C-1 規則（code block lead-in）驗證：確認每個 fenced code block 前有至少一句對話式說明，符合「Section 2-7 follows all Ch1 editorial rules (P-1 through K-1)」的 C-1 要求
