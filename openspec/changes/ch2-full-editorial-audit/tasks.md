## 1. 前置確認

- [ ] 1.1 確認所有 7 個 section 檔案存在（`docs/tutor/py/ch2/2-1.md` 至 `2-7.md`），確認所有 36 個 challenge 檔案存在（ID 11–46），確認 `docs/tutor/py/ch2/index.md` 已更新為 7 節結構。若任何檔案缺失，記錄並停止 EAL，回報哪些前置 change 尚未 apply

## 2. 「跨章節檢查清單（7 項）」（Cross-chapter kaomoji audit X-1 + Cross-chapter terminology map audit X-2 + Challenge ID continuity audit X-3 + Image numbering continuity audit X-4 + Index link verification audit X-5 + Frontmatter consistency audit X-6 + Section transition coherence audit X-7）

- [ ] 2.1 執行「Cross-chapter kaomoji audit X-1」：收集 2-1.md 至 2-7.md 所有 kaomoji，列出每個 kaomoji 的出現次數與檔案位置，確認同一 kaomoji 跨整個 chapter 不超過 3 次。違規者記錄至 violation log 並建議替換 kaomoji
- [ ] 2.2 執行「Cross-chapter terminology map audit X-2」：建立完整術語教學點地圖（for/range→2-1, while→2-2, break/continue→2-3, list/index/len/append/linear-search→2-4, swap/nested-loop/bubble-sort→2-5, dict/key-value/tuple/hash→2-6），逐檔掃描確認無術語在教學點之前被正式使用（controlled forward reference 例外）
- [ ] 2.3 執行「Challenge ID continuity audit X-3」：掃描 `docs/challenge/` 下所有檔案的 `id` frontmatter，驗證 ID 11–46 共 36 個檔案無間隔、無重複，且每個檔案的 `id` 值與預期一致
- [ ] 2.4 執行「Image numbering continuity audit X-4」：收集 2-1.md 至 2-7.md 所有 `![📷 **圖 N**` placeholder，確認跨 section 無重複編號，並交叉比對每個 section 的 Image Specification Appendix 確認每個 placeholder 有對應 entry
- [ ] 2.5 執行「Index link verification audit X-5」：解析 `docs/tutor/py/ch2/index.md` 的所有內部連結，確認 7 個 section 連結全部指向實際存在的 `.md` 檔案
- [ ] 2.6 執行「Frontmatter consistency audit X-6」：驗證所有 7 個 section 的 frontmatter 一致性（`layout: doc`, `chapter: 2`, `section` 格式 "2-N" 與檔名匹配, `createdTime` ISO 8601 +08:00）。確認 2-1 至 2-6 有 `challenge` 欄位且 slug 對應存在的 challenge 檔案，2-7 無 `challenge` 欄位
- [ ] 2.7 執行「Section transition coherence audit X-7」：逐對比對相鄰 section（2-1→2-2、2-2→2-3、...、2-6→2-7），確認每節結尾的「下一節預告」主題詞與下一節開頭的「接棒」內容匹配

## 3. EAL Round 1 — 「EAL workflow executes on all Chapter 2 section files」

- [ ] 3.1 按 design「EAL 掃描順序與規則清單」逐規則掃描所有 7 個 section 檔案，執行「EAL workflow executes on all Chapter 2 section files」：P-1 標點風格（所有 `——` 按五步驟決策清單判定）→ T-1 術語前引用（對照 2.2 的術語地圖）→ S-1 比喻橋樑 → S-2 笑話後接回 → S-3 段落過渡 → C-1 Code 引言 → E-1 錯誤預防 → M-1 心智模型 → F-1 圖片格式 → V-1 Container 語法 → T-3 無空 Container → K-1 情緒標點密度 → W-1 Code/Walkthrough 一致 → T-2 無殘留 Placeholder。每個違規記錄至 violation log（檔案/行號/Rule ID/描述/建議修正/分類）
- [ ] 3.2 根據 design「違規分類與處理策略」修正所有 Round 1 的 immediate-fix 和 content-fix 違規。結構性問題記錄為「殘留違規（若有）」但不修正。所有違規使用 design「Violation Log 格式」記錄（檔案/行號/Rule ID/描述/建議修正/分類）

## 4. EAL Round 2（若 Round 1 有違規）

- [ ] 4.1 從頭重新掃描所有 7 個 section 檔案，使用與 Round 1 完全相同的規則順序和方法。記錄新的 violation log。修正所有 immediate-fix 和 content-fix 違規

## 5. EAL Round 3（若 Round 2 仍有違規）

- [ ] 5.1 從頭重新掃描所有 7 個 section 檔案。記錄最終 violation log

## 6. 產出總結報告（Audit summary report is produced）

- [ ] 6.1 按 design「總結報告格式」產出「Audit summary report is produced」總結報告，包含：執行輪數、每輪違規數、7 項跨章節檢查結果（X-1 至 X-7 各 pass/fail）、最終狀態（零違規或「殘留違規（若有）」N 項）。若有殘留結構性違規，為每項列出建議的後續修正 change 名稱與範圍描述
