## Context

deque 系列第一題 id 55(card-restack-count)成形於測資引擎升級之前,params 用「固定 t=10 + 手動攤平 n1~n10」的舊 workaround;本題是引擎升級後第一個使用 group 語法 + testcase_plan 分區的正式題目,也是判題引擎 TLE 修復(PR #15)後第一個以「大測資懲罰慢解」為設計目標的題目。所有前置(group/count.from、testcase_plan、op-counter 扁平修復、TLE verdict)均已 merge 進 staging 並完成部署驗證。使用者已逐項拍板:band 結構(小 3 大 2 + 邊界 1)、數字範圍(-999..999)、title「兩端淘汰賽」、difficulty medium、type competition、verdict_detail 缺席(hidden)、reference_solution 用 deque 教法。

## Goals / Non-Goals

**Goals:**

- 新增可判題的正式題目 two-end-elimination(id 56),教 collections.deque 的雙端操作。
- 用 testcase_plan 讓「純 Python O(n²) 雙重迴圈」慢解在大 band 吃 TLE,deque 正解全 AC。
- 保證每場判題涵蓋單元素邊界(max==min)。
- reference_solution 以教學演算法實作,經 content-regression 自動驗證與 generator 期望輸出一致。

**Non-Goals:**

- 不改判題引擎與測資引擎(能力已齊;發現缺口即停下回報,不自行擴充)。
- 不做計分面(部分給分、band 加總、UI 標示)——BACKLOG §1 凍結範圍。
- 不做 staging→main release。
- 不更動 BACKLOG 停車場項目與既有 specs(testcase-plan、python-generator 等僅為使用方)。
- 不驗證「學生必須用 deque」——平台無 AST 檢查,靠題目敘述引導(既有平台限制)。

## Decisions

### 教法採兩端淘汰賽、reference_solution 與 generator 分工

教法(使用者拍板):比較 `d[0]` 與 `d[-1]`,pop 掉「輸」的一端,剩最後一個是答案;複製一份 deque,max 與 min 各跑一輪。正確性論證:全域最大值在任何一次兩端比較都不會輸(≥ 所有值),不會被淘汰;tie 時淘汰哪端不影響答案(對 Ni=1、偶數長度、重複極值皆成立),故比較用 `>=` 或 `<=` 皆正確,敘述與範例前後一致即可。generator 用內建 `max()`/`min()` 產期望輸出(建置期原生 python3 執行、無 op 限制);reference_solution 用 deque 教法——兩者寫法刻意不同(Usage.md 建議),content-regression 以正式池樣本自動驗證教學演算法正確,一份測試守兩個目的。替代案「reference_solution 也用內建」被否決:與 generator 同寫法時測不出教學解法的錯誤。

### testcase_plan 三 band 結構與數值

小 band count 3(override n.max=20):驗邏輯;大 band count 2(override n.min=2500):純 Python O(n²) 門檻實測 n≈1600–2100 即超 10M op 上限,2500..4000 保證慢解必 TLE 且留餘裕(同筆 T 組 ops 累計,單組超門檻整筆必超);邊界 band count 1(override n.min=1、n.max=1):保證每場出現單元素(max==min),值隨機。總 6 筆 ≠ ChallengeView 預設 testcaseCount 5,e2e 可由筆數直接證明走 plan 路徑。替代案 literal 條目(固定輸入)被否決:使用者選「保證出現、數字隨機」,band override 即可表達且與其他條目機制一致。base params:t 2..3;n 1..4000(下限 1 是技術必然——Ni=0 時 max/min 無定義,generator 會拋 ValueError);nums -999..999(含負數抓「mx=0 起算」型 WA bug)。input_budget 65535(T=3、Ni≤4000 最壞約 60KB,在 65536 硬上限內)。

### frontmatter 元資料沿用系列與全站慣例

difficulty medium(演算法比 id 55 的多步驟重排推理簡單,但需懂 deque 與多筆輸入格式,非 easy);type competition(與 id 55 一致,符合「第一行 T」格式);starter_code 空字串(與 id 55 一致,使用者拍板);無 chapter(比照 id 55,競賽系列不掛章節);無 verdict_detail(缺席=hidden,全站 55 題皆然;TLE 區分型題目不宜洩漏測資規模);無 testcase_count(與 testcase_plan 互斥,scaffold 產生的預設值必刪)。tags:data structure、deque。

### 敘述結構照系列第一題樣式

結構照 card-restack-count.md:題目說明、動手推演(以小例逐步走兩端淘汰賽)、輸入說明、輸出說明、範例。敘述明確引導使用 collections.deque,並預告「大測資會讓過慢的寫法超時」——只寫事實,不承諾具體筆數位置。輸出順序「先 max 後 min」是使用者原話逐字指定,勿對調。範例的比較方向(>= 或 <=)與動手推演一致。

## Implementation Contract

- **行為**:學生在 /challenge/two-end-elimination 頁面提交程式碼,判題以 6 筆池測資執行:正確解 6/6 AC;純 Python O(n²) 雙重迴圈解在大 band 2 筆顯示 TLE 黃色徽章(其餘筆 AC/WA 視邏輯而定);每場必有一筆單元素測資,輸出為同一數字重複兩次(如「-7 -7」)。
- **資料形狀**(frontmatter 契約,欄位名以 Usage.md 為準):layout challenge、id 56、title 兩端淘汰賽、difficulty medium、type competition、algorithm two_end_elimination、tags [data structure, deque]、description 一句話、params(t: int 2..3;cases: group repeat t,內含 n: int 1..4000 與 nums: int -999..999 count.from n separator 換行)、input_budget 65535、testcase_plan(三條 band:count 3/override cases.params.n.max 20;count 2/override cases.params.n.min 2500;count 1/override cases.params.n.min 1 與 n.max 1)、generator(讀 T→逐筆讀 Ni 與 Ni 行→print(max, min))、starter_code 空字串、reference_solution(collections.deque 兩端淘汰賽,max/min 各跑一輪)。禁止出現 testcase_count 欄位。
- **失敗模式**:params/plan 拼錯或非法宣告會在 pnpm build:pools 與 scripts/challenge-params.test.ts 直接報錯指名本檔(fail-loud,無靜默 fallback);reference_solution 與 generator 期望輸出不一致時 content-regression 測試失敗並指名本題。
- **驗收判準**:(1) pnpm build:pools 成功產出本題池且無錯誤;(2) pnpm test --run 全綠(challenge-params 冒煙 + content-regression 涵蓋新題);(3) pnpm typecheck 與 pnpm lint 通過;(4) 本機 pnpm dev 手動提交 deque 正解得 6/6 AC;(5) 生產建置 e2e(pnpm build + docs:preview + agent-browser):正解 6/6 AC、錯解(如輸出恆 -1)得 WA、O(n²) 扁平慢解在大 band 筆顯示 TLE。
- **範圍邊界**:只新增 docs/challenge/two-end-elimination.md 一個檔案;不修改任何既有程式、spec、既有題目;池產物與 key_material 等 gitignored 檔不進 commit。

## Risks / Trade-offs

- [慢解用 C 內建(list.pop(0)、sorted、max/min)不會 TLE] → settrace 本質限制(C 層不產生行事件),已知且接受;主防線是敘述引導用 deque,錯解典型樣態(O(n²) 純 Python 雙重迴圈)確定會 TLE。
- [大 band TLE 筆的判題耗時吃滿 op 上限,單場總時可能偏長] → staging 實測 6 筆全 TLE 約 75 秒含頁面載入、單筆在 6 秒預算內;本題正常情境只有 2 筆 TLE,總預算 36 秒(6 筆 × 6 秒)足夠。e2e 階段以實測確認。
- [學生可 import sys; sys.settrace(None) 關閉計數] → 教學平台威脅模型下接受,已記入 BACKLOG §2.8 已知限制,非本題範圍。
- [id 56 假設建檔時最大 id 仍為 55] → scaffold 由 pnpm new-challenge 自動分配 id,Step 0 已核對且本地與 remote 同步;若 scaffold 分配出不同 id,以 scaffold 為準並回頭修 spec 內的 id 敘述。

## Migration Plan

單檔新增,無遷移;rollback = 刪除 docs/challenge/two-end-elimination.md 並重跑 pnpm build:pools(cleanup 自動刪孤兒池)。

## Open Questions

(無——未決 0–3 已全部由使用者拍板。)
