# dev 真機驗證紀錄（2026-08-05，pnpm dev + agent-browser 隔離 session）

## 提交 1：stack 正解（使用者原稿原樣，含 max 遮蔽）
結果：20/20 AC，最慢單筆 37ms（隨機壓力筆）。

## 提交 2：天真解 A（每移除從頭重掃）
結果：12/20。TLE 恰為第 11~18 筆（5 隨機壓力 + 3 巢狀 literal），每筆 ~1.7s（op-counter 於 10M 事件同步 raise）；暖身（1~10）與邊界（19~20）全 AC。斷崖精準,無誤殺。

## 提交 3：str.replace 繞法（C 內建、op-count 不可見）
- 降級前（60KB 獵殺筆仍在）：20/20 AC，第 18 筆牆鐘 6984ms > 5000ms 但 verdict AC——證實 worker 5 秒軟旗標對同步學生碼結構性失效（setTimeout macrotask 永遠輸給 await 接續 microtask 的 clearTimeout）。
- 降級後（3×20KB 巢狀 literal）：20/20 AC，最慢單筆 903ms。依 spec「Bypass acceptance after hunt downgrade」視為接受的聰明解。

## 附註
- 平台級發現：判題引擎唯一真實牆鐘為 useExecutor 6s×筆數總預算硬殺；WALL_CLOCK_MS 軟旗標對同步碼永不觸發。建議另開 change 評估（run 完成後以 elapsed 補判 TLE）。

# Audit R1 修正後複驗（2026-08-05）

R1 audit 6 findings → 12 名 opus/sonnet 對抗驗證（Workflow wf_f8765896-c5e）→ 修正 5 項、駁回 1 項（LOW-2 端點實已覆蓋）。修正後：

- 三筆巢狀 literal 改為兩兩相異（ab/cd/ef 交錯，sha256 前綴 8e8508ff/73d1935c/902c2bfe），探針複核 naive A/B 於三形狀全部 ≥6×10⁷ ops（≥6× 上限）、正解 50,005 ops。
- build:pools 重洗（2361359 bytes）、challenge-params + content-regression 全綠、spectra validate/analyze 零 critical。
- dev 三連測：正解 20/20 AC；天真解 A 12/20（TLE 恰為 11~18）；replace 繞法 20/20 AC（依 Bypass acceptance 條款）。

# Audit R2 修正後複驗（2026-08-05）

R2 fresh audit 4 findings → 8 名 opus/sonnet 對抗驗證（Workflow wf_1236e4b1-18b）→ 4 項全修（含 R2-HIGH：三筆同長同殘量 literal 可被 `len(b)==20000` 長度分支繞過）。修正內容：三筆巢狀 literal 改異長（30000/34001/38002）異殘量（0/1/2，哨兵字母）；input_budget 65000→42000；spec 驗證 scenario 改述實際閘門（確定性抽樣＋wrapper 冒煙＋人工補驗）；BACKLOG §2.8 就地訂正牆鐘軟旗標失效。

- 探針：天真 A/B 於三筆新 literal 全部 ≥2.5×10⁷ ops（≥2.5× 上限）；正解 75k/85k/95k ops。
- build:pools（2814650 bytes）、challenge-params ＋ content-regression 全綠、spectra validate/analyze 零 critical。
- dev 五連測：正解 20/20 AC；天真 A 12/20（TLE 11~18）；天真 B 17/20（TLE 16~18，僅巢狀筆——符合 spec 條款 (b)）；**長度作弊解（len>=20000→print 0）13/20**：隨機壓力筆 WA×5、異殘量筆 WA×2、僅殘量恰為 0 的 lit1 僥倖 AC——R2-HIGH 攻擊確認已封；replace 繞法 20/20 AC（巢狀筆 1.7s/2.3s/3.2s，整批 ~7.3s ≪ 120s）。
- content-regression 未覆蓋的 plan 位置（0、17、18、19 等）已由上述 dev 全 20 筆判題實測覆蓋（每次提交跑滿 20 筆，含全部 literal）。
