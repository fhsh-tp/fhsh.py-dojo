## Why

`docs/tutor/py/ch1/reference.md` 中的 23 筆學術文獻，原始來源為對話記錄整理，部分條目未經學術資料庫交叉驗證。經稽核發現：

- 3 筆有細節錯誤：#10、#11 缺少 DOI；#14 將期刊名稱誤寫為作者
- 6 筆無法驗證或存在高風險：#15 疑似 AI 幻覺生成（MDPI 2026 文獻在所有搜尋引擎均無蹤跡）；#18–#20、#22、#23 的 URL 或識別碼未能確認
- 另有 #16、#22 同樣將出版社/期刊名誤標為作者

作為教師與學生使用的教育資源，每一筆引用都必須可追溯至權威來源。現在修正是因為模組一內容已定稿，參考文獻頁是最後需要品質把關的部分。

## What Changes

- **建立 inline 文獻驗證腳本** `tools/ref-verifier/src/ref_verifier/verify_inline.py`：解析 `reference.md` 的 inline markdown 格式，對每筆文獻透過 Semantic Scholar API、CrossRef API 及 HTTP URL 可達性檢查進行三層驗證，輸出結構化驗證報告
- **修正 `docs/tutor/py/ch1/reference.md`**：根據驗證結果修正所有錯誤條目（作者欄位、補 DOI、移除或替換幻覺文獻、修正年份/篇名/卷期頁碼）
- **更新 `ch1-research-references` spec**：新增「所有文獻須經權威來源驗證」需求

### 已知必要修正

| # | 問題 | 修正方式 |
|---|------|---------|
| 10 | 缺少 DOI | 補充 `10.1016/j.edurev.2017.09.003` |
| 11 | 缺少 DOI | 補充 `10.1007/s10956-015-9581-5` |
| 14 | 作者欄位為期刊名 | 改為 Ye, H., Liang, B., Ng, O.-L., & Chai, C. S. |
| 15 | 元資料錯誤（非幻覺） | 實為 Pajares Pescador et al. (2026), DOI: 10.3390/educsci16020345，修正作者/篇名/期刊 |
| 16 | 作者欄位為期刊名 | 查詢 S2/CrossRef 取得正確作者 |
| 22 | 作者欄位為出版社名 | 查詢 S2/CrossRef 取得正確作者 |
| 23 | ERIC ID 未確認 | 驗證 ERIC URL 並修正作者欄位 |

## Non-Goals

- 不新增額外文獻（23 筆全數保留，#15 確認為真實文獻）
- 不重新下載或更換已存在的 10 份本地 PDF（已確認完整）
- 不重新設計參考文獻頁的版面結構或分類方式
- 不修改 lit-fetcher 工具的核心功能（僅重用其 API client）

## Capabilities

### New Capabilities

（無新增 capability）

### Modified Capabilities

- `ch1-research-references`：新增「所有 23 筆文獻須經至少一個權威來源驗證」需求，包括學術論文須有正確作者/年份/篇名/DOI、外部 URL 須可存取

## Impact

- 修改檔案：`docs/tutor/py/ch1/reference.md`
- 新增檔案：`tools/ref-verifier/src/ref_verifier/verify_inline.py`
- 修改 spec：`openspec/specs/ch1-research-references/spec.md`
- 相依工具：`tools/ref-verifier/`（重用 S2 API client）、`tools/lit-fetcher/`（重用 search API）
- 外部 API：Semantic Scholar API、CrossRef API、各出版社/資料庫 URL
