## 1. 實作 CLI 腳本骨架

- [x] 1.1 建立 `scripts/new-challenge.ts`，設定 shebang (`#!/usr/bin/env npx tsx`) 與必要的 Node.js `import`（`fs`、`path`、`process`）
- [x] 1.2 實作 CLI 參數解析：讀取 `process.argv`，解析位置參數 `<name>` 與選項 `--title`、`--difficulty`、`--algorithm`

## 2. 輸入驗證

- [x] 2.1 實作 **CLI script scaffolds a new challenge file** 的錯誤處理：`<name>` 未提供時印出用法說明並以 code 1 離開
- [x] 2.2 實作 **Invalid name format** 驗證：用正則表達式檢查 `<name>` 只含小寫字母、數字、連字號，否則以 code 1 離開並印出規定訊息
- [x] 2.3 實作 **Invalid difficulty value** 驗證：確認 `--difficulty` 為 `easy`、`medium`、`hard` 之一，否則以 code 1 離開並印出規定訊息
- [x] 2.4 實作 **Output file already exists** 檢查：若 `docs/challenge/<name>.md` 已存在則以 code 1 離開並印出規定訊息

## 3. 自動計算 id

- [x] 3.1 實作 **CLI script scaffolds a new challenge file** 的 id 計算邏輯：讀取 `docs/challenge/` 目錄中所有 `.md` 檔案，用正則解析各檔案 frontmatter 中的 `id:` 欄位，取最大值 + 1；若目錄不存在或無任何檔案則預設為 `1`

## 4. 產生骨架檔案內容

- [x] 4.1 實作 **Generated skeleton is valid and parseable** 的 frontmatter 產生函式：以 template literal 組合完整 YAML frontmatter，包含 `layout`、`id`、`title`、`difficulty`、`tags`（空陣列）、`algorithm`、`testcase_count: 5`、`params`（預設一個 `n: {type: int, min: 1, max: 10}` 欄位）、`generator`（讀取 `n = int(input())` 並 `print(n)`）、`starter_code`（`def solve(): pass` 骨架加 `n = int(input())`）
- [x] 4.2 實作 Markdown 內文部分：在 frontmatter 後附加標準章節骨架（`## <title>`、`### 演算法說明`、`### 輸入說明`、`### 輸出說明`、`### 範例`，各含佔位文字）
- [x] 4.3 將組合好的完整檔案內容寫入 `docs/challenge/<name>.md`；若 `docs/challenge/` 目錄不存在則先用 `mkdirSync` 建立；寫入成功後印出 `[new-challenge] Created: docs/challenge/<name>.md`

## 5. 整合 package.json

- [x] [P] 5.1 在 `package.json` 的 `scripts` 區塊新增 **npm script entry runs the generator** 條目：`"new-challenge": "npx tsx scripts/new-challenge.ts"`
