## Problem

本機 dev server(vitepress dev)會把題目 frontmatter 完整送到瀏覽器,學生(或任何開啟 dev tools 的人)可在 page module 中直接讀到 `reference_solution` 的完整正解程式碼。使用者於 2026-08-01 實際觀察到此現象並要求移除。實測確認:dev server 的 challenge 頁模組含 reference_solution 內容;staging 正式站的 page chunk 則已是乾淨的(build 期剝除自 2026-07-27 起生效),洩漏面僅存在於 dev 模式。

## Root Cause

`.vitepress/plugins/strip-generator.ts` 以 `apply: 'build'` 掛載,僅在 production build 剝除 `generator` 與 `reference_solution`;dev 模式刻意完整放行 frontmatter。`generator` 在 dev 放行是必要的(dev 判題策略在瀏覽器以 Pyodide 執行 generator 產生期望輸出),但 `reference_solution` 在前端任何模式都沒有消費者(全站 grep 僅 build 期腳本 scripts/generate-pools.ts、scripts/new-challenge.ts 與測試使用)——dev 一併送出純屬多餘的洩漏面,是 2026-07-27 補剝 reference_solution 時沿用「dev 全放行」設計留下的缺口。

## Proposed Solution

把 plugin 從單一 build 實例改為回傳兩個實例(Vite 支援巢狀 plugin 陣列,config.mts 呼叫點 stripGenerator() 維持不變):

- build 實例:照舊剝除 generator 與 reference_solution(行為零變化)。
- serve 實例(新增):只剝除 reference_solution,generator 與其他欄位必須逐字保留。

兩實例共用既有的結構化剝除(YAML 縮排行掃描)與 fail-loud 後置斷言;斷言中的 survivor 檢查與「其他欄位無損」檢查以該實例的剝除欄位清單參數化——serve 實例必須驗證 generator 未受損。不刪除任何題目檔案中的 reference_solution 欄位:該欄位是 content-regression 建置期互驗的依據,且 build 期本來就不出貨。

## Non-Goals

- 不改動任何 docs/challenge/*.md 題目檔案(欄位保留供建置期測試;若要連 repo 原始檔都不含正解,屬另一個需要重新設計 content-regression 的變更)。
- 不改動 docs/shared/challenge.data.ts(已是白名單映射,不含 reference_solution)。
- 不改動判題引擎、加密池與 dev 判題流程;dev 模式 generator 仍完整放行。
- 不處理「dev 模式 generator 本身即為正解」的固有暴露——dev 僅供本機開發,學生只接觸正式站。
- 不處理 Vite dev static middleware 裸 GET 原始檔的路徑(dev 固有行為,transform hook 無從攔截;修法對象是頁面實際載入的模組請求)。

## Success Criteria

- dev server 的 challenge 頁模組(如 /challenge/buffer-audit-log.md)不再含 reference_solution 內容(以 buffer-audit-log 的 popleft/remove_newest 字串為探針),但 generator 內容仍在(drop_newest 探針)且 dev 判題提交正解仍得 AC。
- production build 行為零變化:docs:build 後該題 page chunk 兩欄位探針皆 0。
- .vitepress/plugins/__tests__/strip-generator.spec.ts 更新後全數通過:掛載模式改驗兩實例各自 apply;新增 serve 情境(reference_solution 剝除、generator 與其他欄位逐字無損);既有 A/B/C/E 測試群組維持通過。
- pnpm test --run 全套、pnpm typecheck、pnpm lint 皆綠。

## Impact

- Affected specs: generator-strip-plugin(MODIFIED:production 剝除欄位清單補上 reference_solution 使 spec 同步 2026-07-27 後的現實;dev 模式 requirement 改為 generator 放行 + reference_solution 剝除)
- Affected code:
  - Modified: .vitepress/plugins/strip-generator.ts, .vitepress/plugins/__tests__/strip-generator.spec.ts, .vitepress/config.mts
  - New: (無)
  - Removed: (無)
