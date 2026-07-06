## 1. 移除 npm wasm-pack 相依與其 build 允許項

- [x] 1.1 由 `package.json` 的 devDependencies 移除 `wasm-pack` 項，並由 `pnpm-workspace.yaml` 的 `allowBuilds` 移除 `wasm-pack`（移除後若 `allowBuilds` 為空則刪除整個 block），落實「CI dependency install needs no wasm-pack binary」需求所依賴的「wasm-pack 非 npm 相依」前提，並實作 design 決策 "Remove the npm wasm-pack dependency rather than pin or repoint it"。驗證：`grep -n wasm-pack package.json pnpm-workspace.yaml` 不再出現 wasm-pack 相依/允許項。
- [x] 1.2 重新產生 `pnpm-lock.yaml` 使其不再含 wasm-pack 及其僅供 wasm-pack 使用的 transitive 相依（於本機執行安裝以更新 lockfile）。驗證：`pnpm install --frozen-lockfile` 成功、輸出無 wasm-pack postinstall 行；`grep -c "wasm-pack@" pnpm-lock.yaml` 為 0（或不再有 top-level wasm-pack 套件）。

## 2. 還原 CI verify 安裝步驟並更新註解

- [x] 2.1 [P] 將 `.github/workflows/ci.yml` 的 Install dependencies 步驟由 `pnpm install --frozen-lockfile --ignore-scripts` 改回 `pnpm install --frozen-lockfile`，並更新該步驟註解說明 wasm-pack 由 cargo（本機）與 `jetli/wasm-pack-action`（release CI）提供、不再經 npm——實作「CI dependency install needs no wasm-pack binary」需求（含「No ignore-scripts workaround is needed」場景），並落實 design 決策 "Revert the CI `--ignore-scripts` workaround once the root cause is gone"。驗證：`grep -n "ignore-scripts" .github/workflows/ci.yml` 無結果；install 步驟為純 frozen 安裝且註解已更新。

## 3. 文件：宣告 wasm-pack 為本機前置需求

- [x] 3.1 [P] 在 `CONTRIBUTE.md` 與 `README.md` 的環境需求／建置前置處，新增「wasm-pack 以 cargo 安裝（例如 cargo install wasm-pack）、不再由 pnpm 提供」的說明，對齊「Full project build in CI」需求中「wasm-pack 由 toolchain 提供、專案不宣告 npm wasm-pack 相依」的規範，並落實 design 決策 "Document cargo as the local wasm-pack source"。驗證：兩檔皆出現 wasm-pack 以 cargo 安裝的前置需求敘述。

## 4. 端到端驗證（安裝／解析／建置／四道 gate）

- [x] 4.1 驗證移除後工具鏈解析正確且建置可行：`pnpm exec which wasm-pack` 不再回 `node_modules/.bin` 路徑（解析到 cargo 全域版）；`pnpm build:wasm` 以 PATH wasm-pack 完成並在 `docs/public/wasm/` 產出檔案。驗證：前述兩指令皆符合預期，坐實「Full project build in CI」需求中「wasm-pack comes from the toolchain, not npm」場景於本機的等效行為。
- [x] 4.2 跑四道 gate 確認無回歸：`pnpm typecheck`、`pnpm lint`、`pnpm test --run`、`cargo test --manifest-path testcase-generator/Cargo.toml` 全數通過。驗證：四者皆 exit 0；lint warning 數不超過既有門檻。
