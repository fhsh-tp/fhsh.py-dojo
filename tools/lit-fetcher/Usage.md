# Usage Guide — lit-fetcher

本文件是 lit-fetcher 的完整使用指南。涵蓋所有子命令的參數說明、典型工作流程、以及疑難排解。

---

## 目錄

1. [安裝與設定](#1-安裝與設定)
2. [子命令總覽](#2-子命令總覽)
3. [search — 搜尋核准 venue 論文](#3-search--搜尋核准-venue-論文)
4. [verify — 驗證現有文獻合規性](#4-verify--驗證現有文獻合規性)
5. [download — 下載論文 PDF](#5-download--下載論文-pdf)
6. [典型工作流程](#6-典型工作流程)
7. [Venue 比對機制](#7-venue-比對機制)
8. [FJU EZProxy 設定](#8-fju-ezproxy-設定)
9. [Semantic Scholar API Key](#9-semantic-scholar-api-key)
10. [輸出目錄與檔案格式](#10-輸出目錄與檔案格式)
11. [疑難排解](#11-疑難排解)
12. [作為 Python 模組使用](#12-作為-python-模組使用)
13. [新增自訂 venue](#13-新增自訂-venue)

---

## 1. 安裝與設定

### 前置需求

```bash
# 確認 uv 已安裝
uv --version   # 需要 >= 0.6

# 確認 Python >= 3.12
python3 --version
```

### 安裝步驟

```bash
# 從專案根目錄出發
cd term-project/tools/lit-fetcher

# 安裝依賴（uv 自動建立 .venv）
uv sync

# 驗證 CLI 可用
uv run lit-fetcher --help
```

預期輸出：

```
usage: lit-fetcher [-h] {search,verify,download} ...

Literature Fetcher for SkillSleep

positional arguments:
  {search,verify,download}
    search              Search for papers in approved venues
    verify              Verify existing refs against venue list
    download            Download PDFs for papers

options:
  -h, --help            show this help message and exit
```

### 環境變數設定

```bash
cp .env.example .env
```

編輯 `.env`：

```env
# 【選填】輔大 EZProxy（僅 download --use-proxy 需要）
FJU_PROXY_USER=你的學號
FJU_PROXY_PASS=你的密碼
FJU_PROXY_URL=https://ezproxy.lib.fju.edu.tw/login

# 【選填】輸出目錄（預設：../../refs，即 term-project/refs/）
OUTPUT_DIR=../../refs

# 【選填】Semantic Scholar API Key（有 key 速度快 10 倍）
# 申請：https://www.semanticscholar.org/product/api#api-key
SEMANTIC_SCHOLAR_API_KEY=

# 【選填】搜尋年份範圍
SEARCH_YEAR_MIN=2024
SEARCH_YEAR_MAX=2026
```

**沒有 .env 也能運作**——所有變數都有預設值。沒有 API key 只是速度較慢（rate limit）。

---

## 2. 子命令總覽

| 子命令 | 用途 | 需要網路 | 需要 .env |
|--------|------|---------|-----------|
| `search` | 搜尋核准 venue 上的論文 | 是 | 選填（API key） |
| `verify` | 驗證 refs/ 中論文的 venue 合規性 | 是 | 選填（API key） |
| `download` | 下載論文 PDF | 是 | 選填（proxy 帳密） |

---

## 3. search — 搜尋核准 venue 論文

### 基本用法

```bash
# 使用預設 10 組搜尋關鍵字
uv run lit-fetcher search
```

預設搜尋關鍵字：

1. `"skill internalization LLM reinforcement learning"`
2. `"continual learning large language model LoRA"`
3. `"knowledge distillation LLM agent"`
4. `"on-device edge LLM fine-tuning training"`
5. `"parameter efficient fine-tuning catastrophic forgetting LLM"`
6. `"RAG retrieval augmented vs fine-tuning LLM"`
7. `"curriculum learning reinforcement learning LLM agent"`
8. `"self-distillation continual learning language model"`
9. `"on-device personalization language model"`
10. `"LoRA adapter merging continual learning"`

### 參數

| 參數 | 說明 | 範例 |
|------|------|------|
| `--queries` | 自訂搜尋關鍵字（取代預設） | `--queries "LoRA continual" "skill LLM"` |
| `--save` | 將結果儲存為 abstract.md 到 refs/ | `--save` |
| `--output` | 指定輸出目錄（取代 OUTPUT_DIR） | `--output /tmp/papers` |

### 範例

```bash
# 自訂搜尋關鍵字
uv run lit-fetcher search --queries "self-distillation LLM" "edge training LoRA"

# 搜尋並儲存
uv run lit-fetcher search --save

# 搜尋並儲存到指定目錄
uv run lit-fetcher search --save --output /path/to/my/refs
```

### 輸出說明

搜尋完成後會顯示一個表格：

```
                     Papers in Approved Venues
┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━┓
┃ Title                   ┃ Year ┃ Venue          ┃ OA ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━┩
│ TreeLoRA: Efficient...  │ 2025 │ ICML           │ ✓  │
│ SD-LoRA: Scalable...    │ 2025 │ ICLR           │ ✓  │
│ ...                     │      │                │    │
└─────────────────────────┴──────┴────────────────┴────┘
```

- **OA ✓**：open access，可用 `download` 命令直接下載 PDF
- **OA ✗**：付費論文，需要 `download --use-proxy` 透過輔大 proxy 下載

### 運作原理

1. 對每組關鍵字呼叫 Semantic Scholar API（`/paper/search`）
2. 取得每篇論文的 venue 資訊
3. 使用 venue_matcher 比對核准名單
4. 僅回傳 venue 符合的論文
5. `--save` 時呼叫 saver 建立 abstract.md

---

## 4. verify — 驗證現有文獻合規性

### 基本用法

```bash
# 驗證預設 refs/ 目錄
uv run lit-fetcher verify

# 驗證指定目錄
uv run lit-fetcher verify --refs-dir /path/to/refs
```

### 參數

| 參數 | 說明 | 範例 |
|------|------|------|
| `--refs-dir` | 指定 refs 目錄（取代 OUTPUT_DIR） | `--refs-dir ../../refs` |

### 輸出說明

```
                         Venue Compliance Check
┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ Paper              ┃ Venue                ┃ Status         ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ arXiv-2305.17333   │ NeurIPS              │ ✓ Approved     │
│ arXiv-2510.13537   │ arXiv.org            │ ✗ Not approved │
│ arXiv-2604.02268v1 │ N/A                  │ ✗ Not approved │
└────────────────────┴──────────────────────┴────────────────┘
```

- **✓ Approved**：論文已確認發表在核准 venue
- **✗ Not approved**：論文僅為 arXiv preprint 或發表在非核准 venue
- **Not found on S2**：Semantic Scholar 上找不到此論文（可能太新）

### 運作原理

1. 掃描 refs/ 目錄中的所有子目錄
2. 從目錄名稱擷取 arXiv ID（例如 `arXiv-2305.17333`）
3. 透過 Semantic Scholar API 查詢論文的正式發表 venue
4. 使用 venue_matcher 比對核准名單
5. 顯示結果表格

### 注意事項

- 每次 API 請求間有 **3 秒延遲**（避免 429 rate limit）
- 15 篇論文的完整驗證約需 **45-60 秒**
- 若有 Semantic Scholar API key，可大幅加速

---

## 5. download — 下載論文 PDF

### 基本用法

```bash
# 下載所有 arXiv 論文的 PDF（open access）
uv run lit-fetcher download

# 強制重新下載已存在的 PDF
uv run lit-fetcher download --force

# 透過輔大 proxy 下載付費論文（需設定 .env）
uv run lit-fetcher download --use-proxy
```

### 參數

| 參數 | 說明 | 範例 |
|------|------|------|
| `--refs-dir` | 指定 refs 目錄 | `--refs-dir ../../refs` |
| `--force` | 重新下載已存在的 PDF | `--force` |
| `--use-proxy` | 啟用 FJU EZProxy 下載付費論文 | `--use-proxy` |

### 下載邏輯

| 目錄名稱格式 | 下載方式 | 條件 |
|-------------|---------|------|
| `arXiv-XXXX.XXXXX` | 直接從 `arxiv.org/pdf/` 下載 | 無條件 |
| `doi-10.XXXX_XXXX` | 透過 FJU EZProxy 下載 | 需 `--use-proxy` + `.env` 設定 |
| 其他 | 跳過 | — |

### 輸出

PDF 儲存位置：`refs/<paper-id>/paper.pdf`

```
  Downloading 2305.14314...
    ✓ refs/arXiv-2305.14314/paper.pdf
  Downloading 2604.02268...
    ✓ refs/arXiv-2604.02268v1/paper.pdf

Downloaded: 15, Failed: 0
```

---

## 6. 典型工作流程

### 工作流程 A：初次建立文獻庫

```bash
cd term-project/tools/lit-fetcher

# Step 1: 設定環境
cp .env.example .env
# 編輯 .env（至少設定 OUTPUT_DIR）

# Step 2: 搜尋核准 venue 的論文並儲存
uv run lit-fetcher search --save

# Step 3: 下載所有 PDF
uv run lit-fetcher download

# Step 4: 驗證合規性
uv run lit-fetcher verify
```

### 工作流程 B：驗證已有文獻

```bash
cd term-project/tools/lit-fetcher

# 驗證現有 refs/ 的 venue 合規性
uv run lit-fetcher verify --refs-dir ../../refs
```

### 工作流程 C：補充特定主題的論文

```bash
cd term-project/tools/lit-fetcher

# 用自訂關鍵字搜尋
uv run lit-fetcher search \
  --queries "idle time training neural network" "sleep consolidation LLM" \
  --save

# 下載新增論文的 PDF
uv run lit-fetcher download
```

### 工作流程 D：下載付費論文（需輔大帳號）

```bash
cd term-project/tools/lit-fetcher

# 確認 .env 已設定 FJU_PROXY_USER 和 FJU_PROXY_PASS
cat .env | grep FJU

# 下載付費論文
uv run lit-fetcher download --use-proxy
```

---

## 7. Venue 比對機制

`venue_matcher.py` 使用四層比對策略（依優先順序）：

### Pass 1：精確比對

```
輸入 "Neural Networks" → 精確匹配期刊 "Neural Networks" ✓
輸入 "ICML" → 精確匹配會議 "ICML" ✓
```

### Pass 2：縮寫精確比對

```
輸入 "tpami" → 展開為 "ieee transactions on pattern analysis..." → 匹配 ✓
輸入 "jmlr" → 展開為 "journal of machine learning research" → 匹配 ✓
```

支援的縮寫：

| 縮寫 | 展開 |
|------|------|
| `neurips` / `nips` | Neural Information Processing Systems |
| `icml` | International Conference on Machine Learning |
| `iclr` | International Conference on Learning Representations |
| `aaai` | Association for the Advancement of Artificial Intelligence |
| `ijcai` | International Joint Conference on Artificial Intelligence |
| `cvpr` | Computer Vision and Pattern Recognition |
| `iccv` | International Conference on Computer Vision |
| `ijcnn` | International Joint Conference on Neural Networks |
| `tpami` | IEEE Transactions on Pattern Analysis and Machine Intelligence |
| `tnnls` | IEEE Transactions on Neural Networks and Learning Systems |
| `jmlr` | Journal of Machine Learning Research |
| `tacl` | Transactions of the Association for Computational Linguistics |
| `tist` | ACM Transactions on Intelligent Systems and Technology |

### Pass 3：子字串比對（最短距離優先）

```
輸入 "Neural Information Processing Systems Conference" → 子字串匹配 "NeurIPS" ✓
輸入 "ICML 2025" → 子字串匹配 "ICML" ✓
```

當多個 venue 被子字串匹配時，選擇**長度最接近**的（避免 "Neural Networks" 誤匹配 "IJCNN"）。

### Pass 4：縮寫子字串比對

```
輸入 "Published at NeurIPS Workshop" → 分詞後找到 "neurips" → 匹配 ✓
```

---

## 8. FJU EZProxy 設定

### 設定方式

在 `.env` 中設定：

```env
FJU_PROXY_USER=410XXXXXXX        # 你的輔大學號
FJU_PROXY_PASS=your_password      # 你的密碼
FJU_PROXY_URL=https://ezproxy.lib.fju.edu.tw/login
```

### 運作原理

1. 使用帳號密碼向 FJU EZProxy 進行 POST 認證
2. 取得認證後的 session cookies
3. 將 DOI URL 改寫為 EZProxy 代理的 URL 格式（`doi-org.ezproxy.lib.fju.edu.tw`）
4. 透過代理存取出版商頁面
5. 從 HTML 中擷取 PDF 下載連結（支援 Elsevier、IEEE、Springer 等常見出版商的 pattern）
6. 下載 PDF

### 限制

- 僅支援有 DOI 的論文（目錄名稱格式：`doi-10.XXXX_XXXX`）
- 出版商 PDF 連結擷取為 heuristic-based，可能不支援所有出版商
- 需要輔大的 VPN 或校內網路存取權限（EZProxy 可能需要校內 IP）
- 若 EZProxy 登入頁面格式變更，可能需要更新 `downloader.py` 的表單欄位

### 測試連線

```bash
# 測試 proxy 認證（手動）
curl -v -d "user=YOUR_ID&pass=YOUR_PASS" https://ezproxy.lib.fju.edu.tw/login
```

---

## 9. Semantic Scholar API Key

### 為什麼需要

無 API key 的 rate limit 為 ~1 req/sec（100 req/5min）。有 key 後提升到 10 req/sec。

### 申請方式

1. 前往 https://www.semanticscholar.org/product/api#api-key
2. 填寫申請表（通常即時核發）
3. 將 key 填入 `.env`：

```env
SEMANTIC_SCHOLAR_API_KEY=your_api_key_here
```

### 無 key 的替代方案

工具會自動處理 429 rate limit：
- 內建 exponential backoff retry（最多 3 次，等待 2s / 4s / 8s）
- verify 命令每次請求間有 3 秒延遲
- search 命令每次查詢間有 1 秒延遲

無 key 仍可正常使用，只是較慢。

---

## 10. 輸出目錄與檔案格式

### 目錄結構

預設輸出到 `term-project/refs/`（由 `OUTPUT_DIR` 環境變數控制）。

```
refs/
├── arXiv-2604.02268v1/
│   ├── abstract.md         # 論文 metadata（標題、作者、摘要、venue、合規狀態）
│   ├── paper.pdf           # PDF 全文（download 命令產生）
│   └── main.tex            # 若手動放入的原始 LaTeX 檔案
├── arXiv-2601.19897/
│   ├── abstract.md
│   └── paper.pdf
├── doi-10.1109_TPAMI.2024.3367329/
│   ├── abstract.md
│   └── paper.pdf
└── ...
```

### 目錄命名規則

| 條件 | 命名格式 | 範例 |
|------|---------|------|
| 有 arXiv ID | `arXiv-{id}` | `arXiv-2604.02268` |
| 無 arXiv ID，有 DOI | `doi-{doi}` | `doi-10.1109_TPAMI.2024.3367329` |
| 都沒有 | `paper-{title_slug}` | `paper-TreeLoRA-Efficient-Continual-Learning` |

DOI 中的 `/` 會被替換為 `_`。

### abstract.md 欄位說明

| 欄位 | 說明 | 值範例 |
|------|------|--------|
| `Authors` | 前 10 位作者，超過 10 位加 "et al." | `Yu-Yang Qian, Yuan-Ze Xu et al.` |
| `Year` | 發表年份 | `2025` |
| `Venue` | Semantic Scholar 回傳的 venue 名稱 | `International Conference on Machine Learning` |
| `arXiv` | arXiv ID（若有） | `2501.12345` |
| `DOI` | Digital Object Identifier（若有） | `10.1234/example` |
| `Open Access` | 是否為 open access | `Yes` / `No` |
| `PDF URL` | PDF 直接下載連結 | `https://arxiv.org/pdf/2501.12345` |
| `Approved Venue` | 匹配到的核准 venue 名稱 | `ICML` / `Not checked` |
| `Venue Type` | venue 分類 | `conference` / `q1_journal` / `Not checked` |

---

## 11. 疑難排解

### 問題：429 Too Many Requests

```
Error: Client error '429' for url 'https://api.semanticscholar.org/...'
```

**原因**：Semantic Scholar API rate limit。

**解決方式**：
1. 等待 5 分鐘後重試
2. 設定 `SEMANTIC_SCHOLAR_API_KEY` 提升 rate limit
3. 工具會自動 retry（最多 3 次），通常第 2 次就成功

### 問題：Module not found

```
ModuleNotFoundError: No module named 'lit_fetcher'
```

**解決方式**：

```bash
cd term-project/tools/lit-fetcher
uv sync
uv pip install -e .
```

### 問題：Venue 比對結果不正確

例如 "Neural Networks" 匹配到 IJCNN 而不是期刊。

**解決方式**：這個 bug 已修復（v0.1.0+）。如果仍有問題，檢查 `venue_matcher.py` 的 Pass 1 精確比對是否包含該 venue。

### 問題：PDF 下載失敗

```
  Downloading 2604.02268...
    ✗ Failed
```

**可能原因**：
1. 論文太新，arXiv 尚未處理 PDF
2. 網路連線問題
3. arXiv 暫時性服務中斷

**解決方式**：
1. 稍後重試：`uv run lit-fetcher download --force`
2. 手動下載：`curl -o paper.pdf https://arxiv.org/pdf/2604.02268`

### 問題：FJU Proxy 下載失敗

```
  Downloading via proxy: 10.1109/TPAMI.2024.3367329...
    ✗ Proxy download failed
```

**可能原因**：
1. `.env` 中帳號密碼錯誤
2. 不在輔大網路環境（EZProxy 可能需要校內 IP 或 VPN）
3. 出版商 PDF 連結格式未被支援
4. EZProxy 登入頁面格式已變更

**解決方式**：
1. 確認帳密正確
2. 連接輔大 VPN 後重試
3. 手動透過瀏覽器登入 EZProxy 下載

---

## 12. 作為 Python 模組使用

除了 CLI，你也可以在 Python 腳本或 Claude Code agent 中直接使用：

### 搜尋論文

```python
import asyncio
from lit_fetcher.apis import search_semantic_scholar
from lit_fetcher.venue_matcher import is_approved_venue

async def find_papers():
    papers = await search_semantic_scholar("continual learning LoRA LLM", limit=20)
    for p in papers:
        venue = p.get("venue", "")
        approved, matched = is_approved_venue(venue)
        if approved:
            print(f"✓ {p['title']} — {matched}")

asyncio.run(find_papers())
```

### 驗證單篇論文

```python
import asyncio
from lit_fetcher.apis import get_paper_by_arxiv_id
from lit_fetcher.venue_matcher import is_approved_venue

async def check_paper():
    paper = await get_paper_by_arxiv_id("2305.17333")
    venue = paper.get("publicationVenue", {}).get("name", "")
    approved, matched = is_approved_venue(venue)
    print(f"Venue: {venue}, Approved: {approved}, Matched: {matched}")

asyncio.run(check_paper())
```

### 下載 PDF

```python
import asyncio
from pathlib import Path
from lit_fetcher.downloader import download_arxiv_pdf

async def get_pdf():
    ok = await download_arxiv_pdf("2305.17333", Path("./paper.pdf"))
    print(f"Downloaded: {ok}")

asyncio.run(get_pdf())
```

### Venue 比對

```python
from lit_fetcher.venue_matcher import is_approved_venue, classify_venue

# 檢查是否為核准 venue
approved, name = is_approved_venue("NeurIPS")         # (True, "NeurIPS")
approved, name = is_approved_venue("arXiv")            # (False, None)
approved, name = is_approved_venue("Neural Networks")  # (True, "Neural Networks")
approved, name = is_approved_venue("tpami")            # (True, "IEEE TPAMI")

# 分類 venue
classify_venue("ICML")              # "conference"
classify_venue("Neural Networks")   # "q1_journal"
classify_venue("arXiv")             # "other"
```

---

## 13. 新增自訂 venue

若教授指定的 venue 不在預設名單中，可在 `src/lit_fetcher/config.py` 中新增：

### 新增會議

```python
APPROVED_CONFERENCES = [
    "ICML", "NeurIPS", ...,
    "ACL",      # 新增
    "EMNLP",    # 新增
    "Association for Computational Linguistics",  # 全名
]
```

### 新增期刊

```python
APPROVED_Q1_JOURNALS = [
    "Nature Machine Intelligence", ...,
    "IEEE Access",  # 新增
]
```

### 新增縮寫（venue_matcher.py）

```python
_ABBREV_MAP = {
    ...,
    "acl": "association for computational linguistics",  # 新增
    "emnlp": "empirical methods in natural language processing",  # 新增
}
```

修改後需重新安裝：

```bash
uv pip install -e .
```
