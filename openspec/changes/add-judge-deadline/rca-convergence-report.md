# RCA 報告：`add-judge-deadline` 兩輪對抗覆核未歸零

## 前言

受審對象為 change `add-judge-deadline`（branch `feat/judge-deadline`），目的是讓判題引擎補上真正生效的每筆測資 deadline。協定規定 propose → apply → audit → 多代理對抗覆核 → 合成 evidence table → fix → commit，並要求 2 輪內歸零。R1 動用 14 個代理、47 條原始發現，存活 1 條 critical ＋ 13 條 major；修正輪三個 commit（`201d9b5`／`3e47819`／`7e31aed`）；R2 動用 10 個代理、27 條原始發現，存活 2 條 critical ＋ 9 條 major，送驗的 6 條全數 CONFIRMED、零推翻。R2 對 R1 的 11 項必修逐條驗證的結果是 4 項生效、5 項半生效、2 項完全未生效。本報告由三份乾淨脈絡的獨立分析合成，並經我獨立複核關鍵事實（複核方式與結果見文中「證據」欄與第五節）。

---

## 一、兩輪抓到什麼

| 輪次 | 結構性缺陷（改變設計） | 出貨級缺陷（可被學生利用／可誤判） | 文件／量測缺陷 |
|------|------------------------|------------------------------------|----------------|
| **R1**（47 條原始，存活 1C＋13M） | 5,000 ms 軟旗標對同步 Python 永不觸發（macrotask 必輸給 clearTimeout 的 microtask）；沙箱守衛用 `find_module`，在現行 Pyodide 已是死碼；watchdog 接在無任何呼叫端的 `useExecutor.run()` 上 | `sys.settrace(None)` 凍結 op 計數；同行攤平稀釋成本；`math.perm ＋ Legendre` 收編路線實測 20/20、單筆最大 2,052–2,182 ms，安全倍率由 13.3× 降為 2.29× | 矩陣 O3「收編路線併入 O2 量測」為偽——收編路線當時一條都沒量 |
| **修正輪**（3 commit，零覆核） | 沙箱改 `find_spec` ＋ 6 條真 Pyodide 測試；watchdog 改接 `useChallengeRunner.submit()`；trace 還原清單擴充 | — | 新增 `measure/routes/prize_mathperm.py` 與 `rank_mathfactorial.py` 兩次量測；**新增** design〈D5 衝突的處置〉一節、一次維護者三選一裁決、一份修訂**已上線題目保證**的 spec delta |
| **R2**（27 條原始，存活 2C＋9M，送驗 6/6 CONFIRMED） | 沙箱守衛可由 `sys.meta_path.pop(0)` 兩行拆除，另有 `_pyodide._importhook.jsfinder` 完全不碰 meta_path 的旁路——R2 在生產建置上武器化為「6.5 秒的測資記成 AC 1 ms、5/5 通過」；dev watchdog 的唯一真實環境 `vitepress dev` 無跨來源隔離、`SharedArrayBuffer` 不存在，`arm()` 為 no-op，**淨效果與修正前完全相同**；收編路線量錯對象（逐位剝零＝矩陣 F11 的死路，非 spec／D6.b／F19 的 Legendre），**D5 衝突從來不存在** | `builtins.__import__` 置換使 op 計數器永久毒化（輸出正常、ops 恆為 0）；`_op_limit = 1` 使內建守衛含上限數值的原文顯示在生產結果面板 | 「七筆停在 deadline」實為八筆（判定序列 `AAAAAAAATTTTTTTATAAA`，A=12、T=8），且 `12 + 7 = 19 ≠ 20` 內部自我否證，該數字已寫進準備上線的 spec delta；`trace-matrix.md:100`（「使可行域成為空集合」）與 `:103`（「D5 所擔心的空集合未發生」）同檔直接矛盾；design.md:227 的「約 15 秒」無矩陣 ID 且在當時量測配置下原理上不可得 |

每一輪的機械驗證（vitest 全套件、typecheck、lint、`spectra analyze`／`validate`）**每次都全綠**。

---

## 二、根因

三份分析共提出 19 條根因，去重與層次判定後合成為 9 條。編號 `A`＝驗證裝置解析度分析、`B`＝對象選錯分析、`C`＝規範傳播分析。

---

### 根因 1｜既有改善清單存在於另一條 branch，本 change 的工作樹讀不到

**陳述**：三份分析被要求對照的兩份既有 RCA，在 `feat/judge-deadline` 上**根本不存在**。我實測：`openspec/changes/archive/` 底下唯一的 RCA 是 `2026-08-06-add-bracket-check-duo/rca-convergence-report.md`（I-1～I-8、P-1～P-11、T-1～T-6）；`2026-08-10-add-exhibit-route-duo/rca-convergence-report.md`（I-9～I-14）與 `rca-handoff-review.md`（RC-1～RC-6、H-1～H-6）只存在於未合併的 `feat/exhibit-route-duo`（commit `3c517c0`、`ea911a1`）。rank-code-duo 的教訓則只活在 `~/.claude/.../memory/project_rank_code_duo.md`。也就是說：本 change 的作者與兩輪 14＋10 個稽核代理，在結構上**不可能**讀到 I-9～I-14 與 H-1～H-6，而 I-11 與「上界取最貴、下界取最便宜」正是本次第 3 條失效的正解。

**證據**：`git ls-tree -r --name-only feat/exhibit-route-duo | grep -i rca` 列出兩檔；同指令對 `feat/judge-deadline` 為空。三份分析中，分析 A 與 B 對 I-11／RC-4／H-6 的引用全部轉述自任務簡報的摘句（簡報引用了 I-11 的標題），分析 C 則誠實回報「檔案不存在、無法核對」——**一份談「引用了不存在的來源而無人核對」的報告，自身的來源引用也讀不到**，這是分析 C 自己標記為未解的觀察，我在此定性完成。

**解釋哪幾次失效**：不直接造成任何一次，但它是後面所有「舊病復發」欄位得以成立的**使能條件**——沒有它，第 3 條失效有現成的正解（P-7 全稱否定句、P-5 下限紀律、I-11 家族化）擋在前面。

**與既有清單的關係**：**RC-1／RC-6 的舊病復發，且升了一級**。RC-1 說「驗證通道＝作者活體工作樹，交付通道是 tip／clone」；本次是「改善清單的通道＝寫它的那條 branch，使用它的通道＝別條 branch」。H-3（乾淨 worktree 驗證）對它完全無效——乾淨 clone 上那兩個檔案照樣不存在。既有清單沒能阻止它，是因為 H 系列全部在談「被審物如何驗證」，沒有一條在談「改善清單本身住在哪裡」。

---

### 根因 2｜證物不隨發現移交：finding 只交付散文數字，可執行物件留在 `/tmp`

**陳述**：R1 **已經量對了**。至少三個代理（CF-JD1／MX-F2／RB-F9）各自依 shipped spec 實作真正的 `math.perm ＋ Legendre` 路線，在同一支 `measure.sh`、同一條 `:8788` 生產路徑上得到 20/20、單筆最大 2,052–2,182 ms，被合成為 CONFIRMED／必修（阻擋）。但產生那個數字的 `.py` 活在 `/tmp/perm_route.py`（R1 journal 明寫），交付給修正輪的只有散文裡的「2,052 ms、20/20」。修正輪因此必須**從名稱重新實作**，寫出 `while p % 10 == 0: p //= 10`，量得 12/20、5,026 ms——與它正在修的那條 finding 自帶的數字差 2.4 倍、分數完全相反——然後據此宣告「D5 可行域為空集合」。鑑別性的關鍵詞在鏈上逐段掉落：spec「math.perm-with-Legendre」→ tasks「math.perm＋Legendre」→ 檔名 `prize_mathperm.py` → results 標籤 `coopt_mathperm` → 矩陣 O3「`math.perm`」。

**證據**：`measure/routes/prize_mathperm.py` 檔頭註解**逐字抄了 spec 的「math.perm with Legendre trailing-zero counting」，函式體卻是逐位剝零**——來源讀過、抄進註解、身體寫成別的東西，沒有任何一步比對這兩者（我已讀原檔確認）。`results.jsonl` 第 21 列 `prize-order-code:coopt_mathperm` score=12、max_ms=5026、verdicts `AAAAAAAATTTTTTTATAAA`（我以 Python 解析確認 A=12、T=8）。主代理事後複現的 `prize_mathperm_legendre.py` 得 20/20、單筆最大 2,234 ms。

**解釋哪幾次失效**：失效 3 的直接機制；並解釋為何處置從 R1 建議的「把 13.3× 誠實改為 2.44×」升級成「宣告空集合、請維護者裁決、修訂已上線 spec」。

**層次取捨**：三份分析都指向此處但命名不同——A 稱「發現被壓縮成標題＋嚴重度＋處置」、B 稱「名稱不足以還原物件」、C 稱「證物是暫存品」。我取 C 的框架（**證物監管鏈斷裂**）為根因，A／B 的描述是它的兩個後果：壓縮是原因端，名稱磨損是傳遞端。理由：把 `perm_route.py` 一個檔案放進 repo，A 與 B 描述的機制**同時消失**；反之，改善 evidence table 的欄位或統一命名，只要物件仍在 `/tmp`，重新實作的自由度就還在。

**與既有清單的關係**：**P-4 的舊病復發（未綁定）**。P-4 白紙黑字要求 Evidence 為四元組「值 @ {harness} × {被測程式:身分} × {被測輸入:repo 可定址位置} × {版本/sha}」——這正是缺的東西。它沒能阻止本次，是因為它的綁定範圍寫成「矩陣的 Evidence 欄」，而 audit finding 不是矩陣列。I-13 第二子句（「裁決宣稱的修正必須有對應的程式 diff」）字面上被滿足了：diff 存在、落在交付物件上、SSOT 也同步了——錯的是被量的程式不是被斷言的程式，I-13 修的是動詞而非名詞。

---

### 根因 3｜斷言對象一律是等價類，證據永遠是單一成員，而「選哪個成員、依什麼方向選」在整條流程裡沒有任何一格可存放

**陳述**：本 change 四份產物中沒有任何一處把斷言對象具體化成可執行代表。spec 的對象一律是全稱名詞（student code、the `str.replace` bypass、the `math.perm`-with-Legendre route），tasks 的驗收出口一律是單數不定冠詞，而量測工具的簽章 `measure.sh <slug> <solution.py>` 吃的是**一個檔案**。類與成員的落差由執行者臨場裁量，不留痕、不受審。三個實例：(a) 沙箱 spec 的 requirement 名為「Sandbox guard is injected before user code」——對象是**注入順序**（作者可控），不是**逃逸能力**（攻擊者可控），因此 6 條新測試全在測 import 拼法（`import js`／子模組／from-import／`importlib`），沒有一條碰 `sys.meta_path.pop(0)` 或 jsfinder；(b) `prize_mathperm.py` 選了 spec 未指名的最貴寫法；(c) `gemblast_strreplace.py` 掃全部 26 個字母，而最便宜的合理寫法只掃 `set(s)`。

**方向規則的缺席**（分析 C 的獨立貢獻）：既有心法「op 上界取最便宜寫法、收編預算取最昂貴合理寫法」在本次被**忠實執行**了——收編路線取了最貴寫法。問題是這條心法是為「替一條必須存活的路線編列預算」而寫；本次的命題方向相反，要宣告的是「這條路線**不再通過**」，一個全稱否定句。否定一條路線的存活，必須以它**最便宜**的合理寫法背書。心法只寫了「取哪個寫法」沒寫「為哪一種命題」，於是在方向翻轉時靜默失效，而且失效時看起來像在遵守規範。

**證據**：`.vitepress/theme/__tests__/sandbox-pyodide.spec.ts` 8 條 `it()` 中無一提及 `meta_path`（我 grep 確認：全 repo 測試中提到 `sys.meta_path` 的只有 `worker-utils.spec.ts:65`，且它斷言的是「守衛有被插入 head」——再一次是注入順序）。R2 反駁代理實測 `sys.meta_path.pop(0); import js` → `ok=true`、輸出 `ESCAPED [object global]`。分析 C 以 native CPython 複驗：`n=200000, m=100000` 時逐位剝零 12,203 ms、Legendre 307 ms（39.8×，輸出相同）；gem-blast 三筆對抗 literal 26 字母全掃 3,203／4,116／5,133 ms vs `set(s)` 703／1,055／1,509 ms（3.4–4.6×）。

**解釋哪幾次失效**：失效 1 與失效 3；並解釋一條 **R2 未發現、本報告新增**的同型失效——gem-blast 的 `str.replace` 收編路線同樣以最貴寫法量測而宣告翻面（18/20），其 spec delta 寫成條件句，會自動採納這個錯誤量測，**這是第二份可能被錯誤量測影響的已上線題目保證**。

**層次取捨**：分析 A 把它命名為 patch-shaped test（照補丁寫的測試／change-witness testing），分析 B 命名為「類 vs 成員無存放格」，分析 C 命名為「命題方向未標注」。我判定 B 的層次最根本並把 A、C 收為它的兩個子規則：A 描述的是**成員從哪裡來**（從被改動的動詞倒推），C 描述的是**成員該往哪個方向挑**（依命題方向）。理由：即使照 A 的建議把測試改成家族全掃描，若沒有 C 的方向規則，收編路線仍會被以最貴寫法量；即使照 C 標了方向，若沒有 B 的存放格，方向規則沒有地方可以被檢查。

**與既有清單的關係**：**I-11 與 P-7 的舊病復發**。I-11 已寫明「斷言對象一律定義為參數化家族並全掃描，禁止只把當輪抓到的單一實例釘進 CAPS」；P-7 已寫明「任何『結構性不可用／不可能』的句子必須附已檢驗過的修補變體清單」。兩條沒能阻止本次的原因有三：其一，I-11 根本讀不到（根因 1）；其二，兩條的綁定範圍都寫成「下一個 change 採用」而本次是**平台 change**，形式上不在射程；其三，兩條的詞彙全是出題語彙（CAPS、斷言牆、殺手帶、X 軸），寫判題引擎測試的人不會認出它適用。

---

### 根因 4｜每一道檢查都選在與被宣稱性質正交的軸上，因此必然全綠而宣稱依然為偽

**陳述**：這條回答了「為什麼每一輪的機械驗證每次都全綠」——綠燈不是被繞過，是被選在錯誤的軸上。四個實例：(a) 收編路線的唯一自審是「以 30 組隨機輸入與正解交叉驗證輸出一致，確保量到的差異來自成本而非寫錯」——被宣稱的性質是**成本**，而輸出等價恰恰是唯一無法分辨「spec 指名的演算法」與「同輸出的另一條路」的檢查；它保證那支程式是對的，而錯的正是「它是哪一條路」。(b) dev watchdog 測的是「`arm()` 有沒有接在提交路徑上」，與「`arm()` 在該路徑唯一會執行的環境裡是否有作用」正交。(c) 對照組 `rank-code-backfill:control_mathfactorial` 被記為「0/20 符合預期」，實際判定序列是 `RRRRRRRRRTTTTTTRRRRR`——**14 筆 RE（其中 6 筆在 3–8 ms 崩潰）＋6 筆 TLE**，是輸入解析崩潰而非成本致死，而它要背書的 spec 條文寫的是牆鐘上界。(d) `spectra analyze` 回報「Consistency ✓ Clean」，而它的 Consistency 指需求／任務交叉引用完整，與同一份文件裡的 `12+7≠20` 完全正交——那面綠燈卻被寫進 commit message 當成正確性背書。

**證據**：commit `3e47819` message 自陳「兩條路線皆先以 30 組隨機輸入與正解交叉驗證輸出一致」，而 `measure/` 與 `probes/` 底下 grep 不到任何隨機交叉驗證腳本，**該檢查連物件都不存在**。`results.jsonl` 我逐列驗算：22 列全部自洽（`score == verdicts.count('A')`、`len(verdicts) == rows == len(per_ms)`），缺陷 100% 發生在 JSONL → 散文的手抄段。

**解釋哪幾次失效**：三次全部，加上「每一輪機械驗證全綠」這個關鍵事實與「七筆／八筆」錯誤數字通過 7 道閘（作者自審 → commit message 覆述 → vitest 374 passed → typecheck → lint → `spectra validate` → `spectra analyze` Consistency Clean）。

**與既有清單的關係**：**全新**。I-12（成本閘只能模擬實測有效的機制）是鄰居但講的是閘門模擬了不存在的機制；本條講的是通過條件與被斷言的性質不同軸。I-11 處理斷言**覆蓋不足**，本條處理斷言**軸向錯誤**——即使全掃描，掃的仍是不相干的維度。

---

### 根因 5｜測試套件沿著交付合體的接縫被切成兩半，於是部分缺陷連承接面都沒有

**陳述**：交付物是「`pyodide.worker.ts` × 真 Pyodide × 真 Worker 環境」這個合體。測試套件卻剛好在這條接縫上一刀切開：真 Pyodide 套件（`sandbox-pyodide.spec.ts`、`deadline-pyodide.spec.ts`）只餵 `buildWrappedCode()` 的輸出，從不載入 worker；worker 套件（`pyodide-worker-run-only`、`pyodide-worker-trace-reset`）一律 `vi.mock('/pyodide/pyodide.mjs')`，把 `setInterruptBuffer`、`globals.set/clear` 全換成 `vi.fn()`。兩半各自綠燈，而合體沒有任何測試實例化。更尖銳的是紀律的不對稱：`sandbox-pyodide.spec.ts` 第一段自己宣告「wrapper 一律來自 `buildWrappedCode`，絕不用抄本」（註解甚至說明上一支探針就是因為手抄守衛而誤報），第二段卻把 worker 的每筆前置手抄成 `resetBetweenTestcases()`，註解自陳「Mirror of the Worker's per-testcase preamble」——而 `builtins.__import__` 毒化正是從沒套用紀律的那一側漏掉。

**證據**：我 grep 確認 `vi.mock('/pyodide/pyodide.mjs'` 只命中兩支 worker 測試（其中 `loadPyodide` 出現在 mock 工廠內，非真實載入），與真 Pyodide 兩支測試交集為空。R2 的覆核代理反而做對了：用正則從 `pyodide.worker.ts` 原始碼抽出 `SYS_MODULE_SNIPPET`／`TRACE_RESTORE_SNIPPET` 逐字重現。

**解釋哪幾次失效**：失效 1 與失效 2 的落地面；並解釋 `builtins.__import__` 永久毒化、`_op_limit = 1` 原文外洩這兩條為何連一條紅燈都沒有——它們只在合體上存在，而整條驗證管線沒有任何欄位承接（`measure.sh` 的 `READ_ROWS` 每列只取 `tr.dataset.verdict` 與毫秒，結果面板文字從不被讀）。

**與既有清單的關係**：**全新**。RC-1 的差集是「檔案在不在 tip 上」（版本控制軸），H-3 的乾淨 worktree 可以殺；本條的差集是「替身 vs 交付合體」（組裝軸），乾淨 clone 裡 mock 還是 mock。

---

### 根因 6｜斷言不帶執行環境維度，於是修正可以接在一個該機制結構性不存在的環境上

**陳述**：失效 2 的反證就寫在同一份 design 的一節之隔：D6／E2c 明文「`vitepress dev` 沒有跨來源隔離，因此開發期 `SharedArrayBuffer` 不存在」。R1 的必修標題是「dev 路徑未武裝」，修正輪把「未武裝」讀成「沒有 `arm()` 呼叫」（可 grep 驗證，R2 也確實 grep 到並判「修正有效」），而不是「沒有中斷會發生」。因為 trace-matrix 的 R 表（需求→任務→驗收出口）沒有 env 欄，「在哪個環境成立」從來不是斷言的一部分。決定性佐證是同一輪兩個 commit 的並置：`201d9b5`（00:01）宣稱「dev 提交路徑補上 watchdog」，`7e31aed`（00:31）寫殘餘 R2「真正處在降級狀態的只有 `vitepress dev`，那裡沒有學生」——兩句合起來就是「這個修正沒有效果」，分居兩檔兩節，無任何通道把它們放在一起讀。

**證據**：`deadline.ts` 的 `createInterruptChannel()` 在無 SAB 時回傳 `{supported:false, view:null}`，`arm()` 首行 `if (view === null) return`；`useChallengeRunner-dev.spec.ts`／`-prod.spec.ts` 內 grep 不到任何 `arm`／Watchdog／`SharedArrayBuffer` 斷言；套件裡唯一提到 `SharedArrayBuffer` 的斷言仍留在 `useExecutor.spec.ts:56`（`expect.any(SharedArrayBuffer)`），而 `useExecutor.run()` 至今無任何呼叫端。R2 用來證明「修正有效」的實測是在 `:8788`（`preview:cf`）跑的生產路徑，不是 dev 路徑。

**層次取捨**：分析 A 稱之為「驗證環境比交付環境更有能力，替被驗程式補上了它缺的前提」；分析 B 稱之為「斷言不帶 env 維度」。我取 B 為根因、A 為後果。理由：node／jsdom 無條件擁有 `SharedArrayBuffer` 只是「前提未被寫下」時的一種表現；即使把測試搬到真瀏覽器，只要沒有一格要求寫出「這條路徑的真實環境是哪一個」，同樣的錯誤仍會發生在下一個環境相關的機制上。

**解釋哪幾次失效**：失效 2 獨佔；並解釋 R2「4 生效／5 半生效」中「半」的來源——驗證與被驗證物在不同環境。

**與既有清單的關係**：**全新**。既有清單完全沒有環境維度。與 gem-blast RCA 的「牆鐘軟旗標對同步碼失效」同構（機制存在但在該情境下永不觸發），但那次被記成單一 bug，沒有抽成維度——**I-9（平台事實對帳）本次確實被執行了**（軟旗標的教訓有被帶進矩陣的 C 表），失效的是「自家矩陣內的環境事實」與「自家程式路徑」從未被 join。

---

### 根因 7｜反駁層以「文字是否錯」判定，不以「證據對象是否對」判定；對象型 finding 因此被系統性淘汰，並反過來對下一輪發出許可

**陳述**：這一條決定了根因的**性質**。R1 的 RB-F2 已經完整發現、完整量測了 gem-blast 的拼寫問題：把 `for c in ALPHABET` 改成 `for c in set(s)`，同一條繞道 20/20、max 3,263 ms，反駁者獨立重跑得 3,136 ms——**數字被承認屬實**。但它被判 REFUTED，理由是「逐字核對三處，措辭已經是條件句」。反駁者自己也選錯了對象：它檢查的是 spec delta 的條件句，而 `design.md:239` 寫的是無條件的「該繞道**不再通過完整計畫**」、BACKLOG §2.8 結案寫的也是無條件句。唯一可執行的殘餘建議（把 `set(s)` 版收進 `measure/routes/`）被降為「可選」。四小時後，修正輪對 prize 路線犯了同一個錯——這不是同一 change 內同一錯誤犯兩次的巧合，而是**第一次犯被抓到、被量到、被反駁掉，因此第二次獲得了許可**。

**證據**：R1 合成表該列 disposition 欄原文為「無需處理（可選：把 set(s) 版收進 `measure/routes/` 當下界候選）」；同輪反駁代理的 severity_correction 明寫「應為 REFUTED，不只是降級」。同一形狀也出現在 R1 合成報告第 3 節的指示——它已明寫「在 R 表把『既有 sandbox 測試維持全綠』標為無效驗收出口，改為『執行期 import 阻擋整合測試』」，修正輪卻只寫了測 import 拼法的整合測試（失效 1），同樣是把對象型指示讀成動作型指示。

**解釋哪幾次失效**：解釋為何根因 2、3 沒有在 R1 就被修掉；並解釋為何 R2 送驗的 6 條全數 CONFIRMED、零推翻——錯誤此時已固化成文件事實，反駁者核對的文字與文件一致。

**與既有清單的關係**：**全新**，且屬「審查裝置」層。P-9（複核品質檢查）與 P-10（verdict 分歧處理）是鄰居，但兩者管的是複核的**形式品質**與**分歧仲裁**，都沒有規定「以文件措辭推翻一條已被獨立重跑證實的量測」是非法的。

---

### 根因 8｜修正輪是全流程唯一沒有對手的階段，而規範性後果恰好在此誕生；收斂算術因此不可達

**陳述**：協定為每條發現指派專職反駁者（預設立場是它錯了），修正輪則完全無人覆核——它的覆核者是下一輪。而本次修正輪新增的物件是：一份修訂已上線題目保證的 spec delta（`3e47819` 的**新增檔**）、design 的新章節、一次呈給維護者的三選一、以及維護者的裁決——這些在被 commit 前受過的對抗覆核次數是 **0**。它們最後被抓到，只是因為協定超時而多跑了 R2。

不對稱是結構性的三疊：(a) **oracle 可得性**——驗別人的宣稱時，宣稱自帶可證偽的期望觀測；驗自己的修正時，目標是「缺陷不見了」，一個關於缺席的命題，而確認缺席用的正是剛剛才寫下的那份列舉（根因 3），複現在構造上不可能失敗。(b) **角色**——對手只掛在宣稱上，沒掛在修正上。(c) **成本**——驗一條發現是有界的且能砍掉工作；驗自己的修正是無界的（修正新開的每一個面）且只會製造工作。

直接後果是收斂算術：每個修正保證在它被做出的**下一輪**才被審，輪數的下界是**缺陷的世代數**而非缺陷數；只要修正輪自己會生出 critical，「≤2 輪歸零」在數學上不可達。另有一項可觀察的不進化：R1 之後新增的約 19 條測試全部是上一輪個別缺陷的迴歸見證，沒有一條是上一輪失效**模式**的家族斷言——套件的成長律是「每個過去的缺陷配一條測試」，構造上攔不住同家族的下一個成員。R2 的兩條 critical 全部長在主代理手寫 lens 的「額外：找找還有沒有其他到達 JS bridge 的路徑／其他污染面」子句上，而那個普遍化不在 repo、不在 skill、不在 spec——**prompt 進化了，repo 沒有**。

**證據**：三個 fix commit 的訊息末段技術影響全部以套件數字加 analyze／validate 作為證據；R1 的 8 個反駁代理全部針對稽核發現，零個針對修正。

**與既有清單的關係**：**RC-4 的舊病復發**。既有清單沒能阻止它的原因很具體：H-6（把上一輪修正 diff 列為下一輪第一條 lens）**已被採納且確實運作**（R2 的三條 lens 就是修正 diff），但 H-6 是**偵測器不是預防器**——它把修正的覆核延到下一輪，正好落在協定要求的 ≤2 輪窗口之外。I-4（修復後 diff-scoped 重賞金）方向正確，且已被前一份 RCA 明確判定為「已知根因的修復措施放錯階段」，本次原樣重演。

---

### 根因 9｜證據嚴謹度與規範後果成反比：唯一能決定 spec 的那張表，是唯一不可重跑的表

**陳述**：矩陣制度在本 change 確實運作，但只運作在**不產生規範後果**的表上。C／M／P／E 表的數字有腳本、可重跑（分析 C 實跑 `probes/bench_counting_modes.mjs`，M1 24.0×、M2 8.0×、M3 100,001×、M4 1.43× 與成本單位 5× 全部吻合）。而 O 表——唯一決定 deadline 常數、唯一產生「空集合」結論、唯一支撐兩份已上線題目 spec 修訂的表——其宣告的重跑指令 `sweep.sh` 開頭是 `: > $OUT`（先截斷），且路線迴圈只 glob `routes/gemblast_*.py`：**照文件重跑會銷毀證據，且不會重生那兩條決定性的列**。它們是手動單次 `measure.sh` 呼叫、手動 append 的；散文數字再由人眼從 JSONL 抄出，其中一個抄錯。

**結論先於量測**（分析 C 的獨立貢獻）：D5 宣稱常數「由既有題目的量測結果決定，不預先寫死」，但釘定的 5,000 ms 恰等於 design 自己指出的、平台原本就存在卻從未觸發的那個 `setTimeout` 常數。當量測（即使是錯的）與它衝突時，D5 白紙黑字的原定處置是「保留舊行為」，實際採取的卻是第三條路：維持常數、改寫已上線題目的保證。三個選項的代價敘述全部落在同一個錯誤量測與一個虛構數字上（「約 15 秒」無 ID，且因所有超時筆都被 deadline 截斷、design.md:197 自承「真實耗時無從得知」，在當時配置下原理上不可得），而唯一不需要改變任何既有物的選項恰好是被選中的那個。

**證據**：我複核 `sweep.sh` 全文確認 `: > $OUT` 與 `routes/gemblast_*.py`；`design.md:159` 與 `trace-matrix.md:94` 皆宣稱「重跑指令為 sweep.sh」。`openspec/specs/expression-eval-challenges/spec.md:75` 登記的另外 4 條收編路線至今零量測，而 tasks 4.4 在 `3e47819` 被從「量測 gem-blast 的 `str.replace` 繞道」**改寫**為「量測**所有**……（括號內恰好列舉已做的三條）」並打勾——**驗收條件被改寫成交付物的形狀**。

**與既有清單的關係**：**T-1 的舊病復發，且屬於「改善清單本身未落地」這一類**。T-1（`scripts/trace-reconcile.ts`，含數值白名單比對，規則是「沒有 ID 的數字不得出現在任何文件」）**從未實作**——`scripts/` 底下無此檔，`pnpm lint` 只掃 `.vitepress` 與 `scripts`。它若存在，「約 15 秒」與「七筆」都會在 commit 前變紅。I-5（出貨後量測閘＋STALE）與 T-3（sha 失效傳播）同屬預測到但未綁定；I-13（文件數字單一來源）同樣讀不到（根因 1）。

---

## 三、改善清單（接續 I-14，編號 I-15 起）

排序依「防止的嚴重度 ÷ 採用成本」。每條的綁定範圍一律寫成可機械判定的觸發條件，**不使用「下一個 change 採用」這種寫法**——那正是既有教訓失效的原因。

| ID | 改善 | 防止 | 可機械化 | 綁定範圍（觸發條件） |
|----|------|------|----------|----------------------|
| **I-15** | **finding↔fix 數字對帳閘**：凡 fix 重跑了某條 finding 指名的量測，必須在同一 commit 內附兩列對照表（finding 值／重跑值，含 score、max_ms、判定序列）。分數不同、或 max_ms 差異超過 ±20%，即為阻擋條件：必須先以文字說明差異來源並取得覆核，才可寫任何依賴該數字的結論 | 根因 2。本次修正輪拿到的 finding 白紙黑字寫著 20/20、2,052 ms，自己量出 12/20、5,026 ms，分數相反、差 2.4 倍，卻直接據以宣告「空集合」。任何一次對帳都會當場擋下整條鏈 | **完全可** | commit diff 觸及 `openspec/changes/*/measure/results.jsonl` 且該 change 目錄存在本輪 evidence table；檢查器逐 label 比對 |
| **I-16** | **證物入庫才算交接**：finding schema 增必填欄 `artifact_path`。證據來自臨時檔（路徑含 `/tmp` 或 scratchpad）者，該檔必須在 finding 送出前複製進受審 change 的 `measure/routes/` 或 `probes/` 並改填 repo 相對路徑，否則該 finding severity 上限為 `observation`（不得為 major／critical、不得成為必修）。fix 輪禁止重造：要用不同物件必須新增檔案並填 `supersedes` | 根因 2 的傳遞環節。R1 的正確 Legendre 實作在 `/tmp/perm_route.py` 隨 session 蒸發，修正者只能照散文重做，而重做的自由度正是錯誤進入的地方 | **完全可** | 稽核／反駁代理的 StructuredOutput schema 必填欄 ＋ 合成步驟 `test -f` 檢查；`.spectra` 內記錄本輪所有 artifact_path，archive 時一併保存 |
| **I-17** | **量測表格一律由腳本派生，禁止手抄**：新增 `measure/derive.py`，從 `results.jsonl` 產出 design 量測表與矩陣 O 表全文（含每列 #A/#T 與自洽斷言 `score == verdicts.count('A')`、`len(verdicts) == rows == len(per_ms)`），文件該區塊以 `<!-- derived: measure/derive.py -->` 包夾，CI 重跑並 diff。同時 `sweep.sh` glob 改為 `routes/*.py`、移除 `: > $OUT`、結尾硬斷言「`routes/` 與 `solutions/` 檔案總數 == 輸出列數」 | 根因 9。JSONL 22 列全部自洽（已複核），錯誤 100% 在人眼抄寫段；「七筆」在同段落內就有 `12+7=19≠20` 與含 8 個 T 的判定序列自我否證。順帶修掉「照文件重跑會截斷證據且不重生決定性列」 | **完全可**（核心 <30 行） | commit diff 觸及 `**/measure/results.jsonl` 或含 `derived` 標記的區塊；另加 doc lint：design／trace-matrix／specs 出現 `\d+ 筆`／`\d+ of \d+ entries` 而該數字不在 derive 輸出集合中即失敗 |
| **I-18** | **修訂已上線保證的差別門檻**：若 change 的 `specs/<cap>/spec.md` 是對已存在於 `openspec/specs/` 的 capability 的 MODIFIED delta，則必須 (a) 獨立成一條 tasks 項並走一輪只審它的對抗覆核（不得與 ADDED 合併審）；(b) 附「反向假設實測」——實測至少一種會使該修訂變成不必要的寫法／參數並記錄結果；(c) 完成後才可呈維護者 | 根因 9 與本次最嚴重的後果。撤銷保證比新增能力更難回復（會進入 `openspec/specs/` 成為後續 change 引用的既成事實），而本次兩份被修訂的保證，其依據恰好是全 change 中最不可重跑的兩列——門檻與後果完全反向。(b) 單獨就足以攔下本次 | **半可**（(a)(c) 全機械，(b) 的「反向假設」需人選） | `git diff --name-only` 命中 `openspec/changes/*/specs/<cap>/spec.md`，且 `openspec/specs/<cap>/spec.md` 已存在，且 delta 含 `## MODIFIED Requirements` |
| **I-19** | **命題方向決定寫法**：把既有心法改寫為帶方向的兩條——(1) 編列預算／設上界（「這條路必須活下來」）→ 取最昂貴的合理寫法；(2) 宣告一條路線已死／不再通過／可行域為空（任何全稱否定句）→ 必須以**最便宜的合理寫法**背書，且同段落列出至少兩種寫法的實測 ID。詞表 lint：`不再通過｜已死｜不可能｜空集合｜no longer passes｜structural` 命中即要求同段落有 ≥2 個量測 ID | 根因 3 的方向子規則；本次兩份已上線題目保證被錯誤修訂（prize-order-code 已確認，gem-blast 高度可疑且尚未修正） | **半可**（詞表與 ID 數量全機械；「哪個算最便宜合理」需人判，但被強制寫出後即可覆核） | `openspec/changes/*/design.md`、`proposal.md`、`specs/**/spec.md` 內任何命中詞表的句子；與 T-1 同一支腳本 |
| **I-20** | **路線身分綁定 ＋ 反向覆蓋率閘**：`measure/routes/*.py` 強制帶機讀 header `# route-id: <spec 路徑>#<Requirement 名>` 與 `# spelling: cheapest｜as-recorded｜control`；腳本檢查 (a) route-id 指向的 Requirement 存在；(b) 掃 `openspec/specs/**` 中所有登記為 co-opted／surviving alternative 的路線，每條至少要有一支對應 route 檔；(c) 來源條文指名的技術關鍵詞（本例 `Legendre`）必須出現在代表檔的**非註解行** | 根因 3 的對象子規則。`prize_mathperm.py` 檔頭逐字引用了 spec 的路線名而檔身是另一條路，(c) 當場擋下；`expression-eval-challenges/spec.md:75` 登記的 4 條收編路線至今零量測，(b) 當場擋下 | **半可**（(a)(b)(c) 皆 grep 級；「這支程式是不是那條演算法」由 spelling 欄加人工簽名補足） | change 的 spec delta 或 design 出現「收編／繞道／co-opted／surviving alternative」字樣，或 `measure/`／`probes/` 有新增檔；閘跑在 archive 前與任何 `specs/` delta commit 前 |
| **I-21** | **「符合預期的失敗」必須歸因**：任何被記為「符合預期／as expected／必須失敗」的量測，必須在同一列記錄失敗原因分佈（判定序列 R/T/W 逐項計數）並斷言原因與預期一致。預期是 TLE 而實測以 RE 為主、或有任何一筆在 100 ms 內失敗者，一律阻擋 | 根因 4 在對照組上的變體。`rank_mathfactorial.py` 被記為「0/20 符合預期」，實際 14 筆 RE（6 筆在 3–8 ms 崩潰）＋6 筆 TLE，肇因是輸入解析格式與該題 reference_solution 不同；spec 的 C-builtin bypass lethality 條文正靠它背書 | **完全可**（約 10 行） | `results.jsonl` 中 `score == 0` 的列，或文件中對某量測使用上述措辭的段落 |
| **I-22** | **裁決前自證包**：呈給維護者的每個選項，其代價敘述中的每個數字必須附三元組（矩陣 ID、可重跑指令、產生它的程式路徑）。因量測配置而被截斷、原理上不可得的量，**禁止以估計值填入**：必須解除限制重量一次，或明寫 `UNMEASURABLE` 並使該選項標記為不可比較。若選項清單中有一項是「不改動任何既有物」，必須明寫它為何不是預設偏好 | 根因 9 的決策端。本次三選一中兩項建立在錯誤量測上，第三項被「約 15 秒」（無 ID、原理上不可得）擋掉——三個選項沒有一個是自證的 | **完全可** | change 文件出現「維護者裁決／二選一／三選一／請裁決」等段落標記；該段落內所有阿拉伯數字必須在 trace-matrix 有 ID 且該列 rerun 欄非空 |
| **I-23** | **修正輪內建對手，且不計入輪數**：協定改為 …→ fix → **diff-scoped 反向驗證** → commit。對每一條必修各派一個「假設此修正無效」的代理，四個固定問句：①它的執行環境前提成立嗎？②它作用的對象是發現量測的那個對象嗎？③它可以被移除或旁路嗎？④它的測試是否只是它自己的迴歸見證？報告落盤 `audit/<round>/fix-antiverify/`。該輪禁止以「全套件綠、typecheck、lint、analyze 全過」作為落地證據。此覆核**不計入**輪數，以免輪數壓力把它換掉 | 根因 8。本次三個 fix commit 引入的新規範內容在 commit 前受過的覆核次數為 0；四個問句在同一輪內同時攔截根因 3／5／6 的產物 | **完全可**（報告數 == 必修數、每份含四個固定小節標題，皆可數） | fix 階段結束、commit 階段開始之間；條件為 `git diff --name-only` 命中 `openspec/changes/*/specs/` 或 `*/measure/` |
| **I-24** | **收斂終止條件改成算術上可達的形式**：合成代理的 StructuredOutput 增必填欄 `criticals_introduced_by_this_rounds_fix`（整數）；歸零判定改讀「連續兩輪該欄為 0」，而非讀「本輪存活發現數」 | 根因 8 的收斂算術。承認輪數下界是缺陷的世代數而非缺陷數；也讓「未收斂」不再可能只是門檻在動（呼應全域守則第 4 條凍結標尺） | **完全可** | 協定文件 ＋ 每輪合成代理的 schema |
| **I-25** | **繞道家族表**：每一道 SHALL 型防護（sandbox guard、op counter、deadline）在其 spec 內新增一張表，欄位 `{家族名, 動詞, 代表實例, 測試案例 id}`，動詞至少涵蓋四類：**移除守衛／旁路守衛（不經其掛載點）／替換守衛所依賴的前置物／攔截守衛的寫入**；對應測試以 `it.each` 直接由該表驅動 | 根因 3 在平台防護場域的落地（I-11 的平台版並取得機械觸發點）。`sys.meta_path.pop(0)`（移除）、jsfinder（旁路）、`builtins.__import__`（替換前置）三條缺陷各屬一類，現行 6 條測試全部落在第 0 類（拼法） | **半可** | 綁在檔案而非 change：`openspec/specs/pyodide-sandbox-guard/spec.md` 與 `judge-deadline/spec.md` 必須含 `## Bypass families` 表；CI parse 表列數與測試檔 `it.each(BYPASS_FAMILIES)` 陣列長度比對；新增任何 SHALL 型防護 requirement 而無此表，validate 報 Critical |
| **I-26** | **交付合體測試 ＋ 凍結替身數量**：新增一支以真 Pyodide 驅動 `pyodide.worker.ts` 本體（或以從 worker 原始碼匯出的常數逐字驅動）跑完一次 run／run_only 批次的測試；禁止測試檔手抄任何 Python 片語——`sandbox-pyodide.spec.ts` 的 `resetBetweenTestcases()` 必須改為 import worker 匯出的 snippet 常數 | 根因 5。讓 `builtins.__import__` 毒化、`_op_limit = 1` 外洩這一類只在合體上存在的缺陷有承接面 | **完全可** | `pretest` 兩條 grep：(a) `vi.mock('/pyodide/pyodide.mjs'` 的檔案數不得大於今日值；(b) 真 Pyodide 測試檔內不得出現 `Mirror of` 或任何未由 import 取得的三引號 Python 字串常數 |
| **I-27** | **斷言帶環境維度（X 表）**：trace-matrix 的 R 表新增必填 `env` 欄，值域 `{node｜vitest｜vitepress-dev｜preview:cf｜production}`；另新增 X 表 `{程式路徑, 它假設的執行期能力, 該能力在哪些環境成立, 它唯一的真實環境}`。任何一列的「唯一真實環境」欄為否，其對應修正一律標 `INERT`，不得在 tasks／裁決表計為已落地 | 根因 6。本案立即命中：`useChallengeRunner.submit()` × `SharedArrayBuffer` × `{vitepress dev: 否}` → INERT，dev watchdog 修正當場被判無效，不必等 R2 | **半可**（欄位存在性與 INERT↔tasks 打勾一致性全機械；env 值需人填） | change diff 觸及 `.vitepress/theme/composables/**` 或 `workers/**`；另以 grep 取 `createInterruptChannel()`／`crossOriginIsolated`／`SharedArrayBuffer` 的每個使用點，其所在函式名必須出現在 X 表中 |
| **I-28** | **對象型 finding 的反駁規則**：finding schema 增布林欄 `class_vs_member`；反駁 schema 增必填欄 `objects_checked`（檔案:行號清單）與 `alternate_member_measured`（是／否／不適用＋數據）。硬規則：`class_vs_member: true` 的 finding，反駁只有兩條合法出路——(1) 出示斷言對象確實只含被量的那一個成員；(2) 量另一個成員並顯示結論不變。**「文件措辭已是條件句」不構成推翻**。`alternate_member_measured == 否` 時工作流拒絕接受 REFUTED，自動降為 CONFIRMED-pending | 根因 7。RB-F2 會活下來（反駁者已重跑得 3,136 ms，走不到出路 2），`set(s)` 版會在 R1 就進 `measure/routes/`，prize 路線的同型錯誤在修正輪就沒有先例可援 | **半可**（schema 必填與布林閘全機械；「出路 1 是否成立」需模型判斷，但已從默認放行改成默認擋下） | 對抗覆核工作流的 StructuredOutput schema 驗證——反駁代理填不出欄位即無法回傳 |
| **I-29** | **改善清單集中化 ＋ 落地稽核**：把 I／P／T／RC／H 全系列從各 change 的 archive 目錄搬到 repo 根的單一 registry（例如 `openspec/lessons/registry.md`），任何 RCA 只新增條目、不新建檔；每輪稽核的**第一條 lens 固定為「既有 registry 逐條落地稽核」**，輸出每條的 `landed｜partial｜not-landed｜n/a` 與證據路徑 | 根因 1，以及「改善清單本身未落地」這一整類（T-1 開了兩份 RCA 都沒實作，而它正是本次三個文件錯誤的唯一守門） | **半可**（搬移與「每條 registry 條目必須有落地狀態」可機械檢；狀態判定需人／代理） | registry 檔存在性由 `spectra validate` 檢查；任何 RCA 檔若新增 `I-`／`H-`／`T-` 開頭條目而未同步寫入 registry 即失敗 |

**建議實施優先序**：I-15 → I-17 → I-16 → I-18 → I-23／I-24 → I-29 → 其餘。理由：三份獨立分析**一致**把 finding→fix 的交接判為最短、殺傷最大的槓桿（I-15＋I-16 直接攔下失效 3 與那次維護者裁決）；I-17 是全清單成本最低者（<30 行 Python）而當場暴露「七筆 vs 八筆」與「對照組其實死於 RE」；I-18 攔下唯一一項不可逆的傷害。

**可證偽的驗收預測**（供下一個同類 change 直接檢驗）：若 I-15／I-16／I-17 落地，下一個同類 change 的 R1 存活發現數應降至個位數，且修正輪引入的 critical 數（I-24 的必填欄）應為 0；若不為 0，則根因 8 的診斷（對手角色缺席）比根因 2（證物監管鏈）更根本，優先序應調換。

---

## 四、本輪未能完成的驗證

1. ~~**gem-blast 的第二份已上線保證未證實**~~ → **已於 2026-08-12 定案，本報告的預測成立**。`gemblast_strreplace_set.py`（最便宜寫法）以 `measure.sh` 在同一條 `:8788` 生產路徑實測：**20/20、單筆最大 3,115 ms**（預估 0.7–1.5 s 偏低，但「遠低於 5,000 ms、繞道仍通過」的結論正確）。「繞道不再通過完整計畫、18/20」確為偽。處置：`rank-code-challenges` delta 整份刪除，`gem-blast-challenge` delta 改記真值後保留（該題主 spec 明文要求本 change 修訂該條文，不得刪除）。連帶更新 design〈量測結果〉、trace-matrix O3／O4、proposal 影響範圍。**釘定常數的拘束上界因此由 376 ms 改為 3,115 ms，餘裕由 13.3 倍改為 1.61 倍。**
2. ~~**`expression-eval-challenges/spec.md:75` 登記的 4 條收編路線至今零量測**~~ → **已於 2026-08-12 量畢**：四條全部 20/20，單筆最大 65 ms（E1 52／R2 12／N1 57／E3′ 65），對上界無影響。路線檔已佚失、由 spec 名稱重新實作（與根因 2 同型），故先以 `measure/verify_routes.py` 對該題自己的 20 筆 literal 驗明輸出等同 `reference_solution` 才量。D5 的上界涵蓋範圍自此完整。
3. **兩條純程式面缺陷的誕生原因未解釋**：`builtins.__import__` 置換使 op 計數器永久毒化、`_op_limit = 1` 使守衛原文外洩。本清單只解釋了為何測不到（根因 4／5），不解釋為何會被寫成這樣。
4. ~~**`challenges.json` 的 metadata 與實測列數不一致**~~ → **已於 2026-08-13 查明並修正，結論為無害**。成因是單一規則：產生該檔的臨時腳本把 `count` 記成 `testcase_plan` 的**項目數**，沒有把 `count:` band 展開成它所代表的測資數。判準是機械的——**九筆錯的 `count` 全部等於該題的 plan 項目數，無一例外**，且錯的正好是全部九道 band-bearing 題目（另兩道有 plan 的題目為 20 筆全 literal，項目數恰等於測資數而僥倖正確）。實際偏差遠大於原記載的兩筆：gem-blast-playtest 記 8 實為 20、pillbox-reminder 與 print-farm-schedule 記 5 實為 20、prize-order-code 與 rank-code-backfill 記 9 實為 20。

   **無害的三項證據**：(a) 生產路徑的 `planTotal()`（`.vitepress/theme/composables/useChallengeRunner.ts:54-69`）算法為「Σ band counts ＋ 每個 literal 算 1」，**正確**，且其結果與每一次實測列數相符——D7 的「列數等於測資總數」驗收因此驗的是對的分母，結論成立；(b) `challenges.json` 從未被 `measure.sh` 或 `sweep.sh` 讀取（grep 全 change 目錄，唯一提及它的是本報告）；(c) 該檔的 `has_ref` 與 `has_plan` 兩欄 66 題**零錯誤**，O2 據以選出的 16 支 `reference_solution` 集合未受汙染。

   **處置**：新增 `measure/inventory.py` 重新產生該檔，算法明文對齊 `planTotal()`；九筆 `count` 修正，其餘欄位零變動。原檔是臨時產物、產生器未進 repo——與根因 2（證物留在 repo 之外）同型，故這次連產生器一起 commit。
5. **commit `3e47819` 宣稱的「30 組隨機輸入交叉驗證」在 repo 內查無腳本**。該宣稱是未執行、執行了但用了錯的輸入格式、還是執行了但結果被忽略，三種可能對應不同根因，本輪無法判定。（`rank_mathfactorial.py` 的輸入解析格式與該題 reference_solution 根本不同，若交叉驗證真的跑過，它不可能通過。）
6. **`spectra analyze` 的能力邊界是推論而非查證**。「它檢查工件結構一致性而非事實蘊涵」是從它在一份含跨檔算術自我否證的文件集上回報零 Warning 反推的，未讀實作。
7. **R1 為何沒找到 `meta_path` 拆除**，儘管它有明確的殘餘旁路 lens 且確實找到了守衛是死碼。假說是「找到最便宜的逃逸即終止搜尋」，逐字稿裡無直接證據，故列為假說。
8. **jsfinder 旁路的歸類懸而未決**。它連 `meta_path` 都不經過，挑戰的是「守 `meta_path` 就守得住 bridge」這個抽象本身——那是**威脅模型不覆蓋攻擊面**，不是測試設計錯誤；本報告九條根因沒有一條在講「保護模型從一開始就不覆蓋攻擊面」。這是清單不完整的直接證據。
9. **R2 的 lens 定義域為何是「本輪改動過的東西」而非「本輪結論所依賴的東西」**，無根因。這正是它抓到 prize 路線卻漏掉 gem-blast 路線（同一 commit、同一目錄、同一種物件）的表面原因，但表面原因不是根因。
10. **工作區狀態**：我未建立、修改或刪除 repo 內任何檔案，未執行 `sweep.sh`，暫存全部寫在 scratchpad。`git status --porcelain` 非空，殘留兩支未追蹤檔 `openspec/changes/add-judge-deadline/measure/routes/gemblast_strreplace_set.py`（mtime 01:13）與 `prize_mathperm_legendre.py`（01:11），兩者皆早於本次 RCA 開始、為主代理事後複現失效 3 的證物。**我判斷刪除等於銷毀證據，故保留原狀並在此明確回報**，處置由主代理決定。此為協定規則 4 未達成的唯一項目，且三份獨立分析各自做了同樣的判斷。

---

## 五、後設觀察

**一、同一個模式第四次出現：教訓被寫成文字，但沒有變成閘門——而這次連文字都讀不到。** 前一份 handoff RCA 已把這句話寫成第四節標題，並為 H 系列每條標註「可機械化」欄。本次的新變體更極端：I-9～I-14 與 RC-1～RC-6／H-1～H-6 物理上位於未合併的 `feat/exhibit-route-duo`，rank-code-duo 的教訓只在 memory 檔，I-1～I-8／P／T 系列在一個已歸檔 change 的子目錄裡。**五個載體、三種可見性、零個索引**。三份獨立分析中兩份靠簡報摘句轉述、一份判定「不存在」——改善清單的閱讀率在本次是 0。這使「舊病復發」的歸因需要修正：不是作者忽視教訓，是教訓不在他的通道上。

**二、綁定範圍寫成「下一個 change 採用」，每次都有一個形式上成立的理由不適用。** handoff RCA 的診斷是「正在寫的接手筆記不是一個 change」；本次是「這是平台 change，不是出題 change」。I-11／P-5／P-7 的詞彙全是出題語彙（CAPS、斷言牆、殺手帶、X 軸），一個寫判題引擎測試的人不會認出它適用於自己。**射程必須寫成 diff 命中的 glob 或 schema 必填欄**——本報告 I-15～I-29 全部照此改寫，這是與前三份 RCA 最大的形式差異。

**三、失效點的層級每一份 RCA 上移一級，且下一級已經可以預測。** rank-code-duo／bracket-check 談**被審物**（測資與數字）；exhibit-route-duo 的 handoff review 談**審查裝置**（驗證通道 ≠ 交付通道）；本篇談**改善清單自身**（清單在交付通道之外、清單從未被稽核是否落地）。依此外推，下一次的失效點很可能在「落地稽核這道程序本身」——因此 I-29 把它寫成每輪的第一條 lens 而非一次性動作，並要求輸出逐條狀態，讓它自己也可被稽核。

**四、RC-1 的一般式在本次長出三個新物種。** RC-1 原本只描述「作者的活體工作樹 vs tip／clone」（版本控制軸）。本次三次同形失效各是它的一個新軸：**測試替身 vs 交付合體**（組裝軸，根因 5）、**測試環境能力 vs 部署環境能力**（執行期軸，根因 6）、**改善清單所在 branch vs 工作 branch**（知識軸，根因 1）。H-3（乾淨 worktree 驗證）對前三者中的任何一個都零效果。建議把 RC-1 在 registry 中升格為一條**維度**而非一條發現：「凡宣稱『已驗證』者，須指名驗證通道與交付通道的差集是什麼」。

**五、修正輪是三份 RCA 共同指認、卻三次都沒被修好的階段。** RC-4 指認它、I-4 指認它、本篇根因 8 再次指認它。前兩次的處方（H-6 把修正 diff 列為下一輪第一條 lens）**確實被採納且有效**——R2 的三條 lens 就是它，兩條 critical 都是它找到的。問題在於它是偵測器：它把修正的覆核推到下一輪，正好落在協定要求的 ≤2 輪窗口之外。這是本次最乾淨的一課：**採納一條偵測型改善，會讓缺陷更晚被發現卻更難被歸零**。I-23（同輪內對修正下對手）＋I-24（把修正引入的 critical 數獨立計數、不計入輪數）是配套，缺一則另一條會被輪數壓力換掉。

**六、三份分析在同一處收斂，這本身是最強的訊號。** 三份獨立分析、三種完全不同的鏡頭（偵測系統的解析度、對象選錯族、規範傳播鏈），在「finding→fix 之間只交付散文、不交付可執行物件」這一點上完全一致，且三份都把它列為成本最低、殺傷最大的槓桿。同時三份都獨立注意到：**R1 已經量到了正確答案**（20/20、2,052–2,182 ms，被獨立重跑證實、判 CONFIRMED／必修）。整條失效鏈的起點不是「沒查到」，而是「查到了，但證物沒有跟著走」。
