# Copyright (c) 2025-2026 Mark Buckwell and contributors
# SPDX-License-Identifier: MIT

"""Guards against Mermaid diagrams and TeX maths silently reaching the PDF
as raw source instead of rendered images (issue #23).

WeasyPrint has no JS engine, so unlike the website - which renders both
client-side via Mermaid.js and MathJax - the PDF build shells out to
mermaid-cli and mathjax-full to pre-render them to static images.
prodockit.pdf deliberately leaves the content unrendered rather than
failing the build when those aren't found, which is the right default for
a project that uses neither, but means a project that *does* use them gets
a quietly broken PDF and no error.

The detection itself now comes from `prodockit.testing`, and the fixtures
from its pytest plugin (issue #27). This file previously carried its own
copy of both. That copy matched only arrow syntax, so an unrendered
entity-relationship diagram - whose `||--o{` cardinality syntax has no
arrowhead at all - would have passed silently; the library version handles
it. What remains here is the part that is genuinely specific to this
project: which fences it configures, and the actual diagram on its own
Diagrams page.
"""

import pytest
from prodockit.pdf.config import _find_mmdc_bin, _find_tex2svg_script
from prodockit.testing import (
    assert_no_unrendered_mermaid,
    assert_no_unrendered_tex,
    contains_unrendered_mermaid,
)


def _fence_is_configured(config, fence_name):
    extensions = config.get("project", {}).get("markdown_extensions", {})
    fences = extensions.get("pymdownx", {}).get("superfences", {}).get("custom_fences", [])
    return any(fence.get("name") == fence_name for fence in fences)


def _arithmatex_is_configured(config):
    extensions = config.get("project", {}).get("markdown_extensions", {})
    return "arithmatex" in extensions.get("pymdownx", {})


# --- Config vs tooling: fails fast, and names the cause --------------------


def test_mermaid_renderer_is_available_when_the_mermaid_fence_is_configured(prodockit_config):
    """Fails fast, and names the cause, when tools/mermaid isn't installed -
    rather than leaving it to be inferred from odd-looking PDF content."""
    if not _fence_is_configured(prodockit_config, "mermaid"):
        pytest.skip("no mermaid custom fence configured in zensical.toml")
    assert _find_mmdc_bin(None) is not None, (
        "zensical.toml configures the mermaid fence, but no mmdc binary was found - "
        "run `prodockit init-tools` and `npm ci --prefix tools/mermaid`, or Mermaid "
        "diagrams will silently render as raw source in the PDF (issue #23)"
    )


def test_maths_renderer_is_available_when_arithmatex_is_configured(prodockit_config):
    if not _arithmatex_is_configured(prodockit_config):
        pytest.skip("pymdownx.arithmatex not configured in zensical.toml")
    assert _find_tex2svg_script(None) is not None, (
        "zensical.toml enables pymdownx.arithmatex, but no tex2svg script was found - "
        "run `prodockit init-tools` and `npm ci --prefix tools/mathjax`, or maths will "
        "silently render as raw LaTeX in the PDF (issue #23)"
    )


# --- The built PDF ---------------------------------------------------------


def test_no_page_contains_literal_mermaid_source(prodockit_pdf_page_texts):
    assert_no_unrendered_mermaid(prodockit_pdf_page_texts)


def test_no_page_contains_literal_tex_source(prodockit_pdf_page_texts):
    assert_no_unrendered_tex(prodockit_pdf_page_texts)


# The node labels of the flowchart in zensicalbasics.md's Diagrams section.
# mermaid-cli is run with htmlLabels off (WeasyPrint can't render Mermaid's
# default <foreignObject> labels), so a rendered diagram puts these into the
# PDF as real SVG <text> - which is what makes them assertable here.
DIAGRAM_NODE_LABELS = ("Start", "Error?", "Debug", "Yay!")


def test_the_diagrams_section_diagram_is_actually_present(prodockit_pdf):
    """Counterpart to the literal-source checks above, which on their own
    would still pass if the diagram vanished from the PDF entirely instead
    of rendering as text.

    Deliberately not `page.get_images()`: a Mermaid diagram is embedded as
    an SVG and rasterises to *vector drawings*, not a raster image, so that
    check passes or fails on whatever unrelated images (emoji, icons) happen
    to share the page - it would have reported success here even with the
    diagram missing.

    Located by the diagram's own content rather than by surrounding prose:
    several pages mention "Mermaid" and "Diagrams" without containing it.
    """
    for page in prodockit_pdf:
        text = page.get_text()
        if all(label in text for label in DIAGRAM_NODE_LABELS):
            assert page.get_drawings(), (
                "The flowchart's node labels are present but the page has no vector "
                "drawings - its boxes and arrows did not render"
            )
            return
    pytest.fail(
        f"No PDF page contains all of the flowchart's node labels {DIAGRAM_NODE_LABELS} - "
        "the diagram is absent from the PDF rather than merely unrendered"
    )


# --- The false positive that broke a real CI run ---------------------------
#
# Kept here rather than left to the library's own suite: it is this
# project's prose that triggered it, and this project's build that broke.


def test_prose_that_merely_starts_a_line_with_a_diagram_keyword_is_not_flagged():
    """additionaltooling.md's "a visual commit graph and richer history
    browsing" wrapped, in CI's fonts, so that "graph" began a line. A
    keyword-only check read that as an unrendered diagram - and passed
    locally, where the same sentence wrapped elsewhere."""
    wrapped_prose = (
        "annotations - showing who last changed each line, and when -\n"
        "directly above your text, along with a visual commit\n"
        "graph and richer history browsing. It's especially useful once\n"
        "you're using the branches and issues workflow.\n"
    )
    assert not contains_unrendered_mermaid(wrapped_prose)


def test_a_genuinely_unrendered_block_is_still_flagged():
    """The other half of the pair above - narrowing the check must not have
    cost it the failure it exists to catch."""
    unrendered = (
        "the page:\n"
        "graph LR\n"
        "  A[Start] --> B{Error?};\n"
        "  B -->|Yes| C[Hmm...];\n"
    )
    assert contains_unrendered_mermaid(unrendered)
