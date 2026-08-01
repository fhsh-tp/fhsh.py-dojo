## Context

`.vitepress/plugins/strip-generator.ts` 是防止解答外洩的最後一道防線:以 Vite `transform` hook 在 Markdown 模組進入編譯前,從 challenge frontmatter 結構化剝除解答欄位,並以 fail-loud 後置斷言(重新解析 YAML、遞迴 survivor 檢查、其他欄位無損比對)保證「剝乾淨、不誤傷」,任何可疑狀態直接讓建置爆掉。目前整支 plugin 以 `apply: 'build'` 掛載,dev 模式完全不作用——這是 generator 的正確行為(dev 判題策略需要在瀏覽器執行 generator),但讓 `reference_solution` 一併在 dev 送到瀏覽器,即為本次要修的洩漏面。前端(theme/composables)在任何模式都不讀取 reference_solution,全站僅 build 期腳本與離線測試使用。

## Goals / Non-Goals

Goals:
- dev 模式(vitepress dev)送往瀏覽器的 challenge 頁模組不含 reference_solution。
- production build 行為零變化(既有兩欄位剝除與所有 fail-loud 斷言原樣保留)。
- fail-loud 斷言在 serve 實例同樣生效,且能證明 generator 在 serve 模式逐字無損。

Non-Goals:
- 不從 docs/challenge/*.md 原始檔移除 reference_solution(content-regression 依賴)。
- 不改變 dev 模式 generator 的放行(dev 判題必需)。
- 不動 challenge.data.ts(既有白名單映射已隔離此路徑)。
- 不處理 Vite dev static middleware 直接回傳專案原始檔的路徑(裸 GET /challenge/*.md 會拿到磁碟上的原始 Markdown):這是 Vite dev 對整個專案根目錄的固有行為,transform hook 無從攔截,且 dev 僅供本機開發——本修法的對象是頁面實際載入、dev tools 可見的模組請求(帶 import query)。

## Decisions

1. **兩個 plugin 實例,而非單一實例內判斷模式**:Vite 的 `apply` 欄位是宣告式掛載開關,拆成 build 實例(剝 `generator` + `reference_solution`)與 serve 實例(只剝 `reference_solution`)可讓「哪個模式剝哪些欄位」直接寫在掛載宣告上,不需在 transform 內讀取 resolved config 狀態。替代方案(單實例 + `configResolved` 記錄 command 再分支)可行但把模式差異藏進執行期狀態,審視面較差。
2. **共用同一個 transform 工廠,以欄位清單參數化**:剝除邏輯與後置斷言只有「剝哪些欄位」不同。工廠函式接受欄位清單,`stripFields`、survivor 遞迴檢查、「其他欄位無損」比對全部以該清單為準——serve 實例因此自動把 generator 納入「必須無損」的比對集合,等於免費獲得「generator 逐字保留」的建置期證明。
3. **對外匯出維持單一入口**:入口函式回傳兩實例的陣列,config.mts 呼叫點語法不變(Vite 接受巢狀 plugin 陣列並自動攤平)。實例名稱以後綴區分(如 strip-generator:build / strip-generator:serve)便於除錯輸出辨識。
4. **不刪題目檔案欄位**:洩漏的根因是「送到前端」而非「存在於 repo」;刪檔案欄位會毀掉 content-regression 互驗且對出貨面零收益。

## Implementation Contract

- **觀察行為(serve)**:vitepress dev 下請求任一 challenge 頁的 Markdown 模組,回應內容不含 reference_solution 的鍵與值;generator 與其餘所有 frontmatter 欄位與剝除前逐字相同。非 challenge 路徑的 Markdown 不受影響。
- **觀察行為(build)**:與現行完全一致——兩欄位皆剝除,任何斷言失敗即中止建置。
- **介面形狀**:plugin 入口維持既有匯出名稱,回傳值由單一 Plugin 改為 Plugin 陣列(build 實例在前、serve 實例在後);兩實例均 `enforce: 'pre'`,分別 `apply: 'build'` 與 `apply: 'serve'`。config.mts 的 vite.plugins 清單呼叫點不需改動語法(巢狀陣列由 Vite 攤平)。
- **失敗模式**:任一實例的後置斷言(剝除欄位倖存、其他欄位受損、剝除後 YAML 無效或非 mapping、來源 YAML 無效)一律 throw——build 模式中止建置,serve 模式該頁模組載入失敗並在終端顯示錯誤,兩者皆不得靜默放行。
- **驗收準繩**:.vitepress/plugins/__tests__/strip-generator.spec.ts 全數通過(含新增 serve 情境與雙實例掛載模式斷言);pnpm test --run、pnpm typecheck、pnpm lint 綠;dev server 實測 challenge 頁模組 reference_solution 探針 0、generator 探針 >0 且提交正解得 AC;pnpm docs:build 成功(56 題全數通過 fail-loud 斷言)且 dist 內該題 page chunk 兩欄位探針皆 0。
- **範圍邊界**:in scope = .vitepress/plugins/strip-generator.ts、其測試檔、.vitepress/config.mts(僅在型別簽名需要時);out of scope = docs/challenge/*.md、docs/shared/challenge.data.ts、判題引擎、加密池、CI 設定。
