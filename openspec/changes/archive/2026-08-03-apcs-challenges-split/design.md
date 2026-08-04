## Context

挑戰題庫單頁 `/challenges` 由 `docs/challenges.md` 餵 `challenge.data.ts` 的全量資料給 `ChallengeListView`。學生完成進度以題目 slug 為 primary key 存於 IndexedDB（`local-progress-store`），slug 由 `deriveChallengeSlug` 從 `/challenge/` 路徑段推導——因此**題目檔案不可搬動**，分類只能靠 frontmatter。「已完成 X / Y」目前分子取全站 `completedCount`、分母取當頁題數，單頁時恰好一致，拆頁後會錯帳。挑戰頁 header「← 返回」與錯誤態「返回列表」皆 `router.go('/')` 回首頁。

**名詞表**

| 名詞 | 定義 |
|------|------|
| category | 題目 frontmatter 選填欄位，值域 `python` \| `apcs`，預設 `python` |
| Python 挑戰頁 | `/challenges`（`docs/challenges.md`），只列 `category === 'python'` 的題目 |
| APCS 挑戰頁 | `/apcs-challenges`（`docs/apcs-challenges.md`），只列 `category === 'apcs'` 的題目 |
| 所屬列表頁 | 題目 category 對應的列表頁 URL |
| 頁內完成計數 | 分子與分母皆以當頁題目集合計算的「已完成 X / Y」 |

**frontmatter schema 範例**

```yaml
layout: challenge
id: 55
title: 撲克牌重排計數
difficulty: medium
category: apcs   # 新欄位；省略時視為 python
algorithm: card_restack_count
```

## Goals / Non-Goals

**Goals:**

- 以最小改動把挑戰題庫拆為 Python / APCS 兩個列表頁，全部重用 `ChallengeListView` 與 `ChallengeCard`。
- category 欄位進入資料層契約（型別、loader、resolver、scaffold、Usage.md）一次到位。
- 拆頁引入的三個一致性問題（完成計數、首頁最新挑戰、返回導航）同批修正。

**Non-Goals:**

- 不搬動任何題目檔案、不改 slug 推導、不動進度儲存層（`progress.ts` 的 `completedCount` 保留原語意不刪除）。
- 不做 query param 版單頁分類（VitePress 靜態產站下 hydration 閃爍、nav 高亮、同路徑換 query 不重渲染三重成本，已在討論中否決）。
- 不新增第三種 category、不做列表頁分頁（pagination）、不改搜尋與難度篩選行為。
- 不回填四題 APCS 的 `chapter` 欄位（卡片不顯示 chapter，維持空值）。

## Decisions

1. **category 用 resolver 擋未知值，鏡射 `exercise-type` 模式**：新增 `docs/shared/challenge-category.ts` 匯出 `CHALLENGE_CATEGORIES = ['python', 'apcs']`、`ChallengeCategory` 型別與 `resolveChallengeCategory(raw)`（未知／缺值 → `'python'`）。替代方案「loader 內聯 `?? 'python'`」被否決：無法擋 typo（`apsc`、大寫），會無聲掉錯頁。
2. **型別×邊界矩陣（追溯單一真相來源）**：

   | frontmatter `category` 原始值 | resolver 結果 | 出現頁面 | 守門 |
   |---|---|---|---|
   | 省略 | `python` | Python 挑戰頁 | — |
   | `python` | `python` | Python 挑戰頁 | — |
   | `apcs` | `apcs` | APCS 挑戰頁 | — |
   | 其他任意值（typo、大小寫、非字串） | `python` | Python 挑戰頁 | `challenge-category.test.ts` 全檔掃描指名該題失敗 |

   Runtime 安全預設（不會讓題目消失），build/test 期 fail loud（指名檔案），與 `challenge-params.test.ts` 冒煙守門同哲學。
3. **過濾位置在頁面 `.md` 的 `<script setup>`**：兩個列表頁各自 `challenges.filter(...)` 後餵 `ChallengeListView`，元件維持「吃什麼列什麼」的純展示契約。替代方案「`ChallengeListView` 加 category prop 自行過濾」被否決：把資料選擇邏輯下沉進展示元件，首頁還得再繞。
4. **頁內完成計數在 `ChallengeListView` 內以 props 自算**：`props.challenges.filter(c => progress.isCompleted(c.slug)).length`。不動 store 的全站 `completedCount`（`progress-record-export` 等既有面向可能依賴其語意）。
5. **返回分流以 prop 注入**：`ChallengeView` 由 `frontmatter.category` 經 resolver 算出 `listUrl`，傳給 `AppHeader` 新增的選填 prop `backUrl`（預設 `'/challenges'`）；錯誤態「返回列表」共用同一 `listUrl`。行為變更：由回首頁改為回所屬列表頁。
6. **首頁兩區塊在 `HomeView` 內過濾**：`docs/index.md` 不改，`HomeView` 以 category 分出兩個 computed（各依 id 降序取 3），區塊標題「最新 Python 挑戰」「最新 APCS 挑戰」，「查看全部 →」分別指 `/challenges`、`/apcs-challenges`；任一類為空時沿用現有 `v-else` 空狀態訊息模式。
7. **scaffold 一律輸出 `category` 欄位**：`new-challenge.ts` 加 `--category python|apcs`（預設 `python`），驗證失敗訊息鏡射 `validateDifficulty` 格式；模板一律寫出 `category:` 行，讓新題自我記錄。

## Implementation Contract

- **資料形狀**：`Challenge` 介面新增必填欄位 `category: 'python' | 'apcs'`；`challenge.data.ts` transform 以 `resolveChallengeCategory(frontmatter.category)` 填值。
- **頁面行為**：`/challenges` 只列出 resolver 結果為 `python` 的題目且 title 為「Python 挑戰」；`/apcs-challenges` 只列出 `apcs` 題目且 title 為「APCS 挑戰」。兩頁搜尋、難度篩選、卡片行為與現行完全一致。
- **nav 行為**：頂部 nav 顯示「Python 挑戰」「APCS 挑戰」兩項（原「挑戰題庫」移除），分別連至兩列表頁。
- **完成計數行為**：每個列表頁的「已完成 X / Y」中 X 只計當頁題目集合內已完成者；一題只會被計入其所屬頁。
- **返回行為**：任一挑戰頁（含載入錯誤狀態）的返回按鈕導向該題所屬列表頁；`category` 缺值或未知時導向 `/challenges`。
- **scaffold 行為**：`pnpm new-challenge foo --category apcs` 產出的 frontmatter 含 `category: apcs`；`--category` 給未知值時以非零狀態退出並印出合法值清單；省略旗標時產出 `category: python`。
- **失敗模式**：未知 category 在 runtime 一律靜默歸入 `python`（題目不消失）；`docs/shared/challenge-category.test.ts` 掃描 `docs/challenge/*.md` 全檔，任何未知值指名檔案讓測試失敗。
- **驗收出口**：`pnpm typecheck`、`pnpm lint`、`pnpm test --run` 全綠；`challenge-category.test.ts` 覆蓋 resolver 四類邊界與全檔掃描；`new-challenge.test.ts` 覆蓋 `--category` 三情境（省略／合法／非法）。
- **範圍邊界**：in scope＝上述七個決策觸及的檔案；out of scope＝`progress.ts`、`challenge-slug.ts`、判題與測資產生鏈、任何 `docs/challenge/*.md` 內文（僅四題加一行 frontmatter）。

## Risks / Trade-offs

- [返回行為變更：習慣回首頁的學生可能困惑] → 按鈕語意（「返回列表」）本就指列表頁，且首頁在 nav 品牌連結一鍵可達；風險低。
- [未知 category 靜默歸 python 可能延遲發現錯標] → 測試層全檔掃描 fail loud 指名檔案，CI 品質閘門（`ci-quality-gate`）擋合併。
- [首頁兩區塊拉長頁面] → 每區僅 3 張卡，與現行單區塊等寬網格，增量一列。
- [`AppHeader` 新 prop 預設 `/challenges`，若未來新增第三類頁面忘記傳值會導錯頁] → 值域擴充時 `CHALLENGE_CATEGORIES` 是單一真相來源，resolver 測試會先失敗。

## Migration Plan

1. 資料層先行：resolver + 型別 + loader + 測試（此時 UI 尚未分頁，全部題目 resolver 結果照舊進 `/challenges`，站台行為不變）。
2. UI 分頁：新頁面、challenges.md title、nav、ChallengeListView 計數、HomeView 兩區塊、返回分流。
3. 工具鏈收尾：scaffold 旗標＋測試、Usage.md、四題 frontmatter 標 `category: apcs`。
4. 回滾：整包 revert 即可；資料層與 UI 層無跨 commit 依賴，frontmatter 新欄位對舊程式碼是未知欄位、無害。

## Open Questions

（無——七項決策皆已在 discuss 階段與使用者定案。）
