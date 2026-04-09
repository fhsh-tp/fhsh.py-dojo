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

The system SHALL provide a `docs/tutor/py/ch1/reference.md` file with frontmatter `layout: doc` and `title: 模組一參考文獻`. The file SHALL list all 23 academic references organized into four topic sections:

1. **數學素養 (Mathematical Literacy)** — PISA framework, Taiwan 108 curriculum math domain
2. **運算思維 (Computational Thinking)** — Wing, ISTE/CSTA, Barr & Stephenson, Brennan & Resnick, Shute et al., Grover & Pea
3. **整合研究 (Integration Research)** — Weintrop et al., Olteanu, Lee et al., systematic reviews
4. **台灣課綱與教育資源 (Taiwan Curriculum & Resources)** — 108 curriculum, Hsu & Hu, NRICH, Project Euler

Each entry MUST include: author(s), year, title, publication venue, and either a relative link to a local PDF (`./references/filename.pdf`) or a verified external URL.

#### Scenario: Reference page renders in sidebar

- **WHEN** VitePress builds the site
- **THEN** `reference.md` SHALL appear in the Chapter 1 sidebar navigation

#### Scenario: Local PDF links resolve correctly

- **WHEN** the reference page contains a relative link to `./references/filename.pdf`
- **THEN** clicking the link SHALL download the corresponding PDF from the `references/` directory

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