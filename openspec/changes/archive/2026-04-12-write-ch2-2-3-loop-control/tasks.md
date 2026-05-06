## 1. 結構建置（Section 2-3 file exists with correct frontmatter）

- [x] 1.1 確認 `docs/tutor/py/ch2/` 目錄存在，必要時建立
- [x] 1.2 建立 `docs/tutor/py/ch2/2-3.md` 骨架檔案，填入正確 frontmatter（`layout: doc`、`chapter: 2`、`section: "2-3"`、`createdTime` 含 `+08:00`）——滿足「Section 2-3 file exists with correct frontmatter」規格需求
- [x] 1.3 確認 VitePress 側邊欄設定中 2-3 出現於正確順序（section 2-3 file appears in sidebar navigation）

## 2. 挑戰題設計與建立（six challenge files exist for section 2-3 (IDs 20–25)）

- [x] 2.1 設計 ID 20 `break-example`（難度 easy），確認 generator 使用 `break` 在 `for`/`while` 迴圈，符合 T-1（challenge generators use only taught constructs）
- [x] 2.2 建立 `docs/challenge/20-break-example.md`，含完整 frontmatter、正確 generator、starter_code；驗證 generator 輸出正確（challenge generators produce correct output）
- [x] 2.3 設計 ID 21 `break-practice-1`（難度 easy），確認符合 T-1 規則
- [x] 2.4 建立 `docs/challenge/21-break-practice-1.md`，含完整 frontmatter、正確 generator、starter_code；驗證 generator 輸出
- [x] 2.5 設計 ID 22 `break-practice-2`（難度 medium），確認符合 T-1 規則
- [x] 2.6 建立 `docs/challenge/22-break-practice-2.md`，含完整 frontmatter、正確 generator、starter_code；驗證 generator 輸出
- [x] 2.7 設計 ID 23 `continue-example`（難度 easy），確認 generator 使用 `continue` 在 `for`/`while` 迴圈，符合 T-1
- [x] 2.8 建立 `docs/challenge/23-continue-example.md`，含完整 frontmatter、正確 generator、starter_code；驗證 generator 輸出
- [x] 2.9 設計 ID 24 `continue-practice-1`（難度 easy），確認符合 T-1 規則
- [x] 2.10 建立 `docs/challenge/24-continue-practice-1.md`，含完整 frontmatter、正確 generator、starter_code；驗證 generator 輸出
- [x] 2.11 設計 ID 25 `continue-practice-2`（難度 medium），確認符合 T-1 規則
- [x] 2.12 建立 `docs/challenge/25-continue-practice-2.md`，含完整 frontmatter、正確 generator、starter_code；驗證 generator 輸出
- [x] 2.13 確認所有六道挑戰題 ID 20–25 皆存在且有效（all six challenge files exist and are valid）；完成「Six challenge files exist for section 2-3 (IDs 20–25)」規格需求

## 3. Break 知識點內容撰寫

- [x] 3.1 撰寫開頭過渡段落，明確銜接 2-2（while loops），說明「在迴圈執行中途改變流程」的新需求（section 2-3 covers break and continue as two knowledge points）
- [x] 3.2 撰寫 break H2 小節標題與知識點說明，符合 C-1（code blocks follow conversational lead-in rule C-1）
- [x] 3.3 撰寫 break 範例程式碼，同時展示 `for` 迴圈用法（break knowledge point includes example and trace table；break example demonstrates for loop usage）
- [x] 3.4 撰寫 break 範例程式碼，展示 `while` 迴圈用法（break example demonstrates while loop usage）
- [x] 3.5 建立 break 執行追蹤表（trace table），含欄位：迴圈次數／條件狀態／動作（繼續/break）／輸出，清楚標示觸發 break 的那一列——滿足「Section 2-3 trace tables follow mental model rule M-1」（break trace table shows break execution；break trace table is complete）
- [x] 3.6 立即說明 break 的常見錯誤（E-1）：誤用 break 當 continue、break 只跳出最內層迴圈（break pitfall warned at point of introduction；section 2-3 follows error prevention rule E-1）
- [x] 3.7 插入 `<ChallengeLink id="20" />` 於 break 範例小節，附簡短解題情境說明（example challenges linked with walkthrough context；section 2-3 challenges are linked from the tutorial section）
- [x] 3.8 撰寫 break 練習小節，插入 `<ChallengeLink id="21" />` 與 `<ChallengeLink id="22" />`，各附 1–2 句提示，不提供詳細解法（practice challenges linked with hints only）

## 4. Continue 知識點內容撰寫

- [x] 4.1 撰寫 break → continue 的 H2 過渡段落（2–4 句：總結 break、點出限制、引入 continue）（section 2-3 follows section transition rule S-3；major section transition between break and continue）
- [x] 4.2 撰寫 continue H2 小節標題與知識點說明，符合 C-1
- [x] 4.3 撰寫 continue 範例程式碼，展示 `for` 迴圈用法（continue knowledge point includes example and trace table；continue example demonstrates for loop usage）
- [x] 4.4 撰寫 continue 範例程式碼，展示 `while` 迴圈用法（continue example demonstrates while loop usage）
- [x] 4.5 建立 continue 執行追蹤表（trace table），含欄位：迴圈次數／條件結果／動作（跳過/執行）／輸出，標示所有被跳過的迭代（continue trace table shows continue skipping；continue trace table is complete）
- [x] 4.6 立即說明 continue 的常見錯誤（E-1）：while 迴圈中 continue 可能導致無限迴圈（若迴圈變數更新置於 continue 之後）（continue pitfall warned at point of introduction）
- [x] 4.7 插入 `<ChallengeLink id="23" />` 於 continue 範例小節，附簡短解題情境說明（continue example challenge linked）
- [x] 4.8 撰寫 continue 練習小節，插入 `<ChallengeLink id="24" />` 與 `<ChallengeLink id="25" />`，各附 1–2 句提示

## 5. 圖片佔位符與圖片規格附錄

- [x] 5.1 在每個 H2 小節（至少 break 與 continue 各一）插入符合 F-1 雙行格式的圖片佔位符（section 2-3 image placeholders follow dual-line format rule F-1；image placeholder has both link and caption）
- [x] 5.2 確認圖片路徑使用 `/assets/tutor/py/ch2/` 前綴，編號格式 `圖N`（ungenerated image still has link placeholder）
- [x] 5.3 在文件末尾建立「圖片規格附錄」（Image Specification Appendix），列出每張圖的完整 AI 生圖 prompt（section 2-3 ends with an Image Specification Appendix；appendix lists all image prompts）
- [x] 5.4 確認所有 prompt 使用美式火柴人漫畫風格、對話驅動分格（無旁白框）、繁體中文對話框、英文技術詞（image prompts use correct visual style）

## 6. 編輯規則驗查

- [x] 6.1 逐一審查所有 em-dash 用法，套用 P-1 決策清單（section 2-3 follows punctuation style rule P-1；explanatory em-dash replaced with colon；dramatic em-dash preserved）
- [x] 6.2 確認所有比喻／類比前有一句「meta-cognitive bridge」說明目的（section 2-3 follows analogy bridge rule S-1；analogy has meta-cognitive setup）
- [x] 6.3 確認所有笑點／顏文字後有明確「回到主題」銜接語，或屬 H3 邊界例外（section 2-3 follows post-humor connector rule S-2；joke followed by connector）
- [x] 6.4 確認 VitePress 自訂容器語法均使用 `> [!TYPE]` 格式（section 2-3 uses correct VitePress custom container syntax rule V-1；custom container syntax is correct）
- [x] 6.5 確認無空白自訂容器，未完成者包入 HTML 注解（section 2-3 has no empty UI elements rule T-3；no empty containers in 2-3）
- [x] 6.6 確認無任何 TBD 佔位符殘留（section 2-3 has no residual TBD markers rule T-2；no TBD markers in 2-3.md）
- [x] 6.7 確認所有 code block 前有至少一句引言散文，無標題直連 code block 的情況——滿足「Section 2-3 code blocks follow conversational lead-in rule C-1」（code block has lead-in text）
- [x] 6.8 確認無提前使用 `list`、`dict`、`tuple` 等未教詞彙（section 2-3 follows T-1 terminology forward-reference rule；no premature use of list, dict, or tuple）
- [x] 6.9 審查顏文字密度：每 30 行散文至少 1 個、每 10 行至多 1 個；同一顏文字在本節不超過 2 次；至少涵蓋 2 種情感分類（section 2-3 follows emotional punctuation density rule K-1；prose block has adequate emotional punctuation；prose block does not have excessive emotional punctuation；kaomoji variety is maintained）
