## Summary

把三件核心領域知識封裝成 repo 內 committed 的 Claude Code skill（挑戰命題、Phoenix 科普寫作、EAL 編審），並為題目 frontmatter 導入可擴充的 `type`（題型）taxonomy。

## Motivation

專案目前 0 個自訂 committed skill：領域知識（如何出題、Phoenix 科普寫作 15 規則、Editorial Audit Loop 編審流程）散落在文件與未進版控的全域 skill 中，任何 AI agent 或維護者都無法可攜地重用（對應開發端分析報告風險 #3）。同時題目缺乏正式的「題型」分類，無法區分基礎練習與競賽題、也不利於未來擴充填空／遊戲化等新題型。本變更把領域知識沉澱為隨 repo 版控、可 `/`叫用的 skill，並建立一個可擴充的題型 taxonomy。

## Proposed Solution

1. 於 `.claude/skills/<name>/SKILL.md` 新增三個 committed skill：
   - `challenge-author`：依 `Usage.md` 契約 + `pnpm new-challenge` scaffold + generator/`reference_solution` + `content-regression` 驗證，一鍵引導出題（basic/competition 的樣板差異以 skill 內的人工引導提供）。
   - `phoenix-sci-writing`：封裝 `phoenix-popular-science-article-style-enhance.md` 的 15 條科普寫作規則（P-1 / T-1 / S-1~3 / C-1 / E-1 / M-1 / O-1 / W-1 / T-2 / F-1 / V-1 / T-3 / K-1）。
   - `eal-editorial-audit`：封裝 Editorial Audit Loop 迭代編審流程（固定掃描順序、逐輪修正、≤3 輪或零違規終止），對應既有 spec `editorial-audit-loop`。
2. 為題目 frontmatter 導入 `type` 欄位與可擴充 taxonomy：本版實作 `basic`（基礎）與 `competition`（競賽）；`fill_in_blank`（填空）與 `gamified`（遊戲化）登錄為 deferred（下一版）；`guided`（引導）登錄為 future placeholder。`type` 為選填、預設 `basic`，以相容既有 54 題。`pnpm new-challenge` 新增 `--type` 旗標與驗證，並在產出的 frontmatter 寫入 resolved `type`（scaffold 產出單一樣板 + `type` 欄位；basic/competition 的樣板差異由 challenge-author skill 的人工引導提供，不自動產出不同 boilerplate）。

## Non-Goals

- 不實作 `fill_in_blank`、`gamified` 的樣板或執行邏輯（僅在 taxonomy spec 登錄為 deferred）。
- 不設計或實作 `guided` 引導題型（僅 placeholder，設計中）。
- 不改動既有 54 題的內容或既有 frontmatter（`type` 選填、預設 basic，向後相容）。
- 不動全域 `phoenix-writing` skill 或其他不可攜的全域資產。
- 不重寫 `editorial-audit-loop` spec 的既有 requirement（skill 為其可執行封裝）。

## Capabilities

### New Capabilities

- `domain-skills`: repo 於 `.claude/skills/` 提供三個 committed skill（challenge-author / phoenix-sci-writing / eal-editorial-audit），各含 SKILL.md + frontmatter（name/description）與規定的內容契約，隨 repo 版控、可攜、可 `/`叫用。
- `challenge-exercise-type`: 題目 frontmatter 的 `type` 欄位與可擴充題型 taxonomy（basic/competition 已實作、fill_in_blank/gamified deferred、guided future），含選填預設 basic 的相容規則與 `pnpm new-challenge --type` 的驗證與 scaffold 行為。

### Modified Capabilities

- `challenge-type-unification`: `DataChallenge` 的 data-only 欄位列舉新增 `type: ExerciseType`（選填、預設 basic），使既有 spec 的欄位列舉與實作一致。

## Impact

- Affected specs: `domain-skills`（新增）、`challenge-exercise-type`（新增）、`challenge-type-unification`（修改）
- Affected code:
  - New: `.claude/skills/challenge-author/SKILL.md`、`.claude/skills/phoenix-sci-writing/SKILL.md`、`.claude/skills/eal-editorial-audit/SKILL.md`、`docs/shared/exercise-type.ts`、`docs/shared/exercise-type.test.ts`
  - Modified: `scripts/new-challenge.ts`（新增 `--type` 旗標與 `=value` 語法、`validateType`、frontmatter 輸出 `type`）、`scripts/new-challenge.test.ts`（擴充 `type` 與 `--type=value` 測試、EXERCISE_TYPES lockstep）、`docs/shared/challenge.data.ts`（`DataChallenge` 新增 `type` 欄位、以 `resolveExerciseType` runtime 解析）、`Usage.md`（文件化 `type` 欄位並指向 challenge-author skill）
