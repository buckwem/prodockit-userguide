#!/usr/bin/env python3
"""Write a Zensical configuration without public-site analytics.

The public User Guide uses consent-gated analytics. Its University of Surrey
GitLab mirror must not load analytics or display a consent interface, so that
pipeline builds from the generated configuration written by this tool.
"""

from __future__ import annotations

import argparse
import re
import tomllib
from pathlib import Path


TABLE_HEADER = re.compile(r"^\s*\[([^]]+)]\s*(?:#.*)?$")


def without_analytics(source: str) -> str:
    """Remove the analytics and consent tables from Zensical TOML text."""

    output: list[str] = []
    skipping = False
    for line in source.splitlines(keepends=True):
        match = TABLE_HEADER.match(line)
        if match:
            table = match.group(1).strip()
            skipping = table == "project.extra.analytics" or (
                table == "project.extra.consent"
                or table.startswith("project.extra.consent.")
            )
        if not skipping:
            output.append(line)
    return "".join(output)


def write_config(source_path: Path, destination_path: Path) -> None:
    """Write and validate the analytics-free configuration."""

    generated = without_analytics(source_path.read_text(encoding="utf-8"))
    parsed = tomllib.loads(generated)
    extra = parsed.get("project", {}).get("extra", {})
    if "analytics" in extra or "consent" in extra:
        raise ValueError("generated Surrey configuration still enables analytics")
    destination_path.write_text(generated, encoding="utf-8")


def main() -> None:
    """Generate the configuration named on the command line."""

    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    arguments = parser.parse_args()
    write_config(arguments.source, arguments.destination)


if __name__ == "__main__":
    main()
