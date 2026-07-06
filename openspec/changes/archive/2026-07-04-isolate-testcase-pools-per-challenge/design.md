## Context

平台目前在 build 階段為每個 challenge 產出加密測資池，命名為 `<algorithm>.bin`；runtime 在 prod 模式以 `fetch(/pools/<algorithm>.bin)` 載入並交給 WASM 判定。`algorithm` 欄位是 challenge frontmatter 中描述「演算法分類」的字串（如 `nested-loop`、`for-loop`），原始用途是教學分組，並非全站唯一鍵。

實際上有 5 個 algorithm 群被多題共用（nested-loop 8 題、for-loop 4 題、while-loop 2 題、brute-force 2 題、trial-division 2 題），共 18 題擠在 5 個檔名。`generate-pools.ts` 主迴圈逐檔處理時，後者覆蓋前者，最終每個 algorithm 只剩字母序最後一題的測資。Runtime 端再以 `algorithm` 抓池，於是 13 題在 prod／staging 上載入到別題的測資──輸入行數、param 形狀、expected_output 全部錯位，永遠 WA。

Dev mode 走 WASM 隨機生成 + Pyodide 即時跑 generator，完全不讀池檔，因此「pnpm dev 正常」。`pnpm build:pools` 雖然會在 dev 啟動時執行並寫出錯誤的池，但 dev runner 從未讀取它。

既有 spec 中：
- `encrypted-pool-generation` Scenario「Pool file created for each challenge」明文寫 `named <algorithm>.bin`──spec 把 bug 制度化了。
- `wasm-pool-judge` 已有 `load_pool` 對 payload `challenge_id` 做 identity check，但 generate-pools 把 `challenge_id` 設成 algorithm，identity 校驗失效於「同 algorithm 多題」場景。
- `challenge-runner-orchestration` 設定介面目前只有 `algorithm`，沒有獨立的 challenge 唯一鍵。

## Goals / Non-Goals

**Goals:**

- 同一 algorithm 多題共用時，每題擁有獨立加密測資池，runtime 取池與判定皆以「per-challenge unique slug」為鍵。
- 加入 build-time invariant（重複 slug 即失敗），讓未來題目重新命名造成的碰撞無法靜默通過。
- 不破壞既有加密格式、WASM ABI、challenge frontmatter schema。
- 13 個受害題目在 staging 上能 5/5 AC；5 個倖存題目回歸驗證不退化。

**Non-Goals:**

- 不改 Rust／WASM 內部（`testcase-generator/src/` 樹）；WASM 端只是收到不同的字串鍵。
- 不移除 frontmatter 的 `algorithm` 欄位；仍是教學分類 metadata。
- 不變更加密格式（MAGIC `CXPOOL` / VERSION 0x01 / AES-256-GCM / `[nonce][ct][tag]`）。
- 不提供「找不到 `<slug>.bin` 時退回 `<algorithm>.bin`」的 fallback。
- 不修補 staging 上既存的 WA 失敗記錄；使用者重新提交即生效。

## Decisions

### 池鍵採用 challenge slug（檔名去 `.md`），不是數字 id 也不是 algorithm

**選 slug 的理由：**
- 跟 URL 路徑 `challenge/<slug>.html` 一致，使用者／開發者腦中模型對齊。
- 已是檔案系統強制唯一（同檔名無法共存），slug 唯一性「免費」獲得。
- 人類可讀，部署 log 直接看得懂 `multiplication-table.bin`。

**否決 numeric id：**
- 不可讀，部署 / debug 痛苦。
- 重新編號（如歷史 commit `35b3114` 即發生過）需要連動更名一堆 `.bin`，風險高。

**否決續用 algorithm：**
- 多題共用的本質沒解，只是包裝。

### 保留 `algorithm` 欄位作為教學 metadata，不從 frontmatter 移除

可能用於 sidebar 分組、課程章節對應、未來分析用，且移除是另一個議題、與本變更無關。`RunnerConfig.algorithm` 仍存在但**不再參與池抓取或判定**。

### Build-time 重複 slug 偵測 + 過期池檔白名單清理

- 偵測：`scripts/generate-pools.ts` 主迴圈開始前先建構 `Set<string>` 蒐集所有 slug，遇重複立即 throw（含兩個檔案的路徑訊息）。
- 清理：`main()` 結束時掃 `docs/public/pools/*.bin`，凡 basename 不在「當次成功產出的 slug 集合」中即刪除；只刪 `.bin`，跳過 `.gitkeep` 與目錄。

### Runtime 多打一個必填欄位 `id`，不嘗試從 `algorithm` 推導

`useChallengeRunner` 介面要硬性破壞性新增 `id: string`：
- 在編譯期就會抓到忘記傳的 caller（vue-tsc / tsc strict mode）。
- 沒有 fallback path，避免「忘記傳 → 靜默退回 algorithm → 又見 bug」。

### 不修 WASM 端的 Rust 程式碼

`load_pool(challenge_id, data)` 的 `challenge_id` 在 Rust 端只是一個 `&str` key。把 caller 傳入字串由 algorithm 換成 slug 即可，Rust 內部 hash map 索引仍正常運作。`pool.rs` 內 `PoolPayload.challenge_id` identity check 也自動受惠：因為 build 端 payload 已寫入 slug，runtime 端傳入 slug，identity 對齊。

## Implementation Contract

**Observable behavior（修正後）：**
- 在 prod／staging 開任一 challenge 頁，點「執行」對話框預填的 stdin 行數**等於該題 frontmatter `params` 欄位個數**（單參數題 1 行、雙參數題 2 行）。
- 對 13 個受害題目提交其 starter_code 範圍內的正確解答，結果為 5/5 AC（過去為 0/5 WA）。
- 對 5 個倖存題目重複測試，結果不退化（仍 AC）。

**Interface / data shape：**
- 池檔命名：`docs/public/pools/<slug>.bin`，`<slug>` 為 challenge markdown basename 去 `.md`，符合 `^[a-z0-9-]+$`。
- 加密 payload 內 `challenge_id` 字串欄位值 = `<slug>`（不再是 algorithm）。
- `useChallengeRunner` 設定物件介面：新增必填欄位 `id: string`（即 slug）；`algorithm: string` 維持必填但僅作 metadata。
- Build script CLI 行為：`pnpm build:pools` 在「兩個 challenge 檔名相同」（理論上不可能，但加防呆）或「slug 含 `/`、`..`、空字串、超過 64 字元」時 exit code 非 0、stderr 明示違規檔。

**Failure modes：**
- Runtime fetch `/pools/<slug>.bin` 失敗（404/網路錯）：沿用既有錯誤路徑 `errorMessage.value = '無法載入測資池 (${status})'`；**不**退回 algorithm。
- WASM `load_pool` identity mismatch（極端情境：池檔被人為改名）：沿用既有 error 訊息；challenge 頁顯示「測資池載入失敗」並阻止提交。
- Build script 偵測到重複 slug：throw error 含兩個衝突檔案路徑，build 失敗、CI 紅燈。

**Acceptance criteria：**
- 新增 `scripts/generate-pools.test.ts` 覆蓋：
  - (a) 給定兩個檔案 `foo.md` 與 `bar.md` 宣告同 algorithm，`build:pools` 後 `pools/foo.bin` 與 `pools/bar.bin` 都存在且檔大小 > 0。
  - (b) 給定兩個檔案在不同路徑但檔名（basename）相同（理論上不可能，但模擬手動誤建），build script 必 throw。
  - (c) 解密一個產出的池，其 payload `challenge_id` === slug，不等於 algorithm。
- `pnpm typecheck` 通過（`RunnerConfig` 新欄位若有忘記傳的 caller 會被抓到）。
- `pnpm test` 通過（含 a/b/c 三個新測試）。
- 在 staging 上 13 個受害題目逐題提交範例答案皆 5/5 AC。
- 在 staging 上「執行」對話框預填 stdin 行數 = 題目 params 數。

**Scope boundaries：**
- In scope: `scripts/generate-pools.ts`、`useChallengeRunner.ts`、`ChallengeView.vue`、新測試、三個 spec delta。
- Out of scope: Rust／WASM 內部（`testcase-generator/src/`）、加密格式、frontmatter schema、教學內容、UI 樣式、其他無關 challenge 的 spec。

## Risks / Trade-offs

- [既有 staging 部署殘留 by-algorithm 池檔] → 改動點清理邏輯刪除非 slug 命名的 `.bin`；同時 runtime 不會再去 fetch 它們，殘留也無害。
- [CDN／Cloudflare Pages 邊緣節點快取 `.bin`] → 確認 `_headers` 對 `*.bin` 沒設長 TTL；若有需要，加 cache-busting query string 或 purge cache。新檔名（`<slug>.bin`）與舊檔名（`<algorithm>.bin`）不衝突，至少不會拿到「快取過的舊 algorithm 池」。
- [Cloudflare Pages 部署目錄為 Linux，`readdirSync` 順序可能與本機 macOS 不同] → 修正後池檔以 slug 命名，與處理順序解耦，順序不再影響結果；本來只在「舊行為下倖存者可能不同」這層風險，現在自然消失。
- [破壞性 RunnerConfig 介面] → 只有 `ChallengeView.vue` 一處 caller，破壞範圍小；TypeScript 編譯期可抓。
- [新增單元測試需要實際跑 Python] → 已有 preflight check（line 22-58）；CI 環境若無 PyYAML，新測試會與既有 build 一起失敗，行為一致。
