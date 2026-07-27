# Copyright (c) 2025-2026 Mark Buckwell and contributors
# SPDX-License-Identifier: MIT

"""Shared fixtures for this project's test suite.

These tests check the *built output* - the PDF at
docs/site_documentation.pdf - not the build process itself. Build first,
then run them:

    prodockit pdf
    python -m pytest test/

See issue #23 for why this suite exists: Mermaid diagrams and TeX maths
render client-side on the website but must be pre-rendered to images for
the PDF, and prodockit.pdf deliberately degrades silently when the
renderers aren't installed - so a missing tools/ directory produced a PDF
full of raw diagram and LaTeX source with nothing failing to signal it.
"""

import tomllib
from pathlib import Path

import fitz
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = REPO_ROOT / "docs" / "site_documentation.pdf"
ZENSICAL_TOML_PATH = REPO_ROOT / "zensical.toml"


@pytest.fixture(scope="session")
def zensical_config():
    if not ZENSICAL_TOML_PATH.exists():
        pytest.fail("zensical.toml not found at repo root")
    with open(ZENSICAL_TOML_PATH, "rb") as f:
        return tomllib.load(f)


@pytest.fixture(scope="session")
def pdf_doc():
    if not PDF_PATH.exists():
        pytest.fail(
            f"{PDF_PATH} not found - run `prodockit pdf` before running the test suite"
        )
    doc = fitz.open(PDF_PATH)
    if doc.page_count == 0:
        pytest.fail(f"{PDF_PATH} opened but has no pages")
    yield doc
    doc.close()


@pytest.fixture(scope="session")
def pdf_page_texts(pdf_doc):
    """The whole PDF's text, one string per page, in page order."""
    return [page.get_text() for page in pdf_doc]
