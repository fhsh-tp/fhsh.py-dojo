## 1. Scaffold 與 frontmatter 元資料

- [x] 1.1 以 pnpm new-challenge two-end-elimination --title "兩端淘汰賽" --difficulty medium --type competition 產生 docs/challenge/two-end-elimination.md,id 由 scaffold 自動分配(預期 56 = 現有最大 55 + 1)。驗證:檔案存在、layout challenge、algorithm two_end_elimination、id 為全站唯一且等於現有最大 id + 1。
- [x] 1.2 依 design「testcase_plan 三 band 結構與數值」改寫 frontmatter:刪除 scaffold 預設 testcase_count;params 用 group 語法(t: int 2..3;cases: group repeat t,內含 n: int 1..4000、nums: int -999..999 count from n、separator 換行);input_budget 65535;testcase_plan 依序三條 band(count 3 override cases.params.n.max 20;count 2 override cases.params.n.min 2500;count 1 override cases.params.n.min 1 與 max 1),總 6 筆、無 literal(落實 spec「Banded testcase plan with six testcases」)。驗證:pnpm test --run 的 scripts/challenge-params.test.ts 冒煙對本題無未知型別/欄位錯誤,且 frontmatter 無 testcase_count、無 verdict_detail。
- [x] 1.3 依 design「frontmatter 元資料沿用系列與全站慣例」補齊其餘欄位:tags 為 data structure 與 deque、description 一句話、無 chapter、starter_code 空字串;generator 用內建 max()/min()——讀 T,逐筆讀 Ni 與 Ni 個整數後 print(max, min)(先 max 後 min、空格分隔,落實 spec「Competition-style input and output format」)。驗證:逐欄對照 design Implementation Contract 的資料形狀清單,全部相符。
- [x] 1.4 依 design「教法採兩端淘汰賽、reference_solution 與 generator 分工」撰寫 reference_solution:collections.deque 兩端淘汰賽(比較 d[0] 與 d[-1]、pop 掉輸的一端,剩最後一個是答案;複製一份 deque,max 與 min 各跑一輪),與 generator 寫法刻意不同(落實 spec「Generator and reference solution division of labor」)。驗證:pnpm test --run 的 content-regression 涵蓋本題且通過(deque 解輸出與 generator 期望輸出在正式池樣本一致)。

## 2. 題目敘述

- [x] 2.1 依 design「敘述結構照系列第一題樣式」撰寫題目本文:結構照 card-restack-count.md(題目說明、動手推演、輸入說明、輸出說明、範例);動手推演以小例(含負數)逐步走兩端淘汰賽;敘述明確引導使用 collections.deque;預告大測資會讓過慢的寫法超時(不承諾具體筆數位置);輸出順序先 max 後 min;範例與動手推演的比較方向(>= 或 <=)前後一致。驗證:逐項對照 spec「Two-end elimination challenge content」requirement 的敘述要素清單,並人工核算範例的 max/min 答案正確。

## 3. 建置與本機驗證

- [x] 3.1 pnpm build:pools 成功為本題產出加密池。驗證:指令 exit 0、輸出無本題錯誤,docs/public/pools/ 出現本題池檔(gitignored,不進 commit)。
- [x] 3.2 全套檢查通過:pnpm test --run、pnpm typecheck、pnpm lint 三者 exit 0。驗證:指令輸出全綠,content-regression 與 challenge-params 均涵蓋本題。
- [x] 3.3 pnpm dev 啟動本機站,以 agent-browser 提交 reference_solution 同款 deque 正解,得 6/6 AC(6 筆 ≠ 預設 5,同時證明判題走 testcase_plan 路徑)。驗證:結果面板顯示 結果:6 / 6 通過,verdict 全 AC。

## 4. 生產建置 e2e(PR 前必做)

- [x] 4.1 pnpm build + pnpm docs:preview 起生產建置,以 agent-browser 對本題執行三場景:deque 正解 6/6 AC;錯解(輸出恆為 -1)得 WA 非 AC;純 Python O(n²) 扁平雙重迴圈慢解在大 band 2 筆顯示 TLE(驗收 spec「Performance separation between deque solution and quadratic solution」)。驗證:agent-browser snapshot 的 verdict 統計逐場相符(正解 AC×6;慢解含 TLE×2)。
