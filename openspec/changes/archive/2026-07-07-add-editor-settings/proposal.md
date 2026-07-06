## Why

Production 上有程式底子的學生反映：CodeMirror 的自動完成下拉選單（含斜體的模組／型別提示）與括號自動閉合會干擾他們打字。目前這些行為在 `CodeEditor.vue` 內寫死、無法關閉，學生只能被動接受。此 change 讓學生能自行開關編輯器行為，並把選擇持久化，跨題目、跨 session 都記得。

## What Changes

- 新增全站共用、持久化的「編輯器設定」：v1 提供兩個開關——**自動完成 開/關**、**括號自動閉合 開/關**（兩者預設維持開啟，維持現有行為，不影響尚未調整設定的既有學生）。
- 新增齒輪 ⚙ 入口於題目頁下方按鈕列，點擊彈出 popover 設定面板即時切換。
- 設定以 `localStorage` 持久化（透過 `useLocalStorage`）；讀取為同步，避免首次 paint 閃現預設值。
- 設定變更透過 CodeMirror `Compartment` 的 reconfigure 即時套用，**不重建編輯器**、不丟失游標位置與 undo 歷史。
- `editor-autocomplete` 能力的自動完成與括號自動閉合行為，由「無條件啟用」改為「受使用者設定控制、預設啟用」。

## Capabilities

### New Capabilities

- `editor-settings`: 全站共用、以 localStorage 持久化的編輯器偏好設定；定義設定資料契約（含 schema 版本與數值 clamp）、SSR 安全的讀寫、以及透過 CodeMirror Compartment 對執行中編輯器的即時套用。v1 涵蓋自動完成與括號自動閉合兩個布林開關。

### Modified Capabilities

- `editor-autocomplete`: 自動完成觸發與括號自動閉合，改為受 `editor-settings` 的開關控制；當對應設定為關閉時不得觸發，設定為開啟（含未設定的預設）時維持既有行為。

## Impact

- Affected specs: `editor-settings`（新增）、`editor-autocomplete`（修改）
- Affected code:
  - New:
    - .vitepress/theme/composables/useEditorSettings.ts
    - .vitepress/theme/components/editor/EditorSettingsPopover.vue
    - .vitepress/theme/__tests__/useEditorSettings.spec.ts
  - Modified:
    - .vitepress/theme/components/editor/CodeEditor.vue
    - .vitepress/theme/views/ChallengeView.vue
    - .vitepress/theme/__tests__/CodeEditor.spec.ts
    - openspec/specs/editor-autocomplete/spec.md（透過 delta spec 修改）
  - Removed: （無）
- Dependencies: 沿用既有 `@vueuse/core`（`useLocalStorage`）與 `@codemirror/state`（`Compartment`），不新增第三方套件。
