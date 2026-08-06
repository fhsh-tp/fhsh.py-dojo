# dev 真機 e2e 驗證筆記 — add-bracket-check-duo

## 五路線提交實測（2026-08-06，localhost:5173，agent-browser session `e2e-bracket`）

| 路線 | 提交碼 | 預測（追溯矩陣 V） | 實測 | 命中 |
|------|--------|--------------------|------|------|
| V1 | 1a reference_solution（frontmatter 抽出） | 20/20 AC | 20/20 AC，第 20 筆 stress 41ms | ✅ |
| V2 | 1a 計數器假解（逐種計數＋不可為負） | 15/20，WA 恰第 4/9/12/15/18 筆 | 15/20，WA 恰第 4/9/12/15/18 筆 | ✅ |
| V3 | 1a replace 迴圈繞道 | 20/20 AC（收編；stress 筆牆鐘可見） | 20/20 AC，第 20 筆 3522ms、其餘 ≤6ms | ✅ |
| V4 | 1b reference_solution | 20/20 AC | 20/20 AC | ✅ |
| V5 | 1b 回頭掃描天真解 | 14/20，op 爆殺恰第 14/15/16/18/19/20 筆 | 14/20，TLE 恰同六筆（各 ~1.9s） | ✅ |

## 過程紀錄

- **A3 預測修正（重要）**：初版矩陣預測計數器假解 3/20，V1 提交後重審發現錯誤——計數器在隨機
  NG soup 上會「巧合正確」（NG 對 NG），只死於「各種類數量平衡、執行中不為負、但順序交錯」的
  策展 literal。修法：交錯陷阱從 2 筆增為 5 筆（第 4/9/12/15/18 筆，`([)]`／`[(])`／`(([))]`／
  `{[}]`／`([{)]}` 家族），先改追溯矩陣再同步 spec/design/策展腳本，重建池後 V2 實測精確 15/20。
  教訓：假解得分預測必須以「假解與正解在**每一筆**測資上的一致性」推導，不能只看首個 WA 位置。
- V3 stress 筆 Pyodide 牆鐘 3522ms；R2 以出貨 literal 重測 native 為 2.1s（原 5.5s 量自單種探針形）——
  Pyodide ≈1.7× native。收編判定改由 Pyodide 實測直接推導：即使 20 筆全 stress ≈ 70s < 120s 總預算，
  牆鐘獵殺不可行，判定不變。
- V5 op 爆殺每筆 ~1.9s 即中斷，與 rank-code 觀察一致（op counter 殺 TLE 筆的牆鐘特徵）。
- 引擎 band（enum soup）+ literal 策展混排順序正確：判題順序＝testcase_plan 宣告順序，
  literal 位置驗算（策展腳本斷言 4/9/12/15/18 陷阱位、14/15/16/18/19/20 獵殺位）與實測一致。

## 建置層驗證

- `pnpm build:pools`：64 pools、0 failed；prop-box-packing.bin 1,616,723B、magazine-typeset-check.bin 1,065,334B
- `challenge-params.test.ts` 69 passed；`content-regression.test.ts` 兩題 passed；`wrapper-content-smoke.test.ts` 15 passed（含兩新題，判題 wrapper 真路徑）

## Round 1 audit 修復後重驗（2026-08-06，兩池重洗）

R1 修復內容：1a stress 裁回深度 31000（62000 字元，ref 恰 217,022 ops 與矩陣一致）；1b 六筆獵殺重設計
（互異、lean 下限 m×2k≥20M、3 筆殘留分支答案 7/5/9）；starter 改為不輸出；1b 提醒句改窄（B10）；
C-rfind 收編（B9）；proposal/tasks prose 同步。

| 路線 | 預測 | 實測 | 命中 |
|------|------|------|------|
| V1 1a ref | 20/20 | 20/20 AC | ✅ |
| V2 1a 計數器 | 15/20，WA 恰 4/9/12/15/18 | 15/20，WA 恰同五筆（池重洗後 soup 巧合維持） | ✅ |
| V3 1a replace | 20/20 | 20/20 AC | ✅ |
| V4 1b ref | 20/20 | 20/20 AC（獵殺筆 16~20ms） | ✅ |
| V5 1b 回頭掃描 | 14/20，TLE 恰 14/15/16/18/19/20 | 14/20，TLE 恰同六筆（~1.9s） | ✅ |
| V6 1b 最精簡回頭掃描（1 op/iter，R1 新增路線） | 14/20，同六筆爆殺 | 14/20，TLE 恰同六筆（~2.8s） | ✅ |

守門：build:pools 0 failed；params 69 passed；content-regression 兩題 passed；wrapper-smoke 15 passed。

## Round 2 audit 修復後重驗（2026-08-06，兩池再重洗）

R2 修復內容：A4/A6/D3/R3 繞道數字改以出貨 literal 直接量測（replace 62,018 ops／2.1s、delfind 310,030／1.4s——
原數字量自單種探針形，複核人以 git show 證明真因為「探針形狀≠出貨形狀」）；1a 新增兩筆長交錯陷阱（第 17/19 筆，
28K/35K，counts 平衡但深處交錯）封殺「長行只比數量」混合投機；1b 六筆獵殺重構為不規則混種帶雜訊形
（殘留答案 29/27/18/23 埋 warmup 後、非公式可猜）封殺形狀偵測投機；B5 歸屬修正（reference K15=100,789、
generator 67,337）；題面三處 prose 修正（1a 空堆疊情形、1b 主句與三分支對齊、提醒句去長度因果）；
spec 無括號 literal 措辭修正；V 表補 V6–V8。

| 路線 | 預測 | 實測 | 命中 |
|------|------|------|------|
| V1 1a ref | 20/20 | 20/20 AC | ✅ |
| V2 1a 計數器 | 13/20，WA 恰 4/9/12/15/17/18/19 | 13/20，WA 恰同七筆 | ✅ |
| V3 1a replace | 20/20 | 20/20 AC | ✅ |
| V7 1a 混合投機（短行 stack＋長行比數量；R2 bounty 曾 20/20） | 18/20，WA 恰 17/19 | 18/20，WA 恰 17/19 | ✅ |
| V4 1b ref | 20/20 | 20/20 AC | ✅ |
| V5 1b 天真回掃 | 14/20，TLE 恰 14/15/16/18/19/20 | 14/20，TLE 恰同六筆 | ✅ |
| V6 1b 精簡回掃（1 op/iter） | 14/20 | 14/20，TLE 恰同六筆 | ✅ |
| V8 1b 長行跳過（len>5000 印 0；R2 bounty 形狀投機家族） | ≤16/20，14/15/18/20 必 WA | 16/20，WA 恰 14/15/18/20 | ✅ |

守門：build:pools 0 failed（1a 1,858,805B／1b 1,217,707B）；params 69、content-regression 兩題、wrapper-smoke 15 全綠。
