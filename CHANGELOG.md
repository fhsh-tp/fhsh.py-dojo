# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [1.9.0] - 2026-08-18

APCS 題庫一次補上六題（apcs015–apcs020），把 easy 級別與四種從未練過的技法一起補齊；題目頁數學記號全站改用 LaTeX，並補上會讓 `pnpm test` 失敗的機械守門。

### Added

- **apcs015 基地台佈點規劃**（easy）：k×k 場地擺兩台互不干擾的基地台，逐列輸出邊長 1 到 n 的方案數；鑑別軸為執行成本，逐格掃描每一對方格的寫法在第 9 筆消耗 216,759,740 op、超出上限 21.68 倍([#35])
- **apcs016 跑馬燈顯示計數**（easy）：n 格燈其中 k 格燒壞，求可能畫面數；刻意不建成本斷崖，鑑別點是看穿可自由控制的格數是 n−k 而非 n([#35])
- **apcs017 園遊會代幣兌換**（medium）：每 12 枚剛好整批換上一級，求成功換幾次；刻意改用 12 而非十進位，網路上流傳的公式直接套用會答錯([#35])
- **apcs018 禮堂吊扇風域**（medium）：二維差分，題源為 CSES 1652 的對偶([#37])
- **apcs019 社團教室分配**（hard）：排序後維護每間教室的狀態，題源為 CSES 1164；原題輸出不唯一、CSES 以 special judge 判題，本站逐字比對，因此加上「發給當下空著中編號最小的一間」的行政規則使輸出唯一([#37])
- **apcs020 午間廣播接力帶**（medium）：雙指標搭配上次出現位置，題源為 CSES 1141 的變形([#37])
- 上述六題補上 easy 級別的斷層（原本學生做完 py 基礎系列後直接面對 medium），並填滿既有題庫完全空白的技法——改版前掃描 17 道 apcs 題的正解，技法分佈是單趟掃描模擬 17 題、排序 1 題，而二維陣列、前綴和／差分、雙指標／滑動視窗、頻率表計數皆為 0 題；六題皆為 20 筆 `testcase_plan`、皆附一份與 `generator` 走不同演算法路線的 `reference_solution` 納入自動互驗、`starter_code` 皆為空白起手式，apcs018–apcs020 另各附一張題敘說明圖([#35]、[#37])
- **`Usage.md` 新增「數學記號怎麼寫」**：15 列 do／don't 對照表，每一列都標明取自哪一個真實題目頁，不放虛構範例([#36])
- **新增數學記號 CI 守門 `scripts/latex-notation.test.ts`**（29 個測試，其中 21 條是負向控制），跟著 `pnpm test` 跑，失敗訊息指名檔名、行號與踩到的記號；黑名單獨立成 `scripts/latex-notation-rules.json`，由守門測試與盤點腳本共讀([#36])
- **新增 `scripts/trace-lint.py`**：追溯矩陣的機械檢查器，四段檢查涵蓋證據位址可解析、主張數字綁得回位址、位置欄與文件標記雙向一致、規格與設計散文裡的數字綁得回位址，並內建 self-test([#35])
- 新增 apcs013 展場平面配置圖、apcs014 彈珠台構造圖，以及可重建它們的腳本 `scripts/figures/`([#36])

### Changed

- **66／71 個題目頁的內文數學陳述改用 LaTeX**。原本同一種約束在不同題目有四種寫法（`≤`／`<=`／`小於等於`／`不超過`），指數以 `2^(D−1)` 這種 ASCII 拼寫呈現，現在統一為 `$2^{D-1}$`；**`frontmatter` 一個欄位都沒動**——逐檔比對 `frontmatter` 與 code fence 的 SHA-256，71 檔零改動，因此測資池與 WASM 皆不需重建([#36])
- **`canvas-design` skill 的字型改走 Git LFS**：新增 `.gitattributes`，54 個 `ttf` 以 LFS pointer 進物件庫，字型內容 byte 級不變([#36])
- **CI 的 Vitest 拆成兩步**：先排除 `deadline-pyodide.spec.ts` 平行執行，再單獨序列執行該檔。新增題目使測試總時間由 40.83 秒增為 76.45 秒，而 watchdog 在主執行緒、受測的 Python 迴圈在 worker，兩者被 CPU 競爭餓到的程度不對稱，該檔一度由 11,529 毫秒膨脹到 45,177 毫秒；拆開後回到 803 毫秒、與歷史綠燈一致。負載增加是永久的，因此沒有以重跑了事([#35])

### Fixed

- **行內 LaTeX 公式被推到獨立一行**。Tailwind preflight 的 `svg { display: block }` 讓每個行內 `$…$` 各佔一行，修法是把 `display: inline` 縮限於 MathJax 產出的 `mjx-container > svg`；這是先前就存在的缺陷，也是全站 LaTeX 化的前提([#36])
- **盤點腳本的分類本身曾是漏審來源**。初版記號黑名單漏掉裸的 `<`、`>`、`!=`、`÷`，導致 `quadrant-classifier` 整頁 7 條不等式被歸類成「內文無數學記號」而整頁沒有任何人看過；補齊黑名單後以同一份規則重測基準線，待轉由估計 53 修正為實測 55（轉換後 0）、已完成 3 → 66、無數學元素由 15 修正為 13 → 5([#36])

### 升級注意事項

- **本版起 repo 使用 Git LFS**，clone 環境需具備 `git-lfs`；CI 與建置流程都不讀字型（拿到 pointer 不影響），只有手動重建題敘說明圖時要先 `git lfs pull`
- **判題引擎與既有題目皆未更動**，既有測資零變動、零重新校準，學生端已完成的作答紀錄與分數不受影響

### 已知殘餘

- `scripts/trace-lint.py` 尚未掛進 CI，目前仍仰賴「有人記得跑」，屬專案層級另案
- apcs018 的 `map` 與 apcs019 的 `itertools.compress` 這兩條把內層工作推進 C 內建的寫法可拿滿分（1,448／788 毫秒），這是刻意接受的設計決定而非缺陷：65,536 bytes 的輸入上限把工作量封頂，而為了加大工作量去放大題目規模，反而會把正解自己推向時間上限

## [1.8.0] - 2026-08-14

判題引擎補上真正生效的每筆測資時間上限，並新增六題 APCS 素養題（apcs009–apcs014）。

### Added

- **apcs009 道具箱裝箱檢查**（medium）與 **apcs010 校刊排版檢查器**（medium）：括號配對主題雙題
- **apcs011 福利社老收銀機**（medium）：先加減後乘除的運算式求值([#31])
- **apcs012 折價券疊加試算**（hard）：加減改為右結合，後 12 筆測資加入括弧處理([#31])
- **apcs013 展場動線重建**（medium）：給兩種打卡紀錄還原第三種，考語義鑑別([#33])
- **apcs014 彈珠台軌道預測**（hard）：球數斷崖，考成本鑑別([#33])
- **每筆測資的牆鐘時間上限**：判題會在單筆測資超時的當下中斷執行並判 TLE，`run`／`run_only`／`execute` 三條路徑語義一致([#33])
- 新增 `preview:cf` 腳本（`wrangler pages dev`），可在本機以 Cloudflare 執行環境驗證跨來源隔離——時間上限依賴 `SharedArrayBuffer`，`vitepress dev` 沒有 COOP/COEP 標頭因此驗不到此功能([#33])

### Changed

- **應該 TLE 的提交現在真的會 TLE**。這是本版對學生唯一可見的行為改變。所有正解、以及所有被題目規格明文接受的替代解法得分皆不變，既有題目測資零變動、零重新校準([#33])
- 結果表格改以測資總數為分母：執行被中斷時不再因為只列出已回報的測資而看起來全綠，未執行的測資會明確標示([#33])
- **apcs009–apcs012 四題改為空白編輯器起手**：`starter_code` 由讀取輸入的骨架改為空字串；測資、generator 與參數宣告皆未更動([#32])

### Fixed

- **每筆 5,000 ms 的時間上限從未生效**。原本的軟旗標是 `setTimeout` 排入的 macrotask，而執行結束後的 `clearTimeout` 走 microtask、必定先執行——對同步的學生程式碼（也就是所有提交）永遠不會觸發；正式站所走的 `run_only` 路徑更是連這個失效的旗標都沒有。後果是成本鑑別軸整條失守：在開頭寫 `sys.settrace(None)` 可凍結運算計數器，把 K 次迴圈攤平到同一行可稀釋成本 24 倍，兩種寫法都能讓應該超時的解拿到滿分，且影響全站所有以執行成本為鑑別軸的題目。改以主執行緒 watchdog 搭配中斷緩衝區在到期當下中斷 Python，並將判題執行改為同步入口以確保中斷可被正確捕捉；運算計數器本身完全未動([#33])

### Security

- **沙箱守衛失效**：阻擋 `js`／`pyodide_js`／`pyodide` 匯入的守衛使用 `find_module`，該 API 在現行 Pyodide 已被移除，守衛實際上是死碼。改用 `find_spec` 並補上真 Pyodide 整合測試([#33])
- 修補一處會讓運算計數器被永久污染的缺口([#33])

## [1.7.0] - 2026-08-06

APCS 題庫一次進帳三題素養情境競賽題:二消寶石關卡測試,加上《星海排位》排行榜宇宙的驗證碼雙題(UVa 568/10212 轉譯)。

### Added

- **新挑戰題「寶石消除關卡測試」**(apcs006,medium/競賽題型):手遊關卡測試員驗收二消版面的素養情境——相鄰同色寶石成對消除、連鎖塌落,T 場測試各給 N 個版面,回報單場最大清除量;20 筆測資含 TLE 斷崖(每移除從頭重掃的寫法在壓力筆與巢狀 literal 全滅),巢狀 literal 經對抗審查強化為異長異殘量,長度判別繞過已封堵([#28])
- **新挑戰題「每日榜單驗證碼回填」**(apcs007,medium/競賽題型):UVa 568 素養轉譯——《星海排位》每日榜單的一位數驗證碼(N! 去尾零末位),一次回填 T 天;考點為「別重複計算」,T≤500 筆查詢共用一次增量建表;逐查詢重算的寫法在壓力 band(T≥400、N≥15 萬)恰好全滅([#29])
- **新挑戰題「頒獎順位驗證碼」**(apcs008,hard/競賽題型):UVa 10212 素養轉譯——全球賽季頒獎順位總數 P(N,M) 去尾零末位,N 上看 10 億;考點為「只留必要資訊」,答案只需 M 項區間的個位數與 2/5 因子帳,全範圍迴圈與大數連乘/轉字串路線均會超時或觸發轉換上限([#29])
- 三題皆附獨立實作的 reference_solution,納入 content-regression 自動互驗;正解/天真解/繞道路線均經 dev 與 staging 真機判題驗證,TLE 斷崖逐筆位置與設計預測一致([#28]、[#29])

## [1.6.0] - 2026-08-05

挑戰編號全面升級:字串 id(py001/apcs001)上卡片與內頁、目錄支援編號搜尋,並新增 /c/<id> 短網址直達題目。

### Added

- **挑戰 id 顯示於卡片與內頁**:目錄卡片標題前與挑戰內頁頂欄標題左側,均以 mono 低調小字顯示該題編號(如 `py001`),老師課堂口頭指定題號時,學生可當場對照([#25]、[#26])
- **編號搜尋**:目錄搜尋框支援 id——輸入純數字(如 `3`)精準比對序號、輸入前綴(如 `py00`)比對開頭;Python 與 APCS 列表頁各自只搜自己分類的題目([#25])
- **`/c/<id>` 短網址別名**:`/c/py001` 一次 302 直達該題正式頁面,課堂口頭傳達與手動輸入成本降到最低;不存在的編號回 404([#26])
- **出題 scaffold 自動配號**:`pnpm new-challenge` 依 category 前綴(`py`/`apcs`)自動分配下一個序號,並以 fail-closed 退役帳本防止已下架題目的 slug/id 被誤用復活([#25])

### Changed

- **挑戰 id 由整數改為字串格式**:`py001`–`py054`(Python)與 `apcs001`–`apcs005`(APCS)各自連號;學生本機進度以 slug 為 key,**完全不受影響**([#25])
- staging 測試期短暫存在的 `/challenge/<id>` 別名形式以 `/c/<id>` 取代(該形式從未進入正式站,無既有連結受影響)([#26])

## [1.5.0] - 2026-08-04

挑戰題庫雙軌化:拆分為「Python 挑戰」與「APCS 挑戰」兩個列表頁,並新增 deque 系列驗證向姊妹題「收卷順序驗證」。

### Added

- **新挑戰題「收卷順序驗證」**(id 59,medium/競賽題型):deque 系列驗證向姊妹題——兩位監考老師從一排座位兩端收卷疊成一疊,驗證 M 份「由頂到底」回報單真偽的校園素養情境(全篇不出現 deque/stack 術語);判定語意=回報反轉後對來源做雙指標兩端貪婪,generator 與 reference_solution 雙實作零共用邏輯互驗;20 筆測資含「忘記反轉」陷阱判別筆、enum 策展 band(裸背答案通過率 ≤1/10)與 TLE 壓力筆(全枚舉解 N=800 絕殺、線性判定解放行)([#23])
- **APCS 挑戰獨立列表頁 `/apcs-challenges`**:APCS 系列題(id 55–59)自原題庫獨立成頁,備考學生可聚焦練習;零基礎學生留在 Python 挑戰頁不再誤入進階題。題目檔案零搬動,學生作答進度完全不受影響([#22])
- **題目 frontmatter 新增選填欄位 `category`**(`python` | `apcs`,預設 `python`):資料層 resolver 統一補值並擋未知值;`pnpm new-challenge` 同步新增 `--category` 旗標;並以三道守門測試(category 全檔掃描、category→頁面存在性契約、nav lockstep)防止分類漂移([#22])

### Changed

- **導覽列改為平級雙入口**:「挑戰題庫」拆為「Python 挑戰」與「APCS 挑戰」;`/challenges` 頁面標題改為「Python 挑戰」([#22])
- **首頁「最新挑戰」拆為雙區塊**:「最新 Python 挑戰」與「最新 APCS 挑戰」各取該類最新 3 題([#22])
- **完成進度與返回導向依分類分流**:「已完成 X / Y」改為頁內自算(一題只計入所屬頁);挑戰頁「← 返回」與錯誤態「返回列表」依 category 回到所屬列表頁(原為回首頁)([#22])

## [1.4.0] - 2026-08-03

排程系列素養題上線:「列印工坊排程」與「智慧藥盒提醒」兩道新題,並首度引入效能斷崖測資設計(暴力解 TLE、事件驅動解放行)。

### Added

- **新挑戰題「列印工坊排程」**(id 57,medium/競賽題型):多機台派工模擬素養題——m 台印表機依「最早空閒、同時空閒取編號最小」承接工單,求全部完工時刻;20 筆測資 = 題面範例置首 + 9 暖身 + 8 壓力 + 2 邊界情境(機台多於工單、單一工單)([#20])
- **新挑戰題「智慧藥盒提醒」**(id 58,hard/競賽題型):週期事件模擬素養題,對齊 UVa 1203 定位——Q 種藥依登記順序編號、各依週期觸發提醒,輸出最先發生的 K 次提醒編號(同分鐘先登記者先);壓力測資淘汰「逐分鐘掃時間軸」解法(TLE)、放行線性掃與 heapq 事件驅動解法,規模上界經 op 探針實測定案(暴力解最省角落 2.34 倍超限、正解餘裕逾 1800 倍)([#20])
- **執行面板預設輸入=題面範例**:兩題的第一筆測資固定為題面範例一,學生按「執行」的預設輸入可直接對照題面推演逐步驗算([#20])

## [1.3.0] - 2026-08-01

測資引擎全面升級:分區測資計畫、正式站 TLE 判定與素養導向資料結構新題,並修復判題計數盲區與收斂正解外洩面。

### Added

- **測資引擎競賽式宣告能力**:WASM 單一真相源(建置期與瀏覽器共用同一份測資產生邏輯),params 支援 group/repeat 多筆資料宣告(APCS 式 T 批輸入),seed 決定性與 input_budget 規模預算
- **testcase_plan 測資分區**:題目 frontmatter 可分 band 宣告測資規模(count + override 深層合併與 literal 逐字測資,與 testcase_count 互斥),池以 block 儲存、判題整塊選取——教學小測資與壓力測資從此可在同一題並存
- **正式站 TLE 判定**:超過運算量上限的提交會得到 TLE 而非誤判,以 op-count 探測分類;程式自行拋出 TimeoutError 仍正確判為 RE
- **新挑戰題「緩衝區稽核日誌」**(id 56,medium/競賽題型):素養導向過程輸出題——邊緣裝置緩衝區兩端稽核情境,每批讀數輸出峰值輪與谷值輪兩行移除日誌(兩端相同一律移除最新端),三個測資分區共 6 筆

### Changed

- password-check 補上 reference_solution,content-regression 對全站 56 題的正解互驗覆蓋缺口歸零

### Fixed

- 修復 op-counter 對扁平頂層學生程式碼完全不計數的盲區(op_count 恆 0,運算量上限形同虛設);同時豁免 generator 計數、解毒跨測資 trace 殘留(單筆 RE 不再毒殺下一筆測資)

### Security

- dev 模式(vitepress dev)補剝 reference_solution,關閉本機 dev server 把完整正解送進瀏覽器模組的外洩面;正式站自 v1.2.0 前即於 build 期剝除、無外洩

## [1.2.0] - 2026-07-25

新增可持久化的編輯器設定與資料結構挑戰題系列首題，並修復下載紀錄面板被裁切等多項 UI 問題。

### Added

- **編輯器設定**：齒輪選單可切換「自動完成」與「括號自動閉合」，設定存於瀏覽器並即時生效
- **編輯器字型大小調整**：設定選單內以步進器調整程式編輯器字級（10–24px），即時套用且保留游標與復原歷史
- **新挑戰題「撲克牌重排計數」**（id 55，hard／競賽題型）：資料結構系列首題，採 APCS 多筆資料輸入格式與空白起始程式碼；極限測資讓暴力模擬必然逾時，引導以找規律推導公式作答

### Fixed

- 下載紀錄面板被編輯器下方區域裁切、預設高度下看不到欄位與按鈕：面板改為向上開啟並完整可見（抽出 `useAnchoredPopover` 共用 composable），同時補上點擊外部／Escape 關閉、與設定選單互斥、關閉重開保留已填資料、鍵盤 Tab 可達與焦點歸還等行為
- 編輯器設定選單在拖曳結果區分隔線時與齒輪按鈕脫離的問題
- 字型步進器在達到字級上下限時焦點脫離選單的問題
- 測資池建置在大整數答案題型（如 2^N）下因子行程輸出緩衝不足而以 ENOBUFS 失敗的問題

## [1.1.0] - 2026-07-06

補齊純前端道場的核心能力（學生作答持久化），完成模組一、二完整課程內容，並導入自動化品質守門與測資安全強化。

### Added

- **學生作答情形本機持久化（IndexedDB）**：完成度追蹤（`ChallengeCard` ✓ 徽章 + 題庫頁「已完成 X/54」計數）、作答軌跡錄製（edit｜run｜submit）、可下載作答紀錄 Markdown（含給 LLM 的提示前言）與 JSON
- 模組一、二完整教學內容與互動練習：迴圈與重複課程、數學素養 × 運算思維鷹架、APCS 素養導向題型、畢業考綜合題，以及 19 題程式挑戰的完整說明與範例
- 挑戰題庫搜尋功能與 `Challenge` 型別統一
- 自動化品質守門 CI（`.github/workflows/ci.yml`）：typecheck、lint、vitest、cargo test；雙測資產生器一致性測試（Rust `rng.rs` ↔ Python `generate-pools.ts`）與內容層回歸測試
- 可擴充題型 taxonomy 與領域 skill；挑戰 frontmatter 新增選填 `reference_solution` 欄位
- Ch1 Appendix Python 關鍵字完整參考表；`lit-fetcher` / `ref-verifier` 學術文獻管理工具；`pnpm gen:keymaterial` 指令

### Changed

- 測資池改用 challenge slug 隔離：同 `algorithm` 的不同題目不再共用池檔，避免互相覆寫測資
- Release 產物名由 `crypto-challenge-*` 改為 `fhsh-py-dojo-*`；預設挑戰題名 fallback 由「密碼學挑戰 #N」改為中性的「挑戰 #N」
- AI agent 指令檔（`CLAUDE.md` / `AGENTS.md` / `GEMINI.md`）領域化並補上專案領域指南；統一文件標示 Node.js 22+、新增題目 SOP 以 `pnpm new-challenge` 為首選

### Fixed

- 移除壞掉且有害的 npm `wasm-pack` 相依，改由 PATH 提供（本機 cargo、release CI 用 `jetli/wasm-pack-action`）；並修正 CI 因 wasm-pack postinstall 404 而安裝失敗
- 以自建整合取代 `vitepress-plugin-mermaid`，修復頁面崩潰；修復 `password-check` 測資池生成失敗
- 修正乘法表 generator 的對齊格式

### Security

- 答案金鑰零外洩：作答紀錄於寫入與匯出時皆依測資池 `verdict_detail` 雙重過濾，隱藏題的期望輸出絕不進入下載檔；匯出 Markdown 以變動長度 code fence 與 table／inline 逸出，防止學生輸出偽造報告結構或注入 LLM

### Removed

- 移除無呼叫端的 `useApi` / `useWsApi` composable 死碼與 `.gitignore` 指向已更名 crate 的失效規則

## [1.0.0] - 2026-04-05

### Added

- 初始化「台北市立復興高級中學 Python 自學道場」專案
- 基於 crypto-challenge 架構建立 Python Judge 系統（Rust/WASM + Pyodide）
- 新增 `useApi` / `useWsApi` composable（VueUse useFetch / useWebSocket wrapper）
