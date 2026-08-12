import sys

def to_rpn(toks):
    # 加減優先序 2（右結合）、乘除 1（左結合）、括弧覆寫
    prec = {"+": 2, "-": 2, "*": 1, "/": 1}
    right = {"+", "-"}
    out, st = [], []
    for tk in toks:
        if tk == "(":
            st.append(tk)
        elif tk == ")":
            while st[-1] != "(":
                out.append(st.pop())
            st.pop()
        elif tk in prec:
            while st and st[-1] != "(" and (
                prec[st[-1]] > prec[tk]
                or (prec[st[-1]] == prec[tk] and tk not in right)
            ):
                out.append(st.pop())
            st.append(tk)
        else:
            out.append(int(tk))
    while st:
        out.append(st.pop())
    return out

def run_rpn(rpn):
    st = []
    for tk in rpn:
        if isinstance(tk, int):
            st.append(tk)
        else:
            b = st.pop(); a = st.pop()
            if tk == "+": st.append(a + b)
            elif tk == "-": st.append(a - b)
            elif tk == "*": st.append(a * b)
            else:
                assert b > 0 and a % b == 0
                st.append(a // b)
    return st[0]

data = sys.stdin.read().split("\n")
t = int(data[0])
print("\n".join(str(run_rpn(to_rpn(data[i].split()))) for i in range(1, t + 1)))
