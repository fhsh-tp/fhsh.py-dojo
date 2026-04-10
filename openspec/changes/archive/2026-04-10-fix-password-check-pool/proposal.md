## Problem

`pnpm dev` 在執行 `generate-pools` 時，`password-check.md` 的 pool 生成失敗，導致整個 build pipeline 中斷（exit code 1）。

錯誤訊息：
```
EOFError: EOF when reading a line
```

## Root Cause

兩個問題同時存在：

1. **動態輸入行數超出 params 定義**：`password-check.md` 的 generator 需要 `2 + max_attempts` 行輸入（password、max_attempts、再加上 K 行猜測），但 `generateInputs()` 只根據 `params` 生成 2 行（每個 param 一行）。當 generator 的 `for` 迴圈嘗試讀取第 3 行時，`StringIO` 已耗盡，觸發 `EOFError`。

2. **`type: str` 不是有效的 param type**：`generateInputs()` 的 `gen_value()` 函式不支援 `str` 型別（只支援 `int`、`alpha_upper`、`alpha_lower`、`alpha_mixed`、`hex_string`、`printable_ascii`、`enum`），導致 password 永遠生成為字面值 `"UNKNOWN_TYPE"`。

## Proposed Solution

將 `password-check.md` 的 generator 改寫為 **JSON factory 格式**。框架已在 `runGenerator()`（`scripts/generate-pools.ts` line 229-239）內建支援此格式。

Factory 格式的 generator 只讀取基礎 params（password、max_attempts），然後自行生成猜測行、組裝完整的 input 字串和 expected_output，以 JSON 物件輸出 `{"input": "...", "expected_output": "..."}`。

同時修正 `password` param 的 type 為 `printable_ascii`（含英數和符號，適合密碼場景）。

## Non-Goals

- 不修改 `scripts/generate-pools.ts` 的框架邏輯（現有 JSON factory 格式已足夠）
- 不修改其他 challenge 檔案

## Success Criteria

1. `pnpm dev` 的 `generate-pools` 階段全部 35 個 challenge 均成功（0 failed）
2. `password-check` 的 pool 檔案 `docs/public/pools/password_check.bin` 成功生成
3. 生成的 testcase 涵蓋兩種結果：猜對（OK）和猜錯（LOCKED）
4. 密碼字串使用真實的隨機可印刷 ASCII 字元，而非 `"UNKNOWN_TYPE"`

## Capabilities

### New Capabilities

- `password-check-pool-gen`: password-check challenge 的 pool 生成正確性，使用 JSON factory 格式處理動態行數輸入

### Modified Capabilities

（無。）

## Impact

- 受影響的檔案：`docs/challenge/password-check.md`
