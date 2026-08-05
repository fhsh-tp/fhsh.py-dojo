## Why

1. 題庫的 APCS 競賽題目前集中在字串模擬與排程類，缺「數值素養」題型。經典的 UVa 568／10212（N! 與 N!/(N−M)! 的末位非零數字）在 C 語言考溢位處理，但 Python 大數天生不溢位，考點需要轉譯（追溯矩陣 F16 情境拍板）：568 轉譯為「別重複計算」（多筆查詢共用一次預計算）、10212 轉譯為「只留必要資訊」（大數不會溢位，但會把程式拖死——只保留答案需要的尾端資訊）。
2. 判題平台的 TLE 機制以 Python 層 op counter 為主（上限 10M，C 內建隱形，F1）、總預算牆鐘硬殺為輔（F2），兩題的斷崖設計均已在設計期探針取得確定性數據（F5–F7、F10–F12）。

## What Changes

- 新增兩道 apcs／competition 題目，同一個「遊戲排行榜」宇宙（F16、F17）：
  - `rank-code-backfill`「每日榜單驗證碼回填」（medium）：T 筆查詢（T ≤ 500），每筆求 N! 去尾零末位（N ≤ 200000）。正解一次增量建表 O(maxN+T)（1.31M ops，餘裕 7.6×，F5）；逐查詢重算的天真解 20 筆查詢即破 op 上限（F6）；逐查詢 math.factorial 繞道死於總預算硬殺（F7）。
  - `prize-order-code`「頒獎順位驗證碼」（hard）：T ≤ 3 筆查詢，每筆求 N×(N−1)×…×(N−M+1) 去尾零末位（N ≤ 10⁹、M ≤ 100000）。正解 O(M) 區間模運算（1.67M ops，餘裕 6.0×，F10）；1..N 全乘天真解 op 必破限（F12）；大數連乘繞道死於總預算硬殺、str() 路線踩 4300 位上限 ValueError（F3、F11）。
- 兩題皆用 `testcase_plan`（band＋literal）做 APCS 式配分與斷崖，第一筆 literal＝題面範例；10212 版以 literal 覆蓋 5 因子過剩陷阱（F13）與 M=0 邊界（F15）。
- 兩題皆宣告獨立實作的 `reference_solution` 接受 content-regression 驗證。

## Non-Goals

- 不動判題引擎與 worker（牆鐘軟旗標失效為既知平台議題，屬 `openspec/BACKLOG.md` §2.8，不在本 change 修）。
- 不新增 Rust 端 params 能力（現有 int／group／literal 足夠，F4、F14）。
- 不出 O(log N) 公式解法的變體（難度超出高中生課程目標，討論串已否決）。

## Capabilities

### New Capabilities

- `rank-code-challenges`: 「遊戲排行榜驗證碼」雙題（rank-code-backfill＋prize-order-code）的題目契約、判題斷崖與素養包裝規格。

### Modified Capabilities

(none)

## Impact

- Affected specs: `rank-code-challenges`（新增）
- Affected code:
  - New: docs/challenge/rank-code-backfill.md, docs/challenge/prize-order-code.md
  - Modified: (none)
  - Removed: (none)
