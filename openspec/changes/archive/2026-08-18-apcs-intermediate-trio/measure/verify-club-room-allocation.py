"""Local verification harness for club-room-allocation (apcs019).

Inputs come from the REAL Rust/WASM engine via gen-plan-inputs-club-room-allocation.mts (same path the
shipped pool build uses), so nothing here re-implements input generation.

Checks, all as hard assertions:
  1. generator output == reference_solution output, entry by entry
  2. every entry's actual byte length < input_budget
  3. both spellings of the killed route measured with a settrace counter that
     matches worker-utils.ts's tracer semantics (every trace event counts one)
  4. entries 2..20 non-decreasing in N
  5. the measured minimum room count of the largest entry
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
# gen-plan-inputs-club-room-allocation.mts writes inputs.json next to itself:
#   npx --no-install tsx <HERE>/gen-plan-inputs-club-room-allocation.mts \
#       docs/challenge/club-room-allocation.md <HERE>/inputs.json
OP_LIMIT = 10_000_000

# inputs.json is a ~10 MB regenerated artifact — keep it out of the repo.
INPUTS = os.environ.get('CLIFF_INPUTS', os.path.join(HERE, 'inputs.json'))
data = json.load(open(INPUTS, encoding='utf-8'))
BUDGET = data['inputBudget']
entries = data['blocks'][0]
assert len(entries) == 20, len(entries)


# ── 1 & 2: generator vs reference_solution, and byte sizes ────────────────
def run_py(code, stdin):
    p = subprocess.run([sys.executable, '-c', code], input=stdin, timeout=120,
                       capture_output=True, text=True)
    assert p.returncode == 0, p.stderr[-2000:]
    return p.stdout


agree = []
sizes = []
for i, inp in enumerate(entries):
    g = run_py(data['generator'], inp)
    r = run_py(data['reference_solution'], inp)
    agree.append(g == r)
    sizes.append(len(inp.encode('utf-8')))
    assert g == r, f'entry {i + 1}: generator != reference_solution'
    assert sizes[-1] < BUDGET, f'entry {i + 1}: {sizes[-1]} bytes >= budget {BUDGET}'

AGREE_OK = all(agree)


# ── 5: N per entry, monotonicity ──────────────────────────────────────────
def n_of(inp):
    return int(inp.split('\n', 1)[0])


ns = [n_of(e) for e in entries]
tail = ns[1:]
MONO_OK = all(b >= a for a, b in zip(tail, tail[1:]))
assert MONO_OK, tail


# ── the two spellings of the killed route ─────────────────────────────────
def parse(inp):
    tok = inp.split()
    n = int(tok[0])
    return n, [int(v) for v in tok[1:1 + n]], [int(v) for v in tok[1 + n:1 + 2 * n]]


def brute_loop(inp):
    """Killed route, expanded loop spelling: for every application, scan all
    earlier ones and test each for time overlap."""
    n, starts, durations = parse(inp)
    order = sorted(range(n), key=lambda i: (starts[i], i))
    s = [starts[i] for i in order]
    end = [starts[i] + durations[i] for i in order]
    room = [0] * n
    out = [0] * n
    for i in range(n):
        occupied = set()
        for j in range(i):
            if end[j] > s[i]:
                occupied.add(room[j])
        r = 1
        while r in occupied:
            r += 1
        room[i] = r
        out[order[i]] = r
    return max(room) if n else 0, out


def brute_comp(inp):
    """Same route, cheapest spelling: the scan is a set comprehension, so the
    per-pair work runs one counted event instead of two."""
    n, starts, durations = parse(inp)
    order = sorted(range(n), key=lambda i: (starts[i], i))
    s = [starts[i] for i in order]
    end = [starts[i] + durations[i] for i in order]
    room = [0] * n
    out = [0] * n
    for i in range(n):
        occupied = {room[j] for j in range(i) if end[j] > s[i]}
        r = 1
        while r in occupied:
            r += 1
        room[i] = r
        out[order[i]] = r
    return max(room) if n else 0, out


def count_ops(fn, arg):
    """Same semantics as .vitepress/theme/workers/worker-utils.ts: a tracer
    that returns itself and adds one on every trace event."""
    box = [0]

    def tracer(frame, event, arg_):
        box[0] += 1
        return tracer

    sys.settrace(tracer)
    sys._getframe().f_trace = tracer
    try:
        res = fn(arg)
    finally:
        sys.settrace(None)
    return box[0], res


spellings = []
for name, fn in (('expanded loop', brute_loop), ('set comprehension', brute_comp)):
    ops = []
    for i, inp in enumerate(entries):
        c, _ = count_ops(fn, inp)
        ops.append(c)
    dead = [i + 1 for i, c in enumerate(ops) if c > OP_LIMIT]
    assert dead, f'{name}: no entry exceeds the operation limit'
    assert len(dead) < 20, f'{name}: every entry exceeds the operation limit'
    assert dead == list(range(dead[0], 21)), f'{name}: dead entries are not a contiguous tail: {dead}'
    spellings.append({
        'name': name,
        'ops': ops,
        'deadEntries': dead,
        'score': f'{20 - len(dead)}/20',
        'opsLastEntry': ops[-1],
    })

# ── correctness of the brute routes against the generator, plus the room
#    count that the challenge text's scale claim rests on ─────────────────
rooms = []
for inp in entries:
    k, alloc = brute_loop(inp)
    rooms.append(k)
    expected = run_py(data['generator'], inp).split('\n')
    assert int(expected[0]) == k, 'brute route disagrees with generator on room count'
    assert expected[1].split() == [str(v) for v in alloc], 'brute route disagrees on allocation'

report = {
    'slug': data['slug'],
    'id': 'apcs019',
    'inputBudget': BUDGET,
    'engineWorstCaseBytes': 54004,
    'maxActualInputBytes': max(sizes),
    'perEntryBytes': sizes,
    'perEntryN': ns,
    'perEntryRooms': rooms,
    'generatorReferenceAgree': AGREE_OK,
    'monotonic': MONO_OK,
    'opLimit': OP_LIMIT,
    'spellings': spellings,
    'note': (
        'Inputs generated by the shipped Rust/WASM engine (seed = slug, '
        'pool block 0 of 10). Operation counts use a sys.settrace counter with '
        'the same semantics as worker-utils.ts. Scores are local projections '
        'from the operation limit alone; the browser measurement on the '
        'production judging path is the authority.'
    ),
}

out_path = os.path.join(REPO, 'openspec/changes/apcs-intermediate-trio/measure',
                        'cliff-club-room-allocation.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
    f.write('\n')

print('agreement (generator == reference_solution) all 20:', AGREE_OK)
print('monotonic N over entries 2..20:', MONO_OK)
print('input_budget:', BUDGET, ' engine worst-case:', 54004,
      ' max actual bytes:', max(sizes))
print()
print(f'{"#":>3} {"N":>6} {"bytes":>7} {"rooms":>6} {"loop ops":>12} {"comp ops":>12}')
for i in range(20):
    print(f'{i + 1:>3} {ns[i]:>6} {sizes[i]:>7} {rooms[i]:>6} '
          f'{spellings[0]["ops"][i]:>12,} {spellings[1]["ops"][i]:>12,}')
print()
for sp in spellings:
    print(f'{sp["name"]:>18}: dead entries {sp["deadEntries"]} -> {sp["score"]}, '
          f'entry 20 ops {sp["opsLastEntry"]:,}')
print()
print('rooms at largest entry (N=%d): %d' % (ns[-1], rooms[-1]))
print('wrote', out_path)
