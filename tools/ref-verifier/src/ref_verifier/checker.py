"""Core verification logic: compare local metadata against Semantic Scholar."""

import re
from dataclasses import dataclass, field
from enum import Enum

from .parser import PaperMeta
from .apis import S2Paper


class Severity(str, Enum):
    ERROR = "🔴 ERROR"
    WARNING = "🟠 WARNING"
    INFO = "🟡 INFO"
    OK = "✅ OK"


@dataclass
class Issue:
    severity: Severity
    field: str
    message: str
    local_value: str = ""
    s2_value: str = ""


@dataclass
class VerifyResult:
    paper: PaperMeta
    s2: S2Paper
    issues: list[Issue] = field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        return any(i.severity == Severity.ERROR for i in self.issues)

    @property
    def has_warnings(self) -> bool:
        return any(i.severity == Severity.WARNING for i in self.issues)

    @property
    def status(self) -> Severity:
        if self.has_errors:
            return Severity.ERROR
        if self.has_warnings:
            return Severity.WARNING
        if self.issues:
            return Severity.INFO
        return Severity.OK


# Known conference schedules (month the conference typically takes place)
CONFERENCE_MONTHS: dict[str, dict[int, int]] = {
    # venue_keyword: {year: month}
    "ICML": {2024: 7, 2025: 7, 2026: 7},
    "NeurIPS": {2023: 12, 2024: 12, 2025: 12, 2026: 12},
    "ICLR": {2024: 5, 2025: 4, 2026: 4},
    "AAAI": {2024: 2, 2025: 2, 2026: 2},
    "CVPR": {2024: 6, 2025: 6, 2026: 6},
    "ICCV": {2025: 10},
    "IJCAI": {2024: 8, 2025: 8, 2026: 8},
    "IJCNN": {2024: 6, 2025: 6, 2026: 6},
}

# Typical submission-to-acceptance timeline in months
# Papers are usually on arXiv BEFORE or around the conference, not months after
MAX_ARXIV_DELAY_MONTHS = 3  # allow up to 3 months after conference for late arXiv uploads


def verify_paper(paper: PaperMeta, s2: S2Paper) -> VerifyResult:
    """Run all verification checks on a paper."""
    result = VerifyResult(paper=paper, s2=s2)

    if s2.error:
        result.issues.append(Issue(
            severity=Severity.WARNING,
            field="s2_lookup",
            message=f"Semantic Scholar lookup failed: {s2.error}",
        ))
        return result

    # Check 1: Year mismatch
    _check_year(paper, s2, result)

    # Check 2: Venue mismatch
    _check_venue(paper, s2, result)

    # Check 3: arXiv date vs conference date consistency
    _check_arxiv_date_consistency(paper, s2, result)

    # Check 4: DOI consistency
    _check_doi(paper, s2, result)

    return result


def _check_year(paper: PaperMeta, s2: S2Paper, result: VerifyResult):
    """Check if claimed year matches S2 year."""
    local_year = paper.claimed_year
    s2_year = s2.year

    if local_year and s2_year and local_year != s2_year:
        result.issues.append(Issue(
            severity=Severity.ERROR,
            field="year",
            message=f"Year mismatch: local={local_year}, S2={s2_year}",
            local_value=str(local_year),
            s2_value=str(s2_year),
        ))


def _check_venue(paper: PaperMeta, s2: S2Paper, result: VerifyResult):
    """Check if claimed venue matches S2 venue."""
    local_venue = paper.venue.lower()
    s2_venue = (s2.pub_venue_name or s2.venue).lower()

    if not s2_venue:
        return  # S2 has no venue info

    # Normalize for comparison
    venue_aliases = {
        "icml": ["international conference on machine learning", "icml"],
        "neurips": ["neural information processing systems", "neurips", "nips"],
        "iclr": ["international conference on learning representations", "iclr"],
        "aaai": ["aaai conference on artificial intelligence", "aaai", "proceedings of the aaai"],
        "cvpr": ["computer vision and pattern recognition", "cvpr", "ieee/cvf conference on computer vision"],
        "ijcai": ["international joint conference on artificial intelligence", "ijcai"],
        "ijcnn": ["international joint conference on neural networks", "ijcnn"],
        "iccv": ["international conference on computer vision", "iccv"],
    }

    local_conf = _identify_conference(local_venue, venue_aliases)
    s2_conf = _identify_conference(s2_venue, venue_aliases)

    if local_conf and s2_conf and local_conf != s2_conf:
        result.issues.append(Issue(
            severity=Severity.ERROR,
            field="venue",
            message=f"Venue mismatch: local identifies as {local_conf}, S2 identifies as {s2_conf}",
            local_value=paper.venue,
            s2_value=s2.pub_venue_name or s2.venue,
        ))

    # Check if S2 venue is empty/generic but we claim a specific venue
    if not s2_conf and local_conf and "arxiv" in s2_venue:
        result.issues.append(Issue(
            severity=Severity.WARNING,
            field="venue",
            message=f"S2 shows arXiv but we claim {local_conf}. Paper may not be officially published yet.",
            local_value=paper.venue,
            s2_value=s2.venue,
        ))


def _check_arxiv_date_consistency(paper: PaperMeta, s2: S2Paper, result: VerifyResult):
    """Check if arXiv upload date is consistent with claimed conference date.

    If a paper claims to be at AAAI 2025 (Feb 2025) but was uploaded to arXiv
    in Nov 2025, that's highly suspicious.
    """
    arxiv_ym = paper.arxiv_year_month
    if not arxiv_ym:
        return

    arxiv_year, arxiv_month = arxiv_ym

    # Find which conference and year is claimed
    claimed = paper.claimed_venue_short
    for conf_key, schedules in CONFERENCE_MONTHS.items():
        if conf_key.lower() in claimed.lower():
            # Extract claimed conference year from venue string
            m = re.search(r"(20\d{2})", claimed)
            if not m:
                break
            conf_year = int(m.group(1))
            conf_month = schedules.get(conf_year)
            if not conf_month:
                break

            # Calculate how many months after the conference the arXiv was uploaded
            arxiv_total = arxiv_year * 12 + arxiv_month
            conf_total = conf_year * 12 + conf_month
            delay = arxiv_total - conf_total

            if delay > MAX_ARXIV_DELAY_MONTHS:
                result.issues.append(Issue(
                    severity=Severity.WARNING,
                    field="arxiv_date",
                    message=(
                        f"arXiv uploaded {delay} months AFTER claimed conference "
                        f"({conf_key} {conf_year} = ~{conf_year}-{conf_month:02d}, "
                        f"arXiv = {arxiv_year}-{arxiv_month:02d}). "
                        f"Possible wrong conference year — may be {conf_key} {conf_year + 1}?"
                    ),
                    local_value=f"arXiv {arxiv_year}-{arxiv_month:02d}",
                    s2_value=f"{conf_key} {conf_year} (~{conf_year}-{conf_month:02d})",
                ))
            break


def _check_doi(paper: PaperMeta, s2: S2Paper, result: VerifyResult):
    """Check DOI consistency and year extraction from DOI."""
    if not s2.doi:
        return

    # Some DOIs encode the year (e.g., 10.1109/TPAMI.2025.XXXX)
    m = re.search(r"\.(20\d{2})\.", s2.doi)
    if m:
        doi_year = int(m.group(1))
        local_year = paper.claimed_year
        if local_year and doi_year != local_year:
            result.issues.append(Issue(
                severity=Severity.INFO,
                field="doi_year",
                message=f"DOI contains year {doi_year} but paper claims {local_year}",
                local_value=str(local_year),
                s2_value=f"DOI: {s2.doi}",
            ))


def _identify_conference(venue_str: str, aliases: dict[str, list[str]]) -> str | None:
    """Identify which conference a venue string refers to."""
    for conf_key, patterns in aliases.items():
        for pat in patterns:
            if pat in venue_str:
                return conf_key
    return None
