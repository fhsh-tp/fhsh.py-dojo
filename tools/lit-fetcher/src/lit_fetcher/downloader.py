"""Download papers — open access direct, paywalled via FJU campus proxy."""

import httpx
from pathlib import Path
from urllib.parse import quote
from .config import FJU_PROXY_USER, FJU_PROXY_PASS, FJU_PROXY_HOST, FJU_PROXY_PORT


def _fju_proxy_url() -> str | None:
    """Build the FJU forward proxy URL with LDAP auth credentials."""
    if not FJU_PROXY_USER or not FJU_PROXY_PASS:
        return None
    encoded_pass = quote(FJU_PROXY_PASS, safe="")
    return f"http://{FJU_PROXY_USER}:{encoded_pass}@{FJU_PROXY_HOST}:{FJU_PROXY_PORT}"


async def download_open_access_pdf(url: str, dest: Path) -> bool:
    """Download a PDF from an open access URL."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        async with httpx.AsyncClient(timeout=60, follow_redirects=True) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            content_type = resp.headers.get("content-type", "")
            if "pdf" in content_type:
                dest.write_bytes(resp.content)
                return True
            # Fallback: URL ends with .pdf but no content-type — check magic bytes
            if url.endswith(".pdf") and resp.content[:5] == b"%PDF-":
                dest.write_bytes(resp.content)
                return True
            return False
    except (httpx.HTTPError, httpx.TimeoutException):
        return False


async def download_via_fju_proxy(doi: str, dest: Path) -> bool:
    """Download a paper via FJU campus forward proxy.

    Uses authproxy.fju.edu.tw:3128 as HTTP proxy with LDAP auth.
    This makes requests appear from campus IP, granting institutional access.

    Flow:
    1. Resolve DOI to publisher page via proxy
    2. Extract PDF link from publisher page
    3. Download PDF via proxy
    """
    proxy_url = _fju_proxy_url()
    if not proxy_url:
        return False

    dest.parent.mkdir(parents=True, exist_ok=True)

    try:
        async with httpx.AsyncClient(
            proxy=proxy_url,
            timeout=60,
            follow_redirects=True,
            verify=False,  # campus proxy may use self-signed cert
        ) as client:
            # Step 1: Resolve DOI through proxy
            doi_url = f"https://doi.org/{doi}"
            page_resp = await client.get(doi_url)

            if page_resp.status_code != 200:
                return False

            # Step 2: Try to find PDF link in response
            content = page_resp.text
            pdf_url = _extract_pdf_url(content, page_resp.url)

            if pdf_url:
                pdf_resp = await client.get(str(pdf_url))
                if pdf_resp.status_code == 200 and (
                    "pdf" in pdf_resp.headers.get("content-type", "")
                    or pdf_resp.content[:5] == b"%PDF-"
                ):
                    dest.write_bytes(pdf_resp.content)
                    return True

            # Step 3: Fallback — try common publisher PDF URL patterns
            final_url = str(page_resp.url)
            fallback_urls = _guess_pdf_urls(final_url, doi)
            for fb_url in fallback_urls:
                try:
                    fb_resp = await client.get(fb_url)
                    if fb_resp.status_code == 200 and (
                        "pdf" in fb_resp.headers.get("content-type", "")
                        or fb_resp.content[:5] == b"%PDF-"
                    ):
                        dest.write_bytes(fb_resp.content)
                        return True
                except (httpx.HTTPError, httpx.TimeoutException):
                    continue

            return False
    except (httpx.HTTPError, httpx.TimeoutException, httpx.ProxyError):
        return False


def _extract_pdf_url(html: str, base_url: httpx.URL) -> str | None:
    """Try to extract PDF download URL from publisher page HTML."""
    import re

    # Common publisher PDF link patterns
    patterns = [
        r'href="([^"]*\.pdf[^"]*)"',
        r'href="([^"]*\/pdf\/[^"]*)"',
        r'data-pdf-url="([^"]*)"',
        r'"pdfUrl"\s*:\s*"([^"]*)"',
        r'href="([^"]*\/reader\/[^"]*)"',  # Elsevier reader
        r'<meta[^>]*citation_pdf_url[^>]*content="([^"]*)"',  # citation meta
    ]
    for pat in patterns:
        match = re.search(pat, html, re.IGNORECASE)
        if match:
            url = match.group(1)
            if url.startswith("http"):
                return url
            return str(base_url.join(url))
    return None


def _guess_pdf_urls(final_url: str, doi: str) -> list[str]:
    """Guess PDF URLs based on known publisher URL patterns."""
    urls = []

    # IEEE Xplore
    if "ieeexplore.ieee.org" in final_url:
        import re
        m = re.search(r"document/(\d+)", final_url)
        if m:
            urls.append(f"https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?arnumber={m.group(1)}")

    # Springer / Nature
    if "springer.com" in final_url or "nature.com" in final_url:
        urls.append(final_url.replace("/article/", "/content/pdf/") + ".pdf")

    # Elsevier / ScienceDirect
    if "sciencedirect.com" in final_url:
        urls.append(final_url.replace("/abs/", "/pdf/"))

    # AAAI
    if "ojs.aaai.org" in final_url:
        urls.append(final_url.replace("/view/", "/download/") + "/" + doi.split("/")[-1])

    return urls


async def download_arxiv_pdf(arxiv_id: str, dest: Path) -> bool:
    """Download PDF from arXiv."""
    url = f"https://arxiv.org/pdf/{arxiv_id}"
    return await download_open_access_pdf(url, dest)
