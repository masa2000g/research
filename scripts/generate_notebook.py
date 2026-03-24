#!/usr/bin/env python3
"""
generate_notebook.py — Convert a research report.md into a Jupyter notebook (.ipynb).

Usage:
    python scripts/generate_notebook.py topics/<topic-slug>/report.md
    python scripts/generate_notebook.py topics/<topic-slug>/report.md --output topics/<topic-slug>/notebook.ipynb

Each top-level section (## heading) becomes a Markdown cell.
Fenced code blocks with a language tag become code cells.
Mermaid diagrams are preserved as markdown cells with the fenced block intact.
"""

import argparse
import json
import re
import sys
import uuid
from pathlib import Path


def new_cell_id() -> str:
    return uuid.uuid4().hex[:8]


def make_markdown_cell(source: str) -> dict:
    return {
        "cell_type": "markdown",
        "id": new_cell_id(),
        "metadata": {},
        "source": source.rstrip("\n"),
    }


def make_code_cell(source: str, language: str = "python") -> dict:
    return {
        "cell_type": "code",
        "id": new_cell_id(),
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source.rstrip("\n"),
    }


def split_into_sections(text: str) -> list[tuple[str, str]]:
    """
    Split markdown text into (heading, body) pairs.
    The heading is the ## line (or '' for content before the first heading).
    Returns a list of raw section strings.
    """
    # Split on lines that start with ## (but not ###)
    pattern = re.compile(r"^(#{1,2} .+)$", re.MULTILINE)
    parts = pattern.split(text)

    sections: list[str] = []
    if parts[0].strip():
        sections.append(parts[0])  # content before first heading

    i = 1
    while i < len(parts):
        heading = parts[i]
        body = parts[i + 1] if i + 1 < len(parts) else ""
        sections.append(heading + "\n" + body)
        i += 2

    return sections


def parse_section_to_cells(section: str) -> list[dict]:
    """
    Parse a single markdown section into one or more notebook cells.

    Rules:
    - Fenced code blocks tagged with 'python' become code cells.
    - Everything else (including mermaid blocks) stays as markdown.
    """
    cells: list[dict] = []

    # Regex to find fenced code blocks: ```lang\n...\n```
    fence_pattern = re.compile(r"```(\w+)?\n(.*?)```", re.DOTALL)

    last_end = 0
    for match in fence_pattern.finditer(section):
        lang = (match.group(1) or "").lower()
        code_body = match.group(2)

        # Emit any markdown before this code block
        before = section[last_end : match.start()]
        if before.strip():
            cells.append(make_markdown_cell(before))

        if lang == "python":
            cells.append(make_code_cell(code_body, language="python"))
        else:
            # Keep as markdown (mermaid, bash, json, etc.)
            cells.append(make_markdown_cell(match.group(0)))

        last_end = match.end()

    # Remaining markdown after last code block
    remainder = section[last_end:]
    if remainder.strip():
        cells.append(make_markdown_cell(remainder))

    return cells


def report_to_notebook(report_path: Path) -> dict:
    text = report_path.read_text(encoding="utf-8")

    # Build a title cell from the filename / first H1
    title_match = re.search(r"^# (.+)$", text, re.MULTILINE)
    title = title_match.group(1) if title_match else report_path.stem

    cells: list[dict] = []

    sections = split_into_sections(text)
    for section in sections:
        section_cells = parse_section_to_cells(section)
        cells.extend(section_cells)

    notebook = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.10.0",
            },
            "title": title,
        },
        "cells": cells,
    }
    return notebook


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert a research report.md into a Jupyter notebook."
    )
    parser.add_argument("report", type=Path, help="Path to report.md")
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="Output path for the .ipynb file (default: same directory as report, named notebook.ipynb)",
    )
    args = parser.parse_args()

    report_path: Path = args.report
    if not report_path.exists():
        print(f"Error: {report_path} not found.", file=sys.stderr)
        sys.exit(1)

    output_path: Path = args.output or report_path.parent / "notebook.ipynb"

    notebook = report_to_notebook(report_path)

    output_path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Notebook written to {output_path}")
    print(f"  Cells: {len(notebook['cells'])}")


if __name__ == "__main__":
    main()
