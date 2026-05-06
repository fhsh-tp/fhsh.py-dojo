## 1. 更新 python-ch1-content spec — 修改既有規則

- [x] 1.1 合併「Chapter 1 sections follow punctuation style rule P-1」的 MODIFIED 版本（含 4 條判定清單和 2 個新 scenario）進 `openspec/specs/python-ch1-content/spec.md`，取代原有 P-1 requirement block
- [x] 1.2 合併「Chapter 1 sections follow post-humor connector rule S-2」的 MODIFIED 版本（含 H3 邊界條件和 2 個新 scenario）進 `openspec/specs/python-ch1-content/spec.md`，取代原有 S-2 requirement block

## 2. 更新 python-ch1-content spec — 新增規則

- [x] 2.1 新增「Chapter 1 image placeholders follow dual-line format rule F-1」至 `openspec/specs/python-ch1-content/spec.md`
- [x] 2.2 新增「Chapter 1 VitePress custom containers use correct syntax rule V-1」至 `openspec/specs/python-ch1-content/spec.md`
- [x] 2.3 新增「Chapter 1 sections contain no empty UI elements rule T-3」至 `openspec/specs/python-ch1-content/spec.md`
- [x] 2.4 新增「Chapter 1 sections follow emotional punctuation density rule K-1」至 `openspec/specs/python-ch1-content/spec.md`

## 3. 建立 editorial-audit-loop spec

- [x] 3.1 建立 `openspec/specs/editorial-audit-loop/spec.md`，寫入「Editorial Audit Loop workflow exists for Chapter 1 content」requirement（含文件化 scenario）
- [x] 3.2 寫入「EAL workflow scans all rules in a defined order per round」requirement（含掃描順序 P-1→T-2、violation log 欄位定義）
- [x] 3.3 寫入「EAL workflow terminates after zero violations or maximum 3 rounds」requirement（含 early termination 和 max rounds scenario）
- [x] 3.4 寫入「EAL workflow applies fixes between rounds」requirement（含全檔重新掃描 scenario）
- [x] 3.5 寫入「EAL workflow is reusable across chapters」requirement（含目標目錄參數化和規則子集 scenario）

## 4. 撰寫 phoenix-popular-science-article-style-enhance.md

- [x] 4.1 撰寫 `phoenix-popular-science-article-style-enhance.md`，整合全部 15 條規則（P-1 含判定清單、T-1、S-1、S-2 含 H3 邊界條件、S-3、C-1、E-1、M-1、O-1、W-1、T-2、F-1、V-1、T-3、K-1）的完整定義、判定範例、與違規/合規對照
- [x] 4.2 在 `phoenix-popular-science-article-style-enhance.md` 中加入 Editorial Audit Loop（EAL）工作流程章節：描述輪次、掃描順序、violation log 格式、終止條件、修正→重掃流程
- [x] 4.3 在 `phoenix-popular-science-article-style-enhance.md` 中加入「規則制定與演化指南」章節：描述如何從人工修改中辨識規則模式、何時將規則正式化到 spec、如何測試新規則是否產生誤判

## 5. 更新 ch1-editorial-review.md

- [x] 5.1 更新 `openspec/ch1-editorial-review.md` 第 3 節的規則摘要表，新增 F-1、V-1、T-3、K-1 四行，並將 P-1 和 S-2 標記為「已修訂」
