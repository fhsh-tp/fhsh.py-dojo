## Summary

把三份 AI agent 指令檔（CLAUDE.md / AGENTS.md / GEMINI.md）從純 Spectra 樣板升級為含專案領域知識的上手文件，並清理 crypto-challenge fork 遺留與已無呼叫端的 useApi 死碼。

## Motivation

目前 CLAUDE.md / AGENTS.md / GEMINI.md 僅含 Spectra 受管樣板，完全沒有本專案的技術棧、建置指令、題目契約與必讀清單，導致任何 AI agent（或新進維護者）接手時缺乏領域上下文，容易誤解或走錯建置流程。同時專案自 crypto-challenge fork 而來，殘留多處與現況不符的名稱與規則（release 產物名、失效的 .gitignore 規則、預設題名「密碼學挑戰 #N」、CHANGELOG 停在 1.0.0、Node 版本與 SOP 文件互相矛盾），以及一組全站無呼叫端的 useApi / useWsApi composable 死碼。這些既降低可維護性，也對自動化維護的 agent 造成誤導。本變更對應開發端分析報告風險 #2、#4、#8、#9、#11、#14、#15、#20。

## Proposed Solution

1. 在三份指令檔的 Spectra 受管區塊（`<!-- SPECTRA:START -->` … `<!-- SPECTRA:END -->`）「之外」新增專案領域段落：技術棧、建置指令總表、題目 frontmatter 契約摘要（含 reference_solution）、維護前必讀清單。
2. fork 遺留清理：release 產物改名、CHANGELOG 補 Unreleased、移除失效的 .gitignore 規則並納入 .understand-anything 忽略、統一 Node 版本與新增題目 SOP、修正 CONTRIBUTE 章節跳號、中性化預設題名、處理未啟用的 faker feature。
3. 移除 useApi / useWsApi 死碼與其測試，並以 delta spec 正式移除對應 capability。

## Non-Goals

- 跨 agent 的 Spectra skill 版本／數量不一致（Claude 12、Codex/Gemini 10、舊 commands 8）屬 Spectra 產生器層面，本變更不處理（deferred，報告風險 #5）。
- `tools/lit-fetcher` 文件在地化需改工具契約，另立變更較妥（deferred，報告風險 #6）。
- `settings.local.json` 舊路徑僅本機、未進版控，對其他維護者/agent 無影響，不處理（報告風險 #10）。

## Capabilities

### New Capabilities

- `agent-onboarding-docs`: 定義三份 AI agent 指令檔必須在受管區塊外提供的專案領域內容契約（技術棧、建置指令、題目契約、必讀清單），以及 fork 遺留文件（CHANGELOG、Node 版本、SOP 一致性、章節連號）的維護規範。

### Modified Capabilities

- `release-dist-packaging`: release 產物名由 `crypto-challenge-*` 改為 `fhsh-py-dojo-*`。

### Removed Capabilities

- `vueuse-api-composable`: useApi / useWsApi composable 無任何呼叫端，連同測試移除；以 delta spec 的 REMOVED Requirements 正式下線。

## Impact

- Affected specs: `agent-onboarding-docs`（新增）、`release-dist-packaging`（修改）、`vueuse-api-composable`（移除）
- Affected code:
  - Modified: `CLAUDE.md`、`AGENTS.md`、`GEMINI.md`、`CONTRIBUTE.md`、`Usage.md`、`CHANGELOG.md`、`.gitignore`、`.github/workflows/release.yml`、`docs/shared/challenge.data.ts`、`testcase-generator/Cargo.toml`、`.vitepress/theme/composables/index.ts`
  - Removed: `.vitepress/theme/composables/useApi.ts`、`.vitepress/theme/__tests__/useApi.spec.ts`
