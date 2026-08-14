#!/usr/bin/env python3
"""Check each co-opted route against the challenge's own shipped literals.

The route files for expression-eval-challenges were never committed (they lived
in an untracked design_b/), so they had to be rewritten from their spec names.
That is exactly the failure this change's RCA calls root cause 2, so nothing
gets measured in the browser until it has been shown to reproduce the challenge's
reference_solution byte-for-byte on all twenty shipped entries.

usage: verify_routes.py            (checks every pair below)
exit 0 only if every route matches on every entry.
"""
import io
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
ROUTES = Path(__file__).parent / 'routes'

PAIRS = [
    ('snack-bar-register', ['a011_e1_swapeval.py', 'a011_r2_regexparen.py', 'a011_n1_rewrite.py']),
    ('coupon-combo-quote', ['a012_e3_powencode.py']),
]


def frontmatter(slug):
    text = (ROOT / 'docs' / 'challenge' / f'{slug}.md').read_text()
    return text.split('---', 2)[1]


def literals(fm):
    """Every `- literal: |` block of the testcase_plan, in plan order."""
    out = []
    lines = fm.split('\n')
    i = 0
    while i < len(lines):
        if re.match(r'\s*- literal: \|\s*$', lines[i]):
            indent = len(lines[i]) - len(lines[i].lstrip())
            raw = []
            i += 1
            while i < len(lines):
                cur = lines[i]
                if cur.strip() and (len(cur) - len(cur.lstrip())) <= indent:
                    break
                raw.append(cur)
                i += 1
            # A YAML block scalar's own indentation is set by its first
            # non-empty line. Guessing it (indent + 2) left two spaces on every
            # expression, which only showed up because one route echoes its
            # input line back instead of re-splitting it.
            body_indent = min((len(l) - len(l.lstrip()) for l in raw if l.strip()),
                              default=indent + 2)
            body = [l[body_indent:] if len(l) > body_indent else '' for l in raw]
            out.append('\n'.join(body).rstrip('\n') + '\n')
            continue
        i += 1
    return out


def reference(fm):
    m = re.search(r'^reference_solution: \|\n(.*?)(?=^\S)', fm, re.S | re.M)
    if not m:
        raise SystemExit('reference_solution not found')
    body = m.group(1)
    indent = min(len(l) - len(l.lstrip()) for l in body.split('\n') if l.strip())
    return '\n'.join(l[indent:] for l in body.split('\n'))


def run(code, stdin):
    p = subprocess.run([sys.executable, '-c', code], input=stdin,
                       capture_output=True, text=True, timeout=600)
    if p.returncode != 0:
        return f'<ERROR> {p.stderr.strip().splitlines()[-1] if p.stderr.strip() else "no stderr"}'
    return p.stdout.rstrip('\n')


bad = 0
for slug, route_files in PAIRS:
    fm = frontmatter(slug)
    entries = literals(fm)
    ref = reference(fm)
    if len(entries) != 20:
        print(f'{slug}: expected 20 literal entries, parsed {len(entries)}')
        bad += 1
        continue
    expected = [run(ref, e) for e in entries]
    for rf in route_files:
        code = (ROUTES / rf).read_text()
        got = [run(code, e) for e in entries]
        ok = sum(1 for a, b in zip(expected, got) if a == b)
        mark = 'OK  ' if ok == 20 else 'FAIL'
        print(f'{mark} {slug:20s} {rf:26s} {ok}/20')
        if ok != 20:
            bad += 1
            for k, (a, b) in enumerate(zip(expected, got), 1):
                if a != b:
                    print(f'       entry {k}: expected {a[:70]!r} got {b[:70]!r}')

sys.exit(1 if bad else 0)
