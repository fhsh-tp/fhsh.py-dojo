---
name: challenge-author
description: "引導在 fhsh.py-dojo 新增一道 Python 自學道場題目：scaffold、frontmatter 契約、generator/reference_solution、題型與驗證。"
license: MIT
metadata:
  author: fhsh-py-dojo
  version: "1.0"
---

# challenge-author

在 fhsh.py-dojo 新增一道題目的端到端引導。正本欄位規格見 `Usage.md`，本 skill 為可操作的流程摘要。

## 何時使用

- 使用者要「新增一道題目」「出一題」「加練習題」。
- 需要確認題目 frontmatter 契約、generator 寫法或驗證方式時。

## 流程

### 1. 用 scaffold 建立骨架（勿手動建檔）

```bash
pnpm new-challenge <name> --title "題目名稱" --difficulty easy|medium|hard --category python|apcs --type basic|competition
```

- `<name>`：小寫 kebab-case（例 `bubble-sort`）；`algorithm` 預設為底線版（`bubble_sort`），檔案建於 `docs/challenge/<name>.md`。`<name>` **不可是 id 形狀**（如 `py001`、`apcs003`）——scaffold 會直接拒絕，因為 id 形狀的 slug 會讓 `/challenge/<slug>` 頁面與 `/c/<id>` 短網址別名指向混淆的目錄身分。
- 腳本會**自動分配唯一 `id`**。`id` 為字串，格式為 `<category 前綴><3 位零填充序號>`（例 `py001`、`apcs005`），各 category 自 1 起連號；腳本取該 category 前綴內現有最大序號 +1 配號。手動建檔容易造成 `id` 衝突，故一律用腳本（與 `CONTRIBUTE.md` Phase 2 SOP 一致）。
- `--category` 決定 id 前綴與題目歸屬頁：省略時預設 `python`（前綴 `py`、上架於 `/challenges`）；**出 APCS 題務必加 `--category apcs`**（前綴 `apcs`、上架於 `/apcs-challenges`），事後改 category 需同步手改 id 前綴，成本高。
- `--type` 省略時預設 `basic`。目前只接受 `basic`（基礎）與 `competition`（競賽）；`fill_in_blank` / `gamified` 為 deferred、`guided` 為 future placeholder，尚未實作，指定會被拒絕。

### 2. 編輯 frontmatter 核心欄位

必填：`layout: challenge`、`id`、`title`、`difficulty`、`algorithm`、`params`、`generator`、`starter_code`。
選填（完整清單）：`type`（題型，預設 basic）、`category`（步驟 1 的 `--category` 已寫入，勿手改）、`testcase_count`（預設 5）、`testcase_plan`（測資分區，與 `testcase_count` 互斥）、`input_budget`（單筆測資位元組預算，預設 4096）、`tags`、`reference_solution`、`editor_capture_debounce_ms`。

- `params`：定義每個輸入參數的型別與範圍，順序即 stdin 行順序。型別共 **8 種**：`int` / `alpha_upper` / `alpha_lower` / `alpha_mixed` / `hex_string` / `printable_ascii` / `enum`（固定清單挑一值）/ `group`（巢狀區塊重複 K 次，競賽式多筆測資的核心）。各型別的欄位與約束見 `Usage.md`〈params 參數型別 → 型別一覽〉。
- `generator`：一段 Python 程式，讀入參數（`input()`）並 `print` 出**正確答案**。此即判題的期望輸出。

### 3. （建議）加上 reference_solution

`reference_solution` 為選填欄位：宣告一段**獨立於 generator** 的正確 Python 解法。宣告後，`scripts/content-regression.test.ts` 會驗證「此正解在正式加密池下與 generator 的期望輸出一致」（等同正解對正式池得 Accepted）。建議與 generator 用不同寫法，才能同時抓出 generator 與正解各自的錯誤。

### 4. 撰寫題目說明

frontmatter 之後的 Markdown 內文顯示於題目說明面板，建議含：演算法說明、輸入說明、輸出說明、範例（輸入/輸出）。

### 5. 依題型調整樣板

- `basic`（基礎）：單一演算法練習，說明著重「怎麼做」，範例以最小可理解案例為主。
- `competition`（競賽）：著重「限制與邊界」，說明應含明確的輸入範圍、時間/空間隱含限制與多組邊界範例；`difficulty` 通常 medium/hard。競賽題常需兩個進階機制——「第一行 T 筆、逐筆多行」的輸入結構用 `group` 型別（讀 `Usage.md`〈group 群組 — 競賽式多筆測資〉）；「前幾筆值域小、後幾筆值域大」的 APCS 式配分用 `testcase_plan`（讀 `Usage.md`〈testcase_plan — 測資分區〉，含與 `input_budget`／seed 的互動）。每筆測資要在同一行塞多個值時，用參數的 `count`／`separator`（讀 `Usage.md`〈count — 產生多個值〉）。三節皆附可直接改用的完整 YAML 範例。

### 6. 驗證

```bash
pnpm build:pools                       # 重新編譯加密測資池
pnpm dev                               # 於瀏覽器確認題目與測資，親自跑一次確認 Accepted
node_modules/.bin/vitest --run scripts/content-regression.test.ts   # 若有 reference_solution
```

## 陷阱

- **params 宣告守門**：測資輸入產生邏輯只有一份（Rust crate `testcase-generator`，建置期與瀏覽器共用同一份 WASM）。所有題目的 params 由 `scripts/challenge-params.test.ts` 冒煙測試守門——宣告了引擎不認識的型別或欄位（例如 `type: str`、拼錯的 `min_lenght`）會在測試與建置期指名該題失敗，不會靜默產出壞測資。新增輸入格式能力時只需改 Rust 端並跑 `cargo test`。
- 勿 commit gitignored 產物（`docs/public/pools/`、`testcase-generator/src/key_material.rs`、`.env.pool`、`.understand-anything/`）。

## 參照

- `Usage.md` — frontmatter 完整欄位規格（正本）
- `CONTRIBUTE.md` — 新增題目 SOP
- `scripts/new-challenge.ts` — scaffold 實作
