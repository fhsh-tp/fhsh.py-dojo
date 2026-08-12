#!/usr/bin/env python3
"""Regenerate challenges.json — the per-challenge inventory the sweep is planned from.

Run from the repo root:  python3 openspec/changes/add-judge-deadline/measure/inventory.py

The first version of challenges.json was produced ad hoc and never committed as a
script, and it recorded `count` as the NUMBER OF testcase_plan ENTRIES rather than
the number of testcases. Every one of the nine plan-bearing challenges was wrong
(gem-blast-playtest 8 instead of 20, prize-order-code 9 instead of 20, and so on).
Nothing downstream consumed the field, so no measurement was affected — but a
committed evidence file carrying wrong numbers is exactly the failure this change's
RCA is about, so the derivation now lives here where it can be re-run and diffed.

`count` mirrors planTotal() in .vitepress/theme/composables/useChallengeRunner.ts:
a literal entry contributes one testcase, a band entry contributes its `count`.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).parent / 'challenges.json'
DEFAULT_TESTCASE_COUNT = 5  # docs/../Usage.md: testcase_count defaults to 5


def frontmatter(path):
    return path.read_text().split('---', 2)[1]


def plan_entries(fm):
    """(kind, value) per top-level testcase_plan entry, or None when no plan."""
    m = re.search(r'^testcase_plan:\s*$(.*?)^(?=\w)', fm, re.S | re.M)
    if not m:
        return None
    return re.findall(r'^  - (literal|count):?\s*(.*)$', m.group(1), re.M)


def inventory():
    rows = []
    for md in sorted((ROOT / 'docs' / 'challenge').glob('*.md')):
        fm = frontmatter(md)
        entries = plan_entries(fm)
        if entries is None:
            tc = re.search(r'^testcase_count:\s*(\d+)', fm, re.M)
            count = int(tc.group(1)) if tc else DEFAULT_TESTCASE_COUNT
        else:
            count = sum(1 if kind == 'literal' else int(val) for kind, val in entries)
        rows.append({
            'slug': md.stem,
            'id': re.search(r'^id:\s*(\S+)', fm, re.M).group(1),
            'has_ref': bool(re.search(r'^reference_solution:', fm, re.M)),
            'has_plan': entries is not None,
            'count': count,
        })
    return rows


if __name__ == '__main__':
    rows = inventory()
    OUT.write_text(json.dumps(rows, indent=1, ensure_ascii=False) + '\n')
    planned = sum(1 for r in rows if r['has_plan'])
    print(f'{OUT.name}: {len(rows)} challenges, {planned} with a testcase_plan, '
          f'{sum(1 for r in rows if r["has_ref"])} with a reference_solution')
