## 1. 建立驗證工具

- [x] 1.1 新增 `verify_inline.py` 而非修改既有 parser：在 `tools/ref-verifier/src/ref_verifier/` 下建立 `verify_inline.py`，包含 `InlineRef` dataclass 與 `parse_reference_md()` 函式，從 `reference.md` 解析全部 23 筆 inline 引用（編號、作者、年份、篇名、期刊、URL、PDF 路徑）
- [x] 1.2 引入 CrossRef API 作為備援：在 `verify_inline.py` 中實作 `search_crossref()` async 函式，使用 `https://api.crossref.org/works?query.bibliographic=<title>&rows=5` 端點，附帶 `mailto` header 進入 polite pool
- [x] 1.3 實作 DOI 擷取策略：在 `verify_inline.py` 中實作 `extract_doi_from_url()` 函式，使用正則表達式 `10\.\d{4,9}/[^\s\])"]+` 從 Springer、ScienceDirect、Taylor & Francis 等 URL 中直接擷取 DOI
- [x] 1.4 實作 `check_url()` async 函式：HTTP GET 檢查 URL 可達性，跟隨重導向，回傳 status code；使用正常 User-Agent header
- [x] 1.5 實作 `verify_reference()` 編排函式：根據三層驗證策略（Tier A: S2/CrossRef、Tier B: URL check、Tier C: 本地 PDF + URL、Tier D: 全面搜尋、Tier E: S2 + URL）分派每筆文獻到對應驗證方法
- [x] 1.6 實作 `generate_report()` 函式：輸出 markdown 格式的驗證報告，包含「已驗證」、「需修正」、「無法驗證」、「標記移除」四個區塊
- [x] 1.7 新增 CLI entry point `ref-verifier verify-inline --input <path> --output <dir>`，串接 parse → verify → report 完整流程

## 2. 執行學術論文 API 驗證（Tier A）

- [x] [P] 2.1 執行 S2 DOI/title search 驗證 #3–#9（CT 領域經典論文）：對每篇使用 DOI 擷取策略從 URL 取得 DOI，以 `fetch_paper_by_doi()` 查詢 S2，確認 title、year、authors 均匹配；若無 DOI 則以 title search 查詢。確保 all references are verified against authoritative sources
- [x] [P] 2.2 執行 S2 + CrossRef 驗證 #10–#14（整合研究）：#10 從 ScienceDirect URL 擷取 DOI `10.1016/j.edurev.2017.09.003` 驗證並補充 DOI link；#11 搜尋 title "Defining Computational Thinking for Mathematics and Science Classrooms" 取得 DOI `10.1007/s10956-015-9581-5`；#12、#13 從 URL 擷取 DOI 驗證；#14 從 URL 擷取 DOI `10.1186/s40594-023-00396-w` 取得正確作者名（Ye, Liang, Ng, Chai）。確保 academic reference has correct author field
- [x] [P] 2.3 執行 S2 + CrossRef 驗證 #16、#22、#23：#16 從 URL 擷取 DOI `10.1007/s40751-024-00143-y` 取得正確作者；#22 從 URL 擷取 DOI `10.1007/s42979-024-03386-z` 取得正確作者（目前誤標為 "Springer"）；#23 檢查 ERIC URL `https://files.eric.ed.gov/fulltext/EJ1428026.pdf` 可達性，並以 CrossRef 搜尋取得正確作者。確保 academic reference includes DOI where available

## 3. 執行 URL 可達性檢查（Tier B+C）

- [x] [P] 3.1 HTTP GET 檢查 #1 OECD PISA URL `https://pisa2022-maths.oecd.org/ca/index.html`，確保 web resource URL is accessible
- [x] [P] 3.2 驗證 #2、#17 本地 PDF 存在：確認 `docs/public/references/ch1/Taiwan-108-Math-Curriculum.pdf` 和 `Taiwan-108-Tech-Curriculum.pdf` 均存在
- [x] [P] 3.3 HTTP GET 檢查 #6 ISTE/CSTA 文件 URL（若有外部連結）
- [x] [P] 3.4 HTTP GET 檢查 #18 Hsu & Hu NTNU Scholar URL `https://scholar.lib.ntnu.edu.tw/en/publications/application-of-the-four-phases-of-computational-thinking-and-inte-2/`
- [x] [P] 3.5 HTTP GET 檢查 #19 Edutopia URL `https://www.edutopia.org/article/python-coding-algebra/`
- [x] [P] 3.6 HTTP GET 檢查 #20 NRICH URL `https://nrich.maths.org/9642`
- [x] [P] 3.7 HTTP GET 檢查 #21 Project Euler URL `https://projecteuler.net/`

## 4. 調查 #15 疑似幻覺

- [x] [P] 4.1 執行 #15 處置決策樹：嘗試存取 `https://www.mdpi.com/2227-7102/16/2/345`，若 HTTP 404 則搜尋 S2 "Quasi-Experimental Study CT Mathematical Reasoning" year:2025-2026，再搜尋 CrossRef 同標題。若三管齊下均無結果，判定為幻覺，標記移除。確保 unverifiable reference is handled

## 5. 彙整修正清單

- [x] 5.1 根據 task 2–4 結果，產出修正對照表（Reference #、欄位、現有值、正確值、來源），涵蓋：#10/#11 補 DOI、#14/#16/#22/#23 修正作者、#15 處置決定、其他驗證中發現的錯誤
- [x] 5.2 確認修正清單中所有 author fields contain actual author names，不含期刊名或出版社名

## 6. 修正 reference.md

- [x] 6.1 修正 #10：加入 DOI link `[DOI](https://doi.org/10.1016/j.edurev.2017.09.003)`
- [x] 6.2 修正 #11：加入 DOI link `[DOI](https://doi.org/10.1007/s10956-015-9581-5)`
- [x] 6.3 修正 #14：將 "International Journal of STEM Education (2023)" 替換為正確作者與完整引用格式，確保 reference page lists all academic sources 的每筆條目包含正確作者
- [x] 6.4 修正 #16：將 "Digital Experiences in Mathematics Education (2024)" 替換為正確作者與完整引用格式
- [x] 6.5 修正 #22：將 "Springer (2024)" 替換為正確作者與完整引用格式
- [x] 6.6 修正 #23：將 "ERIC (2024)" 替換為正確作者與完整引用格式
- [x] 6.7 處理 #15：若判定為幻覺則移除該條目並調整後續編號；若找到正確資訊則替換為驗證後的版本
- [x] 6.8 修正驗證過程中發現的其他錯誤（年份、篇名、卷期頁碼、壞連結）
- [x] 6.9 執行 `pnpm dev` 確認 VitePress 建置成功，reference page renders in sidebar，local PDF links resolve correctly

## 7. 更新 spec

- [x] 7.1 更新 `openspec/specs/ch1-research-references/spec.md`，新增「all references are verified against authoritative sources」需求，包含學術論文正確作者/年份/篇名/DOI、外部 URL 可存取、無法驗證的文獻已處理

## 8. 安全稽核後修正

- [x] 8.1 修復 Critical：移除 `_verify_academic()` 中 `fetch_paper_by_doi()` 外層的 `async with semaphore:` 以避免 semaphore 雙重取得死鎖
- [x] 8.2 修復 High：`_verify_policy()` 改為檢查 URL 狀態碼，URL 不可達時回傳 `unverifiable` 而非無條件 `verified`
- [x] 8.3 修復 Medium：`check_url()` 新增 URL scheme 驗證，僅允許 `http://` 和 `https://` 以防止 SSRF
- [x] 8.4 修復 Medium：將 `search_s2_by_title()` 和 `check_url()` 中的 `except Exception` 改為具體異常類型（`httpx.HTTPError`、`KeyError`、`ValueError`）並加入 logging
- [x] 8.5 修復 Medium：`_check_corrections()` 當 `_authors_list` 不存在但作者欄位為已知期刊名時，標記需手動驗證
- [x] 8.6 修正 #15 作者變音符號：Martín-Antón, Carbonero-Martín（加入西班牙語重音符號）
- [x] 8.7 修正 #22 作者變音符號：Celedón-Pattichis, LópezLeiva（加入西班牙語重音符號）
- [x] 8.8 全部修正後重新執行 pytest（11/11 通過）與 VitePress build（成功）
