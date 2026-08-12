#!/bin/zsh
# Measure every shipped reference solution plus the recorded bypass routes.
# Appends one JSON line per run to measure/results.jsonl.
# Requires `pnpm preview:cf` on :8788 — see measure.sh for why dev is not usable.
set -u
HERE=${0:A:h}
OUT=$HERE/results.jsonl
: > $OUT

run() {  # run <slug> <solution> <label>
  print -u2 -- "[sweep] $3"
  $HERE/measure.sh "$1" "$2" "$3" >> $OUT
  local rc=$?
  [[ $rc -ne 0 ]] && print -u2 -- "[sweep] $3 FAILED (rc=$rc)"
  return 0
}

for f in $HERE/solutions/*.ref.py; do
  slug=${${f:t}%.ref.py}
  run "$slug" "$f" "${slug}:reference_solution"
done

for f in $HERE/routes/gemblast_*.py; do
  run "gem-blast-playtest" "$f" "gem-blast-playtest:${${f:t}%.py}"
done

print -u2 -- "[sweep] done — $(wc -l < $OUT) results"
