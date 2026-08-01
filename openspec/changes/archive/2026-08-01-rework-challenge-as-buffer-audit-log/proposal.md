## Summary

將 id 56 題目從「兩端淘汰賽」(結果輸出 max min)大改為素養導向過程輸出題「緩衝區稽核日誌」——輸出改為兩行淘汰過程日誌,使單次掃描與內建函式無法求解,雙端操作(deque)成為最自然解法。

## Motivation

使用者實測發現原題根本缺陷:找 max/min 本質是 O(n) 單次掃描可解的任務(邊讀邊比較即為初學者最自然寫法),完全不需要 deque;TLE band 懲罰的 O(n²) 雙重迴圈是沒人會自然寫出的稻草人,deque 教學實質落空。平台結構性事實:判題只比對輸出(無 AST 檢查)、op-counter 對 C 內建隱形,「用 TLE 強制資料結構」不可行——唯一槓桿是**把過程變成答案**:稽核日誌輸出唯一由雙端比較過程決定,單掃描算得出結果但算不出過程。情境採真實 deque 用途(串流監測/受限緩衝區),素養導向:題目全文與 tags 均不提 deque,讓學生自行辨識資料結構。

## Proposed Solution

- 檔案改名:docs/challenge/two-end-elimination.md → docs/challenge/buffer-audit-log.md(id 56 不變;以 git 改名保留歷史)。
- 新任務語義:邊緣裝置把感測讀數(整數,可能為負,不綁定單位)依序存入緩衝區;因硬體限制每次只能檢視「最早」與「最新」兩端各一筆並移除其中一筆。每筆測資輸出兩行稽核日誌:
  - 峰值輪:每次比較兩端、移除**較小**端並記入日誌(相等時移除**後端**=較新那筆),最後存活者即峰值;該行=依序被移除的讀數+存活者(空格分隔,共 Ni 個數)。
  - 谷值輪:重播同一筆資料、方向相反(移除**較大**端,相等同樣移除後端),存活者即谷值。
  - 單元素 Ni=1:兩行皆為該數本身(無移除)。
- 範例:4 個數 3,-5,8,1 → 峰值輪「1 3 -5 8」、谷值輪「3 1 8 -5」;tie 例 5,2,5 → 「5 2 5」與「5 5 2」。
- frontmatter:title 緩衝區稽核日誌、algorithm buffer_audit_log、tags 改為 data structure 與 模擬(拿掉 deque 洩題字樣);difficulty medium、type competition、starter_code 空字串、無 verdict_detail、無 testcase_count 維持。
- 測資縮規模去 TLE band:params n 改 1..400;testcase_plan 三 band 共 6 筆——count 3(n max 20)+ count 2(n min 200,驗長序列多輪與輸出規模)+ count 1(n min=max=1);input_budget 依新值域精算為 8192(中 band worst-case 約 6013 bytes)。池體積由 2.9MB 回到數百 KB。
- generator 改用雙指標 index 模擬過程(不得用內建 max/min 求答案);reference_solution 用 collections.deque 兩端操作實作——維持寫法刻意不同,content-regression 自動驗證兩者輸出一致。
- 敘述:素養導向情境重寫(全文不提 deque);刪除效能提醒段落(無 TLE band 後留著誤導);動手推演含 tie 步驟;維持系列五段式結構(題目說明、動手推演、輸入說明、輸出說明、範例)。
- 主 spec 的 Purpose 段仍為 archive 產生的 TBD 佔位,本次一併補為正式描述(與 delta 應用不重疊,直接修訂)。

## Non-Goals

- 不改判題引擎與測資引擎;不做計分面;不動其他題目與 BACKLOG 停車場。
- 不在題目任何學生可見表面(敘述、tags、範例)提及 deque 或指定解法——素養導向的核心約束。
- 不保留 TLE 級大測資:過程題不存在自然的「慢但正確」寫法,大測資只剩池體積與判題時間成本。
- 不追求「強制使用 deque」——平台無 AST 檢查,雙指標 index 解同樣正確(教學上同屬雙端操作思維,接受)。

## Alternatives Considered

- 換成滑動視窗最大值(單調 deque 經典題):逐窗 max(slice) 是 C 層、同樣不會 TLE,強制力一樣落空,且難度對高中生跳升過大。否決。
- 維持結果輸出、只改敘述引導:使用者已實測否定,教學目標實質落空。否決。
- 撤題:浪費已完成的 band 架構與系列脈絡。否決。

## Impact

- Affected specs: `deque-challenge-series`(REMOVED 全部 5 條舊 requirement + ADDED 5 條新 requirement;Purpose 由 TBD 補為正式描述)
- Affected code:
  - New: docs/challenge/buffer-audit-log.md(由既有檔案改名後全面重寫 frontmatter 與敘述)
  - Modified: openspec/specs/deque-challenge-series/spec.md(Purpose 段)
  - Removed: docs/challenge/two-end-elimination.md(改名消滅舊路徑)
- 建置產物:pnpm build:pools 重產(舊池 two-end-elimination.bin 由 cleanup 自動刪除、新池 buffer-audit-log.bin 產生;皆 gitignored)
