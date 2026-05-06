## 1. 前置準備

- [x] 1.0 讀取編輯規則定義：(a) `/phoenix-popular-science-article-style-enhance.md` 全部 15 條規則的完整定義、違規/合規對照與 EAL 工作流程, (b) `openspec/specs/python-ch1-content/spec.md` 中 P-1 至 K-1 各規則的 spec-level 定義。兩份文件是所有撰寫工作的必讀前置
- [x] 1.1 確認 `restructure-course-outline` change 已 apply，Ch2 index 已更新為 5 sections 結構
- [x] 1.2 讀取現有 `docs/tutor/py/ch2/2-1.md`、`2-2.md`、`2-3.md` 全文，記錄：(a) 每節最後一個 ChallengeLink 的 slug, (b) 最後一張圖片的編號, (c) 現有 challenge 檔案的最大 ID 數字
- [x] 1.3 讀取 `docs/tutor/py/ch1/1-1.md` 至 `1-4.md` 作為寫作風格參考，確認 phoenix-popular-science-article-style 的 15 條規則
- [x] 1.4 讀取 `docs/tutor/py/ch1/appendix.md` 中 Image Specification Appendix 的格式作為 Ch2 appendix 參考

## 2. 撰寫 Section 2-4 巢狀迴圈 (python-ch2-2-4-content)

- [x] 2.1 [Req: Section 2-4 file exists with correct frontmatter and structure] 建立 `docs/tutor/py/ch2/2-4.md`：撰寫 frontmatter（layout: doc, title, description, chapter: 2, section: "2-4", createdTime, challenge slug 指向例題一）+ VISUAL-STYLE-PREFIX（延用 Ch1/Ch2 美式火柴人漫畫風格）
- [x] 2.2 [Req: Section 2-4 includes 4 AI image specifications] 撰寫開場段落：以日常生活場景引入「迴圈裡面還有迴圈」的概念（例如：檢查教室每一排的每一個座位、電影院逐排逐位檢票），包含 Hook 圖片（圖片編號接續 2-3 最後一張）、學習目標清單（💡 📋 學習目標）。本任務及後續 2.3/2.4/2.6 共插入 4 張圖片佔位符
- [x] 2.3 [Req: Section 2-4 covers nested loops as two knowledge points — KP-A] 撰寫 Knowledge Point A「雙重 for 迴圈基礎」：(a) 類比橋接（S-1）解釋為什麼需要巢狀迴圈, (b) 直角三角形星號圖案程式碼 + trace table（外層 i、內層 j、輸出）——滿足 [Req: Each knowledge point has a trace table demonstrating nested loop execution], (c) 長方形星號圖案, (d) 九九乘法表程式碼 + 縮略 trace table（顯示前 6 次 + 最後 2 次迭代）, (e) 解釋圖片（巢狀迴圈執行流程圖）, (f) 常見錯誤提醒（E-1）：縮排錯誤導致內層只跑一次、外層與內層變數名稱撞名
- [x] 2.4 [Req: Section 2-4 covers nested loops as two knowledge points — KP-B] 撰寫 Knowledge Point B「巢狀迴圈應用」：(a) 過場段（S-3：2-4句總結 KP-A + 指出缺口 + 動機）, (b) 巢狀迴圈 + if 條件組合（找出所有滿足條件的數字對）+ trace table, (c) 等腰三角形圖案（空格 + 星號的計算邏輯）, (d) 效能直覺："外層跑 N 次、內層跑 M 次，總共 N×M 次", (e) 類比圖片（日常生活場景如檢票）, (f) 常見錯誤（E-1）：忘記每行結尾 print() 換行、內外層 range 搞混
- [x] 2.5 [Req: Section 2-4 has 8-10 Judge challenges in APCS beginner transition format — 例題一] 撰寫例題一「Judge 解題實戰：星星直角三角形」：(a) 題目說明（輸入 N，輸出 N 行的直角三角形）, (b) 明確「輸入格式」「輸出格式」區塊, (c) 2-3 組範例 I/O, (d) Step 1 分析 IPO, (e) Step 2 寫程式碼, (f) Step 3 逐行解讀（W-1 一致性）, (g) Step 4 常見錯誤, (h) ChallengeLink
- [x] 2.6 [Req: Section 2-4 has 8-10 Judge challenges in APCS beginner transition format — 例題二] 撰寫例題二「Judge 解題實戰：九九乘法表」：(a) 題目說明（輸入 N，輸出 1~N 的乘法表，格式對齊）, (b) 明確「輸入格式」「輸出格式」+ 對齊要求, (c) 2 組範例 I/O, (d) 完整 IPO + 程式碼 + 解讀 + 錯誤, (e) ChallengeLink, (f) 教學圖片（步驟示意）
- [x] 2.7 [Req: Section 2-4 has 8-10 Judge challenges in APCS beginner transition format — 類題] 撰寫 6-8 道類題（「自己動手試試」區塊）：每道題含 H3 標題 + ChallengeLink + 題目說明 + 輸入格式 + 輸出格式 + 2 組範例 I/O + 限制 + 老師提示。題目建議：(1) 星號長方形, (2) 倒三角形, (3) 等腰三角形, (4) 數字金字塔, (5) 菱形圖案, (6) 配對計數（符合條件的 (i,j) 對數）, (7) 可選：巢狀迴圈累加, (8) 可選：字元圖案
- [x] 2.8 撰寫本節小結 + 下一節預告（預告 2-5 模組總結）
- [x] 2.9 建立所有 2-4 例題與類題的 challenge 檔案（`docs/challenge/<slug>.md`），ID 從現有最大值 +1 開始連續編號，每檔含完整 YAML frontmatter（layout, id, title, difficulty, tags, algorithm, testcase_count≥5, params, generator, starter_code, chapter: ch2, description）
- [x] 2.10 [Req: Section 2-4 follows all 15 editorial rules] 全文自查 2-4.md 的 15 條 editorial rules 合規性（P-1 破折號、T-1 術語時序、S-1 類比橋、S-2 笑話回歸、S-3 過場、C-1 程式碼前導、E-1 錯誤預防、M-1 心智模型、W-1 一致性、T-2 無 TBD、F-1 圖片格式、V-1 container 語法、T-3 無空白元素、K-1 顏文字密度多樣性）

## 3. 撰寫 Section 2-5 模組二總結 (python-ch2-2-5-content)

- [x] 3.1 [Req: Section 2-5 file exists with correct frontmatter as module summary] 建立 `docs/tutor/py/ch2/2-5.md`：撰寫 frontmatter（layout: doc, title, description, chapter: 2, section: "2-5", createdTime，不含 challenge 欄位）+ VISUAL-STYLE-PREFIX
- [x] 3.2 [Req: Section 2-5 contains a knowledge map covering all Module 2 concepts] 撰寫知識地圖：使用 Mermaid mindmap 語法，根節點「模組二：迴圈與重複結構」，4 個主分支（2-1 ~ 2-4），每個分支含 3+ 子概念節點
- [x] 3.3 [Req: Section 2-5 contains a self-check checklist] 撰寫自我檢查表：12-18 個 checkbox 項目，每項以動詞開頭（「能夠...」「知道...」「會用...」），涵蓋 2-1 至 2-4 各 3-4 項，比例均衡
- [x] 3.4 [Req: Section 2-5 contains a Module 3 preview] 撰寫模組三預告段落（2-4 句）：從「你已經學會迴圈」過渡到「但如果有 100 筆成績怎麼辦？」引出串列、搜尋、排序、字典
- [x] 3.5 [Req: Section 2-5 includes 2 AI image specifications] 插入 2 張圖片佔位符（F-1 雙行格式）：(a) Recap 類型總結圖, (b) Hook 類型預告圖
- [x] 3.6 [Req: Section 2-5 has no Judge challenges] 確認 section 2-5 不含任何 ChallengeLink 元素
- [x] 3.7 [Req: Section 2-5 follows editorial rules] 全文自查 2-5.md 的 editorial rules 合規性（P-1, S-3, K-1, F-1, V-1, T-2, T-3）

## 4. 增補既有 Section 練習題 (python-ch2-enhanced-exercises)

- [x] [P] 4.1 [Req: Section 2-1 receives 2-4 additional APCS-style practice problems] [Req: APCS beginner transition format template] 為 2-1.md 末尾「自己動手試試」區塊追加 2-4 道 APCS 風格練習題：每題含 H3 標題 + ChallengeLink + 題目說明 + 輸入格式 + 輸出格式 + 2 組範例 I/O + 限制 + 提示。建議：等差數列求和、數字金字塔、星星正方形、倒數偶數。[Req: New exercises are appended without modifying existing content] 不得修改 2-1.md 的任何既有內容
- [x] [P] 4.2 [Req: Section 2-2 receives 3-5 additional APCS-style practice problems] 為 2-2.md 末尾「自己動手試試」區塊追加 3-5 道 APCS 風格練習題。建議：猜數字遊戲簡化版、最大公因數 GCD、數位根、完美數判斷。New exercises are appended without modifying existing content——不得修改 2-2.md 的任何既有內容
- [x] [P] 4.3 [Req: Section 2-3 receives 2-4 additional APCS-style practice problems] 為 2-3.md 末尾「自己動手試試」區塊追加 2-4 道 APCS 風格練習題。建議：質數判斷、完美數進階、最小質因數搜尋進階。New exercises are appended without modifying existing content——不得修改 2-3.md 的任何既有內容
- [x] [P] 4.4 [Req: All enhanced exercise challenge files follow the standard format] 建立所有 4.1/4.2/4.3 新增題目的 challenge 檔案（`docs/challenge/<slug>.md`），ID 接續 2-4 節的最大 ID，每檔含完整 YAML frontmatter（layout, id, title, difficulty, tags, algorithm, testcase_count≥5, params, generator, starter_code, chapter: ch2, description）

## 5. Ch2 Appendix

- [x] 5.1 建立 `docs/tutor/py/ch2/appendix.md`：(a) frontmatter, (b) Ch2 新增關鍵字補充表, (c) Image Specification Appendix——2-4 節 4 張 + 2-5 節 2 張 = 共 6 張圖片的完整規格（類型、意圖、完整 Prompt 含 VISUAL-STYLE-PREFIX 全文展開、備註）

## 5b. Reference 檔案

- [x] 5.2 建立 `docs/tutor/py/ch2/reference.md`：參考 `docs/tutor/py/ch1/reference.md` 的格式，收錄 Ch2 相關的學術參考文獻。至少包含：(a) 迴圈與重複結構的教學研究, (b) 巢狀迴圈的認知負荷研究, (c) 台灣 108 課綱相關資訊科技領域文件, (d) APCS 官方網站（https://apcs.csie.ntnu.edu.tw/）。格式採 IEEE 編號引用風格，每筆含作者、年份、標題、來源/URL

## 6. Index 更新與驗證

- [x] 6.1 更新 `docs/tutor/py/ch2/index.md`：取消 2-4 和 2-5 的 HTML 註解，確保所有 5 個 section 連結正確指向實際檔案
- [x] 6.2 驗證所有新建 challenge 檔案的 ID 連續性（無間隔、無重複）
- [x] 6.3 驗證所有新建 challenge 檔案的 YAML frontmatter 完整性（必填欄位齊全）
- [x] 6.4 驗證圖片編號與 2-1~2-3 接續、無間隔
- [x] 6.5 執行 `pnpm build` 確認 VitePress 構建成功
