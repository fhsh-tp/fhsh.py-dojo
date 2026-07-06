## Context

`CodeEditor.vue` 目前在 `onMounted` 內把 CodeMirror extensions 寫死成一個固定陣列：`autocompletion()`、`closeBrackets()`、字級、`oneDark` 等皆不可調。有程式底子的學生反映自動完成與型別提示干擾打字，卻無從關閉。

專案既有的持久化分層（`persistence/db.ts` + `stores/progress.ts`）以 IndexedDB 存放「逐題、結構化、量大」的作答軌跡；編輯器偏好則是「全站一份、扁平、需同步讀取」的小資料，性質不同。`@vueuse/core`（提供 `useLocalStorage`）與 `@codemirror/state`（提供 `Compartment`）皆已是相依套件，無須新增。

決策來源：`/spectra-discuss` 結論與 `.spectra/poc/` 方案 A（齒輪 popover）。

## Goals / Non-Goals

**Goals:**

- 讓學生可自行開關自動完成與括號自動閉合，選擇跨題目、跨 session 持久化。
- 預設維持現行行為（兩者皆開），不影響尚未調整設定的既有學生。
- 設定變更即時生效，且不重建編輯器、不丟失游標與 undo 歷史。
- 建立一個可擴充的設定契約與單一 seam，之後新增字級／Tab／行號／佈景等設定時沿用同一機制。

**Non-Goals:**

- 不做逐題（per-challenge）設定；v1 為全站共用一份。
- v1 不納入字級、Tab 寬度、行號、編輯器佈景、自動換行（PoC 中以「規劃中」呈現，留待後續 change）。
- 不處理跨分頁即時同步的一致性保證（多分頁為最佳努力）。
- 不修正「編輯器佈景寫死 oneDark、未跟隨站台亮／暗」的既有不一致——記錄為後續 change。

## Decisions

### 以 localStorage（useLocalStorage）持久化，不用 IndexedDB

設定是小而扁平的全站單一 blob，且需要在編輯器首次 paint 前同步取得，否則會先套預設值、hydrate 後才跳成使用者設定造成閃爍。`localStorage` 為同步讀取，天然符合；IndexedDB 為非同步，會產生上述閃爍，且其結構化能力對本情境是浪費。IndexedDB 續留給 progress／session 那類大且結構化的資料。

替代方案：沿用 IndexedDB 統一持久化層——否決，理由如上（非同步閃爍 + 過度設計）。

### 狀態集中於 useEditorSettings composable（模組級單例 + SSR 安全）

新增 `.vitepress/theme/composables/useEditorSettings.ts` 作為設定契約的唯一擁有者：負責 defaults 合併、schema 版本、值正規化（布林強制、未來數值 clamp）、以及 SSR 安全。以模組級單例持有一個 `useLocalStorage` 背後的共享 reactive ref，讓 `CodeEditor.vue` 與 `EditorSettingsPopover.vue` 讀到同一份即時狀態（同分頁內兩個獨立 `useLocalStorage` 呼叫不會自動互相同步，故需單例）。

SSR 安全：`typeof window === 'undefined'` 時回傳一個臨時的預設值 ref（不快取為單例），避免把 server 端 ref 汙染到 client。此為新的儲存抽象，seam 通過刪除測試：移除它則持久化與設定 UI 皆失效。

替代方案：Pinia store 疊在 composable 疊在 localStorage——否決，三層 pass-through，違反專案深度守則。

### 以 CodeMirror Compartment 即時 reconfigure，不重建編輯器

將可切換的 extension 各包一個 `Compartment`：`acCompartment` 對應自動完成相關 extension（`autocompletion()` 與 stdlib 完成來源註冊），`bracketCompartment` 對應 `closeBrackets()`。設定變更時 `dispatch({ effects: compartment.reconfigure(...) })`，開啟時套用對應 extension、關閉時套用空陣列。如此切換不需 `new EditorView`，游標位置與 undo 歷史都保留。

替代方案：改設定即重建 EditorView——否決，每次切換都清空游標與復原歷史，體驗差。

### 齒輪 popover 為獨立元件 EditorSettingsPopover

新增 `.vitepress/theme/components/editor/EditorSettingsPopover.vue`，自帶齒輪 ⚙ 按鈕與彈出面板，內部以 `useEditorSettings()` 綁定兩個開關；面板支援點擊外部與 Esc 關閉。放置於 `ChallengeView.vue` 下方按鈕列。元件化讓設定 UI 與題目頁解耦，日後改版型（drawer／modal）只需替換此元件。

### 設定資料契約：schema 版本、defaults 合併與數值 clamp

設定型別 `EditorSettings` 含 `version` 欄位；讀取時以 defaults 合併補齊缺漏欄位並正規化（布林欄位強制為布林）。`version` 用於未來欄位演進的向前相容遷移。v1 僅布林欄位，clamp 邏輯為未來數值設定（如字級）預留其位置與測試骨架。

## Implementation Contract

**Behavior（可觀察行為）:**

- 題目頁下方按鈕列出現齒輪 ⚙；點擊彈出 popover，內含「自動完成」「括號自動閉合」兩個開關，預設皆為開啟。
- 關閉「自動完成」後，於編輯器輸入時**不再**出現完成下拉選單；重新開啟即恢復。
- 關閉「括號自動閉合」後，輸入 `(`、`[`、`{` **不再**自動補上對應右括號；重新開啟即恢復。
- 切換任一開關後，編輯器的游標位置與 undo 歷史保持不變（非重建）。
- 重新整理頁面或切換到其他題目，先前的開關選擇仍保留。

**Interface / data shape:**

- `EditorSettings`：`{ version: number; autocomplete: boolean; closeBrackets: boolean }`。
- `useEditorSettings(): Ref<EditorSettings>`——回傳跨元件共享的 reactive ref（client 端為 localStorage 背後單例，SSR 為臨時預設值 ref）。
- localStorage key 使用穩定字串常數；預設值 `{ version: 1, autocomplete: true, closeBrackets: true }`。

**Failure modes:**

- localStorage 不可用（隱私模式／SSR）：讀取回傳預設值、寫入為 no-op；編輯器與作答流程不得因此中斷（最佳努力，對齊既有持久化層的降級策略）。
- 儲存內容損毀或缺欄位：以 defaults 合併與正規化修復，不得拋例外。

**Acceptance criteria:**

- `useEditorSettings.spec.ts`：驗證預設值、缺欄位以 defaults 補齊、布林正規化、寫入後再讀取可還原（persistence round-trip）。
- `CodeEditor.spec.ts`：驗證 `autocomplete: false` 時完成來源不啟用／不顯示；`closeBrackets: false` 時輸入 `(` 不自動補 `)`；預設值下維持既有 autocomplete 與 bracket 行為（既有測試不得回歸）。
- 手動：於題目頁點齒輪切換兩開關，觀察即時生效且游標／undo 不受影響；重整後選擇仍在。

**Scope boundaries:**

- In scope：`useEditorSettings` composable、`EditorSettingsPopover` 元件、`CodeEditor.vue` 的 Compartment 化與即時套用、`ChallengeView.vue` 掛載齒輪、`editor-autocomplete` spec 的行為 gating、上述測試。
- Out of scope：字級／Tab／行號／佈景／換行等設定項、逐題設定、跨分頁強一致、oneDark 亮暗同步修正。

## Risks / Trade-offs

- [模組級單例在測試間狀態殘留] → 於測試提供重設途徑（模組隔離或匯出重設用 helper），並在測試 setup 清 localStorage。
- [SSR 期間誤觸 localStorage] → 以 `typeof window === 'undefined'` 守衛回傳臨時預設值 ref，不快取為單例；沿用 progress store 的 client-only 存取原則。
- [Compartment 初始設定與 localStorage 首讀時序] → 於 `onMounted` 建立 EditorView 前先同步讀取設定值再組 extensions，確保初始狀態即為使用者選擇。
- [關閉自動完成後仍保留完成來源註冊] → 以 Compartment 一併移除自動完成 UI extension；來源即使殘留也不會在無 `autocompletion()` 時顯示，行為正確。

## Open Questions

- （無）決策皆已於 `/spectra-discuss` 收斂。
