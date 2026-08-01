## Why

deque 系列目前只有第一題 id 55「撲克牌重排計數」(hard)。系列需要第二題,教學生用 `collections.deque` 的雙端操作解「找最大最小值」——它是兩輪測資引擎工作(group/`count.from` 引擎升級 PR #13、testcase_plan 測資分區 PR #14)與判題引擎雙缺口修復(op-counter 扁平盲區 + TLE verdict,PR #15)的共同北極星:第一個同時使用 band 分區與 TLE 效能區分的正式題目。三項前置均已 merge 進 staging 並完成部署驗證,現在是出題時機。

## What Changes

- 新增題目 `docs/challenge/two-end-elimination.md`(id 56、title「兩端淘汰賽」、difficulty medium、type competition、tags 含 data structure 與 deque、starter_code 空字串、無 chapter、無 verdict_detail(採預設 hidden)、無 testcase_count(與 testcase_plan 互斥))。
- 輸入格式:第一行整數 T(2..3);每筆測資第一行整數 Ni,接 Ni 行、每行一個整數(-999..999)。輸出:每筆一行「max min」(先 max 後 min,空格分隔),共 T 行。
- params 用 group 語法(cases 以 repeat: t 重複;nums 以 count.from: n、separator 換行);input_budget 65535。
- testcase_plan 三個 band、總 6 筆:小 band count 3(n 上限收到 20,驗邏輯)、大 band count 2(n 下限拉到 2500,讓純 Python O(n²) 解超過 10M op 上限吃 TLE)、邊界 band count 1(n min=max=1,保證每場出現單元素、max==min 的邊界,值隨機)。總數 6 ≠ 預設 5,兼作 e2e 消歧。
- generator 用內建 max()/min() 產期望輸出;reference_solution 用教法「兩端淘汰賽」的 deque 實作(比較 d[0] 與 d[-1]、pop 掉輸的一端;複製一份 deque,max/min 各跑一輪)——與 generator 寫法刻意不同,content-regression 測試自動驗證教學演算法正確性。
- 敘述結構照系列第一題 card-restack-count.md 樣式(題目說明、動手推演、輸入說明、輸出說明、範例),敘述引導使用 deque(平台無 AST 檢查,靠敘述引導),並預告大測資會讓過慢的寫法超時。

## Capabilities

### New Capabilities

- `deque-challenge-series`: deque 系列題目的內容契約——本題(兩端淘汰賽)的輸入/輸出格式、testcase_plan 分區結構、generator 與 reference_solution 分工、敘述教學要素。

### Modified Capabilities

(none)

## Impact

- Affected specs: 新增 `deque-challenge-series`;不修改 testcase-plan、python-generator、challenge-exercise-type、verdict-detail-control(本題僅為其使用方)。
- Affected code:
  - New: docs/challenge/two-end-elimination.md
  - Modified: (無——scaffold 由 pnpm new-challenge 產生新檔,不改既有程式)
  - Removed: (無)
- 建置產物:pnpm build:pools 會為新題產生加密池(gitignored,不進 commit);scripts/challenge-params.test.ts 冒煙與 content-regression 測試自動涵蓋新題。
