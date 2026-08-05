## Why

APCS 素養題庫（apcs001~005）已涵蓋堆疊回數、緩衝稽核、排程、收卷驗證等主題，尚缺「一次掃描＋暫存末端比對」（消除連鎖）型的效率門檻題。使用者（出題老師）已透過 grilling 完成九項設計拍板：以二消寶石遊戲測試情境包裝「移除相鄰重複後比較遺留長度」語義，並要求純 Python O(n²) 解必 TLE、O(n) 解穩過。探針實測已證明：隨機測資殺不死逐趟式天真解，必須以巢狀對消 literal 補殺；str.replace 類 C 內建繞法經 dev 實測確認無法以現有判題機制攔截（牆鐘軟旗標對同步碼結構性失效），依降級條款放行。

## What Changes

- 新增挑戰題 `docs/challenge/gem-blast-playtest.md`（scaffold 配號 apcs006、medium、competition、algorithm `gem_blast_playtest`）。
- 題面：消除遊戲測試員素養情境——一列寶石相鄰兩顆同色互消、兩側靠攏可連鎖；每場測試 N 個版面，回報最卡關版面（剩餘顆數最大值）；共 T 場。全文、tags、description 零資料結構術語。
- 輸入結構：第一行 T；每場第一行 N、接著 N 行小寫字母字串（group + count.from 三層結構）。輸出 T 行整數。
- `testcase_plan` 20 筆：1 範例 literal 置首（＝題面範例一，含全滅→0 版面）＋9 暖身 band＋5 隨機壓力 band（T=1、N=1、L 30000..40000）＋3 筆兩兩異長異殘量巢狀對消 literal（30000/34001/38002、殘量 0/1/2）＋2 邊界 literal（單顆→1、多版面全滅→0）。`input_budget: 42000`。
- generator＝stack 掃描解（暫存末端比對，聚合變數名 best）；`reference_solution`＝雙指標陣列版（預配 buf＋top 索引），實作路徑獨立以互抓錯。starter_code 空字串。
- 驗證含：3000 組隨機雙實作互驗、TLE 斷崖探針複核（天真解 ≥2× 超限、正解餘裕 ≥50×）、dev 真機實測 replace 繞法（實測已定案：牆鐘軟旗標對同步碼結構性失效，60KB 獵殺筆依降級條款改為第三筆 20KB literal，繞法放行；細節見 design Decisions 2）。

## Non-Goals

- 不改動判題引擎、Rust testcase-generator、op-counter 或牆鐘機制（若 60KB 獵殺筆實測無效，接受 replace 繞法放行，不為此開引擎工事）。
- 不攔截 C 內建繞法（op-counter 對 C 隱形、牆鐘軟旗標對同步碼失效皆為既知結構性限制；replace 繞法視為接受的聰明解）。
- 不新增教學文章、不改挑戰列表頁（/apcs-challenges 由 frontmatter 自動收錄）。

## Capabilities

### New Capabilities

- `gem-blast-challenge`: gem-blast-playtest 題目的內容契約——消除語義、輸入輸出格式、素養情境約束（禁資料結構術語）、20 筆 testcase_plan 組成、TLE 斷崖驗收門檻、generator/reference 分工。

### Modified Capabilities

(none)

## Impact

- Affected specs: 新增 `gem-blast-challenge`
- Affected code:
  - New: docs/challenge/gem-blast-playtest.md
  - Modified: openspec/BACKLOG.md（§2.8 補 2026-08-05 牆鐘軟旗標失效實測更正，audit R2 要求）
  - Removed: (none)
