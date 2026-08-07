## Why

批次計畫（2026-08-06 grilling Q1–Q9）的 change C：題 4「展場動線重建」與題 5「彈珠台軌道預測」。前者練「已知兩種走訪紀錄還原第三種」，後者練「不逐一模擬、直接由編號推路徑」，兩題並置形成「重建 vs 不用重建」的對照教學。APCS 題庫目前只到 apcs012，本 change 補上 apcs013／apcs014。

設計期量測推翻了 grilling 期對題 4 的附帶假設（原以為 `list.index()` 的 O(n²) 天真解會撞 op 上限）：`.index()` 與 slicing 的重活全在 C 層，op 計數器抓不到；輸入預算又把序列長度卡在 6000 以內，實測最壞情形只有 60,024 ops／715 ms。因此題 4 的鑑別軸改為語義（雙模式、非排序標號、不對稱形狀），題 5 保留 op 斷崖軸，兩題各自承擔一個教學重點。

## What Changes

- 新增 `docs/challenge/exhibit-route-rebuild.md`（apcs013，medium，competition）：兩種打卡紀錄還原第三種，模式 1（甲＋乙→丙）佔前 10 筆、模式 2（乙＋丙→甲）佔後 10 筆，每筆測資自帶模式標記。
- 新增 `docs/challenge/pinball-track-predict.md`（apcs014，hard，competition）：D 層機台（第 1..D−1 層翻板、第 D 層袋子），預測第 I 顆彈珠落入哪個袋子；球數可超過袋數（機台狀態有週期），前 14 筆測資逐球模擬可過，後 6 筆的總球數大到任何逐球寫法都會跳閘。
- 兩題皆以 20 筆全 literal `testcase_plan` 出貨（走訪紀錄與翻板狀態無法由隨機 band 產生合法輸入），皆宣告 `reference_solution` 並納入 content-regression。
- 策展證據四件套（規劃腳本、語義正本、組裝腳本、量測報告）隨 change 入庫，可搬移重跑並逐 byte 重現出貨 literal。

## Non-Goals

- 不建 apcs013 的 TLE 斷崖：C 層繞道實測不可獵殺，依守則⑤收編為聰明解，題面不寫任何「不可能」句。
- 不獵殺 apcs014 的兩條收編路線（逐層計數 O(2^D)、先取週期再模擬）：兩者語義正確，殺手筆的「小 D 大球數」組成與週期內球數上限即由此推得。
- 不調整判題引擎、op 上限或牆鐘常數。設計期賞金另外確認兩件平台層事實，皆記錄於矩陣並留待獨立 change：op 計數以 source line 為單位（同行攤平可壓低成本）、`testcase_plan` literal 會進入生產 bundle（且 repo 本身公開）。
- 不動既有題目與既有 spec。

## Capabilities

### New Capabilities

- `route-rebuild-challenge`: apcs013 的 I/O 契約、測資計畫、錯誤路線防禦與效能包絡
- `ball-drop-challenge`: apcs014 的 I/O 契約、測資計畫、op 斷崖與收編處置

### Modified Capabilities

(none)

## Impact

- Affected specs: `route-rebuild-challenge`（新增）、`ball-drop-challenge`（新增）
- Affected code:
  - New: `docs/challenge/exhibit-route-rebuild.md`, `docs/challenge/pinball-track-predict.md`, `openspec/changes/add-exhibit-route-duo/trace-matrix.md`, `openspec/changes/add-exhibit-route-duo/curation/`
  - Modified: (none — 兩題各自獨立檔案，題庫頁由 VitePress 自動彙整)
  - Removed: (none)
