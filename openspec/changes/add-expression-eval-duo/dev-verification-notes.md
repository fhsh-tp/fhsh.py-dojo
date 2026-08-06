# dev e2e 驗證筆記 — add-expression-eval-duo

量測四元組：judge=本機 dev（localhost:5173，agent-browser session e2e-b）× 程式身分=design_b/{sol,bounty}/*.py（與設計期探針同檔）× 輸入=正式加密池（pnpm build:pools 後、literal 20 筆整塊）× 版本=plan_b.py seeds (1101, 1202) 賞金修補後版；出貨檔 docs/challenge/{snack-bar-register,coupon-combo-quote}.md 由 assemble_b.py 寫入（literal 位元組相等斷言通過）。

## V 表 ship-e2e 實測（2026-08-06，15 路線，逐筆核對）

### apcs011 snack-bar-register

| 路線 | 預測 | 實測 | per-entry |
|------|------|------|-----------|
| V1 ref | 20/20 | 20/20 ✓ | 全 AC（3–17ms） |
| V3 E1 swap | 20/20（收編） | 20/20 ✓ | 全 AC |
| V4 E2 std | 2/20 {2,3} | 2/20 ✓ | AC 恰 {2,3}；※worker 於 entry 17 死亡，僅 16 列詳情，總分正確定案 |
| V5 L2R | 2/20 {2,3} | 2/20 ✓ | AC 恰 {2,3}，20 列完整 |
| V11 N1 rewrite | 20/20（收編） | 20/20 ✓ | 全 AC |
| V12 R2 regexparen | 20/20（收編） | 20/20 ✓ | 全 AC |

### apcs012 coupon-combo-quote

| 路線 | 預測 | 實測 | per-entry |
|------|------|------|-----------|
| V1 ref | 20/20 | 20/20 ✓ | 全 AC |
| V2 recdesc（604 frames） | 20/20 | 20/20 ✓ | 全 AC——B6 Pyodide 遞迴深度直測二次確認 |
| V3 E1 swapleft | 1/20 {2} | 1/20 ✓ | AC 恰 {2} |
| V4 E2 std | 1/20 {2} | 1/20 ✓ | AC 恰 {2}；※同 011 的 worker 死亡現象（16 列） |
| E3-naive（b012_pow.py 檔） | 8/20 {1-8} | 8/20 ✓ | AC 恰 {1-8}，9-20 全 WA（CRASH 輸出） |
| V7 E3′ pow2 | 20/20（收編） | 20/20 ✓ | 全 AC |
| V8 divtight | 3/20 {1,2,3} | 3/20 ✓ | AC 恰 {1,2,3} |
| V9 parens-std | 8/20 {1-8} | 8/20 ✓ | AC 恰 {1-8} |
| V10 hybrid 雙路徑 | 8/20 {1-8} | 8/20 ✓ | AC 恰 {1-8}——PKline 封殺驗證成立 |

**結論：15/15 路線、每一筆 entry 判定與設計期預測零偏差。** V6（uniform mdr）無獨立路線檔，維持 design-probe 狀態（其行為已被 V8/V10 家族夾擊覆蓋）。

## 平台觀察（非本 change 缺陷，記錄供平台參考）

1. **裸 eval 深鏈導致 Pyodide worker 死亡**：V4（E2 std）在兩題的 entry 17（30KB＋、數千運算子的單行式）令 worker 無聲死亡——判題停止、後 4 筆無詳情列，但總分正確定案（後 4 筆計 0 分）。本機 CPython 跑同檔同輸入無此現象（returncode 0）。經包裝的 eval 變體（V3 swap、V7 pow2、V12 regexparen）不受影響。研判為 Pyodide/WASM 對超長運算子鏈的編譯深度限制。對本 change 零影響（該路線本來就 WA 那些筆），但 worker 死亡後續測資直接消失的行為值得平台層改善（與 C14 op 跳閘同屬 judge 強健性家族）。
2. 收編路線成本（e2e 觀察）：V3/V7/V11/V12 大型筆單筆 wall 均 < 100ms 等級，與設計期 op 量測一致，無成本警語必要。

## 建置驗證快照

- pnpm build:pools：66 pools、0 failed
- challenge-params 冒煙：71 passed（+2 題）
- content-regression：17 passed（含兩題 reference_solution 對正式池 AC）
- pnpm typecheck：0 errors；pnpm lint：0 errors（22 個既有 warnings，非本 change 引入）
