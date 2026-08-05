# Audit 裁決帳本（audit-ledger）

> 依 2026-08-05 RCA 建議建立：每筆 finding 的終局裁決。後續 reviewer 重提已裁決項目須附「使前輪理由失效的新證據」，否則不計入未收斂。

| ID | 輪 | 主張（縮寫） | 裁決 | 理由／證據 |
|----|----|----|----|----|
| R1-HIGH-1 | R1 | spec SHALL NOT 永久凍結防禦 | FIXED（措辭） | 加條件範圍＋BACKLOG 追蹤指向；「永久」被駁（MODIFIED delta 前例）|
| R1-HIGH-2 | R1 | TLE 保證不可執行卻入 spec | FIXED（措辭） | spec 本已限定 offline tracer；補 settrace(None)/C 內建非保證清單 |
| R1-MED-1 | R1 | design 誤稱 literal 不進 bundle | FIXED | strip 只剝 generator/reference；已改寫並警示整欄 strip 陷阱 |
| R1-MED-2 | R1 | 三筆 literal 逐位元組相同 | FIXED | 改 ab/cd/ef 相異內容（R2 再改異長異殘量）|
| R1-LOW-1 | R1 | tasks.md 停留降級前敘述 | FIXED（註記） | 附註路線；input_budget 推論部分被駁 |
| R1-LOW-2 | R1 | 公告界寬於隨機 band | REFUTED | 端點 1/2/40000 皆有覆蓋；內部空洞無行為訊號；spec 明文要求該敘述 |
| R2-HIGH | R2 | 同長同殘量可被 len==20000 分支繞過 | FIXED | 異長 30000/34001/38002＋異殘量 0/1/2；作弊解 dev 實測 13/20 |
| R2-MED-1 | R2 | content-regression 抽樣覆蓋缺口 | FIXED（措辭）＋ACCEPTED | spec 改述實際閘門；共用測試改造屬 out-of-scope（撞 scope boundaries），BACKLOG §2.10 已有覆蓋率條目 |
| R2-MED-2 | R2 | BACKLOG §2.8 補償控制失效未回寫 | FIXED | §2.8 就地訂正＋spec 指向 BACKLOG 追蹤 |
| R2-LOW | R2 | input_budget 65000 死餘裕 | FIXED | 收至 42000（R2 對抗核可區間），R3 再收至 40004 |
| R3-HIGH-1 | R3 | 三份長度鍵 hardcode＋naive B 可 20/20；design 全稱句不實 | FIXED（措辭）＋ACCEPTED | 保證句改條件句式（單分支被封堵／三鍵 hardcode 不被封堵、明列 outside-the-cliff）；攻擊本體與 replace 繞法同屬已接受平台級姿態。RCA 裁定 RELITIGATED/SELF_INFLICTED（design 同段落早已揭露並接受該殘餘）|
| R3-MED-1 | R3 | input_budget 42000 留 1996B 漂移窗 | FIXED | 收至 40004（cargo 實測 40003 fail／40004 pass）；RCA 裁定 SELF_INFLICTED（R2 自加的守衛宣告句）|
| R3-MED-2 | R3 | literal 值遮蔽可行、R1/R2 裁決評的是 strawman | OUT-OF-SCOPE-TRACKED | 機制屬實（computePlanTotal 不讀值），但違反 generator-strip-plugin baseline spec remain-intact 條款且波及全部含 literal 題目 → BACKLOG §2.12；design 警語已改寫不再誤導 |
| R3-LOW-1 | R3 | generator/reference n=0 分歧 | FIXED（自願加固） | R2 已 cleared（不可達＋loud fail），裁決維持；順手 max(counts, default=0) 終結重審。代價：少一個 loud 分歧偵測器 |
| R3-LOW-2 | R3 | 小版面無隨機覆蓋 | REFUTED（三度） | R1 駁、R2 降級、R3 自陳 Not a defect；min_len 3 為 spec 明文契約 |
| R3-LOW-3 | R3 | aaa→1 無 literal 釘住 | REFUTED | 隨機壓力筆單筆含 ~44 個三連字元，錯解被抓機率 ≈1−e^−300、每 block 皆然（結構性必然非薄弱統計）；加 aaa 會違反邊界 literal 的 spec 釘死語義 |
