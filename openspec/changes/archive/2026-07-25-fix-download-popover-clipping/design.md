## Context

挑戰頁 `ChallengeView` 的編輯器下方 action bar 位於 `overflow-hidden`、高度受 flex 限制的欄位中,並帶有可拖曳的結果區分隔線(resizable-result-panel)。bar 上有兩個 popover 觸發鈕:「下載紀錄」(`DownloadRecordButton.vue`)與「編輯器設定」齒輪(`EditorSettingsPopover.vue`)。

- 設定齒輪已解決過 overflow 裁切:Teleport 到 body + `fixed` 定位向上開、以觸發鈕的 `getBoundingClientRect` 錨定、`mousedown` 外點關閉(先於分隔線拖曳)、Escape 關閉、resize 重定位。該檔案檔頭註解完整記載了此設計脈絡。
- 下載紀錄面板為後續 change 實作,採流內 `absolute` 向下開,被祖先裁切;且無外點/Escape 關閉。
- 兩個 popover 互不知情,可同時開啟。

限制:不引入第三方 floating 函式庫;`EditorSettingsPopover` 對外行為不得改變(既有測試 `__tests__/EditorSettingsPopover.spec.ts` 不改斷言)。

## Goals / Non-Goals

**Goals**

- 下載紀錄面板在預設高度下完整可見(桌面與 tablet),不需先展開結果區。
- 兩個 popover 共用同一套錨定與關閉邏輯(單一實作來源)。
- 同時只允許一個 popover 開啟(互斥)。
- 下載面板誤觸關閉後重開,已填的姓名/班級保留。

**Non-Goals**

- 不改 action bar 版面與樣式;不改匯出邏輯;不做手機直向 sheet UI;不引入 floating-ui。

## Decisions

### D1:抽出 `useAnchoredPopover` composable,而非各元件內聯

兩個 popover 需要同一套 ~60 行的定位/關閉/清理邏輯,且未來可能有第三個(內聯方案每次都要複製)。composable 介面:

```ts
function useAnchoredPopover(options: {
  anchorRef: Ref<HTMLElement | null>   // 觸發鈕
  panelRef: Ref<HTMLElement | null>    // 面板(Teleport 到 body)
}): {
  isOpen: Readonly<Ref<boolean>>
  panelStyle: Readonly<Ref<Record<string, string>>>  // fixed + bottom/right
  toggle(): void
  close(): void
}
```

呼叫端負責:面板的 Teleport 標記、`:style="panelStyle"`、以 `isOpen` 控制顯示(`v-if` 或 `v-show` 由呼叫端決定)。composable 負責:定位計算、document `mousedown` 外點關閉、Escape、window resize 重定位、`onUnmounted` 清理、互斥 registry。

### D2:定位公式沿用 `EditorSettingsPopover` 現行實作

`bottom = max(8, innerHeight − anchorRect.top + 8)`、`right = max(8, innerWidth − anchorRect.right)`,面板向上開、右緣對齊觸發鈕右緣;開啟時定位兩次(open 前一次、`nextTick` 後一次)以涵蓋面板首次渲染的尺寸。理由:此公式已在生產環境驗證,包含視窗邊界 clamp。

**上緣高度上限(adversarial review round 1 修正)**:`panelStyle` 另含 `maxHeight = max(0, anchorRect.top − 16)` 與 `overflowY: auto`——結果區可被拖高,anchor 距視窗底的距離不是常數,任何以 `100vh` 為基底的固定 max-height 常數都可能讓面板頂端超出視窗;由 anchor 即時 rect 推導則不會。此值由 composable 供給,兩個面板同時受惠,呼叫端不再自帶 max-height class。

### D3:互斥採 module-level registry

composable 模組層維護單一 `currentClose: (() => void) | null`。任一實例 open 時:若 `currentClose` 存在且非自身,先呼叫它;再把自身的 close 註冊進去。close 時若 registry 指向自身則清空。理由:兩個元件無需互相 import 或透過 props/provide 認識彼此;第三個 popover 加入時零成本獲得互斥。SSR 安全:registry 只在瀏覽器事件路徑中被觸發。

### D4:外點關閉沿用 `mousedown`(非 `click`)

原因與 `EditorSettingsPopover` 現行註解相同:觸發鈕位於可拖曳分隔線旁,抓住把手拖曳時必須在位置改變**前**關閉面板,否則 fixed 面板會在拖曳期間脫離(已移動的)錨點。此 gotcha 的說明註解隨邏輯移入 composable。

**capture phase(adversarial review round 1 修正)**:`SplitPane` 的收合箭頭用 `@mousedown.stop` 防止分隔線 drag 啟動,bubble 階段的 document 監聽收不到該事件,面板會在佈局位移後留在原地脫錨——故外點監聽改掛 **capture phase**(target 端的 `stopPropagation` 攔不住 capture 傳遞)。

**rAF 錨點追蹤 + 焦點管理,並否決 focusin 方案(round 2 修正)**:round 1 曾以 capture `focusin`(焦點移出即關)涵蓋「鍵盤啟動收合、無 mousedown」的路徑,round 2 review 證實該方案有兩個致命傷:(1) Teleport 面板位於 body 末端、不在 anchor 的 DOM tab 順序內,開啟後按 Tab 焦點幾乎必然落在面板外 → 面板被立即關閉,鍵盤使用者永遠進不了面板(對下載面板是相對 in-flow 舊版的真回歸);(2) mousedown 落在面板內不可聚焦文字(label 死區)時,瀏覽器把焦點重置到 body → focusin(body) 被誤判為 outside → 面板被自己內部的點擊關掉。改為:**開啟期間以 `requestAnimationFrame` 追蹤 anchor rect,位移即重定位**(面板跟著走,涵蓋鍵盤收合與任何無 mousedown 的佈局變動);並補標準焦點管理——面板(`tabindex="-1"`)開啟時取得焦點使 Tab 可達其控制項、關閉時若焦點仍在面板內則還給觸發鈕、外點關閉不搶焦點。追蹤迴圈只在開啟期間運行,close/unmount 時 `cancelAnimationFrame`。

### D5:下載面板改 `v-show` + `max-height`

- `v-show`:面板 DOM 常駐,關閉重開後 `name`/`cls`/`full` 等 ref 綁定的輸入值不因重新掛載而重置(現況 `v-if` 會)。設定 popover 維持 `v-if`(其狀態存於持久化 settings ref,無此需求,且維持既有測試不變)。
- 高度上限與內部捲動:由 composable 的 `panelStyle`(`maxHeight` 依 anchor rect 推導 + `overflowY: auto`)統一供給,見 D2;下載面板不自帶 max-height class。另為 `v-show` 常駐 DOM 的姓名/班級輸入框加 `autocomplete="off"`(縱深防禦:欄位整頁存續,避免瀏覽器自動填充沾上)。

### D6:`EditorSettingsPopover` 重構為薄殼

移除其內聯的定位/關閉邏輯,改用 composable;模板與對外行為(data-testid、aria、開關語意)不變。既有測試作為重構的回歸護欄,不改斷言。

## Risks / Trade-offs

- **重構已上線元件的回歸風險**:以既有測試不改斷言全綠為門檻;audit 階段的 adversarial review 再驗一層。
- **jsdom 無真實 layout**:`getBoundingClientRect` 在單元測試回傳零值,定位斷言以 mock rect 驗證公式,實際視覺以 agent-browser e2e(桌面 + tablet 兩種尺寸)把關。
- **v-show 使下載面板 DOM 常駐**:每個挑戰頁多一個隱藏表單節點,成本可忽略;換頁(元件 unmount)時狀態自然釋放,符合「同頁保留、跨頁不保證」的預期。

## Migration Plan

單一 PR 內完成,無資料遷移。實作順序:composable(含測試)→ `DownloadRecordButton` 切換 → `EditorSettingsPopover` 重構 → 回歸與 e2e。

## Open Questions

(無——行為決策已於 grilling 階段與維護者收斂:互斥、右對齊錨定、v-show 保值、max-height 保險皆已定案。)
