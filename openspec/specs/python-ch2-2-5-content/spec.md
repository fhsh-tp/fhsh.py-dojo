# python-ch2-2-5-content Specification

## Purpose

Defines requirements for section 2-5 of the Python tutorial — the Module 2 summary section. This section contains no new code content or Judge challenges; it provides a knowledge map (Mermaid mindmap), a self-check skill checklist, a Module 3 preview, and 2 AI image placeholders. It closes the loop on Module 2 (迴圈與重複結構) and transitions students into Module 3.

## Requirements

### Requirement: Section 2-5 file exists with correct frontmatter as module summary

The file `docs/tutor/py/ch2/2-5.md` SHALL exist with frontmatter fields: `layout: doc`, `title` (display title for the module 2 summary), `description` (one-line summary), `chapter: 2`, `section: "2-5"`, `createdTime` in ISO 8601 with `+08:00` timezone. The `challenge` field SHALL NOT be present (summary sections have no primary challenge).

The file SHALL include a `VISUAL-STYLE-PREFIX` HTML comment immediately after the frontmatter, consistent with other Chapter 2 sections.

#### Scenario: Summary file has valid frontmatter without challenge field

- **WHEN** VitePress builds the site
- **THEN** `docs/tutor/py/ch2/2-5.md` SHALL be parsed successfully with required fields present, and `challenge` field SHALL NOT exist


<!-- @trace
source: write-ch2-completion
updated: 2026-04-13
code:
  - docs/challenge/even-countdown.md
  - docs/public/assets/tutor/py/ch2/圖十三.png
  - docs/challenge/pair-count.md
  - docs/public/assets/tutor/py/ch2/圖二.png
  - docs/public/assets/tutor/py/ch2/圖四.png
  - docs/public/assets/tutor/py/ch2/圖一.png
  - docs/challenge/number-pyramid.md
  - docs/public/assets/tutor/py/ch2/圖五.png
  - docs/challenge/inverted-triangle.md
  - docs/challenge/isosceles-triangle.md
  - docs/tutor/py/ch2/appendix.md
  - docs/challenge/star-diamond.md
  - docs/tutor/py/ch2/reference.md
  - docs/challenge/digital-root.md
  - docs/public/assets/tutor/py/ch2/圖三.png
  - docs/public/assets/tutor/py/ch2/圖十二.png
  - docs/challenge/number-staircase.md
  - docs/tutor/py/ch2/2-4.md
  - docs/tutor/py/ch2/index.md
  - docs/challenge/prime-check.md
  - docs/public/assets/tutor/py/ch2/圖十一.png
  - docs/public/assets/tutor/py/ch2/圖九.png
  - docs/public/assets/tutor/py/ch2/圖八.png
  - docs/challenge/guess-number-simple.md
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/perfect-numbers-range.md
  - docs/challenge/star-rectangle.md
  - docs/challenge/gcd-euclid.md
  - docs/challenge/perfect-number.md
  - docs/tutor/py/ch2/2-2.md
  - docs/challenge/star-square.md
  - docs/challenge/nested-triangle.md
  - docs/public/assets/tutor/py/ch2/圖七.png
  - docs/public/assets/tutor/py/ch2/圖十四.png
  - docs/tutor/py/ch2/2-3.md
  - docs/challenge/smallest-prime-factor.md
  - docs/public/assets/tutor/py/ch2/圖十.png
  - docs/tutor/py/ch2/2-5.md
  - docs/challenge/multiplication-table.md
  - docs/public/assets/tutor/py/ch2/圖六.png
  - docs/challenge/arithmetic-sum.md
-->

---
### Requirement: Section 2-5 contains a knowledge map covering all Module 2 concepts

Section 2-5 SHALL include a Mermaid mindmap diagram that hierarchically organizes all concepts taught in sections 2-1 through 2-4. The mindmap SHALL use the `mindmap` diagram type.

The mindmap root SHALL be "模組二：迴圈與重複結構" and SHALL include branches for:
- 2-1: `for` 迴圈 → `range(n)`, `range(start, stop)`, `range(start, stop, step)`, negative step
- 2-2: `while` 迴圈 → condition-based, sentinel value, infinite loop + break pattern
- 2-3: 迴圈控制 → `break` (early exit), `continue` (skip iteration), nested break behavior
- 2-4: 巢狀迴圈 → pattern printing, multiplication table, conditional combinations, counting patterns

#### Scenario: Mindmap includes all four sections

- **WHEN** the Mermaid mindmap code block is parsed
- **THEN** it SHALL contain nodes for 2-1, 2-2, 2-3, and 2-4, each with at least 3 sub-concept nodes

#### Scenario: Mindmap renders correctly

- **WHEN** VitePress renders the page with Mermaid support
- **THEN** the mindmap SHALL display without rendering errors


<!-- @trace
source: write-ch2-completion
updated: 2026-04-13
code:
  - docs/challenge/even-countdown.md
  - docs/public/assets/tutor/py/ch2/圖十三.png
  - docs/challenge/pair-count.md
  - docs/public/assets/tutor/py/ch2/圖二.png
  - docs/public/assets/tutor/py/ch2/圖四.png
  - docs/public/assets/tutor/py/ch2/圖一.png
  - docs/challenge/number-pyramid.md
  - docs/public/assets/tutor/py/ch2/圖五.png
  - docs/challenge/inverted-triangle.md
  - docs/challenge/isosceles-triangle.md
  - docs/tutor/py/ch2/appendix.md
  - docs/challenge/star-diamond.md
  - docs/tutor/py/ch2/reference.md
  - docs/challenge/digital-root.md
  - docs/public/assets/tutor/py/ch2/圖三.png
  - docs/public/assets/tutor/py/ch2/圖十二.png
  - docs/challenge/number-staircase.md
  - docs/tutor/py/ch2/2-4.md
  - docs/tutor/py/ch2/index.md
  - docs/challenge/prime-check.md
  - docs/public/assets/tutor/py/ch2/圖十一.png
  - docs/public/assets/tutor/py/ch2/圖九.png
  - docs/public/assets/tutor/py/ch2/圖八.png
  - docs/challenge/guess-number-simple.md
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/perfect-numbers-range.md
  - docs/challenge/star-rectangle.md
  - docs/challenge/gcd-euclid.md
  - docs/challenge/perfect-number.md
  - docs/tutor/py/ch2/2-2.md
  - docs/challenge/star-square.md
  - docs/challenge/nested-triangle.md
  - docs/public/assets/tutor/py/ch2/圖七.png
  - docs/public/assets/tutor/py/ch2/圖十四.png
  - docs/tutor/py/ch2/2-3.md
  - docs/challenge/smallest-prime-factor.md
  - docs/public/assets/tutor/py/ch2/圖十.png
  - docs/tutor/py/ch2/2-5.md
  - docs/challenge/multiplication-table.md
  - docs/public/assets/tutor/py/ch2/圖六.png
  - docs/challenge/arithmetic-sum.md
-->

---
### Requirement: Section 2-5 contains a self-check checklist

Section 2-5 SHALL include a self-check checklist with approximately 15 items (minimum 12, maximum 18) in checkbox format. Each item SHALL be a specific, verifiable skill statement starting with a verb (e.g., "能夠用 `for i in range(n)` 寫出重複 N 次的迴圈").

The checklist SHALL cover skills from all four content sections (2-1 through 2-4) with proportional representation:
- 2-1 (for + range): 3-4 items
- 2-2 (while): 3-4 items
- 2-3 (break + continue): 3-4 items
- 2-4 (nested loops): 3-4 items

#### Scenario: Checklist has 12-18 items covering all sections

- **WHEN** the self-check checklist is parsed
- **THEN** it SHALL contain 12 to 18 checkbox items, each referencing a specific programming skill
- **AND** items from each of the four content sections SHALL be present


<!-- @trace
source: write-ch2-completion
updated: 2026-04-13
code:
  - docs/challenge/even-countdown.md
  - docs/public/assets/tutor/py/ch2/圖十三.png
  - docs/challenge/pair-count.md
  - docs/public/assets/tutor/py/ch2/圖二.png
  - docs/public/assets/tutor/py/ch2/圖四.png
  - docs/public/assets/tutor/py/ch2/圖一.png
  - docs/challenge/number-pyramid.md
  - docs/public/assets/tutor/py/ch2/圖五.png
  - docs/challenge/inverted-triangle.md
  - docs/challenge/isosceles-triangle.md
  - docs/tutor/py/ch2/appendix.md
  - docs/challenge/star-diamond.md
  - docs/tutor/py/ch2/reference.md
  - docs/challenge/digital-root.md
  - docs/public/assets/tutor/py/ch2/圖三.png
  - docs/public/assets/tutor/py/ch2/圖十二.png
  - docs/challenge/number-staircase.md
  - docs/tutor/py/ch2/2-4.md
  - docs/tutor/py/ch2/index.md
  - docs/challenge/prime-check.md
  - docs/public/assets/tutor/py/ch2/圖十一.png
  - docs/public/assets/tutor/py/ch2/圖九.png
  - docs/public/assets/tutor/py/ch2/圖八.png
  - docs/challenge/guess-number-simple.md
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/perfect-numbers-range.md
  - docs/challenge/star-rectangle.md
  - docs/challenge/gcd-euclid.md
  - docs/challenge/perfect-number.md
  - docs/tutor/py/ch2/2-2.md
  - docs/challenge/star-square.md
  - docs/challenge/nested-triangle.md
  - docs/public/assets/tutor/py/ch2/圖七.png
  - docs/public/assets/tutor/py/ch2/圖十四.png
  - docs/tutor/py/ch2/2-3.md
  - docs/challenge/smallest-prime-factor.md
  - docs/public/assets/tutor/py/ch2/圖十.png
  - docs/tutor/py/ch2/2-5.md
  - docs/challenge/multiplication-table.md
  - docs/public/assets/tutor/py/ch2/圖六.png
  - docs/challenge/arithmetic-sum.md
-->

---
### Requirement: Section 2-5 contains a Module 3 preview

Section 2-5 SHALL include a preview paragraph (2-4 sentences) that introduces the topics of Module 3 (串列、排序與字典). The preview SHALL:
- Acknowledge what the student has already mastered (loops and repetition)
- Identify the gap: "now you can repeat, but what if you have 100 student grades? You need a way to store and manage large amounts of data"
- Tease Module 3 topics: lists (串列), searching (搜尋), sorting (排序), dictionaries (字典)
- End with an encouraging forward-looking statement

#### Scenario: Preview mentions Module 3 topics

- **WHEN** the preview paragraph is read
- **THEN** it SHALL reference at least 3 of the following terms: 串列/list, 搜尋/search, 排序/sort, 字典/dict


<!-- @trace
source: write-ch2-completion
updated: 2026-04-13
code:
  - docs/challenge/even-countdown.md
  - docs/public/assets/tutor/py/ch2/圖十三.png
  - docs/challenge/pair-count.md
  - docs/public/assets/tutor/py/ch2/圖二.png
  - docs/public/assets/tutor/py/ch2/圖四.png
  - docs/public/assets/tutor/py/ch2/圖一.png
  - docs/challenge/number-pyramid.md
  - docs/public/assets/tutor/py/ch2/圖五.png
  - docs/challenge/inverted-triangle.md
  - docs/challenge/isosceles-triangle.md
  - docs/tutor/py/ch2/appendix.md
  - docs/challenge/star-diamond.md
  - docs/tutor/py/ch2/reference.md
  - docs/challenge/digital-root.md
  - docs/public/assets/tutor/py/ch2/圖三.png
  - docs/public/assets/tutor/py/ch2/圖十二.png
  - docs/challenge/number-staircase.md
  - docs/tutor/py/ch2/2-4.md
  - docs/tutor/py/ch2/index.md
  - docs/challenge/prime-check.md
  - docs/public/assets/tutor/py/ch2/圖十一.png
  - docs/public/assets/tutor/py/ch2/圖九.png
  - docs/public/assets/tutor/py/ch2/圖八.png
  - docs/challenge/guess-number-simple.md
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/perfect-numbers-range.md
  - docs/challenge/star-rectangle.md
  - docs/challenge/gcd-euclid.md
  - docs/challenge/perfect-number.md
  - docs/tutor/py/ch2/2-2.md
  - docs/challenge/star-square.md
  - docs/challenge/nested-triangle.md
  - docs/public/assets/tutor/py/ch2/圖七.png
  - docs/public/assets/tutor/py/ch2/圖十四.png
  - docs/tutor/py/ch2/2-3.md
  - docs/challenge/smallest-prime-factor.md
  - docs/public/assets/tutor/py/ch2/圖十.png
  - docs/tutor/py/ch2/2-5.md
  - docs/challenge/multiplication-table.md
  - docs/public/assets/tutor/py/ch2/圖六.png
  - docs/challenge/arithmetic-sum.md
-->

---
### Requirement: Section 2-5 includes 2 AI image specifications

Section 2-5 SHALL include exactly 2 image placeholders using the dual-line format (F-1 rule).

Image 1 SHALL be a Recap-type summary illustration (e.g., a comic showing a student proudly looking at all the loop structures they've learned).

Image 2 SHALL be a Hook-type preview illustration (e.g., a comic showing a student overwhelmed by many data points, teasing the need for data structures in Module 3).

Each image SHALL have a complete specification in the appendix.

#### Scenario: Both images use dual-line format

- **WHEN** section 2-5 is scanned for image placeholders
- **THEN** exactly 2 image placeholders SHALL be found using the dual-line format


<!-- @trace
source: write-ch2-completion
updated: 2026-04-13
code:
  - docs/challenge/even-countdown.md
  - docs/public/assets/tutor/py/ch2/圖十三.png
  - docs/challenge/pair-count.md
  - docs/public/assets/tutor/py/ch2/圖二.png
  - docs/public/assets/tutor/py/ch2/圖四.png
  - docs/public/assets/tutor/py/ch2/圖一.png
  - docs/challenge/number-pyramid.md
  - docs/public/assets/tutor/py/ch2/圖五.png
  - docs/challenge/inverted-triangle.md
  - docs/challenge/isosceles-triangle.md
  - docs/tutor/py/ch2/appendix.md
  - docs/challenge/star-diamond.md
  - docs/tutor/py/ch2/reference.md
  - docs/challenge/digital-root.md
  - docs/public/assets/tutor/py/ch2/圖三.png
  - docs/public/assets/tutor/py/ch2/圖十二.png
  - docs/challenge/number-staircase.md
  - docs/tutor/py/ch2/2-4.md
  - docs/tutor/py/ch2/index.md
  - docs/challenge/prime-check.md
  - docs/public/assets/tutor/py/ch2/圖十一.png
  - docs/public/assets/tutor/py/ch2/圖九.png
  - docs/public/assets/tutor/py/ch2/圖八.png
  - docs/challenge/guess-number-simple.md
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/perfect-numbers-range.md
  - docs/challenge/star-rectangle.md
  - docs/challenge/gcd-euclid.md
  - docs/challenge/perfect-number.md
  - docs/tutor/py/ch2/2-2.md
  - docs/challenge/star-square.md
  - docs/challenge/nested-triangle.md
  - docs/public/assets/tutor/py/ch2/圖七.png
  - docs/public/assets/tutor/py/ch2/圖十四.png
  - docs/tutor/py/ch2/2-3.md
  - docs/challenge/smallest-prime-factor.md
  - docs/public/assets/tutor/py/ch2/圖十.png
  - docs/tutor/py/ch2/2-5.md
  - docs/challenge/multiplication-table.md
  - docs/public/assets/tutor/py/ch2/圖六.png
  - docs/challenge/arithmetic-sum.md
-->

---
### Requirement: Section 2-5 has no Judge challenges

Section 2-5 is a summary section and SHALL NOT contain any `<ChallengeLink>` components or Judge challenge references.

#### Scenario: No ChallengeLink in summary

- **WHEN** section 2-5 is scanned for `<ChallengeLink`
- **THEN** zero occurrences SHALL be found


<!-- @trace
source: write-ch2-completion
updated: 2026-04-13
code:
  - docs/challenge/even-countdown.md
  - docs/public/assets/tutor/py/ch2/圖十三.png
  - docs/challenge/pair-count.md
  - docs/public/assets/tutor/py/ch2/圖二.png
  - docs/public/assets/tutor/py/ch2/圖四.png
  - docs/public/assets/tutor/py/ch2/圖一.png
  - docs/challenge/number-pyramid.md
  - docs/public/assets/tutor/py/ch2/圖五.png
  - docs/challenge/inverted-triangle.md
  - docs/challenge/isosceles-triangle.md
  - docs/tutor/py/ch2/appendix.md
  - docs/challenge/star-diamond.md
  - docs/tutor/py/ch2/reference.md
  - docs/challenge/digital-root.md
  - docs/public/assets/tutor/py/ch2/圖三.png
  - docs/public/assets/tutor/py/ch2/圖十二.png
  - docs/challenge/number-staircase.md
  - docs/tutor/py/ch2/2-4.md
  - docs/tutor/py/ch2/index.md
  - docs/challenge/prime-check.md
  - docs/public/assets/tutor/py/ch2/圖十一.png
  - docs/public/assets/tutor/py/ch2/圖九.png
  - docs/public/assets/tutor/py/ch2/圖八.png
  - docs/challenge/guess-number-simple.md
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/perfect-numbers-range.md
  - docs/challenge/star-rectangle.md
  - docs/challenge/gcd-euclid.md
  - docs/challenge/perfect-number.md
  - docs/tutor/py/ch2/2-2.md
  - docs/challenge/star-square.md
  - docs/challenge/nested-triangle.md
  - docs/public/assets/tutor/py/ch2/圖七.png
  - docs/public/assets/tutor/py/ch2/圖十四.png
  - docs/tutor/py/ch2/2-3.md
  - docs/challenge/smallest-prime-factor.md
  - docs/public/assets/tutor/py/ch2/圖十.png
  - docs/tutor/py/ch2/2-5.md
  - docs/challenge/multiplication-table.md
  - docs/public/assets/tutor/py/ch2/圖六.png
  - docs/challenge/arithmetic-sum.md
-->

---
### Requirement: Section 2-5 follows editorial rules

Section 2-5 SHALL comply with all applicable editorial rules from phoenix-popular-science-article-style. In particular: P-1 (punctuation), S-3 (transitions — summary section may use simplified transitions), K-1 (kaomoji density and variety), F-1 (image format), V-1 (container syntax), T-2 (no TBD), T-3 (no empty elements).

#### Scenario: K-1 compliance in summary section

- **WHEN** kaomoji density is checked
- **THEN** the density rules (1 per 30 lines min, 1 per 10 lines max) SHALL be satisfied

<!-- @trace
source: write-ch2-completion
updated: 2026-04-13
code:
  - docs/challenge/even-countdown.md
  - docs/public/assets/tutor/py/ch2/圖十三.png
  - docs/challenge/pair-count.md
  - docs/public/assets/tutor/py/ch2/圖二.png
  - docs/public/assets/tutor/py/ch2/圖四.png
  - docs/public/assets/tutor/py/ch2/圖一.png
  - docs/challenge/number-pyramid.md
  - docs/public/assets/tutor/py/ch2/圖五.png
  - docs/challenge/inverted-triangle.md
  - docs/challenge/isosceles-triangle.md
  - docs/tutor/py/ch2/appendix.md
  - docs/challenge/star-diamond.md
  - docs/tutor/py/ch2/reference.md
  - docs/challenge/digital-root.md
  - docs/public/assets/tutor/py/ch2/圖三.png
  - docs/public/assets/tutor/py/ch2/圖十二.png
  - docs/challenge/number-staircase.md
  - docs/tutor/py/ch2/2-4.md
  - docs/tutor/py/ch2/index.md
  - docs/challenge/prime-check.md
  - docs/public/assets/tutor/py/ch2/圖十一.png
  - docs/public/assets/tutor/py/ch2/圖九.png
  - docs/public/assets/tutor/py/ch2/圖八.png
  - docs/challenge/guess-number-simple.md
  - docs/tutor/py/ch2/2-1.md
  - docs/challenge/perfect-numbers-range.md
  - docs/challenge/star-rectangle.md
  - docs/challenge/gcd-euclid.md
  - docs/challenge/perfect-number.md
  - docs/tutor/py/ch2/2-2.md
  - docs/challenge/star-square.md
  - docs/challenge/nested-triangle.md
  - docs/public/assets/tutor/py/ch2/圖七.png
  - docs/public/assets/tutor/py/ch2/圖十四.png
  - docs/tutor/py/ch2/2-3.md
  - docs/challenge/smallest-prime-factor.md
  - docs/public/assets/tutor/py/ch2/圖十.png
  - docs/tutor/py/ch2/2-5.md
  - docs/challenge/multiplication-table.md
  - docs/public/assets/tutor/py/ch2/圖六.png
  - docs/challenge/arithmetic-sum.md
-->