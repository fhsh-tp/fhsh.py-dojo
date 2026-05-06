"""Semantic Scholar API client with rate-limit-aware async fetching."""

import asyncio
from dataclasses import dataclass

import httpx

S2_BASE = "https://api.semanticscholar.org/graph/v1/paper"
S2_FIELDS = "title,venue,year,publicationVenue,externalIds"

# Rate limit: ~1 req/sec without API key
REQUEST_DELAY = 3.0
MAX_RETRIES = 3
RETRY_BACKOFF = [5, 10, 20]  # seconds


@dataclass
class S2Paper:
    """Semantic Scholar paper record."""
    title: str = ""
    venue: str = ""
    year: int | None = None
    pub_venue_name: str = ""
    pub_venue_type: str = ""  # "journal" or "conference" from S2
    arxiv_id: str = ""
    doi: str = ""
    error: str = ""  # non-empty if lookup failed


async def fetch_paper_by_arxiv(
    client: httpx.AsyncClient,
    arxiv_id: str,
    semaphore: asyncio.Semaphore,
) -> S2Paper:
    """Fetch a paper from S2 by arXiv ID with rate limiting and retries."""
    url = f"{S2_BASE}/arXiv:{arxiv_id}?fields={S2_FIELDS}"
    return await _fetch(client, url, semaphore)


async def fetch_paper_by_doi(
    client: httpx.AsyncClient,
    doi: str,
    semaphore: asyncio.Semaphore,
) -> S2Paper:
    """Fetch a paper from S2 by DOI with rate limiting and retries."""
    url = f"{S2_BASE}/DOI:{doi}?fields={S2_FIELDS}"
    return await _fetch(client, url, semaphore)


async def _fetch(
    client: httpx.AsyncClient,
    url: str,
    semaphore: asyncio.Semaphore,
) -> S2Paper:
    """Rate-limited fetch with exponential backoff on 429."""
    async with semaphore:
        for attempt in range(MAX_RETRIES):
            try:
                resp = await client.get(url)

                if resp.status_code == 429:
                    wait = RETRY_BACKOFF[min(attempt, len(RETRY_BACKOFF) - 1)]
                    await asyncio.sleep(wait)
                    continue

                if resp.status_code == 404:
                    return S2Paper(error="not_found_on_s2")

                resp.raise_for_status()
                data = resp.json()

                result = S2Paper(
                    title=data.get("title", ""),
                    venue=data.get("venue", ""),
                    year=data.get("year"),
                )

                # Publication venue (structured)
                pv = data.get("publicationVenue")
                if pv and isinstance(pv, dict):
                    result.pub_venue_name = pv.get("name", "")
                    result.pub_venue_type = pv.get("type", "")

                # External IDs
                ext = data.get("externalIds", {})
                if ext:
                    result.arxiv_id = ext.get("ArXiv", "")
                    result.doi = ext.get("DOI", "")

                await asyncio.sleep(REQUEST_DELAY)
                return result

            except httpx.HTTPError as e:
                if attempt == MAX_RETRIES - 1:
                    return S2Paper(error=f"http_error: {e}")
                await asyncio.sleep(RETRY_BACKOFF[attempt])

        return S2Paper(error="max_retries_exceeded")
