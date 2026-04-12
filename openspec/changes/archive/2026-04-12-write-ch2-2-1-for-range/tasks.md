## 1. 結構設定

- [x] 1.1 更新 `docs/tutor/py/ch2/index.md` 使其符合「Tutor directory follows multi-subject layout」：將章節列表從 4 節擴展為 7 節（2-1 迴圈：讓電腦當免費勞工、2-2 while 條件迴圈、2-3 迴圈控制：break 與 continue、2-4 串列與線性搜尋、2-5 串列進階與氣泡排序、2-6 字典與雜湊表、2-7 模組二總結），每節含正確的相對路徑連結
- [x] 1.2 建立 `docs/tutor/py/ch2/2-1.md` 使其符合「Section 2-1 file exists with correct frontmatter and structure」：包含完整 frontmatter（layout: doc, title, description, chapter: 2, section: "2-1", createdTime, challenge slug）、VISUAL-STYLE-PREFIX HTML comment、依照 design.md「文章 H2 段落結構」排列的 heading 骨架

## 2. Challenge 設計與建立

- [x] 2.1 設計 6 道 challenge 的題目內容，對應「知識節點拆分與例題配置」：知識節點 A（for + range(n)）的 Judge 例題（ID 11，對應 design「Judge 例題：[題名]（ID 11）」+ 「自己動手試試（ID 12, 13）」共 3 題）；知識節點 B（range(start, stop, step)）的 Judge 例題（ID 14，對應 design「Judge 例題：[題名]（ID 14）」+ 「自己動手試試（ID 15, 16）」共 3 題）。每題須明確定義 Input/Output 格式、params 範圍、difficulty、tags
- [x] 2.2 建立 6 個 challenge 檔案使其符合「Six challenge files exist with correct generator scripts」（`docs/challenge/` 下，ID 11–16），每個檔案包含完整 frontmatter（layout: challenge, id, title, difficulty, tags, algorithm, testcase_count ≥ 5, params, generator, starter_code），generator 腳本必須是可執行的正確 Python 程式

## 3. 教學內容撰寫 — 知識節點 A：for + range(n)

- [x] 3.1 撰寫「Section 2-1 opening connects to Module 1 finale hook」開場段落：使用「開場 Hook：從 1-4 預告接棒」策略，從 1-4 的「100 行 input vs 3 行迴圈」接棒。接著撰寫學習目標清單、「為什麼需要迴圈」動機段（使用「生活比喻策略：「罰寫」比喻」，遵循 S-1 analogy bridge 規則：比喻前先說明為什麼要用比喻）
- [x] 3.2 撰寫「Section 2-1 covers for loops and range() as two knowledge points」中知識節點 A 的教學內容：第一個 for 迴圈範例、「心智模型追蹤：Trace Table 格式」（對應「Trace Table：看清每一步」— 符合「Each knowledge point has a trace table demonstrating loop execution」）、「縮排的意義」說明、「錯誤預防策略（E-1 合規）」（忘記冒號、IndentationError、range(5) 不含 5）
- [x] 3.3 撰寫「Section 2-1 has one example challenge and two practice challenges per knowledge point」中知識節點 A 的部分：按 IPO 分析 → Python 程式碼 → 逐行解讀 → Judge 測試說明 → 常見錯誤排查的順序撰寫 Judge 例題 walkthrough（ID 11）。接著撰寫 2 道類題的提示段落（ID 12, 13），各附 `<ChallengeLink>` 元件

## 4. 教學內容撰寫 — 知識節點 B：range(start, stop, step)

- [x] 4.1 撰寫知識節點 B 的教學內容（「Section 2-1 covers for loops and range() as two knowledge points」後半段）：`range(start, stop)` 與 `range(start, stop, step)` 範例、負步長倒數範例、Trace Table（「Each knowledge point has a trace table demonstrating loop execution」）
- [x] 4.2 撰寫知識節點 B 的「常見錯誤：差一錯誤」（「錯誤預防策略（E-1 合規）」）：off-by-one 錯誤（「為什麼 range(1, 5) 只到 4？」）、step 為 0 的 ValueError，搭配 WARNING container 強調
- [x] 4.3 撰寫知識節點 B 的 Judge 例題 walkthrough（ID 14）+ 類題（ID 15, 16），格式同 3.3。接著撰寫本節小結，用 S-3 section transition 預告下一節 while

## 5. 圖片與附錄

- [x] 5.1 在 2-1.md 適當位置插入圖片 placeholder（F-1 雙行格式），確保每個 H2 段落至少一張圖、不超過五段連續純文字。在文末撰寫「Section 2-1 includes Image Specification Appendix」，每張圖包含類型、意圖、完整 prompt（含 VISUAL-STYLE-PREFIX）、備註

## 6. 編輯規則驗證（Section 2-1 follows all Chapter 1 editorial rules）

- [x] 6.1 驗證「Section 2-1 follows all Chapter 1 editorial rules」之標點與格式規則：掃描 2-1.md 逐一檢查 P-1（所有 `——` 按五步驟決策清單判斷）、V-1（所有 container 使用 `> [!TYPE]`）、T-3（無空 container）、F-1（圖片雙行格式完整）、T-2（無殘留 placeholder marker）
- [x] 6.2 驗證術語與敘事規則（含「T-1 前引用處理」）：掃描 2-1.md 逐一檢查 T-1（while/break/continue/list/dict/tuple 不可在正式語境出現）、S-1（每個比喻前有 meta-cognitive bridge）、S-2（笑話後有 callback connector）、S-3（H2 過渡 2-4 句）、C-1（每個 code block 前有 prose lead-in）
- [x] 6.3 驗證內容品質規則：掃描 2-1.md 逐一檢查 E-1（語法陷阱在引入點立即警告）、M-1（每個新 loop pattern 附 Trace Table）、K-1（每 30 行 prose 至少一個情緒標點、每 10 行不超過一個；同一 kaomoji 單檔不超過 2 次；至少使用 2 種情緒類別）、W-1（code block 與 walkthrough 完全對應）
