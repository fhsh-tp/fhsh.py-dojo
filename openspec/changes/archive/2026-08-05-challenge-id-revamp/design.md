## Context

`id` 目前是 frontmatter 整數(1–59 全站流水號),經 4 路 adversarial review 確認:判題、學生進度(IndexedDB)、測資池、下載檔全部以 slug(markdown 檔名)為鍵,id 的執行期用途僅剩目錄排序與 Vue 的 v-for key。id 尚未在任何 UI 露出。兩本目錄(python 1–54、APCS 55–59)共用一條流水號。部署平台為 Cloudflare Pages(實測確認),站台無 base 前綴、未啟用 cleanUrls,docs/public/ 內容會複製到建置輸出根目錄(pools/pyodide 前例)。

已知靜默地雷(review 已定位):challenge.data.ts 的資料層排序與 HomeView 的最新清單排序使用數值減法比較器,id 改字串後會退化為 NaN(資料層那處因 frontmatter 為 any 型別,typecheck 攔不到);new-challenge.ts 的 computeNextId 與 retired-ledger.test.ts 使用僅比對整數的 regex,id 改字串後會分別「恆回傳 1」與「守門斷言靜默空轉」。

## Goals / Non-Goals

**Goals:**

- frontmatter id 改為字串格式:category 前綴 + 3 位零填充序號(py001–py054、apcs001–apcs005),各 category 從 1 起連號
- ChallengeCard 顯示 id;目錄搜尋支援序號感知 id 比對
- 建置期產生 Cloudflare Pages `_redirects`,讓 `/challenge/<id>` 轉址到 canonical slug 網址
- 排序、scaffold 配號、retired ledger、守門測試、文件契約全面同步,不留任何整數假設

**Non-Goals:**

- 不動 slug/檔名(學生資料零影響的前提)
- 不改 canonical 網址(不使用 VitePress rewrites,不改檔名路由)
- 不引入 alias_id/display_id 雙編號欄位(已評估否決:淺介面)
- 不做「py3」這類「前綴+未填充序號」的進階查詢正規化(YAGNI)
- 不新增獨立 order 排序欄位;顯示順序仍由 id 序號決定
- 不要求本機 vitepress dev/preview 模擬轉址(驗證改用 wrangler pages dev 與 staging 探針)

## Decisions

1. **id 格式:`前綴 + 3 位零填充序號`,前綴 registry 與 category 對應(python→py、apcs→apcs)**。零填充讓同前綴字典序=數值序,排序實作最簡;前綴保證 id 非純數字開頭,YAML 一律解析為字串,frontmatter 無需引號。容量 999 題/系列。替代案(整數分區段、alias_id、不 pad)已於討論階段否決。
2. **排序一律改字串 code-unit 比較**(`a < b ? -1 : a > b ? 1 : 0`;challenge.data.ts 資料層排序、HomeView 兩處最新清單降冪)。不用 localeCompare——ICU collation 依執行環境而異,會讓建置產物(_redirects)的可重現性繫於機器而非程式碼。同 category 內等價於序號排序;跨前綴混排時 apcs 系列字典序在前——目前所有消費端(目錄頁、首頁清單)都先以 category 過濾,混排順序無使用者可見影響,此邊界行為明文寫入 spec 封閉。
3. **搜尋兩條規則,原有文字欄位比對不動**:查詢正規化(trim+lowercase)後,(a) 純數字(`^\d+$`)→ 與 id 的序號部分做數值精準比對;(b) 其餘 → 對 id 做 startsWith 前綴比對。序號解析定義為「id 去除開頭非數字字元後的十進位整數」。每個目錄頁的資料在頁面層已按 category 過濾,搜尋範圍天生隔離。
4. **`_redirects` 產生器為獨立建置步驟**:新增 scripts/generate-redirects.ts,掃描 docs/challenge/ 全部 markdown 的 frontmatter id 與檔名 slug,輸出每行 `/challenge/<id> /challenge/<slug> 302` 至 docs/public/_redirects(gitignored,同 pools 模式)。轉址目標一律無 .html 副檔名(CF Pages 會將 .html 正規化為無副檔名網址,帶副檔名目標會造成 302→308 兩跳;此正規化狀態碼屬平台行為,測試不得寫死)。Cloudflare 對格式錯誤行靜默忽略,因此產生器必須自附單元測試守格式與涵蓋率。package.json 於 dev 與 build 管線掛上此步驟。
5. **scaffold 配號改 per-category**:computeNextId 以「指定前綴之最大序號 + 1」計算並輸出零填充字串;掃描 regex 由僅整數改為擷取字串 id 後解析序號。retired ledger 的 ids 型別改 string[],checkRetired 簽章同步;retired-challenges.json 現有內容(ids 為空陣列)不需遷移。
6. **一次性重編以既有整數 id 為序**:python 題依原整數 1–54 映射為 py001–py054,APCS 題依原整數 55–59 映射為 apcs001–apcs005。以拋棄式腳本批次改寫後即刪除,映射規則記錄於 tasks;不保留遷移程式碼。

## Implementation Contract

**行為(使用者可觀察):**

- 目錄頁與首頁的每張 ChallengeCard 顯示該題字串 id(如 apcs003),與標題並列可辨識
- Python 目錄頁搜尋框輸入 3、03 或 003,結果恰為 py003 一題(加上原有文字欄位命中的題目);輸入 py 列出本頁全部 python 題;輸入 py00 列出 py001–py009;輸入 py3 不因 id 規則命中任何題
- 部署站上請求 /challenge/py003 回應 HTTP 302,Location 為對應 slug 的無副檔名網址;瀏覽器最終落在 canonical slug 網址
- 目錄頁題目順序與首頁「最新挑戰」清單行為與改版前一致(各 category 內依序號遞增/遞減)
- pnpm new-challenge 產生的新題,id 為該 category 現有最大序號 + 1 的零填充字串

**介面/資料形狀:**

- Challenge.id 型別由 number 改為 string;DataChallenge 隨之
- computeNextId(fileContents, prefix) 回傳如 py055 的字串;RetiredLedger.ids 為 string[];checkRetired(name, id: string, ledger)
- scripts/generate-redirects.ts 輸出檔每行格式:/challenge/<id> /challenge/<slug> 302,行數等於題目檔數,無重複來源路徑
- 59 個題目檔 frontmatter 的 id 值符合 ^(py|apcs)\d{3}$

**失敗模式:**

- 產生器遇到缺 id 或 id 格式不符的題目檔即以非零退出碼失敗並指名檔案(fail-loud,不靜默略過)
- 搜尋查詢無法解析為序號時僅走前綴比對,不拋錯
- 重複 id 由 challenge-params 冒煙層之外的新增唯一性檢查(產生器內建)攔截

**驗收條件:**

- pnpm typecheck、pnpm lint、pnpm test --run 全綠
- 新增測試涵蓋:排序比較器(同前綴序號序)、搜尋語意矩陣(上述行為全列)、computeNextId per-category 與零填充、checkRetired 字串型別、generate-redirects 格式/涵蓋率/無副檔名目標/唯一性
- grep 驗證 docs/challenge/ 全部檔案 id 符合新格式
- retired-ledger.test.ts 改寫後,對現存 59 檔的斷言實際執行(以測試內部斷言計數或等價手段防真空通過)

**範圍邊界:**

- in scope:上述行為、型別鏈、測試、Usage.md/CONTRIBUTE.md/challenge-author skill/相關 openspec specs 的契約文字
- out of scope:slug、判題鏈、進度儲存、pool 產生器、canonical 路由、VitePress 版本、既有搜尋文字欄位語意

## Risks / Trade-offs

- [修一洞挖一洞:排序改字串比較後跨前綴混排順序改變] → 消費端全部先按 category 過濾,混排無使用者可見面;邊界行為明文入 spec,新增排序測試釘住
- [CF 對 _redirects 壞行靜默忽略,轉址失效無感] → 產生器單元測試守格式;staging 部署後以探針(curl 驗 302/Location)確認;本機可用 wrangler pages dev 模擬
- [批次重編改壞某檔 frontmatter(YAML 損毀)] → 重編後立即跑 pnpm test --run(challenge-params 冒煙測試會指名壞檔)與 build:pools 驗證
- [未來新增 category 忘記登記前綴] → 前綴 registry 集中於單一模組,產生器與 scaffold 共用;未知 category fail-loud
- [平台正規化狀態碼(Pages 308/Workers 307)寫死進測試造成未來誤報] → 測試只驗 3xx 與 Location,不驗確切狀態碼

## Migration Plan

1. 重編與型別鏈(59 檔 frontmatter、Challenge.id、排序、computeNextId、ledger、既有測試修訂)——此階段完成前 id 不得露出
2. 露出(ChallengeCard 徽章、搜尋序號感知)
3. 別名(generate-redirects.ts、package.json 管線、.gitignore)
4. 文件與規格契約(Usage.md、CONTRIBUTE.md、challenge-author skill、openspec specs)
5. 全量驗證(typecheck/lint/test/build)後進 audit
