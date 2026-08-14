#!/usr/bin/env python3
"""Score a candidate submission against a challenge's 20 shipped literal entries.

usage: score.py <slug> <candidate.py>
Prints per-entry OK/NG and the total, comparing against the challenge's own
reference_solution. Correctness only — wall clock and op limit are the browser's job.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path('/Users/phoenix/dev/fhsh-projects/fhsh.py-dojo')


def frontmatter(slug):
    return (ROOT / 'docs' / 'challenge' / f'{slug}.md').read_text().split('---', 2)[1]


def literals(fm):
    out, lines, i = [], fm.split('\n'), 0
    while i < len(lines):
        if re.match(r'\s*- literal: \|\s*$', lines[i]):
            indent = len(lines[i]) - len(lines[i].lstrip())
            raw, i = [], i + 1
            while i < len(lines):
                cur = lines[i]
                if cur.strip() and (len(cur) - len(cur.lstrip())) <= indent:
                    break
                raw.append(cur)
                i += 1
            # block-scalar indentation comes from the first non-empty line
            bi = min((len(l) - len(l.lstrip()) for l in raw if l.strip()), default=indent + 2)
            out.append('\n'.join(l[bi:] if len(l) > bi else '' for l in raw).rstrip('\n') + '\n')
            continue
        i += 1
    return out


def reference(fm):
    m = re.search(r'^reference_solution: \|\n(.*?)(?=^\S)', fm, re.S | re.M)
    body = m.group(1)
    ind = min(len(l) - len(l.lstrip()) for l in body.split('\n') if l.strip())
    return '\n'.join(l[ind:] for l in body.split('\n'))


def run(code, stdin):
    p = subprocess.run([sys.executable, '-c', code], input=stdin,
                       capture_output=True, text=True, timeout=900)
    return f'<ERR> {p.stderr.strip().splitlines()[-1]}' if p.returncode else p.stdout.rstrip('\n')


slug, cand = sys.argv[1], sys.argv[2]
fm = frontmatter(slug)
entries = literals(fm)
assert len(entries) == 20, f'parsed {len(entries)} entries'
ref = reference(fm)
code = Path(cand).read_text()
marks = []
for e in entries:
    marks.append('A' if run(ref, e) == run(code, e) else 'W')
print(''.join(marks), sum(1 for m in marks if m == 'A'), '/20', Path(cand).name)
