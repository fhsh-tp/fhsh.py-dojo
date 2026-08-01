# upgrade-testcase-engine — 驗證紀錄

## A. 部署驗證清單(人工項,staging 部署時逐項勾記)

- [x] **Cloudflare Pages build command**:既有指令結尾即為 `pnpm build`,
  新三段順序由 package.json 內部生效,dashboard 無須修改(2026-07-27 確認);
  merge 後 CF 建置 Deploy successful。
- [x] **CF Node 版本 ≥ 22**:Build system v3 預設 Node 22.16.0(2026-07-27
  dashboard 截圖確認)。
- [x] **staging 部署綠燈**(2026-07-27,merge commit 2ec86d9):GitHub Actions
  verify(新 wasm-pack 流程首跑)與 Cloudflare Pages 皆 success;
  staging.fhsh-py-dojo.pages.dev 以 agent-browser 實測 repeat-greeting
  提交 5/5 AC,console 零 error。
- [x] **池檔大小抽查**(staging deploy 實測):repeat-greeting.bin 112 KB、
  card-restack-count.bin 1.96 MB(2^n 大數輸出所致),皆遠小於 25 MiB 上限。

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
