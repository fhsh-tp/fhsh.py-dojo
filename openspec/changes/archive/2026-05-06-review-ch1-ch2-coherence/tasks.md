## 1. 前置作業

- [x] 1.1 重新檢視 `docs/tutor/py/ch1/1-2.md`、`docs/tutor/py/ch2/2-1.md`、`docs/tutor/py/ch2/2-4.md` 三個檔案的目前內容，確認所有要修改的位置（行號、段落）與本 change 的 design.md 描述一致。
- [x] 1.2 啟動本機 VitePress dev server（`pnpm docs:dev` 或專案實際指令），確認三個檔案目前都能正確渲染、無語法錯誤；保留 dev server 在背景執行，方便每個 Phase 完成後即時預覽。

## 2. Phase 1-A：在 1-2 正式介紹字串運算（對應 design.md 的 Decision 1: 在 1-2 正式介紹字串運算（`+`、`*`），而非在 Ch2 個別補充）

- [x] 2.1 [P] 依 `python-ch1-content` 的 Requirement「Section 1-2 introduces string operators (concatenation and repetition)」在 `docs/tutor/py/ch1/1-2.md` 的「資料型別」H2 內、「三種基礎型別」之後、「`input()` 的型別陷阱」之前，新增一個 H3 子節，介紹字串相加 `+`（串接）與字串乘整數 `*`（重複）兩個運算。本任務直接對應 Decision 1: 在 1-2 正式介紹字串運算（`+`、`*`），而非在 Ch2 個別補充。
- [x] 2.2 在新 H3 子節內，撰寫對比說明：同樣的 `+` 與 `*` 符號，在數字與字串上的語意不同（運算子重載）；補上 `"abc" + 1` 的 `TypeError` 與 `"abc" * 0` 為空字串的常見錯誤示範。
- [x] 2.3 在新 H3 子節內，新增至少一個 trace-style 的範例表格，列出 `"Hello" + "World"`、`"abc" * 3`、`"abc" * 0`、`"abc" + 1`、`"abc" * 1.5` 的執行結果，符合 spec 中的 example table。
- [x] 2.4 在 dev server 預覽 1-2 的修改，確認新 H3 子節在「三種基礎型別」之後、「`input()` 的型別陷阱」之前，且所有程式碼區塊渲染正確。
- [x] 2.5 **Phase 1-A 稽核閘門**：執行 `/spectra-audit`，由三個 sub-agent 並行稽核（連貫性、技術正確性、用語與教學品質）。三個 sub-agent 全部通過才能進入下一個 Phase；任何一個發現問題就回到 2.1–2.4 修正後重跑稽核。

## 3. Phase 1-B：在 2-4 加 `\t` 與 `f-string` 的 inline NOTE（對應 design.md 的 Decision 2: 在 2-4 內補 `\t` 與 `f-string` 的 inline NOTE，而非在 Ch1 加新節）

- [x] 3.1 [P] 依 `python-ch2-2-4-content` 的 Requirement「Section 2-4 introduces escape character `\t` and f-string before first use」，在 `docs/tutor/py/ch2/2-4.md` 的九九乘法表程式碼之前，新增 `\t` 跳脫字元的 NOTE 區塊，說明 `\t` 是 Tab 字元、會跳到下一個 tab 停靠點，並引入「跳脫字元」這個類別名稱、補一個 `\n` 作為類別範例。本任務直接對應 Decision 2: 在 2-4 內補 `\t` 與 `f-string` 的 inline NOTE，而非在 Ch1 加新節。
- [x] 3.2 在 3.1 的 NOTE 之後、第一個 `f"..."` 出現之前，新增 f-string 的 NOTE 區塊，說明 `f"Hello, {name}"` 的大括號嵌入運算式語法，以及 `f"{value:N}"` 的 `:N` 寬度格式（至少 N 個字元寬、預設右對齊）；並提及 1-2 已預告「後面才會學」，現在正式介紹。
- [x] 3.3 確認 3.1、3.2 兩個 NOTE 區塊在文件順序上**確實位於**第一個 `\t` 與第一個 `f"..."` 出現位置之前；若 2-4 內有更早的位置使用這些語法，把 NOTE 往前移。
- [x] 3.4 在 dev server 預覽 2-4 的修改，確認兩個 NOTE 區塊渲染正確（`> [!NOTE]` 容器、程式碼字體、表格如有）。
- [x] 3.5 **Phase 1-B 稽核閘門**：執行 `/spectra-audit`，由三個 sub-agent 並行稽核。三個 sub-agent 全部通過才能進入下一個 Phase。

## 4. Phase 1-C：移除 2-4 提示中未介紹的進階語法（對應 design.md 的 Decision 3: 移除 `print(*range(...))` 提示、保留字串乘法提示）

- [x] 4.1 依 `python-ch2-2-4-content` 的 Requirement「Section 2-4 hints SHALL NOT use unintroduced advanced syntax」，在 2-4 數字金字塔（number-pyramid）類題的「老師的提示」NOTE 中移除 `print(*range(1, i+1))` 的序列展開（unpacking）寫法，只保留 `if j < i` 加空格的解法。本任務直接對應 Decision 3: 移除 `print(*range(...))` 提示、保留字串乘法提示。
- [x] 4.2 在 2-4 等腰三角形（isosceles-triangle）類題的「老師的提示」NOTE 中，把字串乘法的提示改寫為「也可以用字串乘法 `" " * (n-i) + "*" * (2*i-1)`，這個寫法在 1-2 已正式介紹」這類措辭，明確帶出與雙重迴圈寫法是並列選項，不顯得是「偷吃步」。
- [x] 4.3 用 grep 掃描 2-4 全文，確認沒有殘留的 `print(*`、`*range(`、`*list(`、`[x for x in`、`def `、`lambda `、`a[i:j]`、`:=` 等被禁止的語法出現在「老師的提示」NOTE 中（VitePress 的 `[!NOTE]` 容器除外）。
- [x] 4.4 在 dev server 預覽 2-4 的修改，確認所有提示 NOTE 仍然連貫易讀。
- [x] 4.5 **Phase 1-C 稽核閘門**：執行 `/spectra-audit`，由三個 sub-agent 並行稽核。

## 5. Phase 2-A：補充「為什麼包頭不包尾」的 Dijkstra 三理由（對應 design.md 的 Decision 5: 用 Dijkstra 1982 論述背書「為什麼包頭不包尾」）

- [x] 5.1 依 `python-ch2-2-1-content` 的 Requirement「Section 2-1 explains the rationale for half-open range intervals」，在 2-1 的「常見錯誤：差一錯誤」H3 內或緊鄰位置，新增一個 NOTE 或 TIP 區塊，列出三個理由（長度好算、空集合自然、可乾淨切分），每個理由都用一個高一學生能徒手驗算的具體例子說明。本任務直接對應 Decision 5: 用 Dijkstra 1982 論述背書「為什麼包頭不包尾」。
- [x] 5.2 把 2-1 行 108 附近現有的「用久了你會發現這個設計其實很方便（後面會解釋為什麼）」這句話刪除或改寫，讓全章不再賴帳；改寫後的句子可以直接導向新的 Dijkstra NOTE。
- [x] 5.3 用 grep 掃描 2-1 全文，確認「用久了你會發現這個設計其實很方便（後面會解釋為什麼）」的字串沒有殘留。
- [x] 5.4 **Phase 2-A 稽核閘門**：執行 `/spectra-audit`，由三個 sub-agent 並行稽核。

## 6. Phase 2-B：重寫「省略鏈」為「三種便利寫法」（對應 design.md 的 Decision 4: Range 說明採「保留架構、針對性補強」策略）

- [x] 6.1 依 `python-ch2-2-1-content` 的 MODIFIED Requirement「Knowledge Point B includes range parameter reduction consolidation and arithmetic progression callout」，重寫 2-1 行 516–554 的「range 的三種寫法，其實是同一招」子節，把三種形式描述為「三種便利寫法對應三種常見場景」，明確避免「省略」這個詞。本任務直接對應 Decision 4: Range 說明採「保留架構、針對性補強」策略。
- [x] 6.2 重寫 6.1 子節內的 ASCII 圖示樹（行 540–552 區域），讓圖中標籤改為中性描述（例如「shortest / with start / with step」），不要再標 `省略 step → 預設為 1` 這類「省略」措辭。
- [x] 6.3 確認 6.1 子節仍保留行 558–565 的「等差數列數學彩蛋」TIP 區塊，且該 TIP 仍引用 Python Tutorial 4.3 的原文 `It generates arithmetic progressions.` 並對應 `start ↔ a₁`、`step ↔ d`。
- [x] 6.4 用 grep 掃描 6.1 子節（H3「range 的三種寫法，其實是同一招」與下一個 H3 之間），確認沒有殘留的「省略」二字。
- [x] 6.5 **Phase 2-B 稽核閘門**：執行 `/spectra-audit`，由三個 sub-agent 並行稽核。

## 7. Phase 2-C：補「range 不是 list」NOTE（對應 design.md 的 Decision 4: Range 說明採「保留架構、針對性補強」策略 的延伸）

- [x] 7.1 依 `python-ch2-2-1-content` 的 Requirement「Section 2-1 includes a "range is not a list" note」，在 2-1 的「`range()` 的完整用法」H2 結尾、本節小結之前，新增一個 NOTE 區塊：說明 `print(range(5))` 會印 `range(0, 5)`、`range` 是「按需要產生數字」的物件、`list(range(5))` 可看 `[0, 1, 2, 3, 4]`（並標註 `list` 是還沒教的前向引用）。本任務直接對應 Section 2-1 includes a "range is not a list" note 的需求。
- [x] 7.2 在 dev server 預覽，確認新 NOTE 區塊位置正確（範圍三種寫法之後、本節小結之前）。
- [x] 7.3 **Phase 2-C 稽核閘門**：執行 `/spectra-audit`，由三個 sub-agent 並行稽核。

## 8. Phase 2-D：統一「步長 / 一步兩步」用語（對應 Decision 4 的延伸）

- [x] 8.1 依 `python-ch2-2-1-content` 的 Requirement「Section 2-1 uses unified step terminology」，把 2-1 行 465「如果你想『每隔 2 遍寫一次』」改為「如果你想『每次加 2』，產生像 0, 2, 4, 6, 8 這樣的數列」。這是必修的技術錯誤修正。
- [x] 8.2 把 2-1 行 492 的「`i` 每次跳 2」改為「`i` 每次加 2」。
- [x] 8.3 把 2-1 行 689、714 的「每次跳 2」改為「每次加 2」。
- [x] 8.4 把 2-1 行 941 的「每次加 -2」改為「每次減 2」。
- [x] 8.5 用 grep 全篇掃描 2-1，搜尋「每次跳」「每次增加」「每隔.*遍」「每次加 -」這幾個 pattern，確認除了「每次加 N」「每次減 N」（N 為正整數）之外的描述都已改寫，符合 spec 中的 replacement table。
- [x] 8.6 在 dev server 預覽，逐段瀏覽 2-1，確認步長相關描述都統一了。
- [x] 8.7 **Phase 2-D 稽核閘門**：執行 `/spectra-audit`，由三個 sub-agent 並行稽核。

## 9. Phase 3：跨檔案連貫性與用語把關

- [x] 9.1 依 `ch2-cross-chapter-audit` 的 Requirement「Module 2 sections SHALL NOT use Python features before they are introduced anywhere in Ch1 or earlier Ch2 sections」，用 grep 掃描 `docs/tutor/py/ch2/*.md` 全部檔案中所有 `"*" * `、`\t`、`f"`、`f'` 出現位置，逐一確認每個位置之前都有對應的 Ch1 或 Ch2 較早章節的介紹。
- [x] 9.2 依 `ch2-cross-chapter-audit` 的 Requirement「Module 2 hints SHALL NOT introduce syntax that is forbidden by per-section specs」，用 grep 掃描 `docs/tutor/py/ch2/*.md` 中所有「老師的提示」NOTE 區塊，確認沒有違反各 per-section spec 的禁忌語法（特別是 2-4 的 unpacking、list comprehension 等）。
- [x] 9.3 用 grep 掃描三個被修改的檔案（`docs/tutor/py/ch1/1-2.md`、`docs/tutor/py/ch2/2-1.md`、`docs/tutor/py/ch2/2-4.md`）有無大陸用語：軟件、數據、程序（指 program 而非 procedure）、視頻、用戶、默認、登錄、菜單、文件夾、回車、屏幕、鼠標、硬盤、內存、克隆、打印；發現後改為台灣慣用詞。
- [x] 9.4 確認三個檔案的英文技術名詞依台灣慣例保留（range、loop、for、while、step、stop、start、Tab、f-string、Trace Table、Off-by-One Error 等）。
- [x] 9.5 **Phase 3 稽核閘門**：執行 `/spectra-audit`，由三個 sub-agent 並行稽核（特別針對跨檔案連貫性與用語）。

## 10. 收尾驗證

- [x] 10.1 在 dev server 完整瀏覽三個被修改的檔案（1-2、2-1、2-4），確認 Markdown 渲染正常（NOTE/WARNING/TIP 容器、程式碼區塊、表格、圖片、Mermaid 流程圖、LaTeX 數學式）、沒有破版、所有內部連結與 ChallengeLink 都能解析。
- [x] 10.2 跑專案實際的測試套件（`pnpm test` 或 vitest 配置內的指令），確認無回歸；若有 sidebar/nav 測試，特別關注。
- [x] 10.3 檢查所有圖片放在正確路徑（沒有因為 NOTE 區塊插入而破壞圖文交錯）。
- [x] 10.4 **最終稽核閘門**：對整個 change 執行最後一次 `/spectra-audit`，確認三個 sub-agent 對全部 8 個 Phase 的成果都通過；產生最終稽核報告交給使用者確認。本任務直接對應 design.md 的 Decision 6: 每階段強制 `/spectra-audit` 三 sub-agent 稽核。
