## Context

雙題係 UVa 568／10212 的素養轉譯（同一「遊戲排行榜」宇宙）。所有數據主張的單一真相來源為 `trace-matrix.md`；設計期探針（2026-08-06，本機 CPython 3.13.11；Pyodide 0.29.3 同為 3.13，牆鐘另乘 2~4 保守係數）關鍵數據：

| # | 量測 | 數值 | 矩陣 ID |
|---|------|------|---------|
| 1 | op counter 上限／C 內建可見度 | 10M 全事件；math.factorial 整段查詢僅 13 ops（隱形）。例外：CPython 3.12+ 巨數整除落回 `_pylong` 會被計數（對獵殺有利） | F1 |
| 2 | 可靠牆鐘 | 僅總預算硬殺（6s×筆數；20 筆＝120s）；單筆軟旗標對同步碼失效 | F2 |
| 3 | 大數 str() 上限 | int_max_str_digits=4300 → ValueError | F3 |
| 4 | 568 出貨 reference ops（T=500、maxN=200k，逐字實測） | 同值角落 1,555,994／異值角落 1,555,807（餘裕 6.4×） | F5 |
| 5 | 568 天真解 ops | 前 20 筆查詢 10.7M 已破限；500 筆外推 ~268M | F6 |
| 6 | 568 繞道牆鐘 | math.factorial 逐查詢 ~142s native（×2~4 後 ≥2× 總預算） | F7 |
| 7 | 10212 出貨 reference ops（T=3、M=100k，逐字實測） | 2,325,034（餘裕 4.3×） | F10 |
| 8 | 10212 繞道牆鐘 | 大數連乘 8.5s＋逐位剝零 21.0s native／重案；str() 路線 ValueError | F11 |
| 9 | 演算法正確性 | 568 增量表 vs 暴力 1..2000 全吻合；10212 vs 暴力 3000 隨機＋6 定向案例全吻合 | F8、F13、F15 |

## Goals / Non-Goals

- Goals：兩題上架（medium／hard）、TLE 斷崖可靠（op counter 為主）、繞道必死（總預算硬殺為輔）、素養題面零資料結構術語。
- Non-Goals：見 proposal；另不保證「所有想像得到的 C 隱形寫法」都死——驗收以 design 列舉的繞道清單為準（見 D6 與 Risks）。

## Decisions

### D1 考點轉譯與語義

（追溯矩陣：F8、F13、F15、F16、F17）

- `rank-code-backfill`（medium）：每天 N 名玩家的完整名次排列方式數 N×(N−1)×…×1，「驗證碼」＝該數去掉尾端所有 0 後的最後一位。一次回填 T 天。錨點：N=5 → 120 → 碼 2；N=1 → 碼 1。
- `prize-order-code`（hard）：全球賽季 N 個帳號取前 M 名的頒獎順位可能數 N×(N−1)×…×(N−M+1)，同樣取驗證碼。錨點：P(10,2)=90 → 9；M=0（空乘積）→ 1；P(10⁹,1) → 1；P(25,1) → 5（5 因子過剩）。
- 題面用「檢查碼」素養引言（ISBN／身分證末碼），全程不出現資料結構或演算法術語；乘積以展開式呈現。

### D2 斷崖機制對映

（追溯矩陣：F1、F2、F5、F6、F10、F12）

可靠 TLE＝Python 層迭代次數差：
- 568：天真解 O(T×N)（重案 20 筆查詢即破 10M）vs 正解 O(maxN+T)（出貨 reference 1.56M）。
- 10212：天真解 O(N)（自中段 band 底 N=10⁷ 起破限，壓力 band N ≥ 10⁸ → ≥4.55×10⁸ ops）vs 正解 O(T×M)（出貨 reference 2.33M）。
- 正解 op 餘裕下限定為 4×（門檻 ≤2.5M＝上限/4；出貨 reference 逐字實測 6.4×／4.3×。R1 裁決由 limit/5 修正：門檻意圖是「學生形狀的正確解永不接近 10M」，多行迴圈體的真實代價 7.75 ops/iter 下，肥大 2× 的正解變體仍 ≤5M、距上限 ≥2×）；天真解在斷崖筆需 ≥2× 上限（實測遠超）。

### D3 參數與範圍

（追溯矩陣：F4、F9、F14）

- 568：`t` int 1..500；group repeat t { `n` int 1..200000 }。輸入 worst-case ~3504 bytes，input_budget 於 apply 期以引擎估算校準（預設 4096 預期足夠，不足則調升）。
- 10212：`t` int 1..3；group repeat t { `n` int 100000..1000000000；`m` int 0..100000 }。M ≤ N 由值域構造保證（N_min=100000＝M_max）；小 N 案例（如 P(25,1)）一律走 literal。
- 輸出契約：兩題皆輸出 T 行，每行一個 1..9 的數字（10212 的 M=0 行輸出 1）。

### D4 testcase_plan 結構

（追溯矩陣：F16 配分慣例、F18、F12）

兩題各 20 筆＝範例 literal（第 1 筆）＋暖身 band＋中段 band＋壓力 band＋邊界 literal：暖身 band（小值域，天真解可得部分分）；中段 band 兩題角色**不對稱**（F18、F12）——568 為 T 20..40×N 1000..20000，天真解最貴角落 4.44M ops 仍過、屬部分分過渡層；10212 為 N 10⁷..10⁸×M 1000..50000，全範圍天真解自此層即破 op 上限、屬斷崖前緣；壓力 band（斷崖筆：568 為 T 400..500×N 150000..200000；10212 為 N 10⁸..10⁹×M 80000..100000）；邊界 literal（568：N=1、N=200000 恰界；10212：M=0、P(25,1)=5、P(26,2)=5、M=100000 恰界＝N 同值全乘）。斷崖筆數 ≥6，使繞道總牆鐘遠超預算（D6）。

### D5 演算法契約

（generator 與 reference_solution 皆遵循；追溯矩陣：F8、F13）

- 568 增量表：維護 r＝去除 2、5 因子後的乘積 mod 10 與 twos＝2 因子盈餘；lnz(n)＝r×2^twos mod 10（twos>0）或 r（twos=0）。階乘恆有 twos ≥ 0。
- 10212 區間積：須能判定 2 對 5 因子盈餘的符號（分開計數 c2/c5 或單一淨差 bal 皆為合法實作）；盈餘>0 → r×2^盈餘 mod 10；<0 → 答案必為 5；=0 → r。M=0 → 1。
- generator 與 reference_solution 須為獨立寫法（例如一方分開追蹤 c2/c5、另一方以週期表還原），皆通過 content-regression。

### D6 繞道獵殺驗收

（追溯矩陣：F2、F3、F7、F11）

列舉繞道與死法（apply 期逐條實測記入 dev-verification-notes）：
- 568 逐查詢 math.factorial＋一次除尾零：斷崖筆總牆鐘 ~142s native ≥2× 總預算 → 硬殺。
- 10212 大數連乘後 str().rstrip('0')：踩 4300 位上限 ValueError → RE。
- 10212 大數連乘後逐位 //10 剝零：單重案 ~30s native，≥2 重案即 ≥2× 總預算 → 硬殺。
- 10212 math.factorial(N)//math.factorial(N−M)：N ≥ 10⁸ 時記憶體／牆鐘災難 → 硬殺或 worker 崩潰。

## Implementation Contract

1. 兩題以 `pnpm new-challenge` scaffold（apcs／competition），id 由腳本配號，slug 分別為 rank-code-backfill、prize-order-code。
2. frontmatter 依 D3 宣告 params 與 testcase_plan（D4）；`input_budget` 以引擎 worst-case 估算值設定並實測 build:pools 通過。
3. generator／reference_solution 依 D5；`node_modules/.bin/vitest --run scripts/content-regression.test.ts` 與 `scripts/challenge-params.test.ts` 全綠。
4. 判題斷崖驗證：以 settrace 同款計數器實測「正解／天真解／繞道」三類在正式測資輸入下的 op 數與 native 牆鐘，符合 D2／D6 門檻，數據記入 dev-verification-notes.md。
5. 題面（D1）：含檢查碼引言、輸入／輸出說明、範圍（明示 T、N、M 上限與「部分測資的數字非常大」）、範例＝testcase_plan 第 1 筆 literal，逐字一致。

## Risks / Trade-offs

- 若學生的「正解」實作常數項異常肥大（>10 ops/迭代），在壓力 band 有機會逼近 op 上限——以正解餘裕 ≥4×（D2）與 audit 期第三方實作覆測緩解。
- 繞道獵殺依賴總預算硬殺：若未來 useExecutor 預算公式改動，斷崖對繞道的殺傷力需重驗——已在 dev-verification-notes 留數據基準；此依賴不寫成全稱保證，驗收僅覆蓋 D6 列舉清單。
- 10212 的 band 不含小 N（M ≤ N 由值域構造保證），若日後有人把 N_min 調小而未同步 M_max，會產生 M > N 的非法輸入——D3 已將此耦合寫明，challenge-params 冒煙測試會在值域改壞時指名失敗。
