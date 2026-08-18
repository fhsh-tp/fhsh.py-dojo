## Why

APCS 中級題本的能力指標是「以序列型資料結構（陣列、列表）儲存與處理資料」，檢測範圍為陣列、字元、字串。但本站現有 17 道 apcs 題全部落在同一個型態——照著規則掃過一遍序列的模擬題。掃過 17 題的 generator 後的技法分佈是：單趟掃描模擬 17 題、排序 1 題（apcs007 一次 `sorted()`）、二維陣列 0 題、前綴和／差分 0 題、雙指標／滑動視窗 0 題、頻率表計數 0 題。

也就是說，中級真正的核心——**把資料先存進陣列、再回頭整體處理**——目前沒有任何一題在練。學生就算把 17 題全解完，也不會遇到任何一次「非得先把資料收起來不可」的處境。

同時，現有題庫也缺少**效率壓力**。判題平台已具備每筆測資 5000 ms deadline 與 10,000,000 次運算上限（`openspec/specs/judge-deadline/spec.md`），有能力把 O(N²) 暴力解真的擋下來，但除了 apcs015 之外幾乎沒有題目用到這個能力。沒有效率壓力，學生會得出「我用兩層迴圈也過了啊」的結論，排序與前綴和就失去存在理由。

## What Changes

新增三道 APCS 中級素養題（`category: apcs`、`type: competition`），各補一個現有題庫完全空白的技法，且三題都設效率斷崖——暴力解在小測資拿部分分、在大測資被運算上限砍死。

- **`hall-fan-coverage`「禮堂吊扇風域」**（medium）：二維差分。題源為 CSES 1652 Forest Queries 的對偶（矩形區域加值）。禮堂地板切成 R×C 格點評估風場，F 台吊扇各覆蓋一塊矩形，問最涼的一格被幾台吹到。
- **`club-room-allocation`「社團教室分配」**（hard）：排序加 min-heap。題源為 CSES 1164 Room Allocation。N 筆社團借用申請，行政規定一律發「目前空著中編號最小」的教室，問最少要開幾間，以及每筆申請被分到哪一間。
- **`radio-relay-tape`「午間廣播接力帶」**（medium）：固定視窗加頻率表。題源為 CSES 1141 Playlist 的變形。廣播社要從點播單剪一條連續 K 首的接力帶，問有幾種剪法整條不重播。

三題共通的交付形狀：

- `testcase_plan` 20 筆階梯式，第 1 筆即題面範例，N 由小到大平滑爬升，暴力解自然死在中段，得分為部分分而非 0 分
- 每題都宣告 `reference_solution`，寫法刻意與 `generator` 不同，讓 `scripts/content-regression.test.ts` 能同時抓出兩邊各自的錯誤
- 每題都附一張說明圖，沿用 apcs013／apcs014 的既有管線（`scripts/figures/<slug>_plate.py` 產 HTML、`<slug>_plate.sh` 以 headless Chrome 轉 PNG、輸出到 `docs/public/assets/challenge/<id>/圖一.png`）
- 題面數學記號一律遵守 `openspec/specs/challenge-math-notation/spec.md` 的分類表

## Non-Goals

- 不出 APCS 中高級題型（遞迴、樹、圖、搜尋）。`club-room-allocation` 用到 `heapq` 是刻意往中高級搭的一座橋，不是把本 change 的範圍擴張到中高級。
- 不修改 Rust 測資產生引擎（crate `testcase-generator`）。引擎目前不支援「參數值域引用其他參數」，三題的輸入設計一律繞開這個限制，不為了三道題動引擎。
- 不新增教學文章。三題是純挑戰題，配套的教學章節留給後續 change。
- 不發 release。本 change 只做到 merge 進 `staging`。

## Capabilities

### New Capabilities

- `apcs-intermediate-trio-challenges`：三道 APCS 中級素養題的題面契約、測資分區與效率斷崖規範，含每題的暴力解得分、正解複雜度與輸入規模上界。

### Modified Capabilities

(none)

## Impact

- Affected specs: 新增 `apcs-intermediate-trio-challenges`
- Affected code:
  - New:
    - docs/challenge/hall-fan-coverage.md
    - docs/challenge/club-room-allocation.md
    - docs/challenge/radio-relay-tape.md
    - scripts/figures/hall-fan-coverage_plate.py
    - scripts/figures/hall-fan-coverage_plate.sh
    - scripts/figures/club-room-allocation_plate.py
    - scripts/figures/club-room-allocation_plate.sh
    - scripts/figures/radio-relay-tape_plate.py
    - scripts/figures/radio-relay-tape_plate.sh
    - docs/public/assets/challenge/apcs018/圖一.png
    - docs/public/assets/challenge/apcs019/圖一.png
    - docs/public/assets/challenge/apcs020/圖一.png
  - Modified: (none — 題目上架由既有的 category 目錄機制自動處理)
  - Removed: (none)
- 受既有守門測試涵蓋，三題都必須通過：`scripts/challenge-params.test.ts`（params 宣告冒煙）、`scripts/content-regression.test.ts`（reference_solution 與 generator 一致）、`scripts/latex-notation.test.ts`（數學記號）
- 建置期的單筆測資位元組預算會被三題觸及，`input_budget` 需自 4096 調高；硬上限 65536 不可覆寫，三題的規模上界都是從這個上限反推出來的
