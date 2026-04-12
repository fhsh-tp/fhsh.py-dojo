## Context

`docs/tutor/py/ch1/reference.md` 包含 23 筆學術文獻引用，這些引用在 `save-ch1-research-references` change 期間從對話記錄中整理而成。後續稽核揭示 9 筆條目存在不同程度的問題：作者欄位錯誤（將期刊/出版社名誤標為作者）、缺少 DOI、URL 無法驗證、甚至可能為 AI 幻覺。

現有工具：
- `tools/ref-verifier/`：已有 Semantic Scholar API client（`apis.py`），但 parser 僅支援 `refs/*/abstract.md` 目錄結構
- `tools/lit-fetcher/`：已有 S2 search API 與 OpenAlex client（`apis.py`），但預設搜尋範圍為 2024–2026 且綁定 NTUEE 場域篩選

限制：
- Semantic Scholar 無 API key 時限速 ~1 req/sec（`.env` 中 `SEMANTIC_SCHOLAR_API_KEY` 為空）
- 部分文獻為政策文件或網路資源（#1、#2、#17–#21），不在學術資料庫中
- #15（MDPI 2026）極有可能不存在，須有移除/替換策略

## Goals / Non-Goals

**Goals:**

- 建立可重用的 inline markdown 文獻驗證腳本，未來 ch2+ 文獻頁可直接沿用
- 對全部 23 筆文獻逐一驗證，確保作者、年份、篇名、期刊、DOI 均正確
- 產出結構化驗證報告，作為修正依據

**Non-Goals:**

- 不修改 `ref-verifier` 或 `lit-fetcher` 的既有 CLI 介面或核心流程
- 不建構通用文獻管理系統（僅解決 `reference.md` 的驗證需求）
- 不處理 PDF 內容驗證（僅驗證元資料正確性與 URL 可達性）

## Decisions

### 新增 `verify_inline.py` 而非修改既有 parser

`ref-verifier` 的 `parser.py` 以 `refs/*/abstract.md` 目錄結構為基礎，`PaperMeta` dataclass 不包含 inline 引用格式的欄位（如編號、PDF 路徑、外部 URL）。直接修改會破壞現有功能且增加複雜度。

替代方案：fork `parser.py` → 拒絕，因為兩種格式差異大，共用程式碼少。

決定：在 `tools/ref-verifier/src/ref_verifier/` 下新增獨立模組 `verify_inline.py`，直接 import `ref_verifier.apis` 的 S2 client。

### 三層驗證策略

不同類型的文獻需要不同的驗證方法：

| Tier | 對象 | 方法 | 判定標準 |
|------|------|------|---------|
| A: 學術論文 | #3–#14, #16, #22, #23 | S2 DOI lookup → S2 title search → CrossRef title search | 至少一個 API 回傳匹配記錄（title similarity ≥ 0.8） |
| B: 網路資源 | #19, #20, #21 | HTTP GET + status code | HTTP 200 或 301/302（跟隨重導向後 200） |
| C: 政策/機構文件 | #1, #2, #6, #17 | 本地 PDF 存在 + URL 可達性 | 檔案存在且 URL 回傳 200 |
| D: 高風險 | #15 | MDPI URL → S2 → CrossRef → 結論 | 三管齊下均無結果則判定為幻覺 |
| E: 研討會論文 | #18 | NTNU Scholar URL + S2 title search | URL 可達或 S2 有記錄 |

替代方案：僅使用 S2 → 拒絕，因為政策文件和網路資源不在 S2 中。

### 引入 CrossRef API 作為備援

Semantic Scholar 不收錄所有文獻（特別是教育類期刊覆蓋率較低）。CrossRef 以 DOI 為核心，覆蓋範圍更廣。

API 端點：`https://api.crossref.org/works?query.bibliographic=<title>&rows=5`
限速：polite pool 50 req/sec（附帶 `mailto` header）

替代方案：使用 OpenAlex → 可作為第三備援，但 CrossRef 的 bibliographic search 品質更高。

### DOI 擷取策略

多筆文獻的 URL 本身即包含 DOI（如 Springer、ScienceDirect、Taylor & Francis）：
- `link.springer.com/article/10.1186/s40594-023-00455-2` → DOI: `10.1186/s40594-023-00455-2`
- `doi.org/10.1080/0020739X.2020.1858199` → DOI: `10.1080/0020739X.2020.1858199`

使用正則表達式 `10\.\d{4,9}/[^\s\])"]+` 從 URL 中直接擷取 DOI，避免額外 API 呼叫。

### #15 處置決策樹

1. 嘗試存取 `https://www.mdpi.com/2227-7102/16/2/345`
2. 若 HTTP 200 → 文獻存在，擷取正確元資料後保留
3. 若 HTTP 404/其他 → 搜尋 S2 "Quasi-Experimental Study CT Mathematical Reasoning"
4. 若 S2 有結果 → 用正確資訊替換
5. 若 S2 無結果 → 搜尋 CrossRef 同標題
6. 若 CrossRef 有結果 → 用正確資訊替換
7. 若全無結果 → 移除該條目，後續編號遞減調整

**實際結果**：MDPI 回傳 403（CDN bot 防護），但 S2 與 CrossRef 均確認文獻存在（DOI: `10.3390/educsci16020345`）。決策樹走到步驟 4，以正確資訊替換。

### 安全稽核後修正

實作完成後經三角色安全稽核（Scoundrel / Lazy Developer / Confused Developer）發現並修正以下問題：

1. **Critical — Semaphore 雙重取得死鎖**：`_verify_academic()` 外層取得 semaphore 後再呼叫 `fetch_paper_by_doi()`（內部也取得同一 semaphore），`Semaphore(3)` 下 3 個並行任務會死鎖。修正：移除外層 `async with semaphore:`。
2. **High — `_verify_policy()` 無條件回傳 verified**：URL 回傳 404/500 仍標記為已驗證。修正：檢查 URL 狀態碼，失敗時回傳 `unverifiable`。
3. **Medium — SSRF 風險**：`check_url()` 未驗證 URL scheme，可能被指向 `file://` 或內部網路。修正：僅允許 `http://` 和 `https://`。
4. **Medium — 靜默異常吞噬**：`except Exception: return None` 隱藏所有錯誤。修正：改用具體異常類型（`httpx.HTTPError`、`KeyError`、`ValueError`）並加入 logging。
5. **Medium — DOI 路徑缺少作者偵測**：`_authors_list` 僅在 title search 路徑設定，DOI 路徑下不會觸發作者校正邏輯。修正：當作者欄位為已知期刊名但無 `_authors_list` 時，標記需手動驗證。

## Risks / Trade-offs

| 風險 | 影響 | 緩解措施 |
|------|------|---------|
| S2 API 限速導致驗證耗時 | 23 筆 × 3 sec delay ≈ 70 秒 | 接受此延遲；非必要不申請 API key |
| CrossRef 回傳模糊匹配 | 誤判文獻存在 | 實作 title similarity 門檻（≥ 0.8） |
| 網站 bot 防護阻擋 HTTP check | URL 判定為不可達 | 使用正常 User-Agent header；403 視為「可能存在但受保護」 |
| #15 移除後編號變動 | 文件中其他地方可能引用編號 | 搜尋全站確認無交叉引用（reference.md 中的編號僅供該頁使用） |
| 部分 DOI 在 S2 查無紀錄 | 無法交叉驗證 | CrossRef 作為備援；本地 PDF 存在 + URL 可達即可接受 |
