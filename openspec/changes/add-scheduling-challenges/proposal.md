## Why

題庫目前缺「排程/資源指派」類的素養題:學生練過單資料流模擬(deque 系列 id 56)後,沒有題目訓練「多資源狀態維護」與「事件驅動思維」這兩個 APCS 常考核心。本 change 以 2022 運算思維推動計畫「工作中的海狸」與 UVa 1203 (Argus) 為藍本,新增兩道素養導向排程題,並沿用 testcase_plan 既有機制(band 分區 + literal 邊界),不動任何引擎程式碼。

## What Changes

- 新增題目一「列印工坊排程」(slug `print-farm-schedule`,medium/competition):m 台印表機、n 張工單依序派給最早空閒機台(同時空閒→編號小者),輸出全部完工時刻(makespan)。
- 新增題目二「智慧藥盒提醒」(slug `pillbox-reminder`,hard/competition):Q 種藥各有提醒週期(隱含編號 1..Q),輸出最先觸發的 K 次提醒的藥品編號(同時刻→編號小者先),一行一個。
- 題目二以 testcase_plan 壓力 band 淘汰「逐分鐘掃時間軸」解法(TLE),放行「線性掃下次觸發時刻」與 heapq 事件式解法——對齊 UVa 1203 原題定位;壓力 band 上界以 op 探針實測後定案。
- 兩題題面皆為素養導向:僅描述現實世界的處理模式(自動派單系統/藥盒提醒規則),全文與 tags 不出現任何解法字眼(排序、佇列、heap、掃描時間軸等)。
- 兩題皆宣告獨立寫法的 reference_solution(generator 與 reference 分別採掃描/heapq 兩種實作互驗)。

## Capabilities

### New Capabilities

- `scheduling-challenge-series`: 排程系列題的規範語義——題目一派工規則與 makespan 輸出、題目二週期事件序列輸出、tie 規則、輸入格式契約、testcase_plan 分區與效能門檻定位。

### Modified Capabilities

(none)

## Impact

- Affected specs: 新增 `scheduling-challenge-series`;不修改既有 spec(`testcase-plan`、`deque-challenge-series` 僅作為機制與前例引用,零需求變更)。
- Affected code:
  - New: docs/challenge/print-farm-schedule.md、docs/challenge/pillbox-reminder.md
  - Modified: (none)——純內容新增,Rust 引擎、scripts、前端零改動
  - Removed: (none)
- 建置影響:pnpm build:pools 會為兩題各產生加密池(每場 6 筆、floor(200/6)=33 blocks);兩題 params 僅用 int + count.from,worst-case 皆低於預設 input_budget 4096,無需調整。
