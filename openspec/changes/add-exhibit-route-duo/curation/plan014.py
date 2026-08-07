"""apcs014 彈珠台軌道預測 — 測資計畫＋斷言牆（B 表事實的機械正本）。

執行：python3 plan014.py         （驗證＋寫出 literals/ 與 report014.json）
      python3 plan014.py --check （只驗證，不寫檔）

成本模型（設計期賞金修正後）：
  * op 計數器只數 line 事件，逐球模擬可把整段下降攤平到同一行 → **每球約 1 op**
    是任何「逐球」寫法的下界，不是每步 1.105 ops。門檻因此改用**球數**。
  * 逐層計數解（收編）成本 ∝ 2^(D−1)，與球數無關 → 殺手筆用「小 D、大球數」，
    兩條路線才分得開（大 D、球數受 2^(D−1) 卡住時數學上分不開）。
  * 攤平寫法的牆鐘 ∝ 總下降步數 → 殺手筆同時設步數上限，避免陣亡的提交把
    C4 的累計 120 秒預算吃光。
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import semantics014 as S  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
LIT_DIR = os.path.join(HERE, "literals")

MAX_I = 10_000_000             # 球號上限（題面同步）
MAX_D = 17                     # 層數上限（題面同步）：取 17 使全域最大週期 2^16 = 65,536，
                               # 讓收編路線 P1「取週期再模擬」在最壞情形仍付得起（B8）；
                               # 若放到 20，要鑑別「寫死模數 2^18」就必須放一條 I > 262,144
                               # 的 D=20 測試，那條同時會讓 P1 跳閘——兩者互斥（R2-2）
KILL_FROM = 16                 # 第 16 筆起為殺手帶
PASS_STEP_CAP = 1_000_000      # 前段：最貴的逐球寫法（4.158 ops/step）也要能過
KILL_BALL_MIN = 15_000_000     # 殺手帶：每球 1 op 的單球攤平寫法要跳閘（1.5 倍餘裕）
KILL_STEP_MAX = 85_000_000    # 殺手帶上限：陣亡提交每筆 ≈ 11 秒、5 筆 ≈ 54 秒 < C4 的 120 秒
P1_OPS_CAP = 8_000_000         # 收編路線 P1 的 op 模型上限：4.2 ops/step × Σ(D−1)×min(I, 2^(D−1))
MIN_BIG_SPAN = 16              # 大球數測試的週期下限：span ≤ 8 時，逐條非退化斷言會把可用殘值
                               # 砍到只剩 2–4 個，答案塌縮成「I mod 2 或 mod 4」的查表（R2-1）
COOPT_NODES_CAP = 600_000      # 每筆 Σ2^(D−1) 上限：收編路線 L1 最貴寫法（遞迴版）實測約
                               # 13 ops/節點，13 × 600K = 7.8M < C1，留 22% 餘裕
BIG_I = 100_000                # 「大球數」門檻：超過此值的測試才承擔逐條退化性斷言

ENTRIES = [
    # 第 1–15 筆：逐球模擬可過（球數小）
    [(4, 1), (4, 2), (4, 3), (4, 8), (4, 11)],              # 頁面範例（含球數 > 袋數）
    [(2, 1), (2, 2), (3, 1), (3, 4), (5, 16), (4, 2), (2, 7), (3, 10)],  # 邊界
    [(6, 32), (7, 10), (8, 100), (5, 33)],
    [(10, 300), (9, 256), (12, 50), (3, 999)],
    [(14, 1000), (11, 777), (13, 2048), (2, 12345)],
    [(16, 5000), (15, 3000), (6, 40000)],
    [(17, 20000), (16, 15000), (4, 30000)],
    [(17, 30000), (12, 20000), (7, 10000)],
    [(17, 50000), (6, 20), (3, 20000)],
    [(17, 25000), (11, 25000), (5, 15000)],
    [(17, 50000), (3, 2), (8, 3000)],
    [(16, 54000), (2, 1), (9, 1500)],
    [(17, 45000), (16, 6000), (2, 49999)],
    [(17, 35000), (13, 15000), (4, 40000)],
    [(17, 30000), (10, 5000), (5, 80000)],
    # 第 16–20 筆：球數大到「每球至少一個 line 事件」的逐球寫法都跳閘
    #   bulk 用 D=5（週期 16，非退化殘值仍有 12 個，不會塌縮成小模數查表）
    #   每筆另含一條 D=17 大球數測試：週期＝全域最大 2^16，逼任何寫死的小模數失效
    [(5, 3_800_002), (5, 3_810_003), (5, 3_820_005), (5, 3_830_006), (17, 200_001), (12, 4095)],
    [(5, 3_840_002), (5, 3_850_003), (5, 3_860_005), (5, 3_870_006), (17, 210_003), (14, 9000)],
    [(5, 3_880_002), (5, 3_890_003), (5, 3_900_005), (5, 3_910_006), (17, 220_005), (16, 12345)],
    [(5, 3_920_002), (5, 3_930_003), (5, 3_940_005), (5, 3_950_006), (17, 230_007), (10, 300)],
    [(5, 3_960_002), (5, 3_970_003), (5, 3_980_005), (5, 3_990_006), (17, 240_009), (7, 60)],
]

CAPS = {
    "ref": ("eq", 20),
    "reversed": ("eq", 20),
    "P1_periodic_sim": ("eq", 20),
    "L1_levelwise": ("eq", 20),
    "Z1_echo_I": ("eq", 0),
    "Z2_const1": ("eq", 0),
    "Z3_maxbag": ("eq", 0),
    "E1_noreverse": ("eq", 0),
    "E2_zerobased": ("eq", 0),
    "E3_flippernum": ("eq", 0),
    "E4_parityflip": ("eq", 0),
    "E5_dlevels": ("eq", 0),
    "E6_firstonly": ("eq", 0),
    "Z4_bigmax": ("eq", 15),   # 大球數就丟最大袋：前段可過、殺手帶必錯
}


def coopt_nodes(cases):
    """收編路線 L1 的工作量：整台機器的翻板數 Σ2^(D−1)（與球數無關）。"""
    return sum(1 << (D - 1) for D, _ in cases)


def p1_ops(cases):
    """收編路線 P1 的 op 模型，取**最貴**的合理寫法：不是「只模擬 min(I, 週期) 顆球」，
    而是「把整個週期模擬一遍建表再查」——成本 ∝ (D−1)×2^(D−1)，與 I 無關（R2 的
    ladder-inversion 發現：帶著週期洞察的建表寫法反而比毫無洞察的逐球模擬更早死）。"""
    return int(4.2 * sum((D - 1) * (1 << (D - 1)) for D, _ in cases))


# 註：不另設「(D, I mod 2^j) 查表」的一般化斷言——任意查表都能擬合少數幾行，
# 那等同於把公開的出貨答案記下來（C11／F18 已接受的專案層殘餘）。真正要擋的是
# 「用固定模數化約後跑正確演算法」這一族，由下方 fixed_period_family 逐一驗證，
# 其豁免門檻取自值域最大週期（R2-2）。


def main(write=True):
    problems = []
    scores = {k: 0 for k in S.ROUTES}
    per_entry = []

    for i, cases in enumerate(ENTRIES, 1):
        text = S.render_input(cases)
        exp = S.render_expected(cases)
        st = sum(S.steps(D, I) for D, I in cases)
        bl = sum(S.balls(D, I) for D, I in cases)
        nodes = coopt_nodes(cases)
        p1 = p1_ops(cases)
        row = {
            "entry": i,
            "tests": [{"D": D, "I": I, "bag": S.bag_parity(D, I), "steps": S.steps(D, I)} for D, I in cases],
            "total_steps": st,
            "total_balls": bl,
            "coopt_nodes": nodes,
            "p1_ops_model": p1,
            "bytes": len(text.encode()),
        }
        for name, fn in S.ROUTES.items():
            ok = fn(text) == exp
            row[name + "_ok"] = ok
            if ok:
                scores[name] += 1
        per_entry.append(row)

        # ── 結構斷言 ────────────────────────────────────────────────
        for D, I in cases:
            if not (2 <= D <= MAX_D):
                problems.append("entry %d: D=%d 超出 2..%d" % (i, D, MAX_D))
            if not (1 <= I <= MAX_I):
                problems.append("entry %d: I=%d 超出 1..%d" % (i, I, MAX_I))
        if len(cases) < 2:
            problems.append("entry %d: 僅一組測試，只解第一組的路線將白拿一筆" % i)
        if len(set(cases)) != len(cases):
            problems.append("entry %d: 含重複的 (D, I) 組合，memo 寫法可對半砍成本" % i)
        if not any(I >= 2 for _, I in cases):
            problems.append("entry %d: 全部 I=1，多走一層的誤解路線將白拿一筆" % i)
        # 至少一組要讓「原樣輸出球號」「輸出固定袋號」「不做反向」三族同時失效
        if not any(
            S.bag_parity(D, I) != I
            and S.bag_parity(D, I) != 1
            and S.bag_parity(D, I) != (1 << (D - 1))
            and S.bag_parity(D, I) != (I - 1) % (1 << (D - 1)) + 1
            for D, I in cases
        ):
            problems.append("entry %d: 沒有任何一組能同時鑑別零洞察路線族" % i)
        if i < KILL_FROM:
            if st > PASS_STEP_CAP:
                problems.append("entry %d: steps %d > %d（逐球模擬應可過）" % (i, st, PASS_STEP_CAP))
        else:
            if bl < KILL_BALL_MIN:
                problems.append("entry %d: 球數 %d < %d（每球 1 op 的單球攤平寫法可能存活）" % (i, bl, KILL_BALL_MIN))
            if st > KILL_STEP_MAX:
                problems.append("entry %d: steps %d > %d（陣亡提交會吃掉累計牆鐘預算）" % (i, st, KILL_STEP_MAX))
            # 承擔成本鑑別責任的每一條大球數測試都必須逐條非退化
            for D, I in cases:
                if I <= BIG_I:
                    continue
                span = 1 << (D - 1)
                bag = S.bag_parity(D, I)
                if I % span == 0:
                    problems.append("entry %d: 大球數測試 (%d, %d) 落在週期整倍數上，答案恆為最大袋號" % (i, D, I))
                if bag == span and span > 2:
                    problems.append("entry %d: 大球數測試 (%d, %d) 的答案就是最大袋號" % (i, D, I))
                if bag == (I - 1) % span + 1 and span > 2:
                    problems.append("entry %d: 大球數測試 (%d, %d) 的答案等於化約後球號（不做反向也會對）" % (i, D, I))
                if span < MIN_BIG_SPAN:
                    problems.append("entry %d: 大球數測試 (%d, %d) 的週期 %d 太小，逐條非退化斷言會讓答案塌縮成小模數查表"
                                    % (i, D, I, span))
            if not any(I > BIG_I and (1 << (D - 1)) == (1 << (MAX_D - 1)) for D, I in cases):
                problems.append("entry %d: 沒有任何『大球數且週期＝全域最大』的測試，寫死小模數的誤解無法鑑別" % i)
        if nodes > COOPT_NODES_CAP:
            problems.append("entry %d: Σ2^(D−1) = %d > %d，收編路線 L1 的遞迴寫法會被誤殺" % (i, nodes, COOPT_NODES_CAP))
        if p1 > P1_OPS_CAP:
            problems.append("entry %d: 收編路線 P1 的 op 模型 %d > %d，會被誤殺" % (i, p1, P1_OPS_CAP))

    # 第 1 筆（＝題面範例）必須讓所有零洞察／誤解路線當場現形
    first = per_entry[0]
    for name in ("Z1_echo_I", "Z2_const1", "Z3_maxbag", "E1_noreverse", "E5_dlevels", "E4_parityflip"):
        if first[name + "_ok"]:
            problems.append("entry 1（題面範例）無法鑑別 %s" % name)

    for name, (op, cap) in CAPS.items():
        s = scores[name]
        if op == "eq" and s != cap:
            problems.append("route %s: 得分 %d，契約要求 == %d" % (name, s, cap))
        if op == "le" and s > cap:
            problems.append("route %s: 得分 %d，契約要求 <= %d" % (name, s, cap))

    naive_score = sum(1 for r in per_entry if r["entry"] < KILL_FROM)
    if naive_score != KILL_FROM - 1:
        problems.append("逐球模擬預期得分 %d，契約要求 %d" % (naive_score, KILL_FROM - 1))

    # 寫死模數族：任何固定模數 M 的化約都不得拿滿分
    period_family = {}
    for M in [1 << k for k in range(1, 20)]:
        r = S.fixed_period_route(M)
        sc = sum(1 for i, cases in enumerate(ENTRIES, 1)
                 if r(S.render_input(cases)) == S.render_expected(cases))
        period_family[M] = sc
        # M 若是所有大球數測試週期的公倍數，這條路線在數學上就是正確的（過度化約無害），
        # 不算誤解；只有「M 小於某個大球數測試的週期」時才必須被鑑別出來。
        # 豁免門檻取自**值域**（2^(MAX_D−1)）而非出貨資料：只有大到涵蓋全域週期的 M
        # 才是數學上正確的過度化約；用出貨資料當門檻會把「剛好夠用」的錯誤模數放行（R2-2）
        if M < (1 << (MAX_D - 1)) and sc >= 20:
            problems.append("固定模數 M=%d 小於值域最大週期 %d 卻得 %d/20，無法鑑別"
                            % (M, 1 << (MAX_D - 1), sc))

    flat = [(D, I) for cs in ENTRIES for (D, I) in cs]
    if not any(D == 2 for D, _ in flat):
        problems.append("缺 D=2 邊界")
    if not any(I == 1 for _, I in flat):
        problems.append("缺 I=1 邊界")
    if not any(I == (1 << (D - 1)) for D, I in flat):
        problems.append("缺 I=2^(D-1) 邊界")
    if not any(I > (1 << (D - 1)) for D, I in flat):
        problems.append("缺「球數超過袋數」邊界")
    if not any(D == MAX_D for D, _ in flat):
        problems.append("缺 D=%d 邊界" % MAX_D)

    report = {
        "max_I": MAX_I,
        "pass_step_cap": PASS_STEP_CAP,
        "kill_ball_min": KILL_BALL_MIN,
        "kill_step_max": KILL_STEP_MAX,
        "coopt_nodes_cap": COOPT_NODES_CAP,
        "p1_ops_cap": P1_OPS_CAP,
        "fixed_period_family": period_family,
        "max_entry_bytes": max(r["bytes"] for r in per_entry),
        "naive_expected_score": naive_score,
        "pass_band_max_steps": max(r["total_steps"] for r in per_entry[:KILL_FROM - 1]),
        "kill_band_min_balls": min(r["total_balls"] for r in per_entry[KILL_FROM - 1:]),
        "kill_band_max_steps": max(r["total_steps"] for r in per_entry[KILL_FROM - 1:]),
        "coopt_nodes_max": max(r["coopt_nodes"] for r in per_entry),
        "p1_ops_max": max(r["p1_ops_model"] for r in per_entry),
        "scores": scores,
        "caps": {k: list(v) for k, v in CAPS.items()},
        "per_entry": per_entry,
        "problems": problems,
    }

    if write and not problems:
        os.makedirs(LIT_DIR, exist_ok=True)
        for i, cases in enumerate(ENTRIES, 1):
            with open(os.path.join(LIT_DIR, "c014_%02d.txt" % i), "w") as fh:
                fh.write(S.render_input(cases))
            with open(os.path.join(LIT_DIR, "c014_%02d.exp" % i), "w") as fh:
                fh.write(S.render_expected(cases))
        with open(os.path.join(HERE, "report014.json"), "w") as fh:
            json.dump(report, fh, indent=1, ensure_ascii=False)

    print(json.dumps({k: report[k] for k in
                      ("max_entry_bytes", "naive_expected_score", "pass_band_max_steps",
                       "kill_band_min_balls", "kill_band_max_steps", "coopt_nodes_max", "p1_ops_max", "scores")},
                     ensure_ascii=False, indent=1))
    if problems:
        print("\n斷言牆失敗：")
        for p in problems:
            print("  -", p)
        return 1
    print("\n斷言牆全數通過。")
    return 0


if __name__ == "__main__":
    sys.exit(main(write="--check" not in sys.argv))
