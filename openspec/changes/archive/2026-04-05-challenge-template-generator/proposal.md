## Why

新增題目需要手動複製 `Usage.md` 中的完整 Markdown 範本，並逐欄位手動修改，容易出錯且費時。現有的 `scripts/` 目錄已有 TypeScript 建置腳本，但缺少互動式或參數化的題目骨架產生工具。

## What Changes

- 新增 `scripts/new-challenge.ts` 腳本，接受命令列參數（題目名稱、難度、演算法名稱）後自動產生 `docs/challenge/<name>.md` 骨架
- `package.json` 新增 `new-challenge` 指令，可直接執行 `pnpm new-challenge <name>`
- 自動計算下一個可用的 `id`（讀取 `docs/challenge/` 目錄中現有檔案的最大 id + 1）
- 產生的骨架包含完整 frontmatter 與 Markdown 內文結構（依 `Usage.md` 規格），填入對應的佔位符

## Non-Goals (optional)

- 不自動實作 `generator` 或 `starter_code` 邏輯，只產生佔位符
- 不互動式詢問每個 `params` 欄位（params 使用單一整數參數作為預設骨架，使用者自行修改）
- 不修改 WASM 測資產生器或加密池建置流程
- 不產生 factory mode 題目骨架（使用者自行依 `Usage.md` 調整）

## Capabilities

### New Capabilities

- `challenge-scaffold-script`: 命令列腳本，依指定參數產生符合規格的題目 Markdown 骨架

### Modified Capabilities

(none)

## Impact

- Affected specs: `challenge-scaffold-script`（新建）
- Affected code:
  - `scripts/new-challenge.ts`（新增）
  - `package.json`（新增 `new-challenge` script entry）
