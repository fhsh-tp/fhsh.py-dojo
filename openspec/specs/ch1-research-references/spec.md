# ch1-research-references Specification

## Purpose

TBD - created by archiving change 'save-ch1-research-references'. Update Purpose after archive.

## Requirements

### Requirement: Reference PDF files exist in ch1 references directory

The system SHALL provide a `docs/tutor/py/ch1/references/` directory containing downloadable PDF files of academic references related to mathematical literacy and computational thinking. The directory SHALL contain the following files:

- `Wing-2006-CT.pdf` — Wing's seminal computational thinking paper
- `Wing-2011-CT-MicrosoftResearch.pdf` — Wing's refined CT definition
- `ISTE-CSTA-2011-CT-Definition.pdf` — ISTE/CSTA operational definition
- `Brennan-Resnick-2012-CT-Assessment.pdf` — CT assessment framework
- `Weintrop-2016-CT-Math-Science.pdf` — CT practices taxonomy for math/science
- `Barr-Stephenson-2011-CT-K12.pdf` — CT integration in K-12
- `Taiwan-108-Math-Curriculum.pdf` — Taiwan 108 curriculum mathematics domain
- `Taiwan-108-Tech-Curriculum.pdf` — Taiwan 108 curriculum technology domain
- `Papert-1980-Mindstorms.pdf` — Papert's constructionism foundation
- `PISA-2022-Math-Framework.pdf` — PISA 2022 mathematics framework draft

Each file MUST be a valid PDF downloaded from its verified source URL.

#### Scenario: PDF files are accessible

- **WHEN** a user navigates to a reference PDF link in the reference page
- **THEN** the browser SHALL download or display a valid PDF file


<!-- @trace
source: save-ch1-research-references
updated: 2026-04-10
code:
  - docs/tutor/py/ch1/1-2.md
  - docs/challenge/triangle-classify.md
  - docs/tutor/py/ch2/2-2.md
  - docs/challenge/quadrant-classifier.md
  - docs/tutor/py/ch1/1-3.md
  - docs/tutor/py/ch1/1-4.md
  - docs/tutor/py/ch2/2-1.md
  - docs/tutor/py/ch2/2-3.md
  - docs/challenge/odd-even.md
  - docs/tutor/py/ch1/references/Barr-Stephenson-2011-CT-K12.pdf
  - docs/challenge/date-validator.md
  - docs/tutor/py/ch1/reference.md
  - docs/tutor/py/ch1/references/Taiwan-108-Tech-Curriculum.pdf
  - .vitepress/config.mts
  - docs/challenge/bmi-classifier.md
  - docs/tutor/py/ch1/references/PISA-2022-Math-Framework.pdf
  - docs/tutor/py/ch1/references/Brennan-Resnick-2012-CT-Assessment.pdf
  - docs/tutor/py/ch1/references/Papert-1980-Mindstorms.pdf
  - docs/tutor/py/ch1/1-1.md
  - docs/challenge/taxi-fare.md
  - docs/challenge/movie-ticket.md
  - docs/tutor/py/ch1/references/Wing-2006-CT.pdf
  - docs/tutor/py/ch1/references/Weintrop-2016-CT-Math-Science.pdf
  - docs/challenge/sign-check.md
  - docs/challenge/vending-change.md
  - docs/tutor/py/ch1/references/Taiwan-108-Math-Curriculum.pdf
  - docs/challenge/quadratic-discriminant.md
  - docs/tutor/py/ch1/references/ISTE-CSTA-2011-CT-Definition.pdf
  - docs/tutor/py/ch1/references/Wing-2011-CT-MicrosoftResearch.pdf
-->

---
### Requirement: Reference page lists all academic sources

The system SHALL provide a `docs/tutor/py/ch1/reference.md` file with frontmatter `layout: doc` and `title: 模組一參考文獻`. The file SHALL list all verified academic references organized into four topic sections:

1. **數學素養 (Mathematical Literacy)** — PISA framework, Taiwan 108 curriculum math domain
2. **運算思維 (Computational Thinking)** — Wing, ISTE/CSTA, Barr & Stephenson, Brennan & Resnick, Shute et al., Grover & Pea
3. **整合研究 (Integration Research)** — Weintrop et al., Olteanu, Lee et al., systematic reviews
4. **台灣課綱與教育資源 (Taiwan Curriculum & Resources)** — 108 curriculum, Hsu & Hu, NRICH, Project Euler

Each entry MUST include: correct author(s), year, title, publication venue, and either a relative link to a local PDF (`./references/filename.pdf`) or a verified external URL. The total number of references SHALL be adjusted if any entries are removed due to verification failure.

#### Scenario: Reference page renders in sidebar

- **WHEN** VitePress builds the site
- **THEN** `reference.md` SHALL appear in the Chapter 1 sidebar navigation

#### Scenario: Local PDF links resolve correctly

- **WHEN** the reference page contains a relative link to `./references/filename.pdf`
- **THEN** clicking the link SHALL download the corresponding PDF from the `references/` directory

#### Scenario: All author fields contain actual author names

- **WHEN** a reference entry is for an academic paper with identifiable authors
- **THEN** the author field SHALL contain the actual author names, not the journal name, publisher name, or database name


<!-- @trace
source: verify-ch1-references
updated: 2026-04-13
code:
  - tools/ref-verifier/uv.lock
  - tools/ref-verifier/src/ref_verifier/cli.py
  - tools/ref-verifier/src/ref_verifier/verify_inline.py
  - docs/tutor/py/ch1/1-3.md
  - tools/ref-verifier/pyproject.toml
  - docs/tutor/py/ch1/1-4.md
  - docs/public/assets/tutor/py/ch1/圖十三.png
  - docs/public/assets/tutor/py/ch1/圖十一.png
  - docs/public/assets/tutor/py/ch1/圖十二.png
  - docs/public/assets/tutor/py/ch1/圖十四.png
  - docs/tutor/py/ch1/appendix.md
  - docs/tutor/py/ch1/reference.md
  - tools/ref-verifier/src/ref_verifier.egg-info/SOURCES.txt
  - docs/public/assets/tutor/py/ch1/圖九.png
  - docs/public/assets/tutor/py/ch1/圖十.png
  - tools/ref-verifier/src/ref_verifier/__pycache__/verify_inline.cpython-313.pyc
tests:
  - tools/ref-verifier/tests/__pycache__/test_verify_inline.cpython-313-pytest-9.0.3.pyc
  - tools/ref-verifier/tests/test_verify_inline.py
-->

---
### Requirement: All references are verified against authoritative sources

Each of the 23 references in `docs/tutor/py/ch1/reference.md` SHALL have been verified against at least one authoritative source. The verification source SHALL be one of: Semantic Scholar, CrossRef, publisher website, or institutional repository.

For academic papers (references #3–#14, #16, #22, #23), the entry SHALL include:
- Correct author names (not journal or publisher names)
- Correct publication year
- Correct title matching the authoritative record
- Correct venue (journal name, conference name, or publisher)
- DOI link where available in the authoritative record

For web resources (references #19, #20, #21), the external URL SHALL return HTTP 200 status (following redirects).

For policy and institutional documents (references #1, #2, #6, #17), the entry SHALL have either a locally stored PDF file that exists at the referenced path, or an external URL that returns HTTP 200 status, or both.

References that cannot be verified against any authoritative source SHALL be removed or replaced with a verified alternative.

#### Scenario: Academic reference has correct author field

- **WHEN** a reference entry for an academic paper is checked against Semantic Scholar or CrossRef
- **THEN** the author field in `reference.md` SHALL match the actual author names from the authoritative record, not the journal name or publisher name

#### Scenario: Academic reference includes DOI where available

- **WHEN** a reference entry for an academic paper has a DOI registered in Semantic Scholar or CrossRef
- **THEN** the reference entry SHALL include a DOI link in the format `[DOI](https://doi.org/<doi>)` or embedded in the existing URL

#### Scenario: Web resource URL is accessible

- **WHEN** a reference entry includes an external URL to a web resource
- **THEN** an HTTP GET request to that URL SHALL return status 200 (after following redirects), or status 403 with a valid HTML response body (indicating bot protection but resource existence)

#### Scenario: Unverifiable reference is handled

- **WHEN** a reference entry cannot be found in any authoritative source (Semantic Scholar, CrossRef, publisher website) AND its URL returns HTTP 404 or connection error
- **THEN** the reference entry SHALL be removed from `reference.md` and subsequent entries SHALL be renumbered

<!-- @trace
source: verify-ch1-references
updated: 2026-04-13
code:
  - tools/ref-verifier/uv.lock
  - tools/ref-verifier/src/ref_verifier/cli.py
  - tools/ref-verifier/src/ref_verifier/verify_inline.py
  - docs/tutor/py/ch1/1-3.md
  - tools/ref-verifier/pyproject.toml
  - docs/tutor/py/ch1/1-4.md
  - docs/public/assets/tutor/py/ch1/圖十三.png
  - docs/public/assets/tutor/py/ch1/圖十一.png
  - docs/public/assets/tutor/py/ch1/圖十二.png
  - docs/public/assets/tutor/py/ch1/圖十四.png
  - docs/tutor/py/ch1/appendix.md
  - docs/tutor/py/ch1/reference.md
  - tools/ref-verifier/src/ref_verifier.egg-info/SOURCES.txt
  - docs/public/assets/tutor/py/ch1/圖九.png
  - docs/public/assets/tutor/py/ch1/圖十.png
  - tools/ref-verifier/src/ref_verifier/__pycache__/verify_inline.cpython-313.pyc
tests:
  - tools/ref-verifier/tests/__pycache__/test_verify_inline.cpython-313-pytest-9.0.3.pyc
  - tools/ref-verifier/tests/test_verify_inline.py
-->