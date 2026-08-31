#!/usr/bin/env python3
"""Validate the consent interface rendered for the canonical website."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


SHORT_MESSAGE = (
    "We use optional analytics cookies to understand which documentation "
    "is useful and improve prodockit."
)


def validate_canonical_html(source: str) -> None:
    """Raise ValueError when source is not the canonical consent page."""

    normalised = " ".join(source.split())
    required = {
        "short consent message": SHORT_MESSAGE,
        "primary Accept control": (
            '<button class="md-button md-button--primary">Accept</button>'
        ),
        "secondary Manage settings control": (
            '<label class="md-button" for="__settings">Manage settings</label>'
        ),
        "default-selected Analytics cookie": (
            '<input type="checkbox" name="analytics" checked>'
        ),
        "consent-gated Analytics loader": (
            "consent&&consent.analytics&&__md_analytics()"
        ),
    }
    for name, fragment in required.items():
        if fragment not in normalised:
            raise ValueError(f"canonical output is missing the {name}")

    if re.search(r">\s*Reject\s*</(?:button|label)>", normalised):
        raise ValueError("canonical output still contains a Reject control")

    measurement_ids = set(
        re.findall(r"googletagmanager\.com/gtag/js\?id=(G-[A-Z0-9]+)", source)
    )
    if len(measurement_ids) != 1:
        raise ValueError("canonical output does not load exactly one GA4 tag")


def main() -> None:
    """Validate the rendered HTML file named on the command line."""

    parser = argparse.ArgumentParser()
    parser.add_argument("html", type=Path)
    arguments = parser.parse_args()
    try:
        validate_canonical_html(arguments.html.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        parser.exit(1, f"error: {error}\n")


if __name__ == "__main__":
    main()
