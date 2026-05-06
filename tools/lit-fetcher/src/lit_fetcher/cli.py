"""CLI entry point for lit-fetcher."""

import asyncio
import argparse
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table

from .apis import search_semantic_scholar, get_paper_by_arxiv_id
from .venue_matcher import is_approved_venue, classify_venue
from .downloader import download_open_access_pdf, download_arxiv_pdf, download_via_fju_proxy
from .saver import save_abstract_md, paper_dir_name
from .config import OUTPUT_DIR, SEARCH_YEAR_MIN, SEARCH_YEAR_MAX

console = Console()


SEARCH_QUERIES = [
    "skill internalization LLM reinforcement learning",
    "continual learning large language model LoRA",
    "knowledge distillation LLM agent",
    "on-device edge LLM fine-tuning training",
    "parameter efficient fine-tuning catastrophic forgetting LLM",
    "RAG retrieval augmented vs fine-tuning LLM",
    "curriculum learning reinforcement learning LLM agent",
    "self-distillation continual learning language model",
    "on-device personalization language model",
    "LoRA adapter merging continual learning",
]


async def cmd_search(args: argparse.Namespace) -> None:
    """Search for papers in approved venues."""
    queries = args.queries or SEARCH_QUERIES
    year_range = f"{SEARCH_YEAR_MIN}-{SEARCH_YEAR_MAX}"
    all_papers: dict[str, dict] = {}

    for query in queries:
        console.print(f"\n[bold blue]Searching S2:[/] {query}")
        try:
            papers = await search_semantic_scholar(query, year_range=year_range, limit=30)
            for p in papers:
                venue = p.get("venue", "")
                pub_venue = p.get("publicationVenue")
                if pub_venue and isinstance(pub_venue, dict):
                    venue = pub_venue.get("name", venue)
                approved, matched = is_approved_venue(venue)
                if approved:
                    p["_approved_venue"] = matched
                    p["_venue_type"] = classify_venue(venue)
                    key = p.get("title", "")[:80]
                    if key not in all_papers:
                        all_papers[key] = p
                        console.print(f"  [green]✓[/] {p['title'][:70]} — {matched}")
            await asyncio.sleep(1)  # Rate limiting
        except Exception as e:
            console.print(f"  [red]Error:[/] {e}")

    console.print(f"\n[bold]Found {len(all_papers)} papers in approved venues[/]\n")

    table = Table(title="Papers in Approved Venues")
    table.add_column("Title", max_width=50)
    table.add_column("Year")
    table.add_column("Venue")
    table.add_column("OA")
    for p in all_papers.values():
        table.add_row(
            p["title"][:50],
            str(p.get("year", "")),
            p.get("_approved_venue", "")[:30],
            "✓" if p.get("isOpenAccess") else "✗",
        )
    console.print(table)

    if args.save:
        output = Path(args.output or OUTPUT_DIR)
        for p in all_papers.values():
            path = save_abstract_md(p, output)
            console.print(f"  Saved: {path}")


async def cmd_verify(args: argparse.Namespace) -> None:
    """Verify existing refs/ papers against approved venue list."""
    refs_dir = Path(args.refs_dir or OUTPUT_DIR)
    if not refs_dir.exists():
        console.print(f"[red]Directory not found:[/] {refs_dir}")
        return

    table = Table(title="Venue Compliance Check")
    table.add_column("Paper")
    table.add_column("Venue")
    table.add_column("Status")

    for paper_dir in sorted(refs_dir.iterdir()):
        if not paper_dir.is_dir() or paper_dir.name.startswith("."):
            continue

        arxiv_id = paper_dir.name.replace("arXiv-", "").replace("v1", "")
        console.print(f"  Checking {arxiv_id}...")

        try:
            paper = await get_paper_by_arxiv_id(arxiv_id)
            if not paper:
                table.add_row(paper_dir.name, "N/A", "[yellow]Not found on S2[/]")
                continue

            venue = paper.get("venue", "")
            pub_venue = paper.get("publicationVenue")
            if pub_venue and isinstance(pub_venue, dict):
                venue = pub_venue.get("name", venue)

            approved, matched = is_approved_venue(venue)
            if approved:
                table.add_row(paper_dir.name, matched or venue, "[green]✓ Approved[/]")
            else:
                table.add_row(paper_dir.name, venue or "N/A", "[red]✗ Not approved[/]")

            await asyncio.sleep(3)  # S2 rate limit: ~1 req/sec without API key
        except Exception as e:
            table.add_row(paper_dir.name, "Error", f"[red]{e}[/]")

    console.print(table)


async def cmd_download(args: argparse.Namespace) -> None:
    """Download PDFs for papers in refs/."""
    refs_dir = Path(args.refs_dir or OUTPUT_DIR)
    downloaded = 0
    failed = 0

    for paper_dir in sorted(refs_dir.iterdir()):
        if not paper_dir.is_dir() or paper_dir.name.startswith("."):
            continue

        pdf_path = paper_dir / "paper.pdf"
        if pdf_path.exists() and not args.force:
            continue

        arxiv_id = paper_dir.name.replace("arXiv-", "").replace("v1", "")

        if paper_dir.name.startswith("arXiv-"):
            console.print(f"  Downloading {arxiv_id}...")
            ok = await download_arxiv_pdf(arxiv_id, pdf_path)
            if ok:
                console.print(f"    [green]✓[/] {pdf_path}")
                downloaded += 1
            else:
                console.print(f"    [red]✗[/] Failed")
                failed += 1
            await asyncio.sleep(1)

        elif paper_dir.name.startswith("doi-") and args.use_proxy:
            doi = paper_dir.name.replace("doi-", "").replace("_", "/")
            console.print(f"  Downloading via proxy: {doi}...")
            ok = await download_via_fju_proxy(doi, pdf_path)
            if ok:
                console.print(f"    [green]✓[/] {pdf_path}")
                downloaded += 1
            else:
                console.print(f"    [red]✗[/] Proxy download failed")
                failed += 1

    console.print(f"\n[bold]Downloaded: {downloaded}, Failed: {failed}[/]")


def main() -> None:
    parser = argparse.ArgumentParser(description="Literature Fetcher for SkillSleep")
    sub = parser.add_subparsers(dest="command")

    p_search = sub.add_parser("search", help="Search for papers in approved venues")
    p_search.add_argument("--queries", nargs="+", help="Custom search queries")
    p_search.add_argument("--save", action="store_true", help="Save results to refs/")
    p_search.add_argument("--output", help="Output directory")

    p_verify = sub.add_parser("verify", help="Verify existing refs against venue list")
    p_verify.add_argument("--refs-dir", help="Refs directory path")

    p_download = sub.add_parser("download", help="Download PDFs for papers")
    p_download.add_argument("--refs-dir", help="Refs directory path")
    p_download.add_argument("--force", action="store_true", help="Re-download existing")
    p_download.add_argument("--use-proxy", action="store_true", help="Use FJU proxy for paywalled papers")

    args = parser.parse_args()

    if args.command == "search":
        asyncio.run(cmd_search(args))
    elif args.command == "verify":
        asyncio.run(cmd_verify(args))
    elif args.command == "download":
        asyncio.run(cmd_download(args))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
