## 1. 前置與盤點證物

- [x] 1.1 確認工作分支的基底含有 commit `29e381c`（行內公式的 CSS 修正）。可觀察結果：在分支上執行 git log 查詢該 commit 有輸出，且 `.vitepress/theme/custom.css` 含 `mjx-container > svg` 規則。驗證方式：若查不到就停止並回報，不得從 `staging` 開分支——少了這條 CSS，53 頁會全部斷行，而驗證卻會在有修正的環境跑出綠燈。
- [x] 1.2 [P] 交付盤點腳本 `scripts/latex-notation-survey.py`，行為是掃描 `docs/challenge/*.md` 的 frontmatter 之後內文並分級輸出。契約：不帶旗標時輸出人可讀清單；帶 `--json` 時輸出含 `total`、`converted`、`pending`、`clean`、`per_file` 五個鍵的物件，`per_file` 每筆含 `symbols`、`detail`、`latex`、`bare_dollar`。掃描面依 design 的「兩級記號黑名單與 lint 逃生門」所定順序計算：內文 → 去 code fence → 去圖片語法 → 去配對的 `$…$`／`$$…$$`。驗證方式：對一份沒有 frontmatter 的暫存 md 執行，確認整份被當內文處理而非靜默跳過。
- [x] 1.3 產生轉換前的證物 `openspec/changes/latex-challenge-notation/measure/notation-before.json`。可觀察結果：該檔的 `pending` 為 55、`converted` 為 3、`clean` 為 13。驗證方式：以 `--json` 執行盤點腳本並比對這三個數字，對不上就先查腳本再往下。
  - 初稿寫 53／3／15，是黑名單還沒收錄裸的 `<` `>`、`!=`、`÷` 時量的；`quadrant-classifier` 整頁 7 條不等式因此被歸成「無記號」，整頁沒有人看過。黑名單補齊後在 `HEAD` 的內容上用同一份規則重測，得到 55／3／13，證物已重新產生。

## 2. 守門測試（先紅燈）

- [x] 2.1 交付 `scripts/latex-notation.test.ts`，實作 spec 的「A test enforces the notation rules」。行為：`pnpm test --run` 在任何題目頁違反記號規則時失敗，訊息形如 `docs/challenge/<slug>.md:<line> 出現 A 級記號 "<="，請改寫成 LaTeX（見 Usage.md 記號分類表）`。依 design 的「兩級記號黑名單與 lint 逃生門」實作 A／B 兩級與 `latex-lint-ignore-next-line` 逃生門，並依 design 的「守門測試放在 vitest 而非獨立腳本」放進 vitest。驗證方式：此時執行必定失敗，違規散布的檔案數等於 `pending`——這是紅燈基準線，把它記進 `measure/lint-red.txt`。實測（擴充後的規則、`HEAD` 的內容）：222 處違規、55 個檔案，加上 `movie-ticket` 的 5 個裸貨幣錢字號被語法關卡抓到。
- [x] 2.2 [P] 驗證守門測試會**一次列出所有違規**而非第一個就停。可觀察結果：紅燈輸出同時包含 `prize-order-code`、`movie-ticket`、`print-farm-schedule` 三個檔名。驗證方式：對紅燈輸出 grep 這三個 slug，三者皆須命中。
- [x] 2.3 [P] 驗證 B 級記號在行內 code span 內不被誤殺。可觀察結果：`print-farm-schedule.md` 甘特圖說明中的 `` `·` `` 不出現在違規清單，但同檔的 6 個散文 `≤` 出現。驗證方式：檢查紅燈輸出中該檔的違規列，確認只有 `≤` 沒有 `·`。

## 3. 分批轉換

依 design 的「分頁批次順序：由高密度到低密度」分五批，每批各自成一個 commit。每批完成後重跑盤點腳本，`pending` 必須恰好減去該批題數；對不上就停下來查，不要繼續往下批做。

- [x] 3.1 完成最高密度 4 題的轉換，實作 spec 的「Challenge body math statements use LaTeX」：`prize-order-code`（21 個記號）、`rank-code-backfill`（19）、`pillbox-reminder`（16）、`ap-layout-plan`（10）。依 design 的「記號分類表：什麼進 LaTeX、什麼留反引號、什麼不動」逐處判斷，並依 design 的「散文中的變數字母也進 LaTeX」把 `N`、`M`、`T`、`n`、`k` 等變數字母一併轉換。這四題是分類表的壓力測試——依 design 的「分頁批次順序：由高密度到低密度」先做它們，任何分類表涵蓋不到的情況要在此時補進表裡再往下。可觀察結果：`rank-code-backfill` 的 `N×(N−1)×…×2×1` 與 `ap-layout-plan` 表格中的 8 個負數以 MathJax 排版呈現。驗證方式：重跑盤點腳本，`pending` 由 53 降為 49。
- [x] 3.2 完成次高密度 5 題的轉換：`exam-collect-verify`（8）、`buffer-audit-log`（7）、`pair-count`（7）、`print-farm-schedule`（7）、`arithmetic-sum`（6）。其中 `print-farm-schedule` 的甘特圖說明含字面的 `` `·` ``，依分類表維持反引號不轉。驗證方式：重跑盤點腳本，`pending` 由 49 降為 44；`print-farm-schedule` 的 `bare_dollar` 為 0 且該字面圖形仍在原處。
- [x] 3.3 完成中密度 12 題的轉換：`gcd-euclid`、`gem-blast-playtest`、`marquee-display-count`、`multiplication-table`、`skip-multiples`、`star-rectangle`、`target-sum`、`collatz-steps`、`first-divisor`、`perfect-numbers-range`、`range-sum`、`star-square`。其中 `marquee-display-count` 的兩個約束被誤包在反引號裡（`` `1 <= n <= 1000000` `` 與 `` `0 <= k <= n` ``），依分類表改寫成 LaTeX。驗證方式：重跑盤點腳本，`pending` 由 44 降為 32。
- [x] 3.4 完成低密度 26 題的轉換（各 2 個記號，多為輸入說明的上下界）：`bmi-classifier`、`card-restack-count`、`countdown`、`digit-counter`、`digit-sum-skip`、`digital-root`、`even-countdown`、`factorial`、`fair-token-exchange`、`guess-number-simple`、`inverted-triangle`、`isosceles-triangle`、`magazine-typeset-check`、`nested-triangle`、`number-pyramid`、`number-reverse`、`number-staircase`、`number-sum`、`odd-numbers`、`perfect-number`、`prime-check`、`prop-box-packing`、`repeat-greeting`、`smallest-prime-factor`、`star-diamond`、`sum-skip-fives`。其中 `bmi-classifier` 的 BMI 公式實作 spec 的「Chinese words are not placed inside math delimiters」，依 design 的「中文與公式混排時只包住數學片段」只把上標包成 LaTeX，中文留在外面。驗證方式：重跑盤點腳本，`pending` 由 32 降為 6；確認 `bmi-classifier` 的內文不含 `\text{`。
- [x] 3.5 完成尾端 6 題的轉換：`beverage-cashier`、`change-calculator`、`coupon-combo-quote`、`date-validator`、`movie-ticket`、`snack-bar-register`。`movie-ticket` 另外實作 spec 的「Currency dollar signs are escaped」，依 design 的「貨幣符號一律 escape 成反斜線加錢字號」把 5 個票價錢字號改為 escape 形式。可觀察結果：該頁同時存在不等式公式與票價而不互相配對，頁面上票價仍顯示為原本的金額。驗證方式：重跑盤點腳本，`pending` 為 0、`converted` 為 66、`clean` 為 5、該頁 `bare_dollar` 為 0；`pnpm test --run` 的守門測試轉綠。

- [x] 3.6 黑名單缺口的補做。稽核輪發現三個沒被列進黑名單的記號形態：裸的 `<` 與 `>`、`!=`、`÷`。補進 `scripts/latex-notation-rules.json` 並讓兩個讀取端都認得新增的 `tierA.patterns` 鍵，然後把因此漏掉的頁面補轉：`quadrant-classifier`（整頁 7 條不等式）、`vending-change`（`付款 < 價格`）、`fair-token-exchange`（3 處 `÷`）。裸比較用「運算元 運算子 運算元」的正規表示式而非直接把 `<` `>` 列成 token——後者會誤殺 HTML 標籤、markdown 引言行首與 `-->`。同時把自動連結（`<https://…>`）納入掃描面的移除清單，它的形態與裸比較完全相同。可觀察結果：擴充後的規則對全部 71 頁零假陽性。驗證方式：兩個讀取端的 self-test 各自新增正負向控制（引言行首／HTML 註解／自動連結三種形態都不得觸發），`pnpm test --run` 綠。
- [x] 3.7 內文有裸單字母變數、但沒有黑名單記號的 8 頁一併轉換：`hello-world`（`S`）、`leap-year`（`Y`）、`odd-even`（`n`）、`parrot-echo`、`password-check`（`K`）、`seconds-converter`（`S`）、`sign-check`（`n`）、`triangle-classify`（`a,b,c`）。依 design 的「散文中的變數字母也進 LaTeX」。可觀察結果：`clean` 由 13 降為 5。

## 4. 守門測試的負向控制與 frontmatter 保全

- [x] 4.1 對守門測試做負向控制。可觀察結果：暫時把 `target-sum.md` 的一個 LaTeX 不等式改回 Unicode 記號，`pnpm test --run` 失敗且訊息指名該檔與該行；還原後通過。驗證方式：把改前改後兩次執行的輸出記進 `measure/lint-negative-control.txt`——沒有負向控制等於沒有檢查。
- [x] 4.2 驗證 spec 的「Frontmatter is not altered by notation changes」。可觀察結果：所有題目頁的改動全部落在 frontmatter 結束標記之後，frontmatter 區段零改動，因此不需重建測資池或 WASM。驗證方式：逐檔取 frontmatter 區段的 SHA-256 並與本 change 之前的版本比對，結果寫進 `measure/frontmatter-untouched.json`；任一檔雜湊不同即為失敗。
- [x] 4.3 [P] 驗證依 design 的「波浪號範圍與純散文數字維持原樣」，波浪號區間與散文數字未被誤轉。可觀察結果：`movie-ticket` 的年齡區間、`prize-order-code` 的「一個 1~9 的數字」與「去掉尾端的 0 得到 9」維持純文字。驗證方式：對這三處做字串比對，確認轉換後仍原樣存在。

## 5. 出題者文件與渲染驗證

- [x] 5.1 實作 spec 的「The authoring guide documents the notation rules」：在 `Usage.md` 的「Markdown 內文結構」章節新增記號分類表。可觀察結果：出題者在寫題目時就讀得到「先問這串字元會不會原封不動出現在輸入或輸出裡」的判斷順序，以及逃生門標記的用法。驗證方式：逐列檢查表中每個實例都能在實際題目頁找到對應（對照 spec 中的可追溯性表格），不得出現虛構範例。
- [x] 5.2 驗證 spec 的「Inline math shares a line with surrounding text」，依 design 的「行內公式渲染的回歸驗證」執行。可觀察結果：在 dev server（localhost:5173）上，含多個行內公式的段落只佔一行，且 `mjx-container > svg` 的 computed `display` 為 `inline`。驗證方式：量段落 `offsetHeight` 並斷言小於「行高乘以公式數量」，結果寫進 `measure/render-verification.jsonl`；不量 CSS 字串，因為要抓的是版面症狀。此項無法用 jsdom 驗（jsdom 不做版面計算），故不進 CI。
  - 實測：12 頁抽樣全數 `svg_display: inline`；9 頁各有一個「2 個行內公式只佔 1 行」的區塊作為正向證據（`render-verdict.json` 的 `inline_proofs`）。
  - 判讀端的兩條斷言在此時修正：「每頁都必須找得到 1 行的多公式區塊」改成跨頁只需一個正向證據——`quadratic-discriminant` 的多公式段落本來就長到會自然換行；「有公式卻沒有多公式區塊」不再算失敗——`movie-ticket` 的 3 個公式分散在 3 個表格儲存格，那是合法版面。這兩條原本是斷言在假設版面，不是版面出問題。
  - 起站台踩到一次：`vitepress dev docs` 會讀到 `docs/.vitepress` 那份設定，端出一個沒有內容也不噴錯的殼，12 頁全數量到 `mjx_count` 0，看起來就像轉換把公式弄壞了。本專案的 root 在 repo 根目錄，指令是 `vitepress dev`。觀測端已加記 `doc_len`、判讀端已加一條斷言把這種情況直接說成「站台起錯了」。
- [x] 5.3 抽樣驗證轉換後頁面沒有 LaTeX 原始碼外洩。可觀察結果：抽樣頁面的 `innerText` 不含 `\le`、`\times`、`^{`、`\cdots` 等字串，`mjx-container` 數量大於 0。驗證方式：逐頁記錄兩個數字進 `measure/render-verification.jsonl`；若連不上 dev server，必須回報連線失敗本身，不得回報成「頁面沒有公式」。
  - 實測：12 頁 `source_leaks` 全空；`mjx_count` 介於 3（`movie-ticket`）到 43（`pillbox-reminder`）；裸錢字號只有 `movie-ticket` 的 5 個票價，其餘皆 0。

## 6. 收尾

- [x] 6.1 產生轉換後證物 `measure/notation-after.json` 並與 `notation-before.json` 對照。可觀察結果：`pending` 由 55 變 0，`converted` 由 3 變 66，`clean` 由 13 變 5。驗證方式：兩份 JSON 的差異表寫進 change 的 measure 資料夾，數字對不上即為未完成。`compare_survey.py` 另外逐檔檢查「違規消失但 LaTeX 片段數沒增加」——那代表記號是被刪掉而不是被轉換。實測 `PASS`，實際轉換 55 頁。
- [x] 6.2 執行完整驗證關卡。可觀察結果：`pnpm typecheck`、`pnpm lint`、`pnpm test --run` 三者皆綠。驗證方式：三個指令各執行一次並保留輸出；任一失敗即停止並回報，不得跳過。實測：typecheck 無輸出即通過；lint 0 errors／21 warnings（全數為既有的 unused-vars，非本次新增）；test 59 個檔案、850 passed、50 skipped（`content-regression` 對沒有 `reference_solution` 的題目的既有 skip）。
