## Context

批次「六題 stack／tree」的 change A。所有規範性事實的單一真相來源為 `trace-matrix.md`（C/A/B/V 編號），本文件 prose 一律由矩陣派生；修訂先改矩陣再同步。探針原始檔於 session scratchpad（probe_harness.py 複製判題 wrapper 同款 settrace tracer）。

## Goals / Non-Goals

- Goals：兩題（1a/1b）frontmatter、測資策展、題面、驗證閉環一次到位；1b 建立 op counter 真斷崖（V5）；1a 明確收編 C 繞道（A4）。
- Non-Goals：不改 Rust 引擎；不出後續 change B/C；不修平台截斷式 UI 議題。

## Decisions

### D1. 相關性輸入以「literal 策展＋enum soup band」解決（C8）

引擎 8 型別無法原生產生合法括號序列。合法／陷阱／獵殺／stress 用 literal（期望輸出仍由 generator 對輸入即時計算）；隨機 band 用 `t` 固定 1＋`s`（enum，values＝該分區允許字元清單，count＝長度範圍，separator ""）產生 soup（1a 幾乎必 NG——判定分布由每分區至少一筆 OK literal 平衡，A8）。band override 只補丁 `values`／`count`（Usage.md override 規則）。

### D2. params 骨架（兩題同構）

```yaml
input_budget: 63488
params:
  t:
    type: int
    min: 1
    max: 1
  s:
    type: enum
    values: ["(", ")", "[", "]", "{", "}"]   # 1b 另加雜訊字元集：a-z 抽樣、數字、.,;（不含空白，避免 strip 誤傷）
    count:
      min: 2
      max: 500
      separator: ""
testcase_plan:
  # 1a 佈局（A7）：L1 範例(1)；band () (2-3)；L 陷阱(4)；band ()[] (5-7)；L OK 保底(8)；
  #   L 陷阱(9)；band ()[] (10-11)；L 陷阱(12)；L 3 種 OK 保底(13)；band(14)；L 陷阱(15)；
  #   band(16-17)；L 陷阱(18)；band(19)；L stress 62KB 深巢(20)
  #   ——交錯陷阱共 5 筆（A3：計數器假解只死於「平衡但交錯」literal，隨機 soup 會巧合正確）
  # 1b 佈局：L1 範例(1)；band(2-3)；L(4)；band(5-7)；L 無括號邊界(8)；band(9-11)；L(12)；
  #   L 3 種展示(13)；獵殺 literal(14,15,16)；band(17)；獵殺 literal(18,19,20)（B4/B7）
```

實際條目數以「band count 加總＋literal 數＝20」封閉（C3）；上述註解為分配藍圖，實作時逐條寫死並以離線驗算腳本核對每條預算與判定分布。

### D3. 1a 繞道處置：收編（A4，rank-code-duo D6.b 判例）

replace 迴圈（93,017 ops／5.5s native @31k 深巢）與 find+切片（434,026 ops／3.6s）皆低於 op 上限一個數量級；牆鐘獵殺需 ≥10 筆 62KB 獵殺筆（硬上限 65536 不可覆寫，不可行）→ 量化證明不可獵殺 → 收編。題面沉默（不寫成本警語也不寫不可能性承諾——1a 主考點是 A3 正確性陷阱，繞道路線得分不影響教學目標的計數器獵殺）。第 20 筆 stress literal 讓此路線成本可見（單筆 ~5.5s native）但不致死（120s 總預算餘裕充足）。

### D4. 1b 斷崖：op counter 逐筆爆殺（B4，R1 重設計）

R1 稽核發現原 6 筆獵殺有兩缺陷：18/19/20 與 14/15/16 逐位元組重複；且最精簡回頭掃描（單行 while，1 op/iter）下餘裕僅 1.11×。重設計為六筆互異獵殺（參數見矩陣 B4）：每筆 lean 下限 m×2k ≥ 20M（1 op/iter 仍 ≥2× op 上限），三筆走 B1(ii) 殘留分支（答案 7/5/9，同樣強迫全行掃描且非 0——壓低常數 0 投機解）。實測：六筆對 1 op/iter 精簡變體逐筆 10M 爆殺（K18 全量 26,290,548 ops）；正解最大筆 66,043 ops。op 爆殺為逐筆（每筆判題獨立 10M 額度），非累積總預算殺——與 1a 的 C 繞道（op 稀疏、只能靠牆鐘）機制不同，這是 1b 能建真斷崖的根本原因。C 層回頭掃描（str.rfind 系）op 稀疏、不可獵殺，收編為 accepted alternative（B9），與 1a replace 同判例。

### D5. generator 與 reference_solution 分工（C9）

- 1a generator：stack 存「字元」＋dict 配對表；reference：stack 存「索引」查原字元（佈局不同、語義同 A1）。
- starter_code：兩題皆讀入後**不輸出**（C10）——原地提交 0/20；「刻意常數輸出」殘餘得分為 accepted residual（1a 全 NG≈11/20、1b 全 0≈3~5/20，逐筆亮 WA 無法通關）。
- 1b generator：stack 存 (字元, 位置) tuple；reference：雙平行 list（chars/positions）。
- 兩題 generator 皆逐行 `input()` 讀取；輸出行尾無多餘空白。

### D6. 題面（素養層，A2/B1 派生）

- 1a「道具箱裝箱檢查」：劇團三種規格道具箱——小箱 `()`、中箱 `[]`、大箱 `{}`；開箱寫左符號、封箱寫右符號；規則：後開的箱要先封、同規格才能互配；每場演出一行紀錄，輸出 `OK`／`NG`。
- 1b「校刊排版檢查器」：稿件行混有一般字元與三種排版標記（圓括號旁註、方括號注音、大括號版面指令）；輸出第一個「無法配對」字元的位置（1-based，所有字元皆計位），全部配對輸出 `0`。三分支語義照 B1 全文寫入輸出說明（含「最早未配對左符號」殘留分支與範例）。
- 兩題題面皆不出現資料結構術語；1a 題面對效能完全沉默（A4）；1b 提醒句限定為窄而實測為真的敘述（B10）：只說「逐字元往回重新掃描的迴圈寫法」經實測超限，不對任何路線做不可能性承諾（C-rfind 反例已收編 B9）。

## Implementation Contract

1. `pnpm new-challenge prop-box-packing --title "道具箱裝箱檢查" --difficulty medium --category apcs --type competition`；`pnpm new-challenge magazine-typeset-check --title "校刊排版檢查器" --difficulty medium --category apcs --type competition`（id 由 scaffold 配號，C1）。
2. 兩題 frontmatter 依 D2 骨架完成 params/testcase_plan/generator/reference_solution/starter_code；literal 由離線腳本產生後貼入（腳本存 scratchpad，不入 repo——與 exam-collect 慣例一致）。
3. 驗收出口：`pnpm build:pools` 零錯誤；`node_modules/.bin/vitest --run scripts/content-regression.test.ts` 兩題通過；`node_modules/.bin/vitest --run scripts/challenge-params.test.ts` 通過；dev e2e 依 V1–V5 預測矩陣逐路線驗證（誤差＝逐筆位置零偏差）。
4. 失敗模式：任一 literal 超預算→建置期指名條目失敗（C4）；generator/reference 語義分歧→content-regression 指名失敗（C9）。

## Risks / Trade-offs

- 1b 獵殺筆餘裕：R1 已按 1 op/iter 下限重算（m×2k ≥ 20M，實測最小筆 26.3M）——這已是 while 迴圈的理論下限，無更省變體空間。
- 1a soup band 的判定分布隨 block 隨機——OK literal 保底（A8），但各 block 的 NG 比例會浮動（可接受，判題抽整 block）。
- 計數器假解在隨機 NG soup 上巧合正確（A3 修訂）——其得分下壓完全依賴 5 筆交錯陷阱 literal；若 audit 認為 15/20 仍過寬，追加陷阱 literal 即可線性下壓。
- 62KB stress literal 使 1a 的 .md 檔約 +62KB（gem-blast 60KB 判例在前，可接受）。
