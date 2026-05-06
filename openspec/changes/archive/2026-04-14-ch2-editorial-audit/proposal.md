## Summary

對模組2（Chapter 2）全部 5 個 section 檔案（2-1.md 至 2-5.md）及其所有 challenge 檔案執行完整的 Editorial Audit Loop（EAL），確認所有撰寫規則合規。若發現違規，在 violation log 中記錄並直接修正；若修正後仍有殘留問題，規劃後續修正 change。

## Motivation

模組2的 5 個 section 由不同的 task 分批撰寫，以下跨章節問題無法在單一 task 內檢測：
- K-1 跨檔案 kaomoji 重複：同一 kaomoji 在整個 chapter 內不得超過 3 次
- T-1 跨節術語一致性：確保沒有任何 section 在教學點之前使用正式術語
- Challenge ID 連續性：無間隔、無重複
- 圖片編號連續性：跨 section 的圖片編號不衝突
- Index.md 準確性：所有 section 連結全部指向實際存在的檔案
- Frontmatter 一致性：所有 section 的 chapter/section/createdTime 格式統一
- Section 間過渡品質：每節結尾的「下一節預告」與下一節開頭的「接棒」是否銜接

## Proposed Solution

套用 EAL 工作流，以 `docs/tutor/py/ch2/` 為目標目錄：
1. Round 1：按固定掃描順序（P-1→T-1→S-1→S-2→S-3→C-1→E-1→M-1→F-1→V-1→T-3→K-1→W-1→T-2）掃描全部 section 檔案，產出 violation log
2. 跨章節檢查：K-1 跨檔、T-1 跨節、Challenge ID、圖片編號、index 連結、frontmatter、section 過渡等 7 項
3. 修正所有違規
4. Round 2-3：重新掃描至零違規或 3 輪上限
5. 產出 EAL Summary Report

## Non-Goals

- 不撰寫新的教學內容
- 不修改撰寫規則本身
- 不產生圖片
- 不涵蓋其他 chapter 的內容

## Capabilities

### New Capabilities
- `ch2-cross-chapter-audit`: 模組2的跨章節品質檢查項目與 EAL 結果驗收標準

### Modified Capabilities
（無）

## Impact

- 可能修改的檔案：`docs/tutor/py/ch2/*.md` + 對應 challenge 檔案
- 執行前提：write-ch2-completion change 完成後
