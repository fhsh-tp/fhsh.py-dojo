## 1. id 重編與型別鏈(id 露出前必須全數完成)

- [x] 1.1 以拋棄式批次腳本將 docs/challenge/ 全部 59 檔 frontmatter 的整數 id 重寫為字串 id:python 題依原整數 1–54 映射為 py001–py054,APCS 題依原整數 55–59 映射為 apcs001–apcs005;不重新命名或移動任何題目檔。完成時所有檔案 id 符合 `^(py|apcs)\d{3}$`、無重複、各前綴序號自 1 連續。(Requirement: Challenge id is a category-prefixed zero-padded string;Requirement: Renumbering never touches slugs or student data keys)驗證:grep 掃描 59 檔全數符合新格式且檔名集合與改前完全相同,`pnpm test --run scripts/challenge-params.test.ts` 全綠(確認 frontmatter 未被改壞)。
- [x] 1.2 Challenge.id 型別由 number 改為 string(.vitepress/theme/types.d/challenge.type.ts),challenge.data.ts 的 loader 移除 `idx + 1` 整數 fallback(缺 id 即為內容錯誤,交由產生器/守門攔截,loader 以空字串標記),排序改字串 code-unit 比較(不用 localeCompare,確保建置輸出跨環境可重現);HomeView.vue 兩處最新清單降冪排序同步改用同一比較器,行為維持「各 category 內序號最高前 3」。(Requirement: Catalogue ordering derives from id string comparison)驗證:`pnpm typecheck` 全綠;新增排序單元測試(先寫紅再轉綠,涵蓋同前綴序號序與降冪取前 3)。
- [x] 1.3 computeNextId 改為 per-category:簽章收 category 前綴,掃描該前綴最大序號 +1 回傳零填充字串;遇到不符格式的既有 id 以非零退出並指名檔案。BuildContentOptions.id 改 string,樣板輸出維持 `id: <string>`。(Requirement: CLI script scaffolds a new challenge file)驗證:new-challenge.test.ts 改寫後全綠,新增 per-category 配號與 fail-loud 案例(TDD:先寫紅)。
- [x] 1.4 RetiredLedger.ids 改 string[],checkRetired 簽章改 (name, id: string, ledger);retired-ledger.test.ts 的 id 掃描 regex 改為擷取字串 id,並斷言「實際解析數=題目檔數」防真空通過;順手修正 new-challenge.ts 中「catalogue progress keyed by id」的過時註解(實為 slug)。(Requirement: Retired slug and id ledger)驗證:`pnpm test --run scripts/retired-ledger.test.ts scripts/new-challenge.test.ts` 全綠,且刻意塞一個壞格式 id 的 fixture 案例會紅。
- [x] 1.5 [P] 修訂前端測試 fixtures:ChallengeCard.spec.ts 與 ChallengeListView.spec.ts 的 fixture id 改字串格式並補齊 Challenge 必填欄位(category/chapter/description),使 fixture 與正式資料形狀一致。驗證:`pnpm test --run` 該兩檔全綠。

## 2. id 露出(依賴群組 1)

- [x] 2.1 ChallengeCard 顯示 id 徽章:卡片於標題旁渲染 challenge.id 原文,兩個目錄頁與首頁最新清單皆生效。(Requirement: ChallengeCard displays the challenge id)驗證:ChallengeCard.spec.ts 新增「卡片顯示 id 文字」斷言(先紅後綠)。
- [x] 2.2 ChallengeListView 搜尋加入序號感知 id 比對:查詢 trim+lowercase 後,純數字→序號精準比對(3/03/003 皆中本頁序號 3),其餘→id startsWith;與原文字欄位比對以 OR 結合;搜尋框 placeholder 更新為含「編號」。(Requirement: Search filters challenges by text matching across multiple fields)驗證:ChallengeListView.spec.ts 以 spec 的 digit-query 矩陣為案例新增測試(含 py00 前綴命中 py001–py009、py3 不經 id 規則命中),先紅後綠。

## 3. 別名轉址(依賴群組 1)

- [x] 3.1 [P] 新增 scripts/generate-redirects.ts:掃描 docs/challenge/*.md,輸出每行 `/challenge/<id> /challenge/<slug> 302` 至 docs/public/_redirects;目標一律無 .html;缺 id/壞格式/重複 id 以非零退出並指名檔案。(Requirement: Build step generates the Cloudflare Pages redirects file)驗證:新增 scripts/generate-redirects.test.ts(TDD 先紅)涵蓋行格式、涵蓋率=檔數、無副檔名目標、重複與壞格式 fail-loud。
- [x] 3.2 [P] package.json 的 dev 與 build 管線掛上 build:redirects 步驟,.gitignore 加入 docs/public/_redirects,使產出檔不進版控。(Requirement: Redirects file is generated output, not source)驗證:執行 `pnpm build:redirects` 後 docs/public/_redirects 存在且行數=題目檔數,git status 不出現該檔。

## 4. 文件與規格契約(依賴群組 1,可與 2/3 並行)

- [x] 4.1 [P] Usage.md 與 CONTRIBUTE.md 的 id 契約改寫:「遞增整數」相關敘述改為字串 id 格式(前綴+3 位零填充、各 category 連號、由 scaffold 自動配號),範例同步更新。驗證:內容審閱——grep 兩檔無殘留「整數」id 敘述,範例與 spec 的格式表一致。
- [x] 4.2 [P] .claude/skills/challenge-author/SKILL.md 的配號說明由「接續現有最大值」改為「該 category 前綴內最大序號 +1」。驗證:內容審閱與 grep 確認無舊敘述殘留。

## 5. 全量驗證(依賴全部群組)

- [x] 5.1 全量守門:`pnpm typecheck`、`pnpm lint`、`pnpm test --run` 全綠;`pnpm build:pools` 成功(確認 59 檔 frontmatter 仍可解析、pool 產出不受 id 影響);grep 驗證 Module 2 引用的挑戰題 id 於 py 前綴內序號連續。(Requirement: Challenge ID continuity across Module 2)驗證:上述指令輸出零錯誤。
- [x] 5.2 別名行為驗證:`pnpm build` 後以 `npx wrangler pages dev <輸出目錄>` 本機模擬,curl 抽測 3 條別名(py001、py054、apcs003)回應 3xx 且 Location 為對應無副檔名 slug 路徑(不斷言確切狀態碼)。(Requirement: Deployed alias URLs redirect to canonical slug URLs)驗證:三條探針全數通過。
