# Copyright (c) 2026 Mark Buckwell and contributors
# SPDX-License-Identifier: MIT

"""The canonical guide must use collision-safe Prodockit macro names."""

import re
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEGACY_NAMES = re.compile(
    r"\{\{\s*(?:heading_counter_reset|reference_style|acronym_style|"
    r"glossary_style|word_count|repo_url|applied_release)\b"
)


def test_canonical_and_surrey_markdown_use_only_prefixed_prodockit_macros() -> None:
    for docs in (ROOT / "docs", ROOT / "surrey-source" / "docs"):
        for page in docs.rglob("*.md"):
            assert LEGACY_NAMES.search(page.read_text(encoding="utf-8")) is None, page


def test_reference_style_setting_is_retained() -> None:
    config = tomllib.loads((ROOT / "zensical.toml").read_text(encoding="utf-8"))
    assert config["project"]["extra"]["reference_style"] == "european"
