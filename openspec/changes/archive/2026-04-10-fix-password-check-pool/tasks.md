## 1. 修正 password-check.md（password-check challenge generates valid test pools）

- [x] 1.1 將 `docs/challenge/password-check.md` 的 `password` param type 從 `str` 改為 `printable_ascii`，並將 `min_length`/`max_length` 改為 `min_len`/`max_len`（符合 `gen_value()` 的 key naming，確保 Password param uses valid generator type）
- [x] 1.2 將 `docs/challenge/password-check.md` 的 generator 改寫為 JSON factory 格式：讀取 password 和 max_attempts 兩個基礎 params 後，自行用 `random` 生成 K 行猜測（隨機決定在哪一輪猜對或全部猜錯），組裝完整的多行 input 字串和 expected_output，最終印出 `json.dumps({"input": ..., "expected_output": ...})`

## 2. 驗證

- [x] 2.1 驗證 password-check challenge generates valid test pools：執行 `pnpm build:pools` 確認全部 35 個 challenge 均成功（0 failed），且 `password_check.bin` 成功生成
