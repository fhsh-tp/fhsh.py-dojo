## 1. 前置確認

- [x] 1.1 確認 write-ch2-completion change 已完成 apply，所有 section 檔案與 challenge 檔案已存在
- [x] 1.2 讀取編輯規則完整定義：(a) `/phoenix-popular-science-article-style-enhance.md` 全部 15 條規則的定義、違規/合規對照, (b) `openspec/specs/python-ch1-content/spec.md` 中 P-1 至 K-1 的 spec-level 定義, (c) Violation Log 格式定義於同一 enhance.md 的「3.3 Violation Log 格式」

## 2. EAL 全規則掃描 (Req: All Module 2 section files pass EAL 15-rule scan)

- [x] 2.1 [Req: All Module 2 section files pass EAL 15-rule scan] Round 1：按順序 P-1→T-1→S-1→S-2→S-3→C-1→E-1→M-1→F-1→V-1→T-3→K-1→O-1（僅適用於系列首篇，Ch2 可跳過）→W-1→T-2 掃描 `docs/tutor/py/ch2/` 全部 section 檔案，記錄所有違規至 violation log
- [x] 2.2 修正 Round 1 發現的所有違規
- [x] 2.3 Round 2：從頭重新掃描全部檔案，記錄殘留違規
- [x] 2.4 修正 Round 2 殘留違規（如有）
- [x] 2.5 Round 3（如需）：最終掃描，確認零違規或記錄無法修正的結構性問題

## 3. 跨章節檢查

- [x] [P] 3.1 [Req: Cross-file kaomoji K-1 compliance across Module 2] 統計所有 section 檔案中每個 kaomoji 的出現次數，確認同一 kaomoji 跨檔不超過 3 次，每檔至少 2 個情緒類別
- [x] [P] 3.2 [Req: Challenge ID continuity across Module 2] 收集所有 Module 2 引用的 challenge ID，驗證連續性（無間隔、無重複）
- [x] [P] 3.3 [Req: Image numbering continuity across Module 2] 從所有 section 檔案提取圖片編號，驗證全域連續性
- [x] [P] 3.4 [Req: Index links resolve to existing files] 檢查 `docs/tutor/py/ch2/index.md` 中每個連結指向的檔案是否存在
- [x] [P] 3.5 [Req: Section transitions are coherent across Module 2] 比對每節結尾預告與下一節開頭，確認主題銜接
- [x] [P] 3.6 [Req: Frontmatter consistency across Module 2] 比對所有 section 檔案的 frontmatter 格式一致性（chapter、section、createdTime 格式）

## 4. 報告與收尾

- [x] 4.1 產出 EAL Summary Report（每輪違規數、最終結果、殘留問題列表）
- [x] 4.2 若有無法修正的結構性問題，列出建議的後續修正 change 名稱與範圍
