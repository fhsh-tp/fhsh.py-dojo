## Context

fhsh.py-dojo 自 crypto-challenge 專案 fork 而來，改造為「台北市立復興高級中學 Python 自學道場」。改造過程留下多處與現況不符的 fork 遺留，且三份 AI agent 指令檔（CLAUDE.md / AGENTS.md / GEMINI.md）僅含 Spectra 受管樣板、無任何專案領域知識。

目前狀態：
- 三份指令檔第 1–28 行為 Spectra 受管區塊（`<!-- SPECTRA:START v1.0.2 -->` … `<!-- SPECTRA:END -->`），會被 `spectra` 模板升級覆蓋；區塊外目前無內容。
- `.github/workflows/release.yml` 打包產物名為 `crypto-challenge-<ref>.tar.gz` / `.zip`。
- `.gitignore` 保留失效規則（指向已更名的 crate target 目錄），且分析階段新增的 `.understand-anything/` 忽略尚未提交。
- `CHANGELOG.md` 停在 1.0.0（2026-04-05）。
- `CONTRIBUTE.md` 標示 Node.js v20+，README/badge 標示 22+；章節編號為 Phase 1→2→3→5（缺 4）。
- `Usage.md` 教學以手動編輯 frontmatter 新增題目，與 `CONTRIBUTE.md` 以 `pnpm new-challenge` 為準的 SOP 矛盾。
- `docs/shared/challenge.data.ts` 的預設題名 fallback 為「密碼學挑戰 #N」。
- `testcase-generator/Cargo.toml` 宣告 `faker` feature（`default = []`，全專案未啟用）。
- `.vitepress/theme/composables/useApi.ts` 匯出的 useApi / useWsApi 全站無呼叫端，僅被自身測試 `useApi.spec.ts` 使用；`composables/index.ts` re-export 之。存在對應 capability spec `vueuse-api-composable`。

## Goals / Non-Goals

**Goals:**

- 讓任何 AI agent 或新進維護者讀完指令檔即掌握技術棧、建置指令、題目契約與必讀清單。
- 消除 fork 遺留造成的名稱/規則/文件不一致。
- 移除確認無用的 useApi 死碼，並讓 capability spec 隨之正確下線。

**Non-Goals:**

- 不處理跨 agent Spectra skill 版本/數量不一致（Claude 12 vs Codex/Gemini 10 vs 舊 commands 8）——屬 Spectra 產生器層面，需重新產生指令檔，另案處理（報告 #5）。
- 不處理 `tools/lit-fetcher` 文件在地化——需變更工具契約，另立變更（報告 #6）。
- 不處理 `settings.local.json` 舊路徑——該檔未進版控、僅本機，對協作者/agent 無影響（報告 #10）。
- 不改動題目 frontmatter schema、不新增 `type` 欄位（屬 Change C 題型 taxonomy 範圍）。
- 不重寫 release.yml 的觸發條件或簽章流程，只改產物檔名。

## Decisions

**D1：領域內容放在受管區塊之外，而非改寫受管區塊。**
理由：受管區塊會被 `spectra` 模板升級覆蓋，任何寫在其中的領域內容都會遺失。於檔案結尾（`<!-- SPECTRA:END -->` 之後）另起「專案領域指南」section 可長期存活。替代方案（改寫受管區塊）被否決，因不可維護。

**D2：三份指令檔內容一致但尊重各自語法慣例。**
理由：CLAUDE.md 用 `/spectra-*` slash 語法、AGENTS.md（Codex）用 `$spectra-*` 語法且無「Plan mode →」行、GEMINI.md 對齊 Gemini。領域段落的實質內容（技術棧、建置指令、題目契約、必讀清單）三者相同，但引用 skill 時各自沿用該檔既有語法。

**D3：CHANGELOG 補 `## [Unreleased]`，不倉促發版。**
理由：本變更不發 release，僅需讓 CHANGELOG 反映 1.0.0 之後的重大變更。以 `## [Unreleased]` section 收錄，符合 Keep a Changelog 慣例，避免擅自決定版號。

**D4：faker feature 於文件說明其保留意圖，不移除宣告。**
理由：`faker` feature 為 optional 且與 `paramspec-enum-faker` 能力相關聯，貿然刪除可能影響未來測資產生。決策為在 Cargo.toml 以註解說明其用途與現況（未預設啟用），並於本 design 記錄；移除與否留待專責變更。此為 in-scope 的「文件化」而非「移除」。

**D5：useApi 以 delta spec REMOVED Requirements 正式下線。**
理由：`vueuse-api-composable` 為既有 capability spec；僅刪程式碼而不處理 spec 會造成 spec 與程式碼漂移。於本變更 delta spec 用 `## REMOVED Requirements`（附 Reason / Migration），archive 時 spec 才會正確移除。

## Implementation Contract

**行為 1：指令檔領域段落（agent-onboarding-docs capability）**
- 觀察行為：`CLAUDE.md`、`AGENTS.md`、`GEMINI.md` 三檔在 `<!-- SPECTRA:END -->` 之後各含一個「專案領域指南」section，內容涵蓋 (a) 技術棧摘要（VitePress 2 + Vue 3 + Pyodide + Rust/WASM testcase-generator + pnpm）、(b) 建置指令總表（`pnpm dev` / `build:pools` / `build:wasm` / `build:pyodide` / `gen:keymaterial` / `typecheck` / `lint` / `test` 各自用途）、(c) 題目 frontmatter 契約摘要（必含 `reference_solution` 為選填欄位）、(d) 維護前必讀清單（`CONTRIBUTE.md` / `README.md` / `Usage.md`）。
- 資料形狀：Markdown section，位於受管區塊外。
- 驗收：三檔皆存在該 section；`grep` 受管標記確認新內容在 `<!-- SPECTRA:END -->` 之後；四項子內容 (a)–(d) 皆可辨識。
- 範圍邊界：只新增領域 section，不改動受管區塊內文。

**行為 2：release 產物改名（release-dist-packaging capability）**
- 觀察行為：release workflow 打包步驟產出的檔名為 `fhsh-py-dojo-<ref>.tar.gz` 與 `fhsh-py-dojo-<ref>.zip`，上傳 assets 亦引用同名。
- 驗收：release.yml 內不再出現 `crypto-challenge` 字串；`tar`/`zip`/upload 三處檔名一致；YAML 可被解析（`python3 -c "import yaml; yaml.safe_load(open('.github/workflows/release.yml'))"` 不報錯）。
- 範圍邊界：僅改產物檔名，不動觸發條件或其他步驟。

**行為 3：fork 遺留文件一致化**
- 觀察行為：`.gitignore` 不再含指向已更名 crate 的失效 target 規則，並含 `.understand-anything/` 忽略；`CONTRIBUTE.md` 的 Node 版本標示為 22+、章節編號連續（無跳號）；`Usage.md` 新增題目 SOP 以 `pnpm new-challenge` 為首選並與 `CONTRIBUTE.md` 一致；`CHANGELOG.md` 含 `## [Unreleased]` section 收錄 1.0.0 後重大變更；`docs/shared/challenge.data.ts` 預設題名 fallback 為中性字樣（不含「密碼學」）；`testcase-generator/Cargo.toml` 的 `faker` feature 有註解說明其保留意圖。
- 失敗模式：challenge.data.ts 改動後若破壞型別，`pnpm typecheck` 會失敗——須維持原型別，只改字串常值。
- 驗收：各檔 `grep` 確認舊字樣消失、新字樣存在；四道 gate 全綠（typecheck / lint / vitest / cargo）。
- 範圍邊界：僅一致化既有文件與常值，不新增功能。

**行為 4：useApi 死碼移除（vueuse-api-composable capability 移除）**
- 觀察行為：`.vitepress/theme/composables/useApi.ts` 與 `.vitepress/theme/__tests__/useApi.spec.ts` 刪除；`composables/index.ts` 不再 re-export useApi / useWsApi；全站 build / typecheck / 測試不受影響。
- 失敗模式：若尚有隱藏呼叫端，typecheck 會失敗——已確認全站無呼叫端。
- 驗收：`grep -rn "useApi\|useWsApi"` 於 `.vitepress`/`docs` 原始碼（排除已刪檔）無結果；`pnpm typecheck` 綠；vitest 少掉 useApi.spec 的測試後仍全綠（預期約 248 passed）；delta spec 含 `vueuse-api-composable` 的 REMOVED Requirements。
- 範圍邊界：只移除 useApi/useWsApi，不動其他 composable。

## Risks / Trade-offs

- [領域內容誤寫入受管區塊 → 被 spectra 升級沖掉] → 一律寫在 `<!-- SPECTRA:END -->` 之後，並於 apply 後 `grep` 驗證位置。
- [challenge.data.ts 改字串常值意外破壞型別或既有題目顯示] → 只改 fallback 字串常值、不動型別；跑 typecheck + vitest 驗證。
- [誤判 useApi 無呼叫端、實際有動態引用] → 已於 propose 前 `grep` 全 `.vitepress`/`docs` 確認無呼叫端；移除後 typecheck / vitest 作為安全網。
- [release.yml YAML 縮排錯誤] → 改後以 python yaml 解析驗證。
- [faker feature 保留但未啟用造成困惑] → 以 Cargo.toml 註解 + design D4 明確記錄其現況與保留理由。

## Migration Plan

- 部署：本變更不需部署，合併即生效；release 產物新名於下次發 tag 時套用。
- 回滾：所有改動為文件/設定/死碼移除，`git revert` 單一 commit 即可回滾；useApi 如日後需要可自 git 歷史還原並重建 spec。

## Open Questions

- 無。所有決策已定案；跨 agent skill 同步與 lit-fetcher 在地化明列為 Non-Goals，留待專責變更。
