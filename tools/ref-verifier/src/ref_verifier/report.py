"""Generate verification report in Markdown and terminal output."""

import json
from datetime import datetime, timezone
from pathlib import Path

from rich.console import Console
from rich.table import Table

from .checker import VerifyResult, Severity

console = Console()


def print_terminal_report(results: list[VerifyResult]):
    """Print a summary table to terminal using rich."""
    errors = [r for r in results if r.status == Severity.ERROR]
    warnings = [r for r in results if r.status == Severity.WARNING]
    infos = [r for r in results if r.status == Severity.INFO]
    oks = [r for r in results if r.status == Severity.OK]

    console.print(f"\n[bold]Verification Report — {len(results)} papers[/bold]\n")
    console.print(f"  ✅ OK: {len(oks)}  |  🟡 Info: {len(infos)}  |  🟠 Warning: {len(warnings)}  |  🔴 Error: {len(errors)}\n")

    if errors or warnings:
        table = Table(title="Issues Found")
        table.add_column("Severity", width=12)
        table.add_column("Paper", max_width=35)
        table.add_column("Field", width=12)
        table.add_column("Message", max_width=60)

        for r in errors + warnings + infos:
            for issue in r.issues:
                table.add_row(
                    issue.severity.value,
                    r.paper.dir_name[:35],
                    issue.field,
                    issue.message[:60],
                )

        console.print(table)


def write_markdown_report(results: list[VerifyResult], output_path: Path):
    """Write a detailed Markdown report."""
    errors = [r for r in results if r.status == Severity.ERROR]
    warnings = [r for r in results if r.status == Severity.WARNING]
    infos = [r for r in results if r.status == Severity.INFO]
    oks = [r for r in results if r.status == Severity.OK]

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    lines = [
        "# Reference Verification Report",
        "",
        f"> Generated: {now}",
        f"> Papers checked: {len(results)}",
        f"> ✅ OK: {len(oks)} | 🟡 Info: {len(infos)} | 🟠 Warning: {len(warnings)} | 🔴 Error: {len(errors)}",
        "",
    ]

    if errors:
        lines.append("## 🔴 Errors (require immediate fix)")
        lines.append("")
        for r in errors:
            _append_paper_section(lines, r)

    if warnings:
        lines.append("## 🟠 Warnings (need investigation)")
        lines.append("")
        for r in warnings:
            _append_paper_section(lines, r)

    if infos:
        lines.append("## 🟡 Info (minor inconsistencies)")
        lines.append("")
        for r in infos:
            _append_paper_section(lines, r)

    lines.append("## ✅ Verified OK")
    lines.append("")
    lines.append("| # | Directory | Title | Venue (local) | S2 Venue | S2 Year |")
    lines.append("|---|-----------|-------|---------------|----------|---------|")
    for i, r in enumerate(oks, 1):
        s2v = r.s2.pub_venue_name or r.s2.venue or "N/A"
        lines.append(
            f"| {i} | `{r.paper.dir_name}` | {r.paper.title[:50]} | {r.paper.venue[:30]} | {s2v[:30]} | {r.s2.year or 'N/A'} |"
        )
    lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    console.print(f"\n[green]Report written to {output_path}[/green]")


def write_json_report(results: list[VerifyResult], output_path: Path):
    """Write machine-readable JSON report."""
    data = []
    for r in results:
        entry = {
            "dir_name": r.paper.dir_name,
            "title": r.paper.title,
            "status": r.status.value,
            "local": {
                "year": r.paper.claimed_year,
                "venue": r.paper.venue,
                "arxiv_id": r.paper.arxiv_id,
                "doi": r.paper.doi,
                "approved_venue": r.paper.approved_venue,
            },
            "s2": {
                "year": r.s2.year,
                "venue": r.s2.venue,
                "pub_venue_name": r.s2.pub_venue_name,
                "pub_venue_type": r.s2.pub_venue_type,
                "arxiv_id": r.s2.arxiv_id,
                "doi": r.s2.doi,
                "error": r.s2.error,
            },
            "issues": [
                {
                    "severity": i.severity.value,
                    "field": i.field,
                    "message": i.message,
                    "local_value": i.local_value,
                    "s2_value": i.s2_value,
                }
                for i in r.issues
            ],
        }
        data.append(entry)

    output_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    console.print(f"[green]JSON report written to {output_path}[/green]")


def _append_paper_section(lines: list[str], r: VerifyResult):
    """Append a paper's issues as a Markdown section."""
    lines.append(f"### `{r.paper.dir_name}`")
    lines.append(f"**{r.paper.title}**")
    lines.append("")
    lines.append(f"- Local venue: `{r.paper.venue}`")
    lines.append(f"- Local year: `{r.paper.claimed_year}`")
    lines.append(f"- S2 venue: `{r.s2.pub_venue_name or r.s2.venue}`")
    lines.append(f"- S2 year: `{r.s2.year}`")
    if r.paper.arxiv_id:
        lines.append(f"- arXiv: `{r.paper.arxiv_id}`")
    if r.s2.doi:
        lines.append(f"- DOI: `{r.s2.doi}`")
    lines.append("")
    for issue in r.issues:
        lines.append(f"**{issue.severity.value}** `{issue.field}`: {issue.message}")
        if issue.local_value:
            lines.append(f"  - Local: `{issue.local_value}`")
        if issue.s2_value:
            lines.append(f"  - S2: `{issue.s2_value}`")
        lines.append("")
    lines.append("---")
    lines.append("")
