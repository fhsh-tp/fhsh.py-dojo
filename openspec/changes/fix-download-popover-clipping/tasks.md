## 1. 共用 composable

- [x] 1.1 建立 .vitepress/theme/composables/useAnchoredPopover.ts(實作 design 決策「D1:抽出 `useAnchoredPopover` composable,而非各元件內聯」、「D2:定位公式沿用 `EditorSettingsPopover` 現行實作」、「D3:互斥採 module-level registry」、「D4:外點關閉沿用 `mousedown`(非 `click`)」;對應 spec requirements:Anchored upward popover positioning、Popover dismissal and repositioning、Mutual exclusion between anchored popovers):介面 `useAnchoredPopover({ anchorRef, panelRef })` 回傳 `{ isOpen, panelStyle, toggle, close }`。內含:向上錨定定位公式(`bottom = max(8, innerHeight − rect.top + 8)`、`right = max(8, innerWidth − rect.right)`,開啟時定位兩次含 `nextTick` 後一次)、document `mousedown` 外點關閉(anchor 與 panel 內的點擊不關)、Escape 關閉、window resize 重定位、`onUnmounted` 移除全部 listeners、module-level 互斥 registry(open 時先關閉其他實例)。檔頭註解說明 overflow-clipping 背景與「mousedown 而非 click(拖曳分隔線先關閉)」的 gotcha。
- [x] 1.2 建立 .vitepress/theme/__tests__/useAnchoredPopover.spec.ts,覆蓋三條 anchored-popover spec requirements(Anchored upward popover positioning、Popover dismissal and repositioning、Mutual exclusion between anchored popovers):以 mock `getBoundingClientRect` 驗證定位公式與 8px clamp;驗證 toggle/close 狀態;兩實例互斥(開 B 自動關 A);外點 mousedown 關閉、anchor/panel 內 mousedown 不關;Escape 關閉;unmount 後 document/window listeners 不再觸發(spy addEventListener/removeEventListener 配對)。

## 2. DownloadRecordButton 切換

- [x] [P] 2.1 修改 .vitepress/theme/components/editor/DownloadRecordButton.vue(實作 design 決策「D5:下載面板改 `v-show` + `max-height`」;對應 spec requirements:Download panel opens as an anchored upward popover、Download panel form state survives reopen):面板改 `Teleport to="body"` + `:style="panelStyle"`(來自 useAnchoredPopover),顯示改 `v-show="isOpen"`(關閉重開保留姓名/班級/完整版勾選),面板 class 加 `max-h-[calc(100vh-96px)] overflow-y-auto`(矮視窗內部捲動),移除原 `absolute right-0 mt-2` 流內定位;按鈕 `aria-expanded` 綁定 `isOpen`;下載成功後仍呼叫 `close()`。
- [x] [P] 2.2 更新 .vitepress/theme/__tests__/DownloadRecordButton.spec.ts,驗證 Download panel opens as an anchored upward popover 與 Download panel form state survives reopen 兩條 requirement:既有下載流程斷言全數保留;新增——面板渲染於 body(Teleport)、填姓名後 close 再 open 值仍在(v-show)、外點 mousedown 關閉、Escape 關閉。

## 3. EditorSettingsPopover 重構

- [x] [P] 3.1 修改 .vitepress/theme/components/editor/EditorSettingsPopover.vue(實作 design 決策「D6:`EditorSettingsPopover` 重構為薄殼」;對應 spec requirement:Editor settings entry point,含新增的互斥行為):移除內聯的 positionPanel/onDocumentPointerDown/onKeydown/onReposition 與對應 listeners,改用 useAnchoredPopover;模板結構、全部 data-testid、aria 屬性、`v-if` 顯示方式與對外行為不變;檔頭註解改為指向 composable 的設計說明。
- [x] 3.2 執行既有 .vitepress/theme/__tests__/EditorSettingsPopover.spec.ts,回歸驗證 Editor settings entry point requirement 行為不變:斷言零修改全數通過(僅允許 test setup 的 import/mock 路徑調整);此為「D6:`EditorSettingsPopover` 重構為薄殼」的回歸門檻。

## 5. Adversarial review round 1 修正

- [x] 5.1 useAnchoredPopover:外點 mousedown 監聽改 capture phase(穿透 `@mousedown.stop` 類控制,對應 spec scenario「Propagation-stopping control cannot bypass dismissal」)、新增 capture `focusin` 關閉(焦點移出 anchor/panel 即關,對應 scenario「Focus moving outside closes」)、`panelStyle` 新增 `maxHeight = max(0, rect.top − 16)` 與 `overflowY: auto`(對應 scenario「Anchor high in a short viewport」);對應測試各一。
- [x] 5.2 DownloadRecordButton:移除固定 `max-h-[calc(100vh-96px)]` class(改由 composable 供給)、姓名/班級輸入框加 `autocomplete="off"`(v-show 常駐 DOM 的縱深防禦);測試補 Escape 路徑保值與 maxHeight 樣式斷言。
- [x] 5.3 新增 .vitepress/theme/__tests__/popover-exclusion.spec.ts:兩個真實元件同頁互斥的整合測試(雙向),驗證 Mutual exclusion between anchored popovers 於元件層成立。
- [x] 5.4 design.md(D2/D4/D5)與 specs/anchored-popover delta spec 同步上述行為修正。

## 6. Adversarial review round 2 修正

- [x] 6.1 useAnchoredPopover:**移除 capture focusin 關閉**(round 2 證實會讓 Tab 關閉面板、且面板內死區點擊會經 focus-reset-to-body 誤關),改為開啟期間 rAF 追蹤 anchor rect、位移即重定位(對應 scenario「Layout shift without mousedown keeps the panel attached」);新增焦點管理——開啟時 focus 面板(需 `tabindex="-1"`)、關閉時焦點在面板內則還給 anchor、外點關閉不搶焦點(對應新 requirement「Popover focus management」三個 scenarios);close/unmount 時 cancelAnimationFrame。
- [x] 6.2 兩個面板模板加 `tabindex="-1"`;composable 測試改寫(focusin 兩測試移除,新增 rAF 追蹤、focus-on-open、Escape 還焦、外點不搶焦四測試);EditorSettingsPopover.spec.ts 維持零修改全綠。
- [x] 6.3 design.md D4 與 specs/anchored-popover delta spec 同步(移除 focus-close 條文,新增 anchor 追蹤條文與 focus management requirement);maxHeight 貼 0 情境於 D2/程式註解記錄為本站佈局不可達(結果區上限 50%)。

## 4. 驗證

- [x] 4.1 `pnpm typecheck`、`pnpm lint`、`node_modules/.bin/vitest --run` 全綠,無新增 warning。
- [x] 4.2 agent-browser e2e(`pnpm dev` 後),端對端驗證 Download panel opens as an anchored upward popover、Mutual exclusion between anchored popovers、Download panel form state survives reopen、Popover dismissal and repositioning:於 1440×900、1024×768、768×1024 三種視窗開啟下載面板,面板完整可見且不需展開結果區;設定與下載互斥(先開設定再點下載,設定關);填姓名 → 外點關閉 → 重開值保留;拖曳結果區分隔線時面板先關閉。
