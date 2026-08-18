"""判題器 op 計數器的忠實複刻——本 change 唯一允許的 op 量測來源。

為什麼要有這個檔：2026-08-15 的交叉檢查發現三個策展代理對「一個 op 是
什麼」給出互相矛盾的定義。其中一份探針同時過濾了 `event == "line"` 與
檔名，對熱路徑帶函式呼叫的寫法會系統性低估。逐份修補只會讓同型錯誤在
下一輪重新長回來，所以改成「只有一份實作，其他人一律 import」。

判題器真身在 .vitepress/theme/workers/worker-utils.ts 的 opGuard：

    def _tracer(frame, event, arg):
        global _op_count
        _op_count += 1
        if _op_count > _op_limit:
            raise TimeoutError(...)
        return _tracer

    sys.settrace(_tracer)
    sys._getframe().f_trace = _tracer

三個關鍵性質，任何複刻都必須同時具備：

1. **不過濾 event 型別。** call、line、return、exception 全部計入。只數
   line 事件會漏掉每次函式呼叫的 call 與 return，兩個事件。
2. **不過濾檔名。** 被呼叫的函式即使定義在別處也照算。
3. **`return _tracer`。** 這讓 tracer 對被呼叫的 frame 繼續生效；回傳
   None 會讓巢狀呼叫完全不被追蹤。

op 數與執行速度無關，只與 bytecode 執行路徑有關。Pyodide 跑的是同一份
CPython bytecode，因此本機量到的 op 數會原封不動搬到瀏覽器——這是本
change 唯一「不需要瀏覽器覆核」的量測軸，牆鐘則完全不是。
"""

import os
import sys

#: 判題器對每筆測資套用的預設 op 上限。
#: 出處 .vitepress/theme/__tests__/pyodide-worker-run-only.spec.ts 的
#: DEFAULT_OP_LIMIT = 10_000_000。
OP_LIMIT = 10_000_000


def count_ops(fn):
    """回傳 ``fn()`` 執行期間判題器會數到的 op 數。

    計數涵蓋 ``fn`` 內部的一切，包含它呼叫的其他函式。回傳值不含
    ``count_ops`` 自身的框架開銷以外的量測外殼——呼叫端若要跟「整支
    提交程式」的數字對齊，請用 :func:`count_ops_source`。
    """
    n_ops = 0

    def tracer(frame, event, arg):
        nonlocal n_ops
        n_ops += 1
        return tracer

    sys.settrace(tracer)
    sys._getframe().f_trace = tracer
    try:
        fn()
    finally:
        sys.settrace(None)
    return n_ops


def count_ops_source(source, stdin_text, filename="route"):
    """在 stdin 餵入 ``stdin_text`` 的情況下執行整份 ``source``，回傳 op 數。

    這條路徑跟判題器最接近：判題器包住的是**整支使用者程式**，不是
    某個函式。路線檔的得分與 op 數一律用這個函式量，不要用
    :func:`count_ops` 包一個函式後再自行加上外殼估計值。

    回傳 ``(ops, stdout_text)``。程式若拋出例外，例外會原樣往外傳，
    呼叫端自行決定那算 runtime error 還是別的處置。
    """
    import io

    code = compile(source, filename, "exec")
    old_stdin, old_stdout = sys.stdin, sys.stdout
    sys.stdin = io.StringIO(stdin_text)
    sys.stdout = buf = io.StringIO()

    n_ops = 0

    def tracer(frame, event, arg):
        nonlocal n_ops
        n_ops += 1
        return tracer

    try:
        sys.settrace(tracer)
        sys._getframe().f_trace = tracer
        try:
            exec(code, {"__name__": "__main__"})
        finally:
            sys.settrace(None)
    finally:
        sys.stdin, sys.stdout = old_stdin, old_stdout
    return n_ops, buf.getvalue()


def count_ops_source_fresh(path, stdin_text, timeout=None):
    """在**全新的直譯器行程**中量 ``path`` 這支程式的 op 數。

    為什麼需要這個：:func:`count_ops_source` 是行內量測，同一個行程裡
    第二次執行同一支程式會少掉模組首次匯入的成本。實測 ``import math``
    在冷行程首次執行時，importlib 的 Python 層會被 tracer 數到 **278 個
    事件**；同一支路線因此在行內量測得 98,421、在新行程量測得 98,699。

    判題器兩種情境都會發生：worker 內第一筆測資是冷的（使用者程式的
    import 發生在 tracer 裝上之後，會被計入），第二筆以後同一個 worker
    已經暖了。op 上限是逐筆套用的，所以**冷數字才是上界**。

    本 change 的規約：任何要寫進文件的 op 數一律取冷數字。行內量測只
    用於同一支程式內部的相對比較，且必須在該處註明。

    回傳 ``(ops, stdout_text, returncode)``。逾時回傳 ``(None, "", None)``。
    """
    import json
    import subprocess
    import sys as _s

    here = os.path.dirname(os.path.abspath(__file__))
    runner = (
        "import sys, json\n"
        f"sys.path.insert(0, {here!r})\n"
        "from judge_ops import count_ops_source\n"
        "src = open(sys.argv[1], encoding='utf-8').read()\n"
        "stdin_text = sys.stdin.read()\n"
        "ops, out = count_ops_source(src, stdin_text, filename=sys.argv[2])\n"
        "sys.stderr.write(json.dumps({'ops': ops, 'out': out}))\n"
    )
    try:
        proc = subprocess.run(
            [_s.executable, "-c", runner, path, os.path.basename(path)],
            input=stdin_text,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return None, "", None
    try:
        payload = json.loads(proc.stderr)
    except ValueError:
        return None, proc.stdout, proc.returncode
    return payload["ops"], payload["out"], proc.returncode


def self_test():
    """證明這份複刻確實會數到函式呼叫的 call 與 return 事件。

    若某份探針過濾了 event 型別或檔名，下面兩個數字會相等或極接近；
    忠實複刻則會看到帶函式呼叫的版本明顯較貴。
    """

    N = 2000

    def inline():
        total = 0
        for i in range(N):
            total += i * 2
        return total

    def via_helper():
        def double(x):
            return x * 2

        total = 0
        for i in range(N):
            total += double(i)
        return total

    a, b = count_ops(inline), count_ops(via_helper)
    assert inline() == via_helper(), "兩種寫法的答案必須相同"
    assert b > a * 1.8, (
        f"忠實複刻應看到函式呼叫版明顯較貴，實測 inline={a} helper={b}。"
        "若兩者接近，表示 tracer 沒有計入 call/return，複刻是錯的。"
    )
    return a, b


if __name__ == "__main__":
    a, b = self_test()
    print(f"self_test 通過：inline={a:,} ops、helper={b:,} ops（比值 {b / a:.2f}）")
    print(f"OP_LIMIT = {OP_LIMIT:,}")
