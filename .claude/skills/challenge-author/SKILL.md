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
pnpm new-challenge <name> --title "題目名稱" --difficulty easy|medium|hard --type basic|competition
```

- `<name>`：小寫 kebab-case（例 `bubble-sort`）；`algorithm` 預設為底線版（`bubble_sort`），檔案建於 `docs/challenge/<name>.md`。
- 腳本會**自動分配唯一 `id`**。`id` 為字串，格式為 `<category 前綴><3 位零填充序號>`（例 `py001`、`apcs005`），各 category 自 1 起連號；腳本取該 category 前綴內現有最大序號 +1 配號。手動建檔容易造成 `id` 衝突，故一律用腳本（與 `CONTRIBUTE.md` Phase 2 SOP 一致）。
- `--type` 省略時預設 `basic`。目前只接受 `basic`（基礎）與 `competition`（競賽）；`fill_in_blank` / `gamified` 為 deferred、`guided` 為 future placeholder，尚未實作，指定會被拒絕。

### 2. 編輯 frontmatter 核心欄位

必填：`layout: challenge`、`id`、`title`、`difficulty`、`algorithm`、`params`、`generator`、`starter_code`。
選填：`type`（題型，預設 basic）、`testcase_count`（預設 5）、`tags`、`reference_solution`。

- `params`：定義每個輸入參數的型別與範圍（`int` / `alpha_upper` / `alpha_lower` / `alpha_mixed` / `hex_string` / `printable_ascii`），順序即 stdin 行順序。
- `generator`：一段 Python 程式，讀入參數（`input()`）並 `print` 出**正確答案**。此即判題的期望輸出。

### 3. （建議）加上 reference_solution

`reference_solution` 為選填欄位：宣告一段**獨立於 generator** 的正確 Python 解法。宣告後，`scripts/content-regression.test.ts` 會驗證「此正解在正式加密池下與 generator 的期望輸出一致」（等同正解對正式池得 Accepted）。建議與 generator 用不同寫法，才能同時抓出 generator 與正解各自的錯誤。

### 4. 撰寫題目說明

frontmatter 之後的 Markdown 內文顯示於題目說明面板，建議含：演算法說明、輸入說明、輸出說明、範例（輸入/輸出）。

### 5. 依題型調整樣板

- `basic`（基礎）：單一演算法練習，說明著重「怎麼做」，範例以最小可理解案例為主。
- `competition`（競賽）：著重「限制與邊界」，說明應含明確的輸入範圍、時間/空間隱含限制與多組邊界範例；`difficulty` 通常 medium/hard。

### 6. 驗證

```bash
pnpm build:pools                       # 重新編譯加密測資池
pnpm dev                               # 於瀏覽器確認題目與測資，親自跑一次確認 Accepted
node_modules/.bin/vitest --run scripts/content-regression.test.ts   # 若有 reference_solution
```

## 陷阱

- **params 宣告守門**：測資輸入產生邏輯只有一份（Rust crate `testcase-generator`，建置期與瀏覽器共用同一份 WASM）。所有題目的 params 由 `scripts/challenge-params.test.ts` 冒煙測試守門——宣告了引擎不認識的型別或欄位（例如 `type: str`、拼錯的 `min_lenght`）會在測試與建置期指名該題失敗，不會靜默產出壞測資。新增輸入格式能力時只需改 Rust 端並跑 `cargo test`。
- 勿 commit gitignored 產物（`docs/public/pools/`、`testcase-generator/src/key_material.rs`、`.env.pool`）。

## 參照

- `Usage.md` — frontmatter 完整欄位規格（正本）
- `CONTRIBUTE.md` — 新增題目 SOP
- `scripts/new-challenge.ts` — scaffold 實作
