"""API clients for Semantic Scholar and OpenAlex."""

import httpx
import asyncio
from typing import Any
from .config import SEMANTIC_SCHOLAR_API_KEY


S2_BASE = "https://api.semanticscholar.org/graph/v1"
OA_BASE = "https://api.openalex.org"

S2_FIELDS = "title,authors,venue,year,externalIds,isOpenAccess,openAccessPdf,publicationVenue,abstract"


async def _s2_request(client: httpx.AsyncClient, url: str, params: dict, headers: dict, max_attempts: int = 4) -> dict:
    last_resp = None
    for attempt in range(max_attempts):
        last_resp = await client.get(url, params=params, headers=headers)
        if last_resp.status_code == 429 and attempt < max_attempts - 1:
            await asyncio.sleep(2 ** (attempt + 1))
            continue
        last_resp.raise_for_status()
        return last_resp.json()
    if last_resp is not None:
        last_resp.raise_for_status()
    return {}


async def search_semantic_scholar(
    query: str,
    year_range: str = "2024-2026",
    limit: int = 50,
    offset: int = 0,
) -> list[dict[str, Any]]:
    headers = {}
    if SEMANTIC_SCHOLAR_API_KEY:
        headers["x-api-key"] = SEMANTIC_SCHOLAR_API_KEY

    params = {
        "query": query,
        "year": year_range,
        "fields": S2_FIELDS,
        "limit": min(limit, 100),
        "offset": offset,
    }

    async with httpx.AsyncClient(timeout=30) as client:
        data = await _s2_request(client, f"{S2_BASE}/paper/search", params, headers)
        return data.get("data", [])


async def search_openalex(
    query: str,
    year_min: int = 2024,
    year_max: int = 2026,
    per_page: int = 50,
) -> list[dict[str, Any]]:
    params = {
        "search": query,
        "filter": f"publication_year:{year_min}-{year_max},type:article",
        "sort": "cited_by_count:desc",
        "per_page": per_page,
        "select": "title,authorships,primary_location,publication_year,doi,open_access,ids",
        "mailto": "lit-fetcher@example.com",
    }

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(f"{OA_BASE}/works", params=params)
        resp.raise_for_status()
        data = resp.json()
        return data.get("results", [])


async def get_paper_by_doi(doi: str) -> dict[str, Any] | None:
    headers = {}
    if SEMANTIC_SCHOLAR_API_KEY:
        headers["x-api-key"] = SEMANTIC_SCHOLAR_API_KEY

    async with httpx.AsyncClient(timeout=30) as client:
        try:
            data = await _s2_request(
                client, f"{S2_BASE}/paper/DOI:{doi}",
                {"fields": S2_FIELDS}, headers
            )
            return data
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise


async def get_paper_by_arxiv_id(arxiv_id: str) -> dict[str, Any] | None:
    headers = {}
    if SEMANTIC_SCHOLAR_API_KEY:
        headers["x-api-key"] = SEMANTIC_SCHOLAR_API_KEY

    async with httpx.AsyncClient(timeout=30) as client:
        try:
            data = await _s2_request(
                client, f"{S2_BASE}/paper/ARXIV:{arxiv_id}",
                {"fields": S2_FIELDS}, headers
            )
            return data
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise
