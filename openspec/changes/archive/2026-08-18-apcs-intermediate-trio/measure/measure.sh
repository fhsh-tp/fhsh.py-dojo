#!/bin/zsh
# Submit one solution to one challenge and report the per-testcase wall clock.
#
# usage: measure.sh <slug> <solution.py> [label]
#
# Must run against `pnpm preview:cf` (Cloudflare's local runtime on :8788), not
# `vitepress dev`: only the former serves the cross-origin isolation headers, and
# without them SharedArrayBuffer is absent, the deadline stops interrupting, and
# every wall-clock number measured here would be the wrong quantity.
#
# Every step carries its own failure signal. An earlier revision of a script in
# this repo routed each command to /dev/null, which turned a call to a
# non-existent subcommand into a silent pass; the only visible output was the
# final score, and the score happened to be right. Nothing here is allowed to
# fail quietly.

set -u
BASE=${BASE:-http://localhost:8788}
export AGENT_BROWSER_SESSION=${AGENT_BROWSER_SESSION:-jd-measure}

SLUG=${1:?usage: measure.sh <slug> <solution.py> [label]}
SOL=${2:?usage: measure.sh <slug> <solution.py> [label]}
LABEL=${3:-$SLUG}

fail() { print -r -- "{\"label\":\"$LABEL\",\"slug\":\"$SLUG\",\"status\":\"FAILED\",\"reason\":\"$1\"}"; exit 1 }

[[ -r $SOL ]] || fail "solution file not readable: $SOL"

agent-browser open "$BASE/challenge/$SLUG" >/dev/null || fail "open failed"

# Wait for the editor to exist rather than sleeping a fixed amount: Pyodide
# warm-up dominates and varies by an order of magnitude between cold and warm.
for _ in {1..60}; do
  READY=$(agent-browser eval "!!document.querySelector('.cm-content')" 2>&1) || fail "eval(ready) failed: $READY"
  [[ $READY == *true* ]] && break
  sleep 1
done
[[ $READY == *true* ]] || fail "editor never appeared"

# The editor mounting is NOT sufficient: on a cold page the submit button lands
# in the accessibility tree noticeably later, and the previous revision of this
# script read the snapshot immediately after `.cm-content` appeared and died
# with "submit button ref not found" on a page that was in fact fine. Poll the
# snapshot for the button itself instead of assuming the editor implies it.
for _ in {1..60}; do
  SNAP=$(agent-browser snapshot 2>&1) || fail "snapshot failed"
  BTN=$(print -r -- "$SNAP" | grep "提交" | head -1 | grep -oE "e[0-9]+" | head -1)
  [[ -n ${BTN:-} ]] && break
  sleep 1
done
TB=$(print -r -- "$SNAP" | grep -i "textbox" | head -1 | grep -oE "e[0-9]+" | head -1)
[[ -n ${TB:-} ]] || fail "editor ref not found"
[[ -n ${BTN:-} ]] || fail "submit button never entered the accessibility tree within 60s"

agent-browser click "$TB" >/dev/null || fail "click(editor) failed"
agent-browser press "Meta+a" >/dev/null || fail "select-all failed"
agent-browser keyboard inserttext "$(cat "$SOL")" >/dev/null || fail "inserttext failed"
agent-browser press "Escape" >/dev/null || fail "escape failed"

# Confirm the editor really holds our code. Two of this project's challenges
# ship an empty starter_code, so a no-op paste is byte-identical to a working
# one — the failure would be invisible without this check.
LEN=$(agent-browser eval "document.querySelector('.cm-content').innerText.length" 2>&1) || fail "eval(len) failed"
LEN=$(print -r -- "$LEN" | grep -oE "[0-9]+" | head -1)
[[ ${LEN:-0} -gt 10 ]] || fail "editor is empty after paste (len=${LEN:-0})"

agent-browser click "$BTN" >/dev/null || fail "click(submit) failed"

READ_ROWS='JSON.stringify({done: !!document.body.innerText.match(/結果：/),
  rows: Array.from(document.querySelectorAll("[data-testid=\"result-panel\"] tbody tr")).map(function(tr){
    return {v: tr.dataset.verdict || "", ms: (tr.children[2] ? tr.children[2].textContent.trim() : "")}
  })})'

# The eval transport returns the stringified payload re-quoted, so the quotes
# arrive escaped. Matching on a literal `"done":true` silently never fires —
# the run finishes, the poll keeps spinning, and the only symptom is a timeout
# that looks like the page hung. Match tolerantly and let Python do the real
# parsing.
finished() { print -r -- "$1" | grep -qE '\\?"done\\?":true' }

for _ in {1..150}; do
  sleep 2
  OUT=$(agent-browser eval "$READ_ROWS" 2>&1) || fail "eval(rows) failed: $OUT"
  finished "$OUT" && break
done
finished "$OUT" || fail "run did not finish within 300s (last payload: ${OUT:0:200})"

print -r -- "$OUT" | LABEL=$LABEL SLUG=$SLUG python3 -c '
import sys, os, json, re

raw = sys.stdin.read().strip()

def parse(text):
    """The transport may hand back the payload, or the payload re-quoted as a
    JSON string. Unwrap until an object appears rather than guessing."""
    for _ in range(3):
        try:
            v = json.loads(text)
        except Exception:
            return None
        if isinstance(v, dict):
            return v
        if isinstance(v, str):
            text = v
            continue
        return None
    return None

d = parse(raw)
if d is not None and not d.get("rows"):
    print(json.dumps({"label": os.environ["LABEL"], "slug": os.environ["SLUG"],
                      "status": "FAILED",
                      "reason": "result panel matched zero rows — selector is wrong"},
                     ensure_ascii=False))
    sys.exit(1)
if d is None:
    print(json.dumps({"label": os.environ["LABEL"], "slug": os.environ["SLUG"],
                      "status": "FAILED", "reason": "unparseable payload",
                      "raw": raw[:300]}, ensure_ascii=False))
    sys.exit(1)

rows = d.get("rows", [])
def ms(x):
    n = re.search(r"[0-9.]+", x or "")
    return float(n.group(0)) if n else None
vals = [v for v in (ms(r.get("ms")) for r in rows) if v is not None]
verdicts = [r.get("v", "") for r in rows]
print(json.dumps({
    "label": os.environ["LABEL"], "slug": os.environ["SLUG"], "status": "OK",
    "rows": len(rows),
    "score": sum(1 for v in verdicts if v == "AC"),
    "verdicts": "".join({"AC": "A", "WA": "W", "TLE": "T", "RE": "R", "none": "-", "": "?"}.get(v, "?") for v in verdicts),
    "max_ms": max(vals) if vals else None,
    "sum_ms": round(sum(vals)) if vals else None,
    "per_ms": vals,
}, ensure_ascii=False))
'
