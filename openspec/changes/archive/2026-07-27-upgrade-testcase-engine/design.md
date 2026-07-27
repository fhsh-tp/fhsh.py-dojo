## Context

測資輸入產生邏輯目前有兩份實作:Rust crate(testcase-generator,編為 WASM 供瀏覽器 dev 模式即時產生)與 scripts/generate-pools.ts 內嵌 Python 腳本(建置期產正式池)。兩者由 scripts/generator-parity.test.ts 以「語意一致 + 型別集合比對」守門,但欄位級變更無自動偵測。params 模型為「一鍵一行、count 獨立隨機」,無法表達競賽式多筆測資格式。三輪 adversarial review 已確認:(1) 判題與池層把 input 當不透明字串,結構上相容新格式;(2) 量級與靜默失敗是實際風險面(池檔上限、TLE、parser 靜默吞未知欄位、Python 端未知型別 fallback);(3) 建置鏈存在 key_material → WASM → pools 的三段順序相依。Node 24 / tsx 載入 web-target WASM 已 spike 驗證可行(bytes init)。

## Goals / Non-Goals

**Goals:**

- 輸入產生邏輯單一真相源:建置期與瀏覽器走同一份 Rust 程式碼。
- params 表達力達到競賽式格式:群組 repeat + count.from 連動,足以宣告「第一行 T,每筆第一行 Ni、再 Ni 行整數」。
- 正式池決定性:同規格必產同池,可重現、可 diff、CI 穩定。
- 壞規格在 parse 期以可讀錯誤失敗:不進入產生期 panic(WASM trap 後實例狀態未定義)。
- 輸入規模在源頭治理:預算超標即建置失敗,下游(池檔大小、前端執行鏈)不需改動。

**Non-Goals:**

- testcase_plan(APCS 分區)實作、池層選取邏輯變更、前端程式碼變更、lib 合流、faker 常駐、既有題目改寫、單筆超過硬上限的大測資。

## Decisions

### D1:Node 端以 bytes init 載入 web-target WASM(不出第二個 build target)

wasm-pack 維持單一 --target web 產物。scripts/wasm-input-generator.ts 以 template-literal 動態 import glue、readFileSync 讀 .wasm、init({ module_or_path: bytes })。理由:spike 已實證可行;避免第二條建置產物鏈;動態 import 使 typecheck 與無產物的 CI 單元測試不受靜態路徑影響。WASM 初始化必須 lazy(首次呼叫才 init),否則 scripts/generate-pools.test.ts 的純單元測試在無產物環境 import 即炸。

### D2:新 WASM 入口 generate_pool_inputs(spec_json, count),spec 物件化

spec_json 形狀:{ "params": {…}, "seed": "<字串,選填>", "input_budget": <bytes,選填> }。頂層未知欄位拒收,但 "testcase_plan" 鍵名保留(出現時回報「reserved, not yet implemented」錯誤,不靜默忽略)。既有 generate_challenge(params_json, count) 保留不動(瀏覽器 dev 模式呼叫,非決定性、僅硬上限防護)。理由:附加模式——前端零改動;spec 物件是 testcase_plan 的 API 地基。

### D3:seed 以 FNV-1a 64-bit 在 Rust 端導出

seed 字串由建置腳本傳入(值為 challenge slug);Rust 端以 FNV-1a(slug bytes + 0x00 分隔 + params_json bytes)→ u64 → SmallRng::seed_from_u64。理由:雜湊在 Rust 端做,跨平台穩定、無外部相依;params 內容一改 seed 自動變;省去 getrandom 環境熵源相依。未帶 seed 時 fallback from_entropy(僅 dev 模式路徑會如此)。

### D4:輸入規模預算採兩層執行

- 硬上限 65536 bytes:parse_params 內無條件強制(worst-case 估算超標即 Err),保護所有呼叫端含 dev 模式。
- 可調預算:generate_pool_inputs 強制 input_budget(預設 4096,上限 65536,超過 65536 的宣告本身為 parse 錯誤)。
- worst-case 估算式:int = max(位數(min), 位數(max)) 含負號;字串型別 = max_len;enum = 最長 value 的 bytes;乘上 count 上界(count.max 或 from 引用參數的 max)加 separator bytes;群組 = 內部總和 × repeat 引用參數的 max,加行分隔。估算永遠 ≥ 實際產出 bytes。錯誤訊息輸出逐參數估算式。

### D5:群組與連動的引用語意(邊界矩陣)

名詞:引用參數 = from/repeat 所指向的參數;宿主 = 帶有 from/repeat 的參數或群組。

| 規則 | 合法 | 違反時 |
| --- | --- | --- |
| 引用參數必須先於宿主宣告(往回引用) | 同層先宣告,或群組內宿主引用頂層先宣告者 | parse 錯誤:forward/unknown reference |
| 引用參數型別 | int 且單值(無 count 或 count 固定 1..1) | parse 錯誤:non-scalar-int reference |
| 引用參數值域 | min ≥ 0(repeat 與 from 皆是;repeat 0 次 = 群組零行,from 0 = 空行) | parse 錯誤:negative reference range |
| from 與 min/max 並存 | 不可 | parse 錯誤:mutually exclusive |
| 群組巢狀 | 群組內不得再宣告群組(深度 1) | parse 錯誤:nested group |
| 群組被 from/repeat 引用 | 不可 | parse 錯誤:group reference |
| 群組內宿主引用同一群組實例內的兄弟參數 | 可(每次 repeat 各自解析) | — |
| repeat 出現在非群組參數上 | 不可 | parse 錯誤(deny unknown fields 自然涵蓋) |

渲染語意:每個純量參數一行;count>1 以 separator 連接(separator 為 "\n" 時跨行);群組每次重複依宣告序渲染內部參數,重複之間以換行銜接。既有「一參數一行」文件契約改寫為「一參數一區塊,預設一行」。

### D6:產生器攜帶跨參數狀態

generate_input 由無狀態 map 改為依宣告序迭代並維護「本 scope 已抽值表」(頂層一份;每次群組重複建立新的群組層表,查找先查群組層再查頂層)。from/repeat 於使用點查表,值必存在(parse 期已保證往回引用)。debug_assert 全部升級為 parse 期 Result 驗證。

### D7:建置鏈三段化與守門替代

package.json 的 dev/build 改為 gen:keymaterial → build:wasm → build:pools → …;ci.yml verify job 加裝 wasm-pack 與 build 順序(cargo 冷編譯成本接受,不引入 cache 以免範圍膨脹);release.yml 沿用 pnpm build 故自動修正;Cloudflare Pages dashboard build command 需手動同步(記入 tasks 的人工驗證項)。generator-parity.test.ts 刪除,守備由 scripts/challenge-params.test.ts 接手:枚舉 docs/challenge/*.md,全部 params 需通過 WASM parse 與預算檢查(此測試需 WASM 產物,無產物時 fail 而非 skip——建置順序保證 CI 有產物)。content-regression.test.ts 改用 WASM 產輸入;python3 缺席時維持 skip,但覆蓋率地板斷言移到 skip guard 之前(以 frontmatter 掃描計數,不依賴 python3)。

## Implementation Contract

- 觀察點 1:pnpm build:pools 在 55 題上成功,產出池檔;連續執行兩次,除檔案時間戳外池內容 byte-identical(seed 決定性)。
- 觀察點 2:deque 式規格(t → 群組[n, nums(count.from=n, separator="\n")])經 generate_pool_inputs 產出格式正確的多行輸入;n 抽值與 nums 行數一致。
- 觀察點 3:違反 D5 矩陣任一列的規格,generate_pool_inputs 與 parse_params 回傳含規則名的可讀錯誤,而非 RuntimeError: unreachable。
- 觀察點 4:cargo test、pnpm test --run、pnpm typecheck、pnpm lint 全綠;既有 55 題 frontmatter 零修改。
- 觀察點 5:scripts/generator-parity.test.ts 不存在;scripts/challenge-params.test.ts 對全部題目綠燈。

## Risks / Trade-offs

- 舊 WASM 產物 + 新原始碼的新鮮度風險(review 發現 R-4):建置順序三段化後 build:pools 必然使用剛建好的 WASM,常規路徑消除;開發者手動跳步仍可能不同步,接受此殘餘(記入 future 文件)。
- content-regression 覆蓋率仍僅 4/55(有 reference_solution 者),不因本次擴大;全題目 parse 冒煙補上宣告層守備,執行層覆蓋另案。
- CF Pages build command 在 repo 外,無法以程式碼保證;以 tasks 的部署驗證項承接。
- deny unknown fields 屬收緊:理論上可能拒收今日「被靜默容忍」的錯誤宣告;全題目冒煙測試在本 change 內即會揭露,屬預期效果而非風險。

## Migration Plan

1. Rust 端先行(能力 + 驗證 + 新入口),cargo test 綠。
2. 建置腳本切換 WASM 並刪除 Python 複寫,build:pools 全量重產驗證。
3. 測試汰換(parity 刪除、冒煙新增、content-regression 改造)。
4. 建置鏈與 CI/文件同步。
5. staging 部署驗證(CF build command、Node 版本、池檔大小)。

回滾:單一 change 整體 revert;snapshot/2026-07-26-pre-engine-upgrade 分支為還原點。

## Open Questions

- 無(discuss 階段已收斂;testcase_plan 相關問題凍結於 future 文件)。
