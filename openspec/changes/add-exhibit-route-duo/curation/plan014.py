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

MAX_I = 10_000_000             # 值域上限（題面同步）
PASS_STEP_CAP = 1_000_000      # 第 1–14 筆：最貴的逐球寫法（4.158 ops/step）也要能過
KILL_BALL_MIN = 20_000_000     # 第 15–20 筆：每球 1 op 的攤平寫法也要跳閘（2 倍餘裕）
KILL_STEP_MAX = 45_000_000     # 殺手筆的總下降步數上限（攤平寫法牆鐘 ≈ 6 秒／筆）
PERIOD_BALL_CAP = 100_000      # 殺手筆內「取週期後仍需模擬的球數」上限（保護收編路線）
LEVELWISE_OPS_CAP = 8_000_000  # 收編路線每筆 op 上限，模型取**最貴**寫法 5 ops/內圈

ENTRIES = [
    # 第 1–14 筆：逐球模擬可過（球數小）
    [(4, 1), (4, 2), (4, 3), (4, 8), (4, 11)],              # 頁面範例（含球數 > 袋數）
    [(2, 1), (2, 2), (3, 1), (3, 4), (5, 16), (4, 2), (2, 7), (3, 10)],  # 邊界
    [(6, 32), (7, 10), (8, 100), (5, 33)],
    [(10, 300), (9, 256), (12, 50), (3, 999)],
    [(14, 1000), (11, 777), (13, 2048), (2, 12345)],
    [(16, 5000), (15, 3000), (6, 40000)],
    [(18, 20000), (17, 15000), (4, 30000)],
    [(20, 30000), (19, 20000), (7, 10000)],
    [(20, 50000), (6, 20), (3, 20000)],
    [(20, 25000), (18, 25000), (5, 15000)],
    [(20, 50000), (3, 2), (8, 3000)],
    [(19, 54000), (2, 1), (9, 1500)],
    [(20, 45000), (16, 6000), (2, 49999)],
    [(20, 35000), (13, 15000), (4, 40000)],
    # 第 15–20 筆：球數大到任何逐球寫法都跳閘（小 D 控制牆鐘）
    [(2, 9_900_000), (3, 5_100_000), (4, 5_050_000), (6, 17), (20, 1234)],
    [(3, 7_300_000), (2, 8_800_000), (4, 4_400_000), (12, 4095), (5, 96)],
    [(4, 5_100_000), (2, 10_000_000), (3, 5_400_000), (20, 3000), (7, 1000)],
    [(2, 10_000_000), (4, 5_600_000), (3, 4_800_000), (9, 255), (14, 9000)],
    [(3, 6_600_000), (4, 6_050_000), (2, 8_100_000), (11, 700), (18, 65535)],
    [(4, 7_200_000), (3, 5_900_000), (2, 7_400_000), (16, 12345), (6, 31)],
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
}


def levelwise_ops(cases):
    """收編路線的 op 模型：最貴寫法（顯式 if/else）每次內圈 5 ops、共 2^(D−1) 次。"""
    return sum(5 * (1 << (D - 1)) for D, _ in cases)


def main(write=True):
    problems = []
    scores = {k: 0 for k in S.ROUTES}
    per_entry = []
    KILL_FROM = 15

    for i, cases in enumerate(ENTRIES, 1):
        text = S.render_input(cases)
        exp = S.render_expected(cases)
        st = sum(S.steps(D, I) for D, I in cases)
        bl = sum(S.balls(D, I) for D, I in cases)
        lw = levelwise_ops(cases)
        row = {
            "entry": i,
            "tests": [{"D": D, "I": I, "bag": S.bag_parity(D, I), "steps": S.steps(D, I)} for D, I in cases],
            "total_steps": st,
            "total_balls": bl,
            "levelwise_ops_model": lw,
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
            if not (2 <= D <= 20):
                problems.append("entry %d: D=%d 超出 2..20" % (i, D))
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
                problems.append("entry %d: 球數 %d < %d（每球 1 op 的攤平寫法可能存活）" % (i, bl, KILL_BALL_MIN))
            if st > KILL_STEP_MAX:
                problems.append("entry %d: steps %d > %d（陣亡提交會吃掉累計牆鐘預算）" % (i, st, KILL_STEP_MAX))
            worst_period = max(min(I, 1 << (D - 1)) for D, I in cases)
            if worst_period > PERIOD_BALL_CAP:
                problems.append("entry %d: 週期內球數 %d > %d，收編的『取週期再模擬』路線會被誤殺"
                                % (i, worst_period, PERIOD_BALL_CAP))
        if lw > LEVELWISE_OPS_CAP:
            problems.append("entry %d: 收編路線 op 模型 %d > %d" % (i, lw, LEVELWISE_OPS_CAP))

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

    flat = [(D, I) for cs in ENTRIES for (D, I) in cs]
    if not any(D == 2 for D, _ in flat):
        problems.append("缺 D=2 邊界")
    if not any(I == 1 for _, I in flat):
        problems.append("缺 I=1 邊界")
    if not any(I == (1 << (D - 1)) for D, I in flat):
        problems.append("缺 I=2^(D-1) 邊界")
    if not any(I > (1 << (D - 1)) for D, I in flat):
        problems.append("缺「球數超過袋數」邊界")
    if not any(D == 20 for D, _ in flat):
        problems.append("缺 D=20 邊界")

    report = {
        "max_I": MAX_I,
        "pass_step_cap": PASS_STEP_CAP,
        "kill_ball_min": KILL_BALL_MIN,
        "kill_step_max": KILL_STEP_MAX,
        "levelwise_ops_cap": LEVELWISE_OPS_CAP,
        "max_entry_bytes": max(r["bytes"] for r in per_entry),
        "naive_expected_score": naive_score,
        "pass_band_max_steps": max(r["total_steps"] for r in per_entry[:KILL_FROM - 1]),
        "kill_band_min_balls": min(r["total_balls"] for r in per_entry[KILL_FROM - 1:]),
        "kill_band_max_steps": max(r["total_steps"] for r in per_entry[KILL_FROM - 1:]),
        "levelwise_ops_max": max(r["levelwise_ops_model"] for r in per_entry),
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
                       "kill_band_min_balls", "kill_band_max_steps", "levelwise_ops_max", "scores")},
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
