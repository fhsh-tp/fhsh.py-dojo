# 內容貢獻指南 (Content Contribution Guide) 🚀

歡迎加入 **fhsh.py-dojo**！本專案的核心目標是提供優質的 Python 教學內容與程式挑戰。這份指南專為 **「內容貢獻者」** 設計，旨在幫助你順利新增 **教學文章 (Tutor)** 或 **程式挑戰 (Challenge)**。

為了確保多位貢獻者同時開發時不會發生 ID 衝突或連結失效，請務必嚴格遵守以下 SOP。

---

## 🌟 核心規則：分支與 Rebase 策略

本專案採用 **Git Flow** 模式，並以 `staging` 分支作為開發集成的核心：

1. **`staging` 是唯一目標**：所有 PR 必須發給 `staging` 分支。
2. **Rebase 是強制性的**：
   - **為什麼？** 因為挑戰題目的 `id` 是由腳本取該 category 前綴內現有最大序號 +1 自動計算的（例如 python 題現有至 `py054` 時新題配 `py055`）。如果兩個人同時基於舊的進度開發，會產生重複的 `id`，導致系統崩潰。
   - **時機 A**：在執行 `new-challenge` 或 `new-tutor` 腳本**之前**，必須先同步最新的 `staging`。
   - **時機 B**：在發起 PR **之前**，建議再次 Rebase 以確保歷史紀錄整潔。

---

## 🛠️ Phase 1: 環境準備 (Environment Setup)

請確保你的電腦已安裝：
- **Node.js (v22+)** 與 **pnpm**
- **Rust & wasm-pack** (新增挑戰時，需要它來測試判定引擎；wasm-pack 以 `cargo install wasm-pack` 安裝，由 cargo 提供，**不隨 `pnpm install` 安裝**)
- **Python 3** (用於測試題目生成器)

```bash
# 安裝 wasm-pack（由 cargo 提供，非 npm 相依）
cargo install wasm-pack

# 安裝 JS 依賴
pnpm install
```

---

## 🏗️ Phase 2: 新增程式挑戰 (New Challenge) SOP

### Step 1: 同步與建立分支
```bash
git checkout staging
git pull upstream staging
git checkout -b content/challenge-<name>
```

### Step 2: 執行生成腳本
**重要**：請勿手動建立檔案，請使用腳本以自動分配唯一的 `id`（字串格式 `<category 前綴><3 位零填充序號>`，取該 category 前綴內現有最大序號 +1，例如 `py055`、`apcs006`）。
```bash
# <name> 必須是小寫 kebab-case (例如: hello-world)
pnpm new-challenge <name> --title "你的題目名稱" --difficulty easy
```
檔案會建立在 `docs/challenge/<name>.md`。

### Step 3: 編輯內容與 YAML Metadata
打開建立的 `.md` 檔案，編輯以下核心區塊：
- `params`: 定義生成器會用到的參數範圍（例如 `n` 為 1~100）。
- `generator`: **關鍵！** 這是一段 Python 程式碼，它必須輸出（print）一組隨機測試資料。
- `starter_code`: 給學生的初始代碼框架。
- `testcase_count`: 預設 5 組，系統會跑 5 次 generator 來產生測資。

### Step 4: 編譯題目池與本地測試
新增題目後，必須重新編譯加密題目池才能在網頁看到：
```bash
pnpm build:pools
pnpm dev
```
前往 `http://localhost:5173/challenges` 找到你的題目，**請親自跑過一次並確認可以通過 (Accepted)**。

---

## 📚 Phase 3: 新增教學文章 (New Tutor) SOP

### Step 1: 同步與建立分支
```bash
git checkout staging
git pull upstream staging
git checkout -b content/tutor-<subject>-<section>
```

### Step 2: 執行生成腳本
```bash
# 格式：pnpm new-tutor <領域> <章節> <小節> --title "標題"
# 範例：新增 Python 模組 1 的 1-4 小節
pnpm new-tutor py ch1 1-4 --title "迴圈的藝術" --challenge hello-world
```
檔案會建立在 `docs/tutor/py/ch1/1-4.md`。

### Step 3: 編輯文章內容
- 遵循 **「概念溯源 -> 教學內容 -> 範例說明 -> 實戰」** 的結構撰寫。
- 如果有對應的挑戰題目，腳本會自動插入 `<ChallengeLink slug="hello-world" />`。

### Step 4: 更新章節索引 (Manual Step)
你必須手動編輯該章節的 `index.md`（例如 `docs/tutor/py/ch1/index.md`），將你的新小節加入清單中，否則導覽列將看不到它。

---

## 📤 Phase 4: 提交 PR 檢核表 (Checklist)

發起 PR 前，請逐一檢查：

1. [ ] **再次 Rebase**：執行 `git fetch upstream && git rebase upstream/staging`。
2. [ ] **程式碼格式化**：執行 `pnpm format`。
3. [ ] **本地預覽**：執行 `pnpm dev`，確認文章顯示正常、挑戰題目可以被解出。
4. [ ] **發送 PR 到 `staging` 分支**：再次確認 Base 分支是 `staging` 而非 `main`。
5. [ ] **標題規範**：PR 標題建議為 `content(challenge): 新增 <名稱>` 或 `content(tutor): 新增 <章節名稱>`。

---

## 🗑️ 刪除或重新命名題目：登記退役帳本

刪掉或改名一道已上線的題目時，**必須**把它的舊 slug（檔名）與舊 id 登記到 `scripts/retired-challenges.json`，否則日後 `pnpm new-challenge` 可能把同一個 slug 配給不相干的新題目，讓學生的本機進度（以 slug 為 key）錯誤地繼承過去。

```json
{
  "slugs": ["caesar-01"],
  "ids": ["py059"]
}
```

- `slugs`：檔名去掉 `.md`，字串。
- `ids`：**字串**格式的挑戰 id（`"py059"`、`"apcs003"`），**不是**數字 `59`、也不是 `"59"`。
- 格式寫錯時 `pnpm new-challenge` 會直接拒絕執行並指名出錯的那一筆——這是刻意的，帳本不能在無人察覺的情況下失效。

---

## 🆘 常見衝突處理：ID 衝突

如果你在 PR 過程中發現 `docs/challenge/` 下的題目 `id` 與其他人重複了：
1. 先 `git rebase upstream/staging`。
2. 手動修改你的 `.md` 檔案，將 `id` 改為該 category 前綴內目前最大序號 +1（3 位零填充，例如 python 題現有至 `py054` 時改為 `py055`）。
3. `git add .` -> `git rebase --continue`。
4. `git push -f origin <your-branch>`。

感謝你的參與，讓我們一起讓 **fhsh.py-dojo** 成為最棒的 Python 學習基地！🐍✨
