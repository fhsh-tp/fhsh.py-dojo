"""Parse abstract.md files into structured paper metadata."""

import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class PaperMeta:
    dir_name: str
    title: str = ""
    authors: str = ""
    year: str = ""
    venue: str = ""
    arxiv_id: str = ""
    doi: str = ""
    pdf_url: str = ""
    approved_venue: str = ""
    venue_type: str = ""

    @property
    def arxiv_year_month(self) -> tuple[int, int] | None:
        """Extract year and month from arXiv ID (YYMM.XXXXX format)."""
        if not self.arxiv_id:
            return None
        m = re.match(r"(\d{2})(\d{2})\.\d+", self.arxiv_id)
        if not m:
            return None
        yy, mm = int(m.group(1)), int(m.group(2))
        return (2000 + yy, mm)

    @property
    def claimed_year(self) -> int | None:
        """Extract numeric year from the year/date field."""
        m = re.search(r"(20\d{2})", self.year)
        return int(m.group(1)) if m else None

    @property
    def claimed_venue_short(self) -> str:
        """Extract short venue name from approved_venue field."""
        # "Yes — ICML 2024" → "ICML 2024"
        m = re.search(r"Yes\s*—\s*(.+)", self.approved_venue)
        return m.group(1).strip() if m else self.venue


def parse_abstract_md(path: Path) -> PaperMeta:
    """Parse a single abstract.md file into PaperMeta."""
    text = path.read_text(encoding="utf-8")
    meta = PaperMeta(dir_name=path.parent.name)

    # Title
    m = re.search(r"^#\s+(.+)", text, re.MULTILINE)
    if m:
        meta.title = m.group(1).strip()

    # Metadata fields
    field_map = {
        "Authors": "authors",
        "Year": "year",
        "Date": "year",  # fallback
        "Venue": "venue",
        "arXiv": "arxiv_id",
        "DOI": "doi",
        "PDF URL": "pdf_url",
    }
    for label, attr in field_map.items():
        m = re.search(rf"\*\*{re.escape(label)}:\*\*\s*(.+)", text)
        if m:
            val = m.group(1).strip()
            if attr == "year" and getattr(meta, attr):
                continue  # don't overwrite Year with Date
            setattr(meta, attr, val)

    # Fallback: extract arXiv ID from directory name
    if (not meta.arxiv_id or meta.arxiv_id == "N/A") and meta.dir_name.startswith("arXiv-"):
        meta.arxiv_id = meta.dir_name.replace("arXiv-", "").replace("v1", "")

    # Fallback: extract DOI from directory name
    if (not meta.doi or meta.doi == "N/A") and meta.dir_name.startswith("doi-"):
        meta.doi = meta.dir_name.replace("doi-", "").replace("_", "/")

    # Venue Compliance
    m = re.search(r"\*\*Approved Venue:\*\*\s*(.+)", text)
    if m:
        meta.approved_venue = m.group(1).strip()
    m = re.search(r"\*\*Venue Type:\*\*\s*(.+)", text)
    if m:
        meta.venue_type = m.group(1).strip()

    return meta


def load_all_papers(refs_dir: Path) -> list[PaperMeta]:
    """Load all papers from refs directory."""
    papers = []
    for d in sorted(refs_dir.iterdir()):
        if not d.is_dir():
            continue
        abstract = d / "abstract.md"
        if abstract.exists():
            papers.append(parse_abstract_md(abstract))
    return papers
