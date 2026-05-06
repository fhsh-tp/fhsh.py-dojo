## Summary

對 Chapter 1 全部 4 個教學檔案（1-1.md、1-2.md、1-3.md、1-4.md）執行完整的 Editorial Audit Loop（EAL），修正所有違規並擴充 K-1 規則以增加顏文字多樣性。

## Motivation

嚴格審計發現 ch1 共計 92 個違規：

- 1-1.md：34 個（S-3×15、P-1×5、S-2×4、S-1×3、C-1×3、E-1×2、T-1×1、K-1×1）
- 1-2.md：44 個（S-3×16、T-2×10、P-1×9、S-2×2、S-1×1、T-1×1、C-1×1、E-1×1、T-3×1、K-1×1、kaomoji 重複×1）
- 1-3.md：11 個（S-3×7、P-1×2、S-2×1、S-1×1）— 前一輪 polish 遺漏
- 1-4.md：3 個（P-1×1、S-2×1、K-1×1）— 前一輪 polish 遺漏

此外，顏文字多樣性嚴重不足：

- `(๑•̀ㅂ•́)و✧` 出現 5 次（4 檔都有）
- `_(´ཀ`」 ∠)_` 出現 4 次（4 檔都有）
- `Σ(ﾟДﾟ；≡；ﾟдﾟ)` 出現 4 次
- Skill catalog 有 30+ 種顏文字分 8 類，但 ch1 只用了約 6 種

## Proposed Solution

### 1. 擴充 K-1 spec 增加顏文字多樣性子條款

在 `python-ch1-content/spec.md` 的 K-1 requirement 中新增：

- 同一 kaomoji 單檔不得超過 2 次
- 跨整個 chapter（1-1 ~ 1-4），同一 kaomoji 不得超過 3 次
- 每個 section 至少使用 2 個不同情緒類別的顏文字（依 phoenix-popular-science-article-style kaomoji catalog 的 8 類分類：Resigned、Celebration、Shock、Frustration、Sadness、Cute、Mischievous、Confusion）

### 2. 按 EAL 掃描順序修正所有違規

掃描順序：P-1 → T-1 → S-1 → S-2 → S-3 → C-1 → E-1 → M-1 → F-1 → V-1 → T-3 → K-1 → O-1 → W-1 → T-2

按檔案分批：先修 1-1（最多結構性修改），再修 1-2（最多 TBD），最後修 1-3 和 1-4 的殘餘違規。

### 3. 全檔 kaomoji 多樣性替換

根據新的 K-1 多樣性規則，替換重複的 kaomoji：
- 從 catalog 中選擇未使用過的顏文字，確保情緒類別匹配
- 優先替換出現 3 次以上的 kaomoji

## Non-Goals

- 不改動文章結構（H2/H3 層級順序不變）
- 不修改 frontmatter
- 不修改 `docs/challenge/*.md`
- 不修改 VitePress 系統配置
- 不新增或刪除圖片佔位符（僅修正格式）
- 不重寫整段內容——只做規則合規修正

## Capabilities

### New Capabilities

（無）

### Modified Capabilities

- `python-ch1-content`：擴充 K-1 規則新增顏文字多樣性子條款（3 條限制 + 2 個 scenario）

## Impact

- 受影響的 spec：`openspec/specs/python-ch1-content/spec.md`（K-1 擴充）
- 受影響的檔案：
  - `docs/tutor/py/ch1/1-1.md`（34 個違規修正）
  - `docs/tutor/py/ch1/1-2.md`（44 個違規修正，含 10 個 TBD 解決）
  - `docs/tutor/py/ch1/1-3.md`（11 個殘餘違規修正）
  - `docs/tutor/py/ch1/1-4.md`（3 個殘餘違規修正 + kaomoji 替換）
