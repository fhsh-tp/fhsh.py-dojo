## Why

challenge 的 `id` 目前是全站流水整數(1–59),對學生完全不可見,唯一執行期用途是目錄排序。課堂需要「口頭指派題號」的能力:老師說「做第 3 題」,學生要能在卡片上看到編號、在搜尋框打編號找到題目、甚至直接輸入短網址到達題目。同時 python 與 APCS 兩本目錄共用一條流水號,未來新題會造成單頁跳號。id 尚未對外露出,現在是重編的唯一窗口——一旦上卡片、進搜尋、進網址,id 即凍結為對外契約。

## What Changes

- **BREAKING(內部契約)**:frontmatter `id` 由整數改為字串格式 `<category前綴><3位零填充序號>`(`py001`–`py054`、`apcs001`–`apcs005`),各 category 從 1 起連號。slug/檔名完全不動,學生本機資料(IndexedDB 進度、session、下載檔)與測資池全部 slug-keyed,零影響(已經 4 路 adversarial review 驗證)。
- ChallengeCard 顯示 id 徽章。
- 目錄搜尋新增「序號感知」id 比對:純數字查詢精準比對序號(3/03/003 皆中本頁序號 3);其餘查詢對 id 做前綴比對(py、py00、py003);每個目錄頁天生只搜自己 category。
- 新增建置期 `_redirects` 產生器:輸出 Cloudflare Pages 轉址表(`/challenge/py003 → /challenge/<slug>` 302,目標一律無副檔名),寫入 docs/public/_redirects(gitignored,同 pools 模式)。
- 排序比較器由數值減法改為字串比較(zero-pad 下同前綴字典序=數值序):目錄頁與首頁「最新挑戰」清單。
- scaffold 配號 computeNextId 改為依 category 前綴掃描最大序號+1;retired ledger 的 id 型別改字串;守門測試的整數 regex 同步放寬,避免靜默空轉。
- 文件與規格契約同步:Usage.md、CONTRIBUTE.md、challenge-author skill、相關 openspec specs 中「遞增整數」相關敘述全面改寫。

## Capabilities

### New Capabilities

- `challenge-id-scheme`: 字串 id 的格式、唯一性、各 category 連號與排序契約
- `challenge-alias-redirects`: 建置期產生 Cloudflare Pages `_redirects` 別名轉址表的行為契約

### Modified Capabilities

- `challenge-search`: 搜尋新增序號感知 id 比對(純數字→序號精準;其餘→id 前綴)
- `challenge-category-catalogue`: ChallengeCard 顯示 id 徽章
- `challenge-scaffold-script`: computeNextId 改依 category 前綴配號;retired ledger id 改字串型別
- `local-progress-store`: retired ledger 條目由 numeric id 改為 string id(僅契約文字,持久化行為不變)
- `ch2-cross-chapter-audit`: id 連續性要求由「全站連續整數」改為「各 category 前綴內序號連續」

## Impact

- Affected specs: challenge-id-scheme(新)、challenge-alias-redirects(新)、challenge-search、challenge-category-catalogue、challenge-scaffold-script、local-progress-store、ch2-cross-chapter-audit
- Affected code:
  - New:
    - scripts/generate-redirects.ts
    - scripts/generate-redirects.test.ts
  - Modified(docs/challenge/ 下全部 59 個題目檔的 frontmatter id,以及下列檔案):
    - .vitepress/theme/types.d/challenge.type.ts
    - docs/shared/challenge.data.ts
    - .vitepress/theme/views/HomeView.vue
    - .vitepress/theme/views/ChallengeListView.vue
    - .vitepress/theme/components/challenge/ChallengeCard.vue
    - scripts/new-challenge.ts
    - scripts/new-challenge.test.ts
    - scripts/retired-ledger.test.ts
    - .vitepress/theme/__tests__/ChallengeCard.spec.ts
    - .vitepress/theme/__tests__/ChallengeListView.spec.ts
    - package.json
    - .gitignore
    - Usage.md
    - CONTRIBUTE.md
    - .claude/skills/challenge-author/SKILL.md
  - Removed: (none)
