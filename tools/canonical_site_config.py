#!/usr/bin/env python3
"""Create the private configuration used only for docs.prodockit.org.

The committed Zensical configuration remains reusable and analytics-free.
The canonical GitHub Pages workflow supplies its Google Analytics measurement
ID through a repository secret and writes the resulting temporary
configuration outside version control.
"""

from __future__ import annotations

import argparse
import re
import tomllib
from pathlib import Path


MEASUREMENT_ID = re.compile(r"G-[A-Z0-9]+")
ANALYTICS_CONFIG = '''

# Added by tools/canonical_site_config.py for the canonical deployment only.
[project.extra.analytics]
provider = "google"
property = {measurement_id}

[project.extra.consent]
title = "Cookie consent"
description = """
  We use optional analytics cookies to understand which documentation is useful
  and improve prodockit.
"""
actions = ["accept", "manage"]

[project.extra.consent.cookies]
analytics.name = "Google Analytics"
analytics.checked = true
'''


def with_canonical_analytics(source: str, measurement_id: str) -> str:
    """Return an analytics-enabled canonical copy of *source*."""

    if not MEASUREMENT_ID.fullmatch(measurement_id):
        raise ValueError(
            "GOOGLE_ANALYTICS_ID must be a GA4 measurement ID such as G-ABC123"
        )

    source_config = tomllib.loads(source)
    source_extra = source_config.get("project", {}).get("extra", {})
    if "analytics" in source_extra or "consent" in source_extra:
        raise ValueError(
            "source configuration already contains analytics or consent; "
            "keep the committed configuration reusable and analytics-free"
        )

    generated = (
        source.rstrip()
        + "\n"
        + ANALYTICS_CONFIG.format(measurement_id=repr(measurement_id))
    )
    extra = tomllib.loads(generated)["project"]["extra"]
    consent = extra["consent"]
    if extra["analytics"]["property"] != measurement_id:
        raise ValueError("the generated analytics configuration did not validate")
    if consent["actions"] != ["accept", "manage"]:
        raise ValueError("canonical consent must offer only accept and manage")
    if consent["cookies"]["analytics"]["checked"] is not True:
        raise ValueError("analytics must be selected when a visitor accepts cookies")
    return generated


def write_config(
    source_path: Path, destination_path: Path, measurement_id: str
) -> None:
    """Write and validate the canonical website configuration."""

    destination_path.write_text(
        with_canonical_analytics(
            source_path.read_text(encoding="utf-8"), measurement_id
        ),
        encoding="utf-8",
    )


def main() -> None:
    """Generate the configuration named on the command line."""

    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("measurement_id")
    arguments = parser.parse_args()
    try:
        write_config(arguments.source, arguments.destination, arguments.measurement_id)
    except (OSError, KeyError, ValueError, tomllib.TOMLDecodeError) as error:
        parser.exit(1, f"error: {error}\n")


if __name__ == "__main__":
    main()
