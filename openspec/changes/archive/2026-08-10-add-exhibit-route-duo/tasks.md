## 1. 語義正本與平台事實

- [x] 1.1 量測判題機制並填入 `trace-matrix.md` 的 C 表（op 上限、tracer 計數語義、5s 軟旗標、累計硬砍、遞迴天花板、輸入預算、池結構），每列附原始碼或實測證據
- [x] 1.2 [P] 建立 `curation/semantics013.py`：形狀產生器、三種打卡序、兩種模式的輸入／期望輸出，滿足 "Exhibit route rebuild I/O contract"
- [x] 1.3 [P] 建立 `curation/semantics014.py`：翻板語義與三條獨立實作（奇偶直推／逐球全模擬／反向讀取），交叉驗證 0 筆不符，滿足 "Pinball track predict I/O contract"

## 2. 測資策展與斷言牆

- [x] 2.1 撰寫 `curation/plan013.py` 的 20 筆 entry 表與斷言牆，逐筆計算每條錯誤路線得分，滿足 "Exhibit route rebuild testcase plan" 與 "Exhibit route rebuild wrong-route discrimination"
- [x] 2.2 撰寫 `curation/plan014.py` 的 20 筆 entry 表與斷言牆（step 門檻、收編路線 op 模型、位樣非回文、每筆 ≥2 組），滿足 "Pinball track predict testcase plan"
- [x] 2.3 兩支腳本各跑出 `literals/` 與 `reportNNN.json`，斷言牆全綠才得寫檔

## 3. 題目檔組裝

- [x] 3.1 以 `pnpm new-challenge` scaffold 兩題並確認配號為 apcs013／apcs014，滿足 "Shared authoring constraints for the exhibit route duo"
- [x] 3.2 [P] 撰寫 `curation/gen013.py`／`curation/ref013.py`（異構實作）並在全 20 筆 literal 上與語義正本一致
- [x] 3.3 [P] 撰寫 `curation/gen014.py`／`curation/ref014.py`（異構實作）並在全 20 筆 literal 上與語義正本一致
- [x] 3.4 撰寫兩份題面 `curation/page013.md`／`curation/page014.md`，遵守 D6 全部約束（禁字、無不可能句、範例＝entry 原樣）
- [x] 3.5 以 `curation/assemble.py` 組裝兩個題目檔：literal 逐 byte 嵌入、禁字檢查、starter_code 空字串、回讀比對

## 4. 設計期賞金與處置

- [x] 4.1 對設計（非實作）執行多路線對抗賞金，逐條裁決 hole／co-opt／wrong-fact，並把結論回填 `trace-matrix.md` 的賞金結果表
- [x] 4.2 對每條 must-fix 做副作用檢查後再修，修完當輪重跑受影響的斷言牆與量測（I-4／I-8）

## 5. 出貨量測閘與驗證

- [x] 5.1 `pnpm build:wasm` 與 `pnpm build:pools` 重建正式池
- [x] 5.2 對出貨 literal 實測 reference_solution／generator／收編路線／錯誤路線的 ops 與牆鐘，回填 `trace-matrix.md` 的 V 表，滿足 "Exhibit route rebuild performance envelope and bypass disposition" 與 "Pinball track predict cost ladder and bypass disposition"
- [x] 5.3 跑 `challenge-params`、`content-regression`、`pnpm typecheck`、`pnpm lint` 四道 scoreboard 閘
- [x] 5.4 在瀏覽器 dev 站以 agent-browser 逐路線提交，核對 V 表預期得分與累計牆鐘預算
