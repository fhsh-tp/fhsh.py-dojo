## Why

九九乘法表（multiplication-table）在 staging 上出現兩個怪象：（1）正確的程式碼被判 0/5 WA；（2）執行對話框預填了兩個數字（如 `3\n13`），但題目只需要一個整數 N。經根因分析，這是 `scripts/generate-pools.ts` 以 `algorithm` 為池檔名（line 334），加上 `useChallengeRunner.ts` 以 `algorithm` 為池抓取鍵（line 298, 307, 310, 343, 367），導致**8 個共用 `algorithm: nested-loop` 的題目互相覆寫測資池**，最終只有字母序最後的 `star-rectangle` 倖存。同一根因擴及 5 個 algorithm 群、影響 13 題；dev mode 因為走 WASM + Pyodide 即時生成完全不讀池檔，所以「pnpm dev 看起來正常」，但 prod／staging 必然失敗。

## What Changes

- **BREAKING**（檔案命名）：池檔名由 `<algorithm>.bin` 改為 `<slug>.bin`（`slug` = challenge markdown 檔名去掉 `.md`）。
- `scripts/generate-pools.ts`：
  - `readChallenge()` 回傳 `slug` 欄位（檔名去 `.md`）。
  - 主迴圈 `outPath` 由 `${algorithm}.bin` 改為 `${slug}.bin`。
  - `encryptPool()` 第二個參數（payload 內 `challenge_id`）由 `algorithm` 改為 `slug`。
  - 新增 build-time invariant：偵測重複 slug 即 throw（防止未來題目重新命名造成新型碰撞）。
  - 結尾清理 `docs/public/pools/` 中不對應任何當前 slug 的 `*.bin`（白名單刪除，跳過 `.gitkeep`）。
- `.vitepress/theme/composables/useChallengeRunner.ts`：
  - 所有 `config.algorithm` 作為池鍵的使用點（`fetch /pools/...`、`wasm.load_pool`、`wasm.select_testcases`、`wasm.judge`）改用 `config.id`（slug）。
  - `RunnerConfig` 介面新增必填 `id: string`；`algorithm` 保留為教學分類用 metadata。
- `.vitepress/theme/views/ChallengeView.vue`：將 frontmatter / route 的 slug 傳給 `useChallengeRunner` 的 `id` 欄位。
- 新增 `scripts/generate-pools.test.ts` 涵蓋：（a）多題共用 algorithm 時各自有獨立池檔；（b）重複 slug 會 throw；（c）`challenge_id` payload 等於 slug 而非 algorithm。
- 部署：本機 `pnpm build:pools` 重生 54 個獨立池檔，staging 觸發 Cloudflare Pages 重建。

## Non-Goals

- **不**修改 `testcase-generator/src/` Rust／WASM 內部結構：`load_pool(key, data)` 的 `key` 參數型別不變，只是傳入字串由 algorithm 改為 slug；`judge.rs` / `pool.rs` / `crypto.rs` 不動。
- **不**改 frontmatter 的 `algorithm` 欄位語意：仍作為教學分類（如 sidebar 分組、課程章節對應）使用。
- **不**改加密格式（MAGIC `CXPOOL`、VERSION 0x01、AES-256-GCM、`[nonce 12B][ct][tag 16B]`）。
- **不**做 fallback「找不到 `<slug>.bin` 時退回 `<algorithm>.bin`」——這正是要根除的 bug，回退等於沒修。
- **不**處理 staging 既存使用者得分紀錄：修正後使用者重新提交即可拿到正確分數。

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `encrypted-pool-generation`: 池檔命名規則由 `<algorithm>.bin` 改為 `<slug>.bin`；payload `challenge_id` 由 algorithm 改為 slug；新增重複 slug 偵測與過期池檔清理。
- `wasm-pool-judge`: `load_pool` 的 `challenge_id` 參數語意明確化為「per-challenge unique slug」，而非可能多題共用的 algorithm；既有「mismatched challenge_id rejected」場景的範例由 `caesar_encrypt` / `vigenere_encrypt` 對齊到 slug 概念（但不改加密格式）。
- `challenge-runner-orchestration`: `useChallengeRunner` 設定介面新增必填 `id`（slug），取代 `algorithm` 作為池鍵；`algorithm` 保留為教學 metadata。

## Impact

- Affected specs:
  - `openspec/specs/encrypted-pool-generation/spec.md`（修改 Requirement 與 Scenarios）
  - `openspec/specs/wasm-pool-judge/spec.md`（澄清 challenge_id 語意）
  - `openspec/specs/challenge-runner-orchestration/spec.md`（runner config 增 id 欄位）
- Affected code:
  - Modified:
    - `scripts/generate-pools.ts`
    - `.vitepress/theme/composables/useChallengeRunner.ts`
    - `.vitepress/theme/views/ChallengeView.vue`
  - New:
    - `scripts/generate-pools.test.ts`
  - Removed: (none)
- Affected runtime artifacts: `docs/public/pools/<algorithm>.bin` 全數作廢，改為 54 個 `docs/public/pools/<slug>.bin`（建置時自動產生，不入 git）。
- Affected challenges（必須在 staging 上重新測試）：
  - nested-loop 群（7 題受害）：inverted-triangle、isosceles-triangle、multiplication-table、nested-triangle、number-pyramid、pair-count、star-diamond
  - for-loop 群（3 題受害）：arithmetic-sum、even-countdown、number-staircase
  - while-loop 群（1 題受害）：digital-root
  - brute-force 群（1 題受害）：perfect-number
  - trial-division 群（1 題受害）：prime-check
  - 倖存者（回歸驗證不退化）：star-rectangle、star-square、guess-number-simple、perfect-numbers-range、smallest-prime-factor
