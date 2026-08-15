"""通用 meta 檢查：``measure/`` **頂層**的每一份量測 json，必須帶一個 ``problems`` 陣列。

掃描範圍刻意寫成頂層而非遞迴，與實作的 glob 一致——2026-08-15 第四輪稽核指出
原本的 docstring 用「凡落在 measure/ 的」這種全稱語氣，承諾大於實作範圍。目前
子目錄底下沒有任何 json，但若日後有人把量測輸出放進子目錄，它會靜默逃過這支檢查。

為什麼要這一支：本 change 的量測腳本有兩種體質——像 curation/plan015.py、
measure/measure016.py 那樣把契約寫成 ``problems`` 清單並以非零碼退出的；以及
像原本的 measure/routes017_measure.py 那樣**不論量到什麼都寫檔、印出、return 0** 的。
後者一旦出現，散文引用的數字就再也沒有任何一層會替它把關。

``problems`` 鍵因此是「這份 json 背後有斷言牆」的機械證據：缺鍵＝那支腳本沒有
契約檢查；鍵非空＝契約真的被違反了，該份 json 不可拿來引用。兩者都是 FAIL。

執行：
  python3 verify/check_measure_json.py            # 檢查 measure/*.json
  python3 verify/check_measure_json.py --self-test # 負向控制（含正向控制）
"""

import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MEASURE = os.path.join(os.path.dirname(HERE), "measure")


def audit(measure_dir):
    """回傳 (違規敘述清單, 檢查過的檔數)。"""
    bad, seen = [], 0
    for path in sorted(glob.glob(os.path.join(measure_dir, "*.json"))):
        name, seen = os.path.basename(path), seen + 1
        try:
            data = json.load(open(path, encoding="utf-8"))
        except (ValueError, OSError) as exc:
            bad.append("%s 無法解析：%s" % (name, exc))
            continue
        if not isinstance(data, dict) or "problems" not in data:
            bad.append("%s 缺少 problems 鍵（代表產生它的腳本沒有斷言牆）" % name)
        elif not isinstance(data["problems"], list):
            bad.append("%s 的 problems 不是陣列：%r" % (name, data["problems"]))
        elif data["problems"]:
            bad.append("%s 記錄了 %d 條違約：%s"
                       % (name, len(data["problems"]), data["problems"][0]))
    return bad, seen


def self_test():
    """負向控制：三種壞檔各造一份，確認都被抓；一份好檔確認不被誤殺。"""
    import tempfile

    fixtures = {
        "good.json": '{"problems": []}',
        "missing.json": '{"routes": []}',
        "wrongtype.json": '{"problems": "none"}',
        "nonempty.json": '{"problems": ["某條契約沒過"]}',
        "broken.json": "{not json",
    }
    expect = {"missing.json": "缺少 problems 鍵", "wrongtype.json": "不是陣列",
              "nonempty.json": "記錄了 1 條違約", "broken.json": "無法解析"}
    with tempfile.TemporaryDirectory() as tmp:
        for name, body in fixtures.items():
            with open(os.path.join(tmp, name), "w", encoding="utf-8") as fh:
                fh.write(body)
        bad, seen = audit(tmp)

    failures = []
    for name, frag in expect.items():
        hit = [b for b in bad if b.startswith(name) and frag in b]
        print("  %-16s %-6s %s" % (name, "FIRED" if hit else "MISS",
                                   hit[0] if hit else "（未觸發預期檢查）"))
        if not hit:
            failures.append("注入 %s 未觸發預期檢查（期望含 %r）" % (name, frag))
    stray = [b for b in bad if b.startswith("good.json")]
    print("  %-16s %-6s %s" % ("good.json", "PASS" if not stray else "FAIL",
                               "正向控制：合格檔未被誤殺" if not stray else stray[0]))
    if stray:
        failures.append("正向控制失敗：合格檔被誤判 —— %s" % stray[0])
    if seen != len(fixtures):
        failures.append("應檢查 %d 份檔案，實際 %d 份" % (len(fixtures), seen))

    if failures:
        print("\n負向控制失敗：")
        for f in failures:
            print("  -", f)
        return 1
    print("\n負向控制全數通過（%d 個注入點皆觸發，合格檔零誤判）。" % len(expect))
    return 0


def main():
    bad, seen = audit(MEASURE)
    print("檢查 measure/*.json：%d 份，違規 %d 份" % (seen, len(bad)))
    for b in bad:
        print("  FAIL", b)
    if bad:
        return 1
    print("全部量測 json 皆帶 problems 陣列且為空。")
    return 0


if __name__ == "__main__":
    raise SystemExit(self_test() if "--self-test" in sys.argv else main())
