#!/usr/bin/env python3
"""Validate GitHub Pages documentation before building the site."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]*]\((?P<target><[^>]+>|[^)\s]+)(?:\s+\"[^\"]*\")?\)")
FENCED_CODE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE = re.compile(r"`[^`]*`")
IGNORED_DIRECTORIES = {".git", ".venv", "site"}


def markdown_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if not any(part in IGNORED_DIRECTORIES for part in path.parts)
    )


def rendered_markdown(markdown: str) -> str:
    return INLINE_CODE.sub("", FENCED_CODE.sub("", markdown))


def validate_no_obsidian_syntax(paths: list[Path]) -> None:
    errors: list[str] = []
    for path in paths:
        markdown = rendered_markdown(path.read_text())
        if "[[" in markdown:
            errors.append(f"{path.relative_to(ROOT)} contains a Wiki link")
        if re.search(r"^> \[![A-Za-z0-9_-]+[+-]?", markdown, re.MULTILINE):
            errors.append(f"{path.relative_to(ROOT)} contains an Obsidian callout")
    if errors:
        raise RuntimeError("Unsupported Obsidian syntax:\n" + "\n".join(errors))


def is_external_link(target: str) -> bool:
    return target.startswith(("#", "//", "/")) or "://" in target or target.startswith(
        ("mailto:", "tel:")
    )


def validate_relative_links(paths: list[Path]) -> None:
    errors: list[str] = []
    for path in paths:
        markdown = rendered_markdown(path.read_text())
        for match in MARKDOWN_LINK.finditer(markdown):
            target = match.group("target").strip("<>")
            if is_external_link(target):
                continue
            target_path = target.split("#", maxsplit=1)[0]
            if not target_path:
                continue
            destination = (path.parent / target_path).resolve()
            if not destination.exists():
                errors.append(f"{path.relative_to(ROOT)} -> {target}")
    if errors:
        raise RuntimeError("Unresolved relative Markdown links:\n" + "\n".join(errors))


def main() -> None:
    paths = markdown_files()
    validate_no_obsidian_syntax(paths)
    validate_relative_links(paths)
    subprocess.run(
        [sys.executable, "-m", "mkdocs", "build", "--strict", "--config-file", "mkdocs.yml"],
        cwd=ROOT,
        check=True,
    )


if __name__ == "__main__":
    main()
