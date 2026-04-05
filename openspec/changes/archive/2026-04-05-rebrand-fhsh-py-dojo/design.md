## Context

此專案由 `crypto-challenge` fork 而來，核心 Judge 架構（Rust WASM testcase-generator、Pyodide、AES-256-GCM pool encryption）完整保留，只有品牌文字、說明文件、Python 依賴宣告，以及 `openspec/specs` 的說明文字需要更新。

此外，新增一個使用 `@vueuse/core` 的通用 composable（`useApi.ts`），提供 HTTP 請求（`useFetch`）與 WebSocket 連線（`useWebSocket`）的包裝，供後續功能使用。

## Goals / Non-Goals

**Goals:**

- 將所有使用者可見的品牌文字從「Crypto Challenge / 密碼學挑戰」改為「台北市立復興高級中學 Python 自學道場」
- 更新 `openspec/specs` 中的說明文字與失效的 `@trace` 路徑引用
- 移除 `pycryptodome` 作為必要依賴（Python 自學道場的題目生成器不需要密碼學套件）
- 新增 `useApi.ts` composable 作為 HTTP / WebSocket 通用 wrapper
- 更新 LICENSE 版權持有人

**Non-Goals:**

- 不修改 Judge 核心架構或任何元件邏輯
- 不修改視覺主題（Matrix Terminal dark / SOC-SIEM light 保持不變）
- 不刪除 `openspec/changes/`

## Decisions

### 版權年份動態抓取

LICENSE 中的年份使用 `new Date().getFullYear()` 在 README/文件中提及動態年份，但 LICENSE 本身是靜態文字檔，直接寫入當前年份（`2026`）即可。若需要每年更新，可在 CI 腳本中自動處理；當前階段靜態寫入為最簡方案。

### `useApi.ts` 設計：Bare Wrapper

`useApi.ts` 採用最小包裝設計（bare wrapper），不預設 `baseURL`、不注入 headers，呼叫方自行傳入完整 URL。這樣保持最大靈活性，後續可在個別 feature 中再包一層設定。

`useFetch` wrapper 回傳 VueUse `UseFetchReturn` 型別，直接透傳所有選項。

`useWebSocket` wrapper 回傳 VueUse `UseWebSocketReturn` 型別，直接透傳所有選項。

### pycryptodome 移除策略

`encrypted-pool-generation` spec 中的 preflight 檢查原本 hard-code `Crypto.Cipher.DES` import test，這是針對密碼學題目的特定需求。移除後，preflight 只需確認 Python 3 與 `PyYAML` 可用即可。`requirements.txt` 只保留 `PyYAML`。

## Risks / Trade-offs

- [Risk] 若未來有題目確實需要 `pycryptodome`，需手動重新加回 `requirements.txt` → 題目作者在 frontmatter generator 中使用 `from Crypto import ...` 時，會在 pool generation 時產生清楚的錯誤訊息，可在當下補加依賴
- [Risk] `useApi.ts` 的 bare wrapper 缺乏型別約束 → 可接受，後續按需擴充
