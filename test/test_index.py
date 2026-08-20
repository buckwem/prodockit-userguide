# Copyright (c) 2025-2026 Mark Buckwell and contributors
# SPDX-License-Identifier: MIT

"""Back-of-book index configuration and built-output regression checks."""

from __future__ import annotations

import re

import pytest


INDEX_TITLE = "Index"


def test_index_generation_is_configured_on_the_index_extension(prodockit_config):
    project = prodockit_config["project"]
    index_config = project["markdown_extensions"]["prodockit.index"]

    assert index_config["include"] is True
    assert index_config.get("title", INDEX_TITLE) == INDEX_TITLE
    assert "pdf_include_index" not in project.get("extra", {})
    assert "pdf_index_title" not in project.get("extra", {})


def _index_text(page_texts):
    """Return the index and only the index, located by its exact page title."""
    for page_number, text in enumerate(page_texts):
        lines = text.splitlines()
        if lines and lines[0].strip() == INDEX_TITLE:
            return "\n".join(page_texts[page_number:])
    pytest.fail(f"No PDF page begins with the exact title {INDEX_TITLE!r}")


def test_built_pdf_contains_representative_live_index_entries(prodockit_pdf_page_texts):
    index_text = _index_text(prodockit_pdf_page_texts)

    # Plain term, nested Parent!Child term, and code-styled term respectively.
    assert re.search(r"(?m)^merge conflict,\s*\d+", index_text)
    assert re.search(r"(?ms)^Git,\s*\d+\s*$.*?^ssh keys,\s*[\d, ]+$", index_text)
    assert re.search(r"(?m)^git commit\s*,\s*\d+", index_text)
