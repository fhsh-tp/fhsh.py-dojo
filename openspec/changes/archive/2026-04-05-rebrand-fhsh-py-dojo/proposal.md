## Why

此專案由 `crypto-challenge` fork 而來，核心 Judge 架構完整保留，但品牌識別、說明文件與範例內容仍殘留密碼學題目的文字。需要將專案重新定位為「台北市立復興高級中學 Python 自學道場」，並新增 HTTP / WebSocket 通用 composable 以支援後續功能開發。

## What Changes

- `package.json`：`name` 改為 `fhsh-py-dojo`；移除 `pycryptodome` 相關依賴；新增 `@vueuse/core`
- `.vitepress/config.mts`：`title`、`description`、GitHub socialLink 改為 FHSH Python 自學道場
- `docs/index.md`：Hero 區塊文字（名稱、tagline）改為 Python 自學道場
- `README.md`：全部改寫為 FHSH Python 自學道場說明
- `CHANGELOG.md`：清空舊歷史，建立 v1.0.0 新起點
- `LICENSE`：版權持有人改為 `MIS@FHSH（臺北市立復興高級中學資訊組）`，年份動態抓取
- `Usage.md`：標題與範例從密碼學題目改為 Python 演算法題
- `openspec/specs/challenge-dual-theme/spec.md`：將 "Cryptography Challenge site" 改為 "FHSH Python 自學道場"，視覺定義（Matrix Terminal / SOC-SIEM）不動
- `openspec/specs/encrypted-pool-generation/spec.md`：移除 preflight 對 `pycryptodome` / `Crypto.Cipher.DES` 的強制檢查；`requirements.txt` 不再強制要求 `pycryptodome`
- `openspec/specs/editor-autocomplete/spec.md`：更新失效的 `@trace` 路徑（原指向已刪除的 caesar-*.md）
- `openspec/specs/vitepress-markdown-panel/spec.md`：更新失效的 `@trace` 路徑（原指向已刪除的 vigenere-encrypt.md）
- **新增** `.vitepress/theme/composables/useApi.ts`：使用 `@vueuse/core` 的 `useFetch` 與 `useWebSocket`，提供通用 HTTP + WebSocket wrapper

## Non-Goals

- 不修改 Judge 核心架構（testcase-generator、Pyodide、WASM、scripts、stores、components）
- 不修改 challenge-dual-theme 視覺美學（Matrix Terminal dark / SOC-SIEM light 風格定義不動）
- 不刪除 `openspec/changes/`（保留所有歷史 changes）
- 不修改 `assets/banner.png`（由使用者自行處理）

## Capabilities

### New Capabilities

- `vueuse-api-composable`：通用 HTTP (`useFetch`) 與 WebSocket (`useWebSocket`) composable wrapper，供後續功能使用

### Modified Capabilities

- `encrypted-pool-generation`：移除對 `pycryptodome` 的強制預檢，Python 題目不需要密碼學套件

## Impact

- Affected specs: `encrypted-pool-generation`（requirement 修改）；`vueuse-api-composable`（新增）；`challenge-dual-theme`、`editor-autocomplete`、`vitepress-markdown-panel` 的 spec 文字/trace 路徑作為 metadata 更新（非 requirement 變更）
- Affected code: `package.json`、`.vitepress/config.mts`、`docs/index.md`、`README.md`、`CHANGELOG.md`、`LICENSE`、`Usage.md`、`.vitepress/theme/composables/useApi.ts`（新增）
- Affected dependencies: 新增 `@vueuse/core`；移除 `pycryptodome` 相關 Python 依賴
