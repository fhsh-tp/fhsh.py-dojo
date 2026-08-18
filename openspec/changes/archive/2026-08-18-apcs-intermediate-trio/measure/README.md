# 量測記錄導覽

先讀這一段再引用任何數字。本目錄同時放著**權威量測**與**已被取代的代理量測**，混用會得到錯誤結論——本 change 進行中已經因此走了兩次冤枉路。

## 權威：瀏覽器實測

| 檔案 | 內容 |
|------|------|
| `browser-cliff.json` | 三題所有解法的得分、逐筆 verdict、逐筆耗時。**規格與設計文件引用的所有分數都出自這裡。** |
| `browser-cliff.jsonl` | 上表的原始逐次輸出，每行一次提交 |
| `figure-readability.json` | 三張說明圖在 1728 與 1280 兩種視窗下的渲染寬度與最小字級 |
| `traceability-check.json` | 規格追溯矩陣三列與 `browser-cliff.json` 的逐列對帳 |
| `gates.txt` | `pnpm typecheck`、`pnpm lint`、`vitest --run` 的完整輸出 |

量測環境是 `pnpm preview:cf`（`wrangler pages dev .vitepress/dist --port 8788`）。**必須走這條路徑**：只有它送出 COOP 與 COEP 標頭，沒有這兩個標頭時 `SharedArrayBuffer` 不存在，每筆測資的 5000 ms deadline 會靜默失效，量到的會是錯的量。理由寫在 `docs/public/_headers` 的註解裡。

## 代理：本機運算計數

| 檔案 | 內容 |
|------|------|
| `cliff-hall-fan-coverage.json` | 本機 CPython 以 `sys.settrace` 計行事件的逐筆 ops |
| `cliff-club-room-allocation.json` | 同上 |
| `cliff-radio-relay-tape.json` | 同上。**參數已變更，此檔內容已被取代**——產生時歌曲編號值域是 10⁶，定稿是 4×10⁶ |
| `verify-*.py`、`crossblock-*.py`、`gen-*.mjs`、`gen-*.mts` | 產生上述代理量測的腳本 |

**這些數字不是分數，不得當作分數引用。** 判題器的運算計數器計的是 Python 層 trace event，因此對兩件事是瞎的：C 內建裡的工作（不論處理多少元素都只記一個 event），以及原始碼排版（把迴圈本體折到迴圈那一行，每次迭代的計數就從三個變成一個，而程式一點也沒變快）。本 change 兩度依據這些代理數字下結論，兩度被瀏覽器實測推翻。

它們保留下來的用途只有一個：在進瀏覽器實測之前，先篩掉明顯不成立的規模設定。

## solutions/

`solutions/` 底下是所有送進瀏覽器量測的解法檔，包含每題的 `generator`、`reference_solution`，以及各種拼法的暴力解。檔名對應 `browser-cliff.json` 裡的 label。

重跑方式：

```bash
pnpm build            # 或至少 build:pools + docs:build
node_modules/.bin/wrangler pages dev .vitepress/dist --port 8788 --compatibility-date=2026-08-11
BASE=http://localhost:8788 zsh ./measure.sh <slug> solutions/<file>.py <label>
```

`measure.sh` 取自 `2026-08-15-add-counting-trio`，未改動。它每一步都帶失敗訊號，特別是「貼上程式碼後檢查編輯器長度」那一項——本站有題目的 `starter_code` 是空字串，沒有這個檢查的話，貼上失敗與貼上成功產生的畫面完全一樣。
