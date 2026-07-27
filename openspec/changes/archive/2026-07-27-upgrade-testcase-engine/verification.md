# upgrade-testcase-engine — 驗證紀錄

## A. 部署驗證清單(人工項,staging 部署時逐項勾記)

- [ ] **Cloudflare Pages build command 更新**:dashboard → 專案設定 → Build
  command,改為與 `package.json` 的 `build` 一致的三段順序:
  `pnpm gen:keymaterial && pnpm build:wasm && pnpm build:pools && pnpm build:pyodide && pnpm docs:build`
  (或直接 `pnpm build`)。**預期觀察**:build log 中 wasm-pack 完成於
  generate-pools 之前;無 "WASM artifact not found" 錯誤。
- [ ] **CF Node 版本 ≥ 22**:dashboard 環境變數 `NODE_VERSION`(或
  `.node-version`)確認 ≥ 22。**預期觀察**:build log 開頭的 Node 版本;
  `package.json` 的 `engines.node >= 22` 若不符會在 install 期警告。
- [ ] **staging 部署綠燈**:push 後 CF build 全綠,站台可開、任一題可判題。
- [ ] **池檔大小抽查**:`docs/public/pools/*.bin` 全部遠小於 25 MiB
  (CF Pages 單檔上限)。**預期觀察**:本機建置全部池檔 < 100 KB
  (2026-07-27 本機實測最大約 11 KB)。

## B. Implementation Contract 觀察點(design.md,7.1 執行紀錄,2026-07-27)

- [x] **觀察點 1 — 決定性**:`pnpm build:pools` 55 題全綠;全題 200 筆輸入
  跨兩個獨立行程 SHA-256 完全一致
  (`b8beefa8e78c4e56bc5e3c7619907173bcd563e311cc820890633ab35fa67190`),
  且 clippy 重構前後雜湊不變(重構零行為變化)。
- [x] **觀察點 2 — deque 式規格**:`generate_pool_inputs` 對
  `t → group[n, nums(count.from=n, separator="\n")]` 產出正確巢狀格式,
  n 抽值與行數逐筆一致(`param_conformance.rs::group_competition_shape_conforms`
  200 seeds + Node smoke 實測)。
- [x] **觀察點 3 — 可讀錯誤取代 trap**:`min>max` 經 WASM 回傳
  `Error: param 'p': min (9) must be <= max (1)`(先前為
  `RuntimeError: unreachable`);後續呼叫正常;`testcase_plan` 保留鍵回報
  reserved 錯誤。D5 矩陣每列違規皆有 parser 單元測試以 `Err` 收場。
- [x] **觀察點 4 — 全綠與零改動**:`cargo test` 105+15 綠、clippy -D warnings
  綠、`pnpm build` 端到端(三段順序)exit 0、`pnpm test --run` 448 綠/51 skip、
  `pnpm typecheck` 綠、`pnpm lint` 綠;`docs/challenge/` 55 題 frontmatter
  於本 change 內零改動。
- [x] **觀察點 5 — 守門交接**:`scripts/generator-parity.test.ts` 已刪除;
  `scripts/challenge-params.test.ts` 57 測試綠,注入 `type: str` 時正確指名
  該檔失敗(負向驗收已測)。
