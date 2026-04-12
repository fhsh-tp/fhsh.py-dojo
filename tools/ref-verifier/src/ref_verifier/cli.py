"""CLI entry point for ref-verifier."""

import asyncio
import argparse
from pathlib import Path

import httpx

from .parser import load_all_papers, PaperMeta
from .apis import fetch_paper_by_arxiv, fetch_paper_by_doi, S2Paper
from .checker import verify_paper, VerifyResult
from .report import print_terminal_report, write_markdown_report, write_json_report

DEFAULT_REFS = Path(__file__).parent.parent.parent / ".." / ".." / "refs"
# Concurrency: 3 parallel requests (S2 rate limit ~1/sec, with 3s delay per request)
CONCURRENCY = 3


async def fetch_one(
    paper: PaperMeta,
    client: httpx.AsyncClient,
    semaphore: asyncio.Semaphore,
) -> tuple[PaperMeta, S2Paper]:
    """Fetch S2 data for a single paper."""
    if paper.arxiv_id and paper.arxiv_id != "N/A":
        s2 = await fetch_paper_by_arxiv(client, paper.arxiv_id, semaphore)
    elif paper.doi and paper.doi != "N/A":
        s2 = await fetch_paper_by_doi(client, paper.doi, semaphore)
    else:
        s2 = S2Paper(error="no_identifier")
    return paper, s2


async def run_verify(refs_dir: Path, output_dir: Path) -> list[VerifyResult]:
    """Main async verification loop."""
    papers = load_all_papers(refs_dir)
    print(f"Loaded {len(papers)} papers from {refs_dir}\n")

    semaphore = asyncio.Semaphore(CONCURRENCY)
    results: list[VerifyResult] = []

    async with httpx.AsyncClient(timeout=30) as client:
        # Create tasks for all papers
        tasks = [fetch_one(p, client, semaphore) for p in papers]

        # Execute with progress
        for i, coro in enumerate(asyncio.as_completed(tasks)):
            paper, s2 = await coro
            result = verify_paper(paper, s2)
            results.append(result)

            # Progress indicator
            status = result.status.value
            issues_count = len(result.issues)
            print(
                f"  [{i+1}/{len(papers)}] {paper.dir_name:40s} "
                f"{status}"
                f"{f'  ({issues_count} issues)' if issues_count else ''}"
            )

    # Sort results: errors first, then warnings, then info, then OK
    severity_order = {"🔴 ERROR": 0, "🟠 WARNING": 1, "🟡 INFO": 2, "✅ OK": 3}
    results.sort(key=lambda r: severity_order.get(r.status.value, 99))

    # Generate reports
    print_terminal_report(results)
    write_markdown_report(results, output_dir / "verification-report.md")
    write_json_report(results, output_dir / "verification-report.json")

    return results


def main():
    parser = argparse.ArgumentParser(description="Verify paper metadata against Semantic Scholar")
    sub = parser.add_subparsers(dest="command")

    # Original: verify refs/ directory
    p_refs = sub.add_parser("verify-refs", help="Verify refs/ directory papers")
    p_refs.add_argument("--refs-dir", type=Path, default=None)
    p_refs.add_argument("--output-dir", type=Path, default=None)

    # New: verify inline markdown references
    p_inline = sub.add_parser("verify-inline", help="Verify inline markdown references")
    p_inline.add_argument("--input", type=Path, required=True, help="Path to reference.md")
    p_inline.add_argument("--output", type=Path, default=None, help="Output directory for report")

    args = parser.parse_args()

    if args.command == "verify-inline":
        from .verify_inline import run_verify_inline
        input_path = args.input
        if not input_path.exists():
            print(f"Error: file not found: {input_path}")
            return
        output_dir = args.output or input_path.parent
        output_dir.mkdir(parents=True, exist_ok=True)
        asyncio.run(run_verify_inline(input_path, output_dir))
    else:
        # Default: original refs/ directory verification
        refs_dir = getattr(args, "refs_dir", None) or DEFAULT_REFS.resolve()
        output_dir = getattr(args, "output_dir", None) or refs_dir

        if not refs_dir.exists():
            print(f"Error: refs directory not found: {refs_dir}")
            return

        output_dir.mkdir(parents=True, exist_ok=True)
        asyncio.run(run_verify(refs_dir, output_dir))


if __name__ == "__main__":
    main()
