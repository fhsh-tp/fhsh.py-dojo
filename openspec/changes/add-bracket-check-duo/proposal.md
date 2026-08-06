## Why

批次「六題 stack／tree 素養題」的 change A：以 UVa 673 為原型出括號配對雙題（追溯矩陣 C1）。1a 考「配對驗證」的正確性陷阱（計數器假解自第 4 筆起 WA，矩陣 A3），1b 以「首錯位置」語義結構性封殺字串刪除類繞道並建立 op counter 真 TLE 斷崖（矩陣 B1/B4/B6）。兩題皆為生活素養情境、題面不出現資料結構術語。

## What Changes

- 新增挑戰 1a `prop-box-packing`「道具箱裝箱檢查」（apcs、competition、medium，矩陣 C1/C2）：T 場開/封箱紀錄，逐場輸出 `OK`／`NG`（矩陣 C7/A1/A2）。
- 新增挑戰 1b `magazine-typeset-check`「校刊排版檢查器」（apcs、competition、medium，矩陣 C1/C2）：混雜訊稿件行，輸出第一個無法配對字元的 1-based 位置或 0（矩陣 B1/B2/B3）。
- 兩題各 20 筆 `testcase_plan`：括號種類三段分區（1–3 筆 `()`、4–12 筆 `()[]`、13–20 筆 `()[]{}`，矩陣 C5）、第 1 筆 literal＝題面範例（C6）、`input_budget: 63488`（C4）。
- 1a：第 4 筆交錯陷阱 literal、第 20 筆 62KB 深巢 stress literal；C 繞道（replace／find+切片）依探針量化證明不可獵殺，收編為 accepted alternative，題面不寫不可能性承諾（矩陣 A3/A4/A6）。
- 1b：6 筆 12KB 獵殺 literal（第 14/15/16/18/19/20 筆），回頭掃描天真解逐筆 op 爆殺、預測 14/20（矩陣 B4）。
- 兩題皆附獨立寫法的 `reference_solution`，由 content-regression 驗證（矩陣 C9）。

## Non-Goals

- 不改動 Rust testcase-generator 引擎（相關性輸入以 literal 策展＋enum soup band 解決，矩陣 C8）。
- 不出批次題 2–5（表達式雙題、tree 雙題為後續 change B/C）。
- 不處理平台層「總預算硬殺截斷式 UI」既有議題（BACKLOG §2.8 同族）。
- 題面不含任何 stack／堆疊／資料結構術語（批次共通要求）。

## Capabilities

### New Capabilities

- `bracket-check-challenges`: 括號配對雙題（1a 驗證版、1b 首錯位置版）的題目內容、測資分區、判題預測與繞道處置規格。

### Modified Capabilities

(none)

## Impact

- Affected specs: `bracket-check-challenges`（新增）
- Affected code:
  - New: docs/challenge/prop-box-packing.md、docs/challenge/magazine-typeset-check.md
  - Modified: （無——scaffold 自動配號不改既有檔）
  - Removed: （無）
