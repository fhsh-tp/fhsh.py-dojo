## Why

第一章附錄（`docs/tutor/py/ch1/appendix.md`）目前只留下一個 `<!-- TBD 增加完整的 Python Keywords Table -->` 佔位符，沒有任何可讀內容。零基礎高中生讀完第一章後，只學過 `True / False / and / or / not / if / elif / else` 這八個關鍵字；他們需要一張「我學到哪裡、接下來會遇到什麼」的全景圖，才不會在自主練習時誤把關鍵字當變數名使用，也不會看到未來章節出現陌生字詞時無所適從。既有 spec 中的 `rule T-2` 已明文禁止第一章出現任何 TBD 殘留標記，這個佔位符必須被填上實質內容。

## What Changes

- 在 `docs/tutor/py/ch1/appendix.md` 中以完整的「Python 關鍵字表」取代 `<!-- TBD 增加完整的 Python Keywords Table -->` 註解
- 新增 H2 前言段落說明「什麼是關鍵字（Reserved Words）」以及「為什麼不能拿它們當變數名」，並附一個 `SyntaxError` 示例
- 表格以 **語義分類** 方式呈現 Python 3.13 的 35 個硬關鍵字 + 4 個軟關鍵字（共 39 個），欄位包含：關鍵字、中文簡述、首次登場章節、示例片段
- 用 VitePress `> [!TIP]` / `> [!WARNING]` 容器補充學習建議（例如「軟關鍵字 `match` 只在特定語境保留」、「高中課綱不會考全部關鍵字，但認得就好」）
- 擴充 `python-ch1-content` 既有能力：新增一條「附錄必須包含可用的 Python 關鍵字表」的 Requirement，並延伸 rule T-2 覆蓋範圍到 `appendix.md`

## Non-Goals

- 本次**不會**深入解釋每個關鍵字的語意（例如 `yield`、`async`、`nonlocal` 的運作原理）：表格只給中文簡述 + 章節指引，詳解留給對應教學章節
- 本次**不會**列出 Python 內建函式（`print`、`input`、`len`、`int` 等）：這些不是 keyword，且 `keyword.iskeyword()` 不會回 `True`
- 本次**不會**把表格抽成獨立 `.md` 檔或 Vue 元件：直接嵌在 appendix.md 即可，避免提前引入元件化複雜度
- 本次**不會**連帶翻譯 rule T-2 的 scope 去涵蓋 `reference.md` 或其他章節檔案；scope 延伸僅針對 `appendix.md`

## Capabilities

### New Capabilities

（無）

### Modified Capabilities

- `python-ch1-content`：新增 Requirement「Chapter 1 appendix contains Python keywords reference table」並延伸既有 rule T-2 的檔案範圍，使其同時涵蓋 `1-1.md` 與 `appendix.md`

## Impact

- Affected specs: `python-ch1-content`（ADDED 一條 requirement + MODIFIED 既有 T-2 requirement）
- Affected code:
  - `docs/tutor/py/ch1/appendix.md`（寫入完整關鍵字表，移除 TBD 註解）
- No build / theme / 元件檔變動；純教材內容更新
