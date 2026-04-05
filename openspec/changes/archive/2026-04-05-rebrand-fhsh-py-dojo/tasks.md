## 1. 依賴與設定更新

- [x] 1.1 更新 `package.json`：`name` 改為 `fhsh-py-dojo`、新增 `@vueuse/core` 至 `dependencies`（@vueuse/core is listed as a dependency）
- [x] 1.2 更新 `requirements.txt`（Python dependency manifest exists at project root）：移除 `pycryptodome`，只保留 `PyYAML`（pycryptodome 移除策略）

## 2. 品牌文字更新

- [x] 2.1 更新 `.vitepress/config.mts`：`title` 改為「台北市立復興高級中學 Python 自學道場」、`description` 更新、`socialLinks` GitHub URL 改為新 remote
- [x] 2.2 更新 `docs/index.md` hero 區塊：`name`、`text`、`tagline` 改為 Python 自學道場文字
- [x] 2.3 全部改寫 `README.md` 為 FHSH Python 自學道場說明（含版權年份動態抓取）
- [x] 2.4 清空 `CHANGELOG.md`，建立 v1.0.0 新起點（格式符合 Keep a Changelog）
- [x] 2.5 更新 `LICENSE`：版權持有人改為 `MIS@FHSH（臺北市立復興高級中學資訊組）`，年份改為 `2026`（版權年份動態抓取）

## 3. Usage.md 更新

- [x] 3.1 改寫 `Usage.md` 標題與開頭說明（「密碼學挑戰題目」→「Python 自學道場題目」）
- [x] 3.2 更新 `Usage.md` 所有密碼學範例（caesar_encrypt、aes_ecb_encrypt、Vigenère、凱薩加密等）改為 Python 算法題範例（如 fibonacci、bubble_sort、binary_search 等）
- [x] 3.3 更新 `Usage.md` 難度分級參考表，改為 Python 算法題難度描述

## 4. openspec/specs 文字更新

- [x] 4.1 更新 `openspec/specs/challenge-dual-theme/spec.md` Purpose 第一行：「Cryptography Challenge site」→「FHSH Python 自學道場（台北市立復興高級中學 Python 自學道場）site」
- [x] 4.2 更新 `openspec/specs/encrypted-pool-generation/spec.md`（Build script generates encrypted testcase pools）：移除 `pycryptodome` 與 `Crypto.Cipher.DES` 的預檢邏輯描述；刪除「Generator with external Python dependencies executes correctly」scenario；更新 "Python dependency manifest exists at project root" 要求（移除 pycryptodome 相關 scenario）
- [x] 4.3 更新 `openspec/specs/editor-autocomplete/spec.md` 所有 `@trace` 區塊：移除已刪除的 `docs/challenge/caesar-basic.md`、`caesar-advanced.md`、`caesar-custom-table.md` 引用
- [x] 4.4 更新 `openspec/specs/vitepress-markdown-panel/spec.md` 所有 `@trace` 區塊：移除已刪除的 `docs/challenge/vigenere-encrypt.md` 引用

## 5. useApi Composable 實作

- [x] 5.1 建立 `.vitepress/theme/composables/useApi.ts`：匯入 `@vueuse/core` 的 `useFetch`，實作 `useApi` bare wrapper（useApi composable provides useFetch wrapper、`useApi.ts` 設計：Bare Wrapper）
- [x] 5.2 在 `useApi.ts` 加入 `useWsApi` 函式：匯入 `useWebSocket`，實作 bare wrapper（useApi composable provides useWebSocket wrapper）
- [x] 5.3 建立 `.vitepress/theme/composables/index.ts` barrel export 檔，匯出 `useApi`、`useWsApi` 及現有的所有 composables（useApi composable is exported from theme composables index）
