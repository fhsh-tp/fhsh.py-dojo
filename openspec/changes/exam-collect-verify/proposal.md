## Why

APCS 挑戰系列已有 id 55《撲克牌重排計數》問「兩端抽出疊放的結果總數」，但缺少驗證向的姊妹題：給定具體的最終堆疊，判斷它是否可能產生。此題型直接對應 deque 兩端操作的核心素養，且能以 TLE 極限測資逼出「從全枚舉走向線性判定」的演算法升級，是 2026-08-04 八題 grilling 討論（含 6 席對抗驗證 wf_85a29712-d89）定案的成果。

## What Changes

- 新增挑戰題《收卷順序驗證》（`docs/challenge/exam-collect-verify.md`，id 由 scaffold 自動配發，預期 59）：medium／competition／apcs，素養情境為「兩位監考老師從一排座位兩端收卷疊成一疊，驗證 M 份『由頂到底』回報的真偽」，全程不出現 deque／stack 術語。
- 判定語意：回報反轉為收卷順序後，對來源做雙指標兩端貪婪比對；同排座號互不相同（題面明文保證），貪婪在此前提下嚴格正確。
- testcase_plan 共 20 筆：範例 literal 置首 1 筆＋考點 literal 9 筆（每筆含「忘記反轉」陷阱行）＋乙′ enum 策展 band 4 筆（來源排列庫＋查詢候選庫，防裸背答案）＋壓力 literal 3 筆（T=1、N=800、M=18，`input_budget: 49152`）＋邊界 literal 3 筆。
- generator（反轉＋雙指標貪婪）與 reference_solution（位置區間外擴法）雙實作零共用邏輯，供 content-regression 互驗。

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `deque-challenge-series`: 新增收卷順序驗證題的題面契約、判定語意、測資結構與驗證要求（系列第二題，比照 buffer-audit-log 的歸屬）

## Impact

- Affected specs: 修改 `deque-challenge-series`（ADDED requirements）
- Affected code:
  - New: docs/challenge/exam-collect-verify.md
  - Modified: (none)
  - Removed: (none)
