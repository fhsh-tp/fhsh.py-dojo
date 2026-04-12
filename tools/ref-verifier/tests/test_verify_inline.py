"""Tests for verify_inline module — parser and DOI extraction."""

from pathlib import Path
from ref_verifier.verify_inline import InlineRef, parse_reference_md, extract_doi_from_url

SAMPLE_MD = """\
---
layout: doc
title: 參考文獻
---

# 模組一參考文獻

## 數學素養（Mathematical Literacy）

1. **OECD (2022)**. PISA 2022 Mathematics Framework. [PDF](/references/ch1/PISA-2022-Math-Framework.pdf) | [Website](https://pisa2022-maths.oecd.org/ca/index.html)

2. **教育部 (2018)**. 十二年國民基本教育課程綱要——數學領域. [PDF](/references/ch1/Taiwan-108-Math-Curriculum.pdf)

## 運算思維（Computational Thinking）

3. **Wing, J. M. (2006)**. Computational Thinking. *Communications of the ACM*, 49(3), 33-35. [PDF](/references/ch1/Wing-2006-CT.pdf)

4. **Grover, S., & Pea, R. (2013)**. Computational Thinking in K-12: A Review of the State of the Field. *Educational Researcher*, 42(1), 38-43. [URL](https://journals.sagepub.com/doi/abs/10.3102/0013189x12463051)

## 整合研究（CT × Math Integration）

5. **International Journal of STEM Education (2023)**. Integration of Computational Thinking in K-12 Mathematics Education: A Systematic Review. [URL](https://link.springer.com/article/10.1186/s40594-023-00396-w)
"""


def test_parse_count():
    refs = parse_reference_md(SAMPLE_MD)
    assert len(refs) == 5


def test_parse_basic_fields():
    refs = parse_reference_md(SAMPLE_MD)
    r1 = refs[0]
    assert r1.number == 1
    assert r1.authors == "OECD"
    assert r1.year == 2022
    assert "PISA 2022 Mathematics Framework" in r1.title
    assert r1.pdf_path == "/references/ch1/PISA-2022-Math-Framework.pdf"


def test_parse_url_extraction():
    refs = parse_reference_md(SAMPLE_MD)
    # ref 4 has [URL]
    r4 = refs[3]
    assert r4.url == "https://journals.sagepub.com/doi/abs/10.3102/0013189x12463051"


def test_parse_venue():
    refs = parse_reference_md(SAMPLE_MD)
    r3 = refs[2]
    assert "Communications of the ACM" in r3.venue


def test_parse_chinese_author():
    refs = parse_reference_md(SAMPLE_MD)
    r2 = refs[1]
    assert r2.authors == "教育部"
    assert r2.year == 2018


def test_parse_both_links():
    refs = parse_reference_md(SAMPLE_MD)
    r1 = refs[0]
    assert r1.pdf_path == "/references/ch1/PISA-2022-Math-Framework.pdf"
    assert r1.url == "https://pisa2022-maths.oecd.org/ca/index.html"


# --- DOI extraction tests ---

def test_extract_doi_from_springer():
    url = "https://link.springer.com/article/10.1186/s40594-023-00396-w"
    assert extract_doi_from_url(url) == "10.1186/s40594-023-00396-w"


def test_extract_doi_from_tandfonline():
    url = "https://www.tandfonline.com/doi/full/10.1080/0020739X.2020.1858199"
    assert extract_doi_from_url(url) == "10.1080/0020739X.2020.1858199"


def test_extract_doi_from_sciencedirect():
    url = "https://www.sciencedirect.com/science/article/abs/pii/S1747938X17300350"
    assert extract_doi_from_url(url) is None  # no DOI in URL


def test_extract_doi_from_sage():
    url = "https://journals.sagepub.com/doi/abs/10.3102/0013189x12463051"
    assert extract_doi_from_url(url) == "10.3102/0013189x12463051"


def test_extract_doi_none():
    url = "https://projecteuler.net/"
    assert extract_doi_from_url(url) is None
