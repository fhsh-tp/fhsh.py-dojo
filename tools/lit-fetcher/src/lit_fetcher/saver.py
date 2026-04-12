"""Save paper metadata and PDFs to refs/ directory."""

from pathlib import Path
from typing import Any


def paper_dir_name(paper: dict[str, Any]) -> str:
    """Generate directory name for a paper."""
    ext_ids = paper.get("externalIds", {}) or {}
    arxiv_id = ext_ids.get("ArXiv")
    doi = ext_ids.get("DOI")

    if arxiv_id:
        return f"arXiv-{arxiv_id}"
    if doi:
        return f"doi-{doi.replace('/', '_')}"
    # Fallback: title slug
    title = paper.get("title", "unknown")
    slug = title[:60].replace(" ", "-").replace("/", "_")
    return f"paper-{slug}"


def save_abstract_md(paper: dict[str, Any], output_dir: Path) -> Path:
    """Save paper metadata as abstract.md."""
    dirname = paper_dir_name(paper)
    paper_path = output_dir / dirname
    paper_path.mkdir(parents=True, exist_ok=True)

    title = paper.get("title", "Unknown Title")
    authors_list = paper.get("authors") or []
    authors = ", ".join(a.get("name", "") for a in authors_list[:10])
    if len(authors_list) > 10:
        authors += " et al."

    year = paper.get("year", "")
    venue = paper.get("venue", "")
    pub_venue = paper.get("publicationVenue")
    if pub_venue and isinstance(pub_venue, dict):
        venue = pub_venue.get("name", venue)

    ext_ids = paper.get("externalIds", {}) or {}
    arxiv_id = ext_ids.get("ArXiv", "")
    doi = ext_ids.get("DOI", "")

    is_oa = paper.get("isOpenAccess", False)
    oa_pdf = paper.get("openAccessPdf")
    pdf_url = oa_pdf.get("url", "") if oa_pdf else ""

    if not pdf_url and arxiv_id:
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}"

    abstract = paper.get("abstract", "N/A")

    md = f"""# {title}

- **Authors:** {authors}
- **Year:** {year}
- **Venue:** {venue}
- **arXiv:** {arxiv_id or 'N/A'}
- **DOI:** {doi or 'N/A'}
- **Open Access:** {'Yes' if is_oa else 'No'}
- **PDF URL:** {pdf_url or 'N/A'}

## Abstract

{abstract or 'N/A'}

## Venue Compliance

- **Approved Venue:** {paper.get('_approved_venue', 'Not checked')}
- **Venue Type:** {paper.get('_venue_type', 'Not checked')}
"""
    md_path = paper_path / "abstract.md"
    md_path.write_text(md, encoding="utf-8")
    return md_path
