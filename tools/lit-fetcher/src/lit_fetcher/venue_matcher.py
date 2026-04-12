"""Match paper venues against approved conference/journal lists."""

from .config import APPROVED_CONFERENCES, APPROVED_Q1_JOURNALS


def _normalize(s: str) -> str:
    return s.lower().strip().replace("-", " ").replace("–", " ")


_CONF_NORMALIZED = [_normalize(c) for c in APPROVED_CONFERENCES]
_JOURNAL_NORMALIZED = [_normalize(j) for j in APPROVED_Q1_JOURNALS]

# Common abbreviation mappings
_ABBREV_MAP = {
    "neurips": "neural information processing systems",
    "nips": "neural information processing systems",
    "icml": "international conference on machine learning",
    "iclr": "international conference on learning representations",
    "aaai": "association for the advancement of artificial intelligence",
    "ijcai": "international joint conference on artificial intelligence",
    "cvpr": "computer vision and pattern recognition",
    "iccv": "international conference on computer vision",
    "ijcnn": "international joint conference on neural networks",
    "tpami": "ieee transactions on pattern analysis and machine intelligence",
    "tnnls": "ieee transactions on neural networks and learning systems",
    "jmlr": "journal of machine learning research",
    "tacl": "transactions of the association for computational linguistics",
    "tist": "acm transactions on intelligent systems and technology",
}


def is_approved_venue(venue: str) -> tuple[bool, str | None]:
    """Check if a venue string matches an approved conference or journal.

    Returns (is_approved, matched_venue_name).
    Prioritizes exact matches over substring matches.
    """
    if not venue:
        return False, None

    norm = _normalize(venue)

    # Pass 1: Exact matches (highest priority)
    all_names = [(n, APPROVED_Q1_JOURNALS[i], "q1_journal") for i, n in enumerate(_JOURNAL_NORMALIZED)]
    all_names += [(n, APPROVED_CONFERENCES[i], "conference") for i, n in enumerate(_CONF_NORMALIZED)]

    for normalized, original, _ in all_names:
        if norm == normalized:
            return True, original

    # Pass 2: Abbreviation exact match
    for abbrev, full in _ABBREV_MAP.items():
        if norm == abbrev:
            for normalized, original, _ in all_names:
                if full == normalized:
                    return True, original

    # Pass 3: Substring match — prefer longer matches to avoid false positives
    # (e.g., "Neural Networks" journal vs "International Joint Conference on Neural Networks")
    candidates: list[tuple[int, str]] = []
    for normalized, original, _ in all_names:
        if normalized in norm or norm in normalized:
            # Score by how close the match length is (exact = best)
            score = abs(len(norm) - len(normalized))
            candidates.append((score, original))

    if candidates:
        candidates.sort(key=lambda x: x[0])
        return True, candidates[0][1]

    # Pass 4: Abbreviation substring match
    for abbrev, full in _ABBREV_MAP.items():
        if abbrev in norm.split():
            for normalized, original, _ in all_names:
                if full == normalized:
                    return True, original

    return False, None


def classify_venue(venue: str) -> str:
    """Classify venue as 'conference', 'q1_journal', or 'other'."""
    if not venue:
        return "other"
    norm = _normalize(venue)
    for conf in _CONF_NORMALIZED:
        if conf in norm or norm in conf:
            return "conference"
    for journal in _JOURNAL_NORMALIZED:
        if journal in norm or norm in journal:
            return "q1_journal"
    return "other"
