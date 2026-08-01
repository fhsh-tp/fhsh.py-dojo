## Context

id 56「兩端淘汰賽」已完成初版(archive 2026-08-01-add-two-end-elimination-challenge、PR #16 已開未 merge、CI 綠),但使用者實測揭露根本缺陷:樸素 O(n) 單掃描(邊讀邊比大小)即可全 AC,deque 教學與 TLE 區分同時落空。平台結構性事實(判題僅比對輸出、op-counter 對 C 內建隱形)決定了「強制資料結構」不可行,唯一槓桿是把過程變成答案。使用者已逐項拍板:過程輸出(max/min 兩輪)、tie 統一移除後端、素養情境(緩衝區稽核,源自真實 deque 用途:串流監測/受限緩衝)、縮規模去 TLE band、改名緩衝區稽核日誌/buffer-audit-log、tags 去 deque。PR #16 凍結待本次 rework 完成後更新。

## Goals / Non-Goals

**Goals:**

- 輸出語義改為過程日誌,使單次掃描與內建 max()/min() 無法產生正確輸出,雙端操作成為最自然解法路徑。
- 素養導向:情境源自真實 deque 用途,學生可見表面(敘述/tags/範例)零 deque 字樣,自行辨識資料結構。
- 過程輸出唯一性:tie 規則釘死(相等移除後端),兩輪統一。
- 池體積從 2.9MB 降回數百 KB,判題時間縮短。

**Non-Goals:**

- 不改判題引擎與測資引擎;不做計分面;不動其他題目。
- 不追求強制 deque(雙指標 index 解同屬雙端思維,接受)。
- 不保留 TLE 級測資與效能提醒敘述。
- 不做 staging→main release;PR #16 的描述更新在 change 之外由既定 PR 流程處理。

## Decisions

### 過程日誌語義與 tie 規則

每筆測資兩行:峰值輪日誌(每次比較緩衝區最早端與最新端,移除較小者記入日誌;**相等時移除後端**;剩最後一筆為存活者=峰值;該行=依序被移除的讀數+存活者,空格分隔共 Ni 個數)、谷值輪日誌(重播同筆資料,移除較大者,tie 同樣移除後端,存活者=谷值)。單元素 Ni=1 兩行皆為該數。正確性:峰值輪中全域最大值永不被移除(≥ 一切),必為存活者;谷值輪對稱。輸出唯一性由 tie 規則保證。替代案「兩輪不同 tie 邊」否決(規則加倍易混淆);「只輸出 max 輪」否決(失去方向相反的第二次練習與驗證面)。

### 素養情境:緩衝區稽核(不提 deque)

情境:邊緣裝置將感測讀數(整數,可能為負,不綁定單位)依序存入緩衝區;硬體限制每次只能檢視/移除「最早」與「最新」兩端。稽核規範要求逐步記錄移除順序——過程輸出在情境內有真實理由(稽核 log)。此情境源自查證過的真實 deque 用途(串流監測/滑動視窗/受限緩衝)。約束:題目敘述、tags、範例、動手推演全程不出現 deque/雙端佇列字樣;動手推演僅以「最早端/最新端」描述。tags 改為 data structure 與 模擬。替代案 work-stealing 與瀏覽器分頁情境否決(機制對應硬拗,真實性受損)。

### 測資縮規模與預算精算

params:t int 2..3 不變;cases group 內 n 改 int 1..400、nums int -999..999 count.from n 不變。testcase_plan 三 band 共 6 筆:count 3(override n.max=20,教學)、count 2(override n.min=200,驗長序列多輪淘汰與輸出行規模)、count 1(override n.min=1、n.max=1,單元素邊界)。去 TLE band 理由:過程題每輪本就 O(1) 比較,「慢但正確」寫法幾乎不存在,大測資無教學標的,只剩 6MB 池成本。input_budget 精算:中 band worst-case = t(1)+換行(1)+3×[n 寬 3+換行 1+值 4×400+分隔 399]+組間換行 2 = 6013 bytes → 宣告 8192(留 36% 餘裕)。總 6 筆維持 e2e 消歧(≠ 預設 5)。

### generator 雙指標與 reference_solution deque 分工

generator 不得以內建 max()/min() 求答案(結果可得、過程不可得),改用**雙指標 index** 模擬:l、r 指向串列兩端,比較 nums[l] 與 nums[r],峰值輪移除較小端(tie 移除 r 端)記錄之並收攏指標,剩 nums[l]==nums[r] 位置為存活者;谷值輪對稱。reference_solution 用 **collections.deque**:d[0]/d[-1] 比較、popleft()/pop() 移除,max/min 各用一份複本跑一輪。兩者演算法同構、實作機制刻意不同(index vs deque),content-regression 以正式池樣本自動互驗。輸出組裝用 list 收集後 ' '.join(map(str, ...)) 一次輸出(避免逐項 print 效能與行尾空白問題)。

### 檔案改名與主 spec Purpose 補正

git 改名 docs/challenge/two-end-elimination.md → docs/challenge/buffer-audit-log.md(id 56 不變、algorithm 改 buffer_audit_log 以符合檔名映射規則)。舊池 two-end-elimination.bin 由 build:pools cleanup 自動刪除。主 spec openspec/specs/deque-challenge-series/spec.md 的 Purpose 段仍為 archive 佔位「TBD」,本次直接補為正式描述(Purpose 不在 delta 應用範圍,直接修訂無衝突)。

## Implementation Contract

- **行為**:學生在 /challenge/buffer-audit-log 頁面提交程式,判題以 6 筆池測資執行:deque 或雙指標正解 6/6 AC;舊語義解(每筆輸出一行「max min」)全部 WA;每場必含一筆全單元素測資(每組兩行輸出同一數字)。
- **資料形狀**(frontmatter 契約):layout challenge、id 56、title 緩衝區稽核日誌、difficulty medium、type competition、algorithm buffer_audit_log、tags [data structure, 模擬]、description 一句話(不提 deque)、params(t: int 2..3;cases: group repeat t 內含 n: int 1..400、nums: int -999..999 count.from n separator 換行)、input_budget 8192、testcase_plan 依序三 band(count 3/n.max 20;count 2/n.min 200;count 1/n.min 1 且 n.max 1)、generator(雙指標過程模擬)、starter_code 空字串、reference_solution(collections.deque 過程模擬)。禁止 testcase_count 與 verdict_detail 欄位;全檔學生可見表面禁止 deque 字樣。
- **輸出契約**:每筆測資恰好兩行;第一行=峰值輪日誌(Ni 個空格分隔整數:依序被移除的 Ni-1 個讀數+存活者);第二行=谷值輪日誌(同格式);比較規則=峰值輪移除較小端、谷值輪移除較大端、相等一律移除後端(最新);共 2T 行。
- **失敗模式**:params/plan 非法宣告在 pnpm build:pools 與 scripts/challenge-params.test.ts fail-loud 指名本檔;generator 與 reference_solution 輸出不一致時 content-regression 失敗指名本題;舊路徑檔案殘留會造成 id/algorithm 撞名並被冒煙測試抓到。
- **驗收判準**:(1) pnpm build:pools 成功產出 buffer-audit-log.bin 且 two-end-elimination.bin 被 cleanup 移除;(2) pnpm test --run 全綠(冒煙+content-regression 涵蓋新題);(3) pnpm typecheck 與 pnpm lint 通過;(4) pnpm dev 提交 deque 正解 6/6 AC;(5) 生產建置 e2e:deque 正解 6/6 AC、舊語義單掃描解(輸出 max min)全 WA、亂序日誌錯解全 WA;(6) grep 檢查題目檔全文無 deque 字樣(含 tags)。
- **範圍邊界**:改動僅 docs/challenge/ 下該檔(改名+重寫)與 openspec/specs/deque-challenge-series/spec.md 的 Purpose 段;不動任何引擎程式、其他題目、UI;池產物不進 commit。

## Risks / Trade-offs

- [雙指標 index 解不用 deque 也 AC] → 接受:同屬雙端操作思維,教學目標是「辨識雙端存取模式」;平台無 AST 檢查,本就無法強制特定型別。
- [學生誤解 tie 規則導致 WA 挫折] → 動手推演含 tie 步驟、範例含重複值案例,規則在輸入/輸出說明中以粗體明示。
- [輸出行較長(中 band 一行 400 個數)] → 判題為整行字串比對,長度無礙;敘述提醒用空格分隔、行尾無多餘空白(join 寫法自然滿足)。
- [改名後外部連結/PR 描述失效] → PR #16 尚未 merge,無已發布連結;PR 標題與描述在 rework 完成後隨即更新。
- [情境宣稱「硬體限制只能存取兩端」屬簡化] → 素養題容許合理簡化,敘述不做超出情境需要的技術宣稱。

## Migration Plan

單題重寫,無資料遷移;rollback = git revert 本 change 的 commits 並重跑 pnpm build:pools(池自動回復)。PR #16 未 merge,無線上使用者受影響。

## Open Questions

(無——語義、tie、情境、規模、命名皆已拍板;無待決事項。)
