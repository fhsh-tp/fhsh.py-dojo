## Context

模組二共 7 節（2-1 至 2-7），由 7 個獨立的 Spectra change 分別撰寫。每個 change 內部包含編輯規則驗證任務，但以下問題只有在全部 section 都完成後才能檢測：

- 跨檔案的 kaomoji 重複（K-1 跨檔規則）
- 跨節的術語使用順序（T-1 教學點地圖）
- Challenge ID 連續性（11–46）
- 圖片編號連續性
- Section 間的過渡銜接品質

**執行前提**：write-ch2-2-1-for-range 至 write-ch2-2-7-summary 全部 apply 完成，所有 section 檔案和 challenge 檔案已存在於磁碟上。

## Goals / Non-Goals

**Goals：**

- 以 EAL 工作流（最多 3 輪）掃描全部 Ch2 內容，達到零違規
- 執行 7 項跨章節專屬檢查
- 產出結構化的 violation log 和總結報告
- 直接修正所有可修正的違規
- 對無法在此 change 修正的結構性問題，產出後續 change 建議

**Non-Goals：**

- 不重新撰寫教學內容
- 不修改規則定義本身
- 不涵蓋 Ch1 內容

## Decisions

### EAL 掃描順序與規則清單

按 `editorial-audit-loop` spec 定義的固定順序掃描。每條規則逐檔掃描所有 7 個 section 檔案：

| 順序 | Rule ID | 規則名稱 | 檢查重點 |
|------|---------|----------|---------|
| 1 | P-1 | 標點風格 | 所有 `——` 按五步驟決策清單判定 |
| 2 | T-1 | 術語前引用 | 比對術語教學點地圖，確認無提前使用 |
| 3 | S-1 | 比喻橋樑 | 每個比喻前有 meta-cognitive bridge |
| 4 | S-2 | 笑話後接回 | 連續 prose 中笑話後有 callback connector |
| 5 | S-3 | 段落過渡 | H2 過渡 2-4 句（摘要+缺口+動機） |
| 6 | C-1 | Code 引言 | 每個 code block 前有 prose lead-in |
| 7 | E-1 | 錯誤預防 | 語法陷阱在引入點立即警告 |
| 8 | M-1 | 心智模型 | 新 pattern 附 trace table/step-by-step |
| 9 | F-1 | 圖片格式 | 雙行格式（`![...]()` + `> 📷`） |
| 10 | V-1 | Container 語法 | `> [!TYPE]` 含驚嘆號 |
| 11 | T-3 | 無空 Container | 所有可見 container 有實質內容 |
| 12 | K-1 | 情緒標點密度 | 30 行 ≥1、10 行 ≤1、kaomoji 種類 |
| 13 | W-1 | Code/Walkthrough 一致 | code block 與 walkthrough 完全對應 |
| 14 | T-2 | 無殘留 Placeholder | 無 deferred-content marker |

### 跨章節檢查清單（7 項）

在 Round 1 的 K-1 和 T-1 掃描階段同時執行，但獨立記錄：

| # | 檢查項目 | 具體方法 |
|---|---------|---------|
| X-1 | K-1 跨檔 kaomoji | 收集所有 7 檔的 kaomoji，確認同一 kaomoji 在整個 chapter ≤ 3 次 |
| X-2 | T-1 跨節術語地圖 | 建立完整術語教學點地圖（for/range→2-1, while→2-2, break/continue→2-3, list/index/len/append→2-4, swap/nested-loop/bubble-sort→2-5, dict/key-value/tuple/hash→2-6），掃描每個 section 確認無提前使用 |
| X-3 | Challenge ID 連續性 | 掃描 `docs/challenge/` 下 ID 11–46 的檔案，確認 36 個 ID 無間隔、無重複 |
| X-4 | 圖片編號連續性 | 跨 section 的圖片編號不衝突（各 section 使用獨立的編號範圍或統一遞增） |
| X-5 | Index 連結驗證 | ch2/index.md 的 7 個連結全部指向實際存在的檔案 |
| X-6 | Frontmatter 一致性 | 所有 section 的 `chapter: 2`、`section` 格式（"2-N"）、`createdTime` 格式（ISO 8601 +08:00）統一 |
| X-7 | Section 過渡銜接 | 每節結尾的「下一節預告」關鍵詞與下一節開頭的「接棒」內容匹配（例如 2-1 結尾提到 while，2-2 開頭回應 while） |

### 違規分類與處理策略

| 類別 | 定義 | 處理方式 |
|------|------|---------|
| **即時修正** | 標點替換、格式修正、kaomoji 替換、container 語法修正 | 在當前 change 的 EAL 修正階段直接改 |
| **內容修正** | walkthrough 與 code 不一致、trace table 缺失、比喻缺 bridge | 在當前 change 直接補寫/改寫 |
| **結構性問題** | section 過渡邏輯不通、術語教學點需要調整（影響多個 section）、challenge generator 邏輯錯誤 | 記錄在總結報告中，建議後續修正 change |

### Violation Log 格式

每條 violation 記錄：

```
| 檔案 | 行號 | Rule ID | 違規描述 | 建議修正 | 分類 |
```

### 總結報告格式

```markdown
## EAL 總結報告

- 執行輪數：N/3
- Round 1 違規數：X
- Round 2 違規數：Y（若有）
- Round 3 違規數：Z（若有）
- 最終狀態：零違規 / 殘留 N 項

### 殘留違規（若有）
| 檔案 | Rule ID | 描述 | 建議後續 Change |

### 跨章節檢查結果
| 檢查項 | 結果 | 備註 |
```

## Risks / Trade-offs

- **[風險] EAL 3 輪仍有殘留違規** → 這代表存在結構性問題（例如術語教學順序需要調整），此時不強行修正，而是產出明確的後續 change 建議，由使用者決定是否接受
- **[風險] 跨章節檢查發現 T-1 違規，但修正需要改動多個 section 的教學順序** → 歸類為「結構性問題」，在報告中詳細說明影響範圍和建議方案，不在此 change 中自行重寫教學內容
- **[風險] Challenge generator 邏輯錯誤** → 僅能做靜態 code review，無法在此 change 中實際執行測試。若發現可疑邏輯，標記為 Warning 並在報告中列出
