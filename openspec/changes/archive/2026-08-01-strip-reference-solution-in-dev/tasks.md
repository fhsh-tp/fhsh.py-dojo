## 1. TDD 紅燈:先寫失敗測試

- [x] 1.1 在 .vitepress/plugins/__tests__/strip-generator.spec.ts 增修雙實例契約測試:掛載模式測試改驗入口回傳兩個實例(第一個 apply 'build'、第二個 apply 'serve',皆 enforce 'pre');新增 serve 情境群組——serve 實例 transform challenge Markdown 後 reference_solution 鍵與內容消失、generator 與其他所有 frontmatter 欄位(title/params/starter_code/algorithm/tags 等)逐字無損、非 challenge 路徑回傳 null;build 實例行為斷言(剝兩欄位)維持既有覆蓋。驗證:npx vitest run .vitepress/plugins/__tests__/strip-generator.spec.ts 顯示新測試對現行單實例實作失敗(紅燈),既有 A/B/C/E 群組不因測試改寫而誤壞。

## 2. 綠燈:實作雙實例剝除

- [x] 2.1 重構 .vitepress/plugins/strip-generator.ts:把 transform 與後置斷言抽成以「剝除欄位清單」參數化的工廠(stripFields、遞迴 survivor 檢查、其他欄位無損比對皆以該清單為準);入口函式回傳 [build 實例(剝 generator + reference_solution)、serve 實例(只剝 reference_solution)],名稱以 :build/:serve 後綴區分;.vitepress/config.mts 呼叫點維持 stripGenerator() 語法,僅在型別需要時調整註記。此任務落實 spec requirement「Production builds strip all answer-bearing frontmatter fields」與「Development mode strips reference_solution while passing generator through」的實作面。驗證:npx vitest run .vitepress/plugins/__tests__/strip-generator.spec.ts 全綠(任務 1.1 的紅燈轉綠)。

## 3. 全套品質閘門

- [x] 3.1 全套測試、型別與 lint 皆綠,證明重構未波及其他套件:pnpm test --run、pnpm typecheck、pnpm lint 三者 exit 0。

## 4. dev server 實測(洩漏面關閉、判題不受影響)

- [x] 4.1 對運行中的 dev server(localhost:5173)實測 challenge 頁模組(瀏覽器實際載入、dev tools 可見的 Vite 模組請求,URL 帶 import query;裸 .md GET 走 Vite static middleware 回原始檔,屬 dev 固有行為、非本修法對象):curl /challenge/buffer-audit-log.md?import 的回應中 reference_solution 探針(popleft、remove_newest、鍵名 reference_solution)為 0 筆、generator 探針(drop_newest)至少 1 筆;另抽 curl /challenge/password-check.md?import 驗 rand_wrong(generator 探針)仍在、字串 reference_solution 與 range(k)(該題正解獨有字串)皆為 0 筆。驗證:上述 grep 計數符合預期。
- [x] 4.2 dev 判題不受影響(驗收 spec requirement「Development mode strips reference_solution while passing generator through」的 Generator field available in dev mode 情境):以 agent-browser 在 localhost:5173 開啟 buffer-audit-log,貼上 collections.deque 正解提交,verdict 顯示 6/6 AC(dev 模式測資由 generator 現算,證明 generator 放行完好)。

## 5. production build 迴歸(行為零變化)

- [x] 5.1 pnpm docs:build 成功完成(56 題全數通過 plugin fail-loud 斷言即為建置期守門),且 docs/.vitepress/dist 中 buffer-audit-log 的 page chunk 對 generator 與 reference_solution 兩組探針(drop_newest、popleft、remove_newest、rand_wrong 於 password-check chunk)皆為 0 筆、合法欄位探針 starter_code 仍在。驗證:grep 計數符合預期。
