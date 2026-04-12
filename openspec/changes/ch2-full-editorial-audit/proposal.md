## Summary

對模組二（Chapter 2）全部 7 個 section 檔案（2-1.md 至 2-7.md）及其 36 個 challenge 檔案執行完整的 Editorial Audit Loop（EAL），確認所有撰寫規則合規。若發現違規，在 violation log 中記錄並直接修正；若修正後仍有殘留問題，規劃後續修正 change。

## Motivation

模組二的 7 個 section 由不同的 change 分批撰寫（write-ch2-2-1 至 write-ch2-2-7），每個 change 內部雖有編輯規則驗證任務，但以下跨章節問題無法在單一 change 內檢測：

- **K-1 跨檔案 kaomoji 重複**：同一 kaomoji 在整個 chapter 內不得超過 3 次
- **T-1 跨節術語一致性**：確保沒有任何 section 在教學點之前使用正式術語（需全 chapter 的術語地圖交叉比對）
- **Challenge ID 連續性**：ID 11–46 無間隔、無重複
- **圖片編號連續性**：跨 section 的圖片編號不衝突
- **Index.md 準確性**：7 個 section 連結全部指向實際存在的檔案
- **Frontmatter 一致性**：所有 section 的 chapter/section/createdTime 格式統一
- **Section 間過渡品質**：每節結尾的「下一節預告」與下一節開頭的「接棒」是否銜接

此 change 作為模組二的品質閘門，必須在所有 section 撰寫完成後、正式發布前執行。

## Proposed Solution

套用現有 `editorial-audit-loop` spec 定義的 EAL 工作流，以 `docs/tutor/py/ch2/` 為目標目錄：

1. **Round 1**：按固定掃描順序（P-1 → T-1 → S-1 → S-2 → S-3 → C-1 → E-1 → M-1 → F-1 → V-1 → T-3 → K-1 → W-1 → T-2）掃描全部 7 個 section 檔案，產出 violation log
2. **跨章節檢查**：在 Round 1 同時執行 K-1 跨檔、T-1 跨節、Challenge ID、圖片編號、index 連結、frontmatter、section 過渡等 7 項跨章節檢查
3. **修正**：修正所有發現的違規
4. **Round 2–3**：從頭重新掃描，直到零違規或達到 3 輪上限
5. **產出總結報告**：記錄每輪違規數、最終殘留違規（如有）
6. **若殘留違規**：針對無法在此 change 內修正的結構性問題，在總結報告中列出建議的後續修正 change 名稱與範圍

## Non-Goals

- 不撰寫新的教學內容（內容已在 write-ch2-2-1 至 write-ch2-2-7 完成）
- 不修改撰寫規則本身（規則定義在 `python-ch1-content` spec，本 change 只是驗證合規）
- 不產生圖片（只驗證 placeholder 格式正確）
- 不涵蓋 Chapter 1 的內容（Ch1 有獨立的 EAL change）

## Capabilities

### New Capabilities

- `ch2-cross-chapter-audit`：定義模組二的跨章節品質檢查項目（K-1 跨檔 kaomoji、T-1 跨節術語地圖、Challenge ID 連續性、圖片編號連續性、index 連結驗證、frontmatter 一致性、section 過渡銜接），以及 EAL 結果的驗收標準

### Modified Capabilities

（無）

## Impact

- 可能修改的檔案：
  - `docs/tutor/py/ch2/2-1.md` 至 `2-7.md`（修正違規內容）
  - `docs/tutor/py/ch2/index.md`（修正連結問題）
  - `docs/challenge/` 下 ID 11–46 的檔案（修正 frontmatter 或 generator 問題）
- 此 change 的執行前提：write-ch2-2-1 至 write-ch2-2-7 全部 apply 完成
