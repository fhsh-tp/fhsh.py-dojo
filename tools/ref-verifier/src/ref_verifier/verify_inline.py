"""Verify inline markdown references against Semantic Scholar, CrossRef, and URL checks.

This module parses reference entries from an inline markdown file (e.g. reference.md)
and verifies each one using academic APIs and URL accessibility checks.
"""

import asyncio
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import httpx

from .apis import S2Paper, fetch_paper_by_doi, S2_BASE, S2_FIELDS, REQUEST_DELAY

import logging

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class InlineRef:
    """A single numbered reference parsed from inline markdown."""
    number: int
    raw_line: str
    authors: str = ""
    year: int | None = None
    title: str = ""
    venue: str = ""
    volume_issue_pages: str = ""
    pdf_path: str = ""
    url: str = ""
    ref_type: str = "academic"  # academic | policy | web_resource


@dataclass
class VerifyResult:
    """Verification outcome for one reference."""
    ref: InlineRef
    status: str = "pending"  # verified | needs_correction | unverifiable | remove
    source: str = ""  # which API confirmed it
    corrections: dict = field(default_factory=dict)  # field -> correct_value
    s2_data: S2Paper | None = None
    crossref_data: dict | None = None
    url_status: int | None = None
    notes: str = ""


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

_REF_LINE_RE = re.compile(
    r"^(\d+)\.\s+"           # number
    r"\*\*(.+?)\s*\((\d{4})\)\*\*"  # **Author (YYYY)**
)

_VENUE_RE = re.compile(r"\*([^*]+)\*")  # *Venue Name*
_PDF_RE = re.compile(r"\[PDF\]\(([^)]+)\)")
_URL_RE = re.compile(r"\[(?:URL|Website)\]\(([^)]+)\)")


def parse_reference_md(text: str) -> list[InlineRef]:
    """Parse numbered references from markdown text.

    Expects lines like:
        1. **Author (YYYY)**. Title. *Venue*, Vol(Issue), Pages. [PDF](path) | [URL](url)
    """
    refs: list[InlineRef] = []
    for line in text.splitlines():
        line = line.strip()
        m = _REF_LINE_RE.match(line)
        if not m:
            continue

        number = int(m.group(1))
        authors = m.group(2).strip()
        year = int(m.group(3))

        # Everything after **Author (YYYY)** closing
        rest = line[m.end():]
        # Remove leading ". " or "." from rest
        rest = rest.lstrip(".").strip()

        # Extract venue (italic text)
        venue = ""
        venue_m = _VENUE_RE.search(rest)
        if venue_m:
            venue = venue_m.group(1).strip()

        # Title is text before the venue (or before links if no venue)
        if venue_m:
            title = rest[:venue_m.start()].rstrip(". ").strip()
        else:
            # Title is text before any link
            link_start = min(
                (rest.find("[PDF]"), rest.find("[URL]"), rest.find("[Website]")),
                key=lambda x: x if x >= 0 else len(rest),
            )
            title = rest[:link_start].rstrip(". |").strip()

        # Extract volume/issue/pages: text after venue italic, before links
        volume_issue_pages = ""
        if venue_m:
            after_venue = rest[venue_m.end():]
            link_start = min(
                (after_venue.find("[PDF]"), after_venue.find("[URL]"), after_venue.find("[Website]")),
                key=lambda x: x if x >= 0 else len(after_venue),
            )
            volume_issue_pages = after_venue[:link_start].strip(", .| ").strip()

        # Extract links
        pdf_path = ""
        pdf_m = _PDF_RE.search(line)
        if pdf_m:
            pdf_path = pdf_m.group(1)

        url = ""
        url_m = _URL_RE.search(line)
        if url_m:
            url = url_m.group(1)

        # Classify reference type
        ref_type = "academic"
        if authors in ("OECD", "教育部", "ISTE & CSTA"):
            ref_type = "policy"
        elif authors in ("Edutopia", "NRICH", "Project Euler"):
            ref_type = "web_resource"

        refs.append(InlineRef(
            number=number,
            raw_line=line,
            authors=authors,
            year=year,
            title=title,
            venue=venue,
            volume_issue_pages=volume_issue_pages,
            pdf_path=pdf_path,
            url=url,
            ref_type=ref_type,
        ))

    return refs


# ---------------------------------------------------------------------------
# DOI extraction
# ---------------------------------------------------------------------------

_DOI_RE = re.compile(r"(10\.\d{4,9}/[^\s\])\">]+)")


def extract_doi_from_url(url: str) -> str | None:
    """Extract a DOI from a URL string, if present."""
    m = _DOI_RE.search(url)
    return m.group(1) if m else None


# ---------------------------------------------------------------------------
# API clients
# ---------------------------------------------------------------------------

CROSSREF_BASE = "https://api.crossref.org/works"
CROSSREF_HEADERS = {
    "User-Agent": "ref-verifier/0.1 (mailto:ref-verifier@fhsh.edu.tw)",
}


async def search_crossref(
    title: str,
    author: str = "",
    rows: int = 5,
) -> list[dict]:
    """Search CrossRef by bibliographic query. Returns list of work items."""
    params: dict = {
        "query.bibliographic": title,
        "rows": rows,
    }
    if author:
        params["query.author"] = author

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(CROSSREF_BASE, params=params, headers=CROSSREF_HEADERS)
            if resp.status_code != 200:
                logger.debug("CrossRef returned %d for query: %s", resp.status_code, title)
                return []
            data = resp.json()
            return data.get("message", {}).get("items", [])
    except httpx.HTTPError as e:
        logger.debug("CrossRef HTTP error for '%s': %s", title, e)
        return []


async def search_s2_by_title(
    title: str,
    year: int | None = None,
) -> S2Paper | None:
    """Search Semantic Scholar by title. Returns best match or None."""
    params: dict = {
        "query": title,
        "fields": S2_FIELDS + ",authors",
        "limit": 5,
    }
    if year:
        params["year"] = f"{year - 1}-{year + 1}"

    async with httpx.AsyncClient(timeout=30) as client:
        try:
            resp = await client.get(f"{S2_BASE}/search", params=params)
            if resp.status_code != 200:
                return None
            data = resp.json()
            results = data.get("data", [])
            if not results:
                return None

            # Find best match by title similarity
            best = results[0]
            best_sim = _title_similarity(title, best.get("title", ""))
            for r in results[1:]:
                sim = _title_similarity(title, r.get("title", ""))
                if sim > best_sim:
                    best = r
                    best_sim = sim

            if best_sim < 0.6:
                return None

            paper = S2Paper(
                title=best.get("title", ""),
                venue=best.get("venue", ""),
                year=best.get("year"),
            )
            pv = best.get("publicationVenue")
            if pv and isinstance(pv, dict):
                paper.pub_venue_name = pv.get("name", "")
                paper.pub_venue_type = pv.get("type", "")
            ext = best.get("externalIds", {})
            if ext:
                paper.arxiv_id = ext.get("ArXiv", "") or ""
                paper.doi = ext.get("DOI", "") or ""

            # Store authors in a custom way via the title field prefix
            authors = best.get("authors", [])
            if authors:
                paper._authors_list = [a.get("name", "") for a in authors]

            return paper
        except httpx.HTTPError as e:
            logger.debug("S2 title search HTTP error for '%s': %s", title, e)
            return None
        except (KeyError, ValueError) as e:
            logger.debug("S2 title search parse error for '%s': %s", title, e)
            return None


def _title_similarity(a: str, b: str) -> float:
    """Simple word-overlap similarity between two titles."""
    wa = set(a.lower().split())
    wb = set(b.lower().split())
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / max(len(wa), len(wb))


# ---------------------------------------------------------------------------
# URL checker
# ---------------------------------------------------------------------------

async def check_url(url: str) -> int:
    """HTTP GET a URL and return the status code. Returns 0 on connection error."""
    # Only allow http/https to prevent SSRF via file:// or other schemes
    if not url.startswith(("http://", "https://")):
        logger.warning("Rejected non-HTTP URL: %s", url)
        return 0
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; ref-verifier/0.1)",
    }
    try:
        async with httpx.AsyncClient(timeout=20, follow_redirects=True) as client:
            resp = await client.get(url, headers=headers)
            return resp.status_code
    except httpx.HTTPError as e:
        logger.debug("HTTP error checking %s: %s", url, e)
        return 0
    except Exception as e:
        logger.debug("Unexpected error checking %s: %s", url, e)
        return 0


# ---------------------------------------------------------------------------
# Verification orchestrator
# ---------------------------------------------------------------------------

async def verify_reference(
    ref: InlineRef,
    client: httpx.AsyncClient,
    semaphore: asyncio.Semaphore,
) -> VerifyResult:
    """Verify a single reference using the tiered strategy."""
    result = VerifyResult(ref=ref)

    if ref.ref_type == "web_resource":
        return await _verify_web_resource(ref, result)
    elif ref.ref_type == "policy":
        return await _verify_policy(ref, result)
    else:
        return await _verify_academic(ref, result, client, semaphore)


async def _verify_web_resource(ref: InlineRef, result: VerifyResult) -> VerifyResult:
    """Tier B: URL accessibility check."""
    if ref.url:
        result.url_status = await check_url(ref.url)
        if result.url_status in (200, 301, 302, 403):
            result.status = "verified"
            result.source = f"URL check (HTTP {result.url_status})"
        else:
            result.status = "unverifiable"
            result.notes = f"URL returned HTTP {result.url_status}"
    else:
        result.status = "unverifiable"
        result.notes = "No URL to check"
    return result


async def _verify_policy(ref: InlineRef, result: VerifyResult) -> VerifyResult:
    """Tier C: Local PDF + URL check."""
    checks = []
    has_valid_source = False
    if ref.pdf_path:
        checks.append(f"PDF path: {ref.pdf_path}")
        has_valid_source = True
    if ref.url:
        status = await check_url(ref.url)
        result.url_status = status
        checks.append(f"URL HTTP {status}")
        if status in (200, 301, 302):
            has_valid_source = True
    if has_valid_source:
        result.status = "verified"
        result.source = "policy/institutional document: " + ", ".join(checks)
    else:
        result.status = "unverifiable"
        result.notes = "Policy document: " + ", ".join(checks) if checks else "no PDF path or URL"
    return result


async def _verify_academic(
    ref: InlineRef,
    result: VerifyResult,
    client: httpx.AsyncClient,
    semaphore: asyncio.Semaphore,
) -> VerifyResult:
    """Tier A/D/E: Academic paper verification via S2 and CrossRef."""

    # Step 1: Try DOI from URL
    doi = extract_doi_from_url(ref.url) if ref.url else None

    # Step 2: If DOI found, query S2
    # Note: fetch_paper_by_doi acquires the semaphore internally — do NOT
    # wrap this in another `async with semaphore:` to avoid deadlock.
    if doi:
        s2 = await fetch_paper_by_doi(client, doi, semaphore)
        if not s2.error:
            result.s2_data = s2
            result.status = "verified"
            result.source = f"S2 DOI:{doi}"
            _check_corrections(ref, result, s2, doi)
            return result

    # Step 3: S2 title search
    s2 = await search_s2_by_title(ref.title, ref.year)
    if s2 and not s2.error:
        result.s2_data = s2
        result.status = "verified"
        result.source = "S2 title search"
        if s2.doi:
            doi = s2.doi
        _check_corrections(ref, result, s2, doi)
        return result

    # Step 4: CrossRef search
    cr_items = await search_crossref(ref.title, ref.authors)
    if cr_items:
        best = cr_items[0]
        best_title = best.get("title", [""])[0] if best.get("title") else ""
        if _title_similarity(ref.title, best_title) >= 0.6:
            result.crossref_data = best
            result.status = "verified"
            result.source = "CrossRef"
            cr_doi = best.get("DOI", "")
            _check_crossref_corrections(ref, result, best, cr_doi)
            return result

    # Step 5: URL check as fallback
    if ref.url:
        result.url_status = await check_url(ref.url)
        if result.url_status in (200, 301, 302, 403):
            result.status = "verified"
            result.source = f"URL only (HTTP {result.url_status})"
            return result

    # If local PDF exists, accept it
    if ref.pdf_path:
        result.status = "verified"
        result.source = "Local PDF only (no API confirmation)"
        return result

    result.status = "unverifiable"
    result.notes = "Not found in S2, CrossRef, or URL check"
    return result


_KNOWN_JOURNAL_NAMES = {
    "International Journal of STEM Education",
    "Digital Experiences in Mathematics Education",
    "Education Sciences",
    "Springer",
    "ERIC",
}


def _check_corrections(
    ref: InlineRef, result: VerifyResult, s2: S2Paper, doi: str | None
) -> None:
    """Populate corrections dict based on S2 data vs current reference."""
    # Check if authors might be a journal/publisher name
    if ref.authors in _KNOWN_JOURNAL_NAMES:
        authors_list = getattr(s2, "_authors_list", None)
        if authors_list and len(authors_list) >= 1:
            if len(authors_list) <= 3:
                corrected = ", ".join(authors_list)
            else:
                corrected = f"{authors_list[0]}, et al."
            result.corrections["authors"] = corrected
        else:
            # S2 DOI lookup doesn't return authors — flag for manual check
            result.corrections["authors"] = "(needs manual verification — author field appears to be a journal name)"

    # Year mismatch
    if s2.year and ref.year and s2.year != ref.year:
        result.corrections["year"] = s2.year

    # DOI missing from reference
    if doi and not extract_doi_from_url(ref.url or ""):
        result.corrections["add_doi"] = doi


def _check_crossref_corrections(
    ref: InlineRef, result: VerifyResult, item: dict, doi: str
) -> None:
    """Populate corrections from CrossRef data."""
    # Extract authors
    cr_authors = item.get("author", [])
    if cr_authors:
        if ref.authors in _KNOWN_JOURNAL_NAMES:
            names = []
            for a in cr_authors[:4]:
                given = a.get("given", "")
                family = a.get("family", "")
                if given and family:
                    names.append(f"{family}, {given[0]}.")
                elif family:
                    names.append(family)
            if len(cr_authors) > 4:
                corrected = ", ".join(names) + ", et al."
            else:
                corrected = ", ".join(names)
            result.corrections["authors"] = corrected

    # Year
    issued = item.get("issued", {}).get("date-parts", [[]])
    if issued and issued[0]:
        cr_year = issued[0][0]
        if cr_year and ref.year and cr_year != ref.year:
            result.corrections["year"] = cr_year

    # DOI
    if doi and not extract_doi_from_url(ref.url or ""):
        result.corrections["add_doi"] = doi


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(results: list[VerifyResult]) -> str:
    """Generate a markdown verification report."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"# Ch1 Reference Verification Report",
        f"",
        f"> Generated: {now}",
        f"> References checked: {len(results)}",
        f"",
    ]

    verified = [r for r in results if r.status == "verified" and not r.corrections]
    needs_fix = [r for r in results if r.status == "verified" and r.corrections]
    unverifiable = [r for r in results if r.status == "unverifiable"]
    remove = [r for r in results if r.status == "remove"]

    # Verified
    lines.append("## Verified")
    lines.append("")
    if verified:
        lines.append("| # | Authors | Title | Year | Source |")
        lines.append("|---|---------|-------|------|--------|")
        for r in verified:
            lines.append(
                f"| {r.ref.number} | {r.ref.authors} | {r.ref.title[:50]} | {r.ref.year} | {r.source} |"
            )
    else:
        lines.append("(none)")
    lines.append("")

    # Needs correction
    lines.append("## Corrections Needed")
    lines.append("")
    if needs_fix:
        lines.append("| # | Field | Current Value | Correct Value | Source |")
        lines.append("|---|-------|--------------|---------------|--------|")
        for r in needs_fix:
            for field_name, correct in r.corrections.items():
                current = getattr(r.ref, field_name, "—")
                if field_name == "add_doi":
                    current = "(missing)"
                    field_name = "DOI"
                lines.append(
                    f"| {r.ref.number} | {field_name} | {current} | {correct} | {r.source} |"
                )
    else:
        lines.append("(none)")
    lines.append("")

    # Unverifiable
    lines.append("## Unverifiable")
    lines.append("")
    if unverifiable:
        lines.append("| # | Title | URL Status | Notes |")
        lines.append("|---|-------|-----------|-------|")
        for r in unverifiable:
            lines.append(
                f"| {r.ref.number} | {r.ref.title[:50]} | {r.url_status or '—'} | {r.notes} |"
            )
    else:
        lines.append("(none)")
    lines.append("")

    # Flagged for removal
    lines.append("## Flagged for Removal")
    lines.append("")
    if remove:
        lines.append("| # | Title | Reason |")
        lines.append("|---|-------|--------|")
        for r in remove:
            lines.append(f"| {r.ref.number} | {r.ref.title[:50]} | {r.notes} |")
    else:
        lines.append("(none)")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

async def run_verify_inline(input_path: Path, output_dir: Path) -> list[VerifyResult]:
    """Run inline reference verification end-to-end."""
    text = input_path.read_text(encoding="utf-8")
    refs = parse_reference_md(text)
    print(f"Parsed {len(refs)} references from {input_path}\n")

    semaphore = asyncio.Semaphore(3)
    results: list[VerifyResult] = []

    async with httpx.AsyncClient(timeout=30) as client:
        tasks = [verify_reference(r, client, semaphore) for r in refs]
        for i, coro in enumerate(asyncio.as_completed(tasks)):
            result = await coro
            results.append(result)
            print(
                f"  [{i+1}/{len(refs)}] #{result.ref.number} {result.ref.authors} ({result.ref.year}) "
                f"→ {result.status}"
                f"{f' [{', '.join(result.corrections.keys())}]' if result.corrections else ''}"
            )

    results.sort(key=lambda r: r.ref.number)

    # Write report
    report = generate_report(results)
    report_path = output_dir / "inline-verification-report.md"
    report_path.write_text(report, encoding="utf-8")
    print(f"\nReport written to {report_path}")

    return results
