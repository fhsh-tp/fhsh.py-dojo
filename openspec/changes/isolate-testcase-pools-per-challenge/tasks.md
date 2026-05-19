## 1. Build 腳本：以 slug 為池檔命名

- [x] 1.1 在 `scripts/generate-pools.ts` 的 `readChallenge()` 衍生並回傳 `slug`（檔名去 `.md`），讓「Build script generates encrypted testcase pools」需求中的「池鍵採用 challenge slug（檔名去 `.md`），不是數字 id 也不是 algorithm」決策落地。驗證：新增 vitest 單元測試對一個 mock challenge md 呼叫 `readChallenge()`，斷言回傳物件含正確 `slug`。
- [x] 1.2 在 `scripts/generate-pools.ts` 主迴圈把 `outPath` 寫成 `<slug>.bin`、把 `encryptPool()` 第二個參數改成 `slug`，並維持 frontmatter `algorithm` 欄位讀取（「保留 `algorithm` 欄位作為教學 metadata，不從 frontmatter 移除」）。驗證：在 fixture 目錄擺兩個共用 `algorithm: nested-loop` 的題目，跑 `npx tsx scripts/generate-pools.ts` 後 `docs/public/pools/` 出現兩個獨立 `<slug>.bin`，且解密後 payload `challenge_id === slug`（涵蓋 spec 場景「Pool file created per challenge slug」、「Pool payload challenge_id equals slug」）。

## 2. Build 腳本：slug 唯一性與過期池檔清理

- [x] 2.1 在 `scripts/generate-pools.ts` 開頭加 slug 蒐集與形狀驗證（`^[a-z0-9-]+$`、長度 1–64、無 `/` `\` `..`），實作「Build script validates slug uniqueness and shape」需求與「Build-time 重複 slug 偵測 + 過期池檔白名單清理」決策。驗證：vitest 提供包含違規 slug（空字串、含 `/`、超長）的 fixture，斷言 script 以非 0 結束且 stderr 列出違規檔路徑。
- [x] 2.2 在 `main()` 成功產池後實作 `docs/public/pools/*.bin` 白名單清理，跳過 `.gitkeep` 與子目錄；若該次 build 0 個成功池則略過清理（「Build script cleans up obsolete pool files」）。驗證：vitest 預置 `pools/nested-loop.bin` 與 `pools/.gitkeep`，跑完後斷言 `nested-loop.bin` 被刪、`.gitkeep` 保留；另一個測試讓所有 challenge 都失敗，斷言 `nested-loop.bin` 仍在。

## 3. Runtime：useChallengeRunner 以 slug 取池

- [x] 3.1 [P] 在 `useChallengeRunner.ts` 的 `RunnerConfig` 介面新增必填 `id: string` 欄位、`algorithm` 保留為 metadata，落實「useChallengeRunner composable provides unified challenge lifecycle API」需求與「Runtime 多打一個必填欄位 `id`，不嘗試從 `algorithm` 推導」決策。驗證：`pnpm typecheck` 通過；新增 vitest 對「忘記傳 `id` 的 caller」用 `@ts-expect-error` 斷言型別錯誤（涵蓋場景「Configuration without id fails at type-check」）。
- [x] 3.2 [P] 在 `useChallengeRunner.ts` 的 prod 分支將 `fetch('/pools/${algorithm}.bin')`、`wasm.load_pool(algorithm, ...)`、`wasm.select_testcases(algorithm, ...)`、`wasm.judge(algorithm, ...)` 全部替換為 `config.id`，達成「Prod strategy uses encrypted pool + WASM judge flow」需求中的 slug-only 行為。驗證：擴充 `useChallengeRunner-prod.spec.ts`，斷言 fetch URL 為 `/pools/<slug>.bin`、傳入 WASM 三個 API 的 key 皆為 slug、且 fetch 404 時不會 retry algorithm 路徑（涵蓋場景「Prod mode fetches encrypted pool by slug」、「Pool fetch failure surfaces without algorithm fallback」）。
- [x] 3.3 在 `.vitepress/theme/views/ChallengeView.vue` 將 challenge slug（來自 frontmatter 或 route）作為 `id` 傳給 `useChallengeRunner`。驗證：在 prod build 後開 `challenge/multiplication-table.html`，DevTools Network 面板觀察到 fetch `/pools/multiplication-table.bin`（非 `/pools/nested-loop.bin`），且執行對話框預填 stdin 僅 1 行。

## 4. WASM 模組契約更新（無 Rust 程式碼變動）

- [x] 4.1 確認「不修 WASM 端的 Rust 程式碼」決策——`testcase-generator/src/{lib,pool,judge,crypto}.rs` 維持不動，僅由 caller 傳入新 slug 字串完成「WASM module decrypts and loads encrypted pool」契約變更。驗證：跑 `cargo test --manifest-path testcase-generator/Cargo.toml` 無 diff 紅燈；review change 內 `git diff testcase-generator/` 為空。
- [x] 4.2 新增整合測試模擬「以 algorithm 字串呼叫 load_pool 但 payload 是 slug」場景，斷言 identity mismatch 被拒絕（涵蓋場景「Category-level identifier rejected for cross-challenge pool」與「Mismatched challenge_id rejected」更新後的範例）。驗證：在 `.vitepress/theme/__tests__/useChallengeRunner-prod.spec.ts` 加 case，斷言 `errorMessage` 含「池載入失敗」相關文字。

## 5. 池檔重新產出與部署驗證

- [x] 5.1 本機跑 `pnpm build:pools`，產出 54 個獨立 `<slug>.bin`、過期 algorithm-named `.bin` 已被清掉。驗證：`ls docs/public/pools/*.bin | wc -l` ≥ 54；不存在 `nested-loop.bin`、`for-loop.bin`、`while-loop.bin`、`brute-force.bin`、`trial-division.bin` 這些舊鍵檔。
- [x] 5.2 本機跑 `pnpm build && pnpm docs:preview`，逐題在 prod preview 提交 13 個受害題目的正確解答（inverted-triangle、isosceles-triangle、multiplication-table、nested-triangle、number-pyramid、pair-count、star-diamond、arithmetic-sum、even-countdown、number-staircase、digital-root、perfect-number、prime-check）。驗證：每題結果 5/5 AC；對照 5 個倖存題目（star-rectangle、star-square、guess-number-simple、perfect-numbers-range、smallest-prime-factor）仍 5/5 AC。
- [ ] 5.3 推上 staging branch 觸發 Cloudflare Pages build，部署完成後重新驗證 multiplication-table 與另 2 個隨機抽樣受害題目。驗證：staging 上執行對話框預填 stdin 行數 = 該題 params 個數；提交範例答案得 5/5 AC；Cloudflare Pages build log 顯示 `build:pools` 寫出 ≥ 54 個 `.bin`。
