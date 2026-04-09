## Why

模組一（Ch1）的練習題設計融合了數學素養（PISA 2022）與運算思維（CT）的學術理論基礎。這些參考文獻目前只存在於對話記錄中，需要持久化為可引用的資源，並作為教材的學術正當性背書。同時為模組一新增一個「參考文獻」附錄頁面，供教師與學生查閱。

## What Changes

- 新增 `docs/tutor/py/ch1/references/` 目錄，存放 10 份可下載的學術 PDF
- 新增 `docs/tutor/py/ch1/reference.md` 參考文獻頁面，列出 23 份已驗證的學術來源
- 參考文獻頁面依主題分類：數學素養、運算思維、整合研究、台灣課綱
- 每份文獻包含：作者、年份、標題、來源連結（PDF 或 URL）

## Non-Goals

- 不翻譯或摘要這些文獻的內容
- 不將參考文獻嵌入教學正文（只作為獨立附錄頁面）

## Capabilities

### New Capabilities

- `ch1-research-references`: 模組一參考文獻附錄頁面與可下載 PDF 資源集

### Modified Capabilities

（無）

## Impact

- 新增檔案：`docs/tutor/py/ch1/reference.md`
- 新增檔案：`docs/tutor/py/ch1/references/*.pdf`（10 份）
- 側邊欄將自動顯示新的 reference.md 頁面（由 `buildTutorSidebar()` 自動掃描）
