import sys

data = sys.stdin.read().split()
ptr = 0
T = int(data[ptr]); ptr += 1
answers = []
for _ in range(T):
    mode = int(data[ptr]); n = int(data[ptr + 1]); ptr += 2
    first = data[ptr:ptr + n]; ptr += n
    second = data[ptr:ptr + n]; ptr += n

    if mode == 1:
        seq_a, seq_b = first, second
        where = {v: i for i, v in enumerate(seq_b)}

        def to_c(a_lo, b_lo, size):
            if size == 0:
                return []
            room = seq_a[a_lo]
            k = where[room] - b_lo
            return (to_c(a_lo + 1, b_lo, k)
                    + to_c(a_lo + 1 + k, b_lo + k + 1, size - k - 1)
                    + [room])

        answers.append(" ".join(to_c(0, 0, n)))
    else:
        seq_b, seq_c = first, second
        where = {v: i for i, v in enumerate(seq_b)}

        def to_a(c_hi, b_lo, size):
            if size == 0:
                return []
            room = seq_c[c_hi]
            k = where[room] - b_lo
            return ([room]
                    + to_a(c_hi - 1 - (size - k - 1), b_lo, k)
                    + to_a(c_hi - 1, b_lo + k + 1, size - k - 1))

        answers.append(" ".join(to_a(n - 1, 0, n)))
print("\n".join(answers))
