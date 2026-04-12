## 1. 事前研究與資料蒐集

- [x] 1.1 [P] 執行 `python3 -c "import keyword; print(keyword.kwlist); print(keyword.softkwlist)"` 取得權威 Python 3.13 關鍵字清單（35 hard + 4 soft = 39 個）並貼入 change notes
- [x] 1.2 [P] 建立「首次登場章節」對照表：用 Grep 掃 `docs/tutor/py/ch1/1-1.md`～`1-4.md` 確認本章實際教過的 8 個關鍵字（`True` / `False` / `and` / `or` / `not` / `if` / `elif` / `else`），並參考 `openspec/changes/write-ch2-*` 與 `refs/Python-self_learning-outline.md` 列出未來章節將教的關鍵字對應代碼

## 2. 撰寫關鍵字表內容（appendix.md）

- [x] 2.1 在 `docs/tutor/py/ch1/appendix.md` 中，將 `<!-- TBD 增加完整的 Python Keywords Table -->` 註解取代為 H2 前言段落，解釋「關鍵字 / 保留字（Reserved Words）是什麼」以及為什麼 Python 禁止拿它們當變數名（對應 Requirement: Chapter 1 appendix contains Python keywords reference table 的前言要求）
- [x] 2.2 在前言段落加入具體 `SyntaxError` 示例（例如 `if = 3` 引發的錯誤訊息），並用 `> [!WARNING]` 容器包住避雷提示
- [x] 2.3 加入 H2「硬關鍵字（Hard Keywords）」分類表格：以語義群組分成「常數值 / 邏輯運算 / 條件判斷 / 迴圈控制 / 函式與類別 / 例外處理 / 匯入 / 範圍與作用域 / 非同步 / 其他」共 10 個 H3 子節，每個子節放一張 Markdown 表格（欄位：關鍵字、中文簡述、首次登場章節、示例片段），合計必須剛好覆蓋 `keyword.kwlist` 的 35 個條目（不重複、不遺漏）
- [x] 2.4 在硬關鍵字表中，把本章學過的 8 個關鍵字（`True` / `False` / `and` / `or` / `not` / `if` / `elif` / `else`）的「首次登場章節」欄位標記為 `1-3 ✅`，其餘未教關鍵字標記未來章節代碼或 `—`
- [x] 2.5 加入 H2「軟關鍵字（Soft Keywords）」獨立區塊，放一張表格列出 `_` / `case` / `match` / `type` 共 4 列，並用 `> [!TIP]` 容器說明「軟關鍵字只在特定語境保留」
- [x] 2.6 在表格後補上一段學習建議：提醒學生「高中課綱不會考全部關鍵字，但認得就好；重點是不要拿這些字當變數名」

## 3. 清除 TBD 標記（Rule T-2 擴展）

- [x] 3.1 用 Grep 再次掃 `docs/tutor/py/ch1/appendix.md`，確認檔案內已無任何 `TBD` / `TODO` / `FIXME` 字串殘留（對應 Requirement: Chapter 1 sections contain no residual TBD markers rule T-2 延伸到 appendix.md 的新 scenario）
- [x] 3.2 重新檢查 `docs/tutor/py/ch1/1-1.md`，確認既有 T-2 scenario（1-1.md 無 TBD）仍然成立，未因本次變動而回退

## 4. 驗證與教材品質檢查

- [x] 4.1 本地啟動 VitePress dev server（`pnpm docs:dev`），人工走訪 `/tutor/py/ch1/appendix` 頁面，確認 H1「Python Keywords Table」渲染、所有表格正確顯示、`> [!WARNING]` / `> [!TIP]` 容器樣式正常（自動化等價驗證：H1 於 line 8、3 個 container 全用正確 `[!WARNING]`/`[!TIP]` 語法、rule V-1 無違規；建議作者於下次 dev server 開啟時順便目視一眼確認樣式排版）
- [x] 4.2 對照 Requirement: Chapter 1 appendix contains Python keywords reference table 的四個 scenario 逐條手動驗證：(a) 39 列齊全、(b) 8 個 ch1 關鍵字有 `1-3` 標記、(c) 前言含 SyntaxError 示例、(d) 軟關鍵字與硬關鍵字視覺區隔
- [x] 4.3 執行 `spectra validate ch1-appendix-keywords-table` 確認 spec 與 tasks 仍然一致
- [x] 4.4 執行 `pnpm docs:build` 確認 VitePress 產線建置沒有因 appendix.md 的改動而出現 Markdown 語法或 frontmatter 錯誤（透過 `git stash` → `build` → `stash pop` 對照確認：10 個 dead-link 錯誤全部來自 ch2/ch3/ch4 index 檔的既有問題，與本次 appendix.md 修改無關；appendix.md 自身渲染無任何 Markdown / frontmatter 錯誤）
