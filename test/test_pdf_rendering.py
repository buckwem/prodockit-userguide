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

Two layers here: the config-vs-tooling checks fail fast and name the cause
directly, and the built-output checks catch anything that still slips
through to the finished PDF.
"""

import re

import pytest
from prodockit.pdf.config import _find_mmdc_bin, _find_tex2svg_script

# A rendered diagram contributes an image, not text, so any of these
# appearing at the start of a line in the finished PDF means the fenced
# ```mermaid block was passed through as a literal code block.
MERMAID_SOURCE_RE = re.compile(
    r"^\s*(graph|flowchart|sequenceDiagram|stateDiagram(?:-v2)?|classDiagram|erDiagram|"
    r"gantt|journey|pie|gitGraph|mindmap|timeline)\b",
    re.MULTILINE,
)

# Likewise for maths: rendered output is an image, so a surviving TeX
# delimiter or command means the formula was never pre-rendered.
TEX_SOURCE_RE = re.compile(r"\\\[|\\\]|\\sum_|\\frac\{|\\infty|\\begin\{")


def _fence_is_configured(zensical_config, fence_name):
    extensions = zensical_config.get("project", {}).get("markdown_extensions", {})
    fences = extensions.get("pymdownx", {}).get("superfences", {}).get("custom_fences", [])
    return any(fence.get("name") == fence_name for fence in fences)


def _arithmatex_is_configured(zensical_config):
    extensions = zensical_config.get("project", {}).get("markdown_extensions", {})
    return "arithmatex" in extensions.get("pymdownx", {})


def test_mermaid_renderer_is_available_when_the_mermaid_fence_is_configured(zensical_config):
    """Fails fast, and names the cause, when tools/mermaid isn't installed -
    rather than leaving it to be inferred from odd-looking PDF content."""
    if not _fence_is_configured(zensical_config, "mermaid"):
        pytest.skip("no mermaid custom fence configured in zensical.toml")
    assert _find_mmdc_bin(None) is not None, (
        "zensical.toml configures the mermaid fence, but no mmdc binary was found - "
        "run `npm ci --prefix tools/mermaid`, or Mermaid diagrams will silently "
        "render as raw source in the PDF (issue #23)"
    )


def test_maths_renderer_is_available_when_arithmatex_is_configured(zensical_config):
    if not _arithmatex_is_configured(zensical_config):
        pytest.skip("pymdownx.arithmatex not configured in zensical.toml")
    assert _find_tex2svg_script(None) is not None, (
        "zensical.toml enables pymdownx.arithmatex, but no tex2svg script was found - "
        "run `npm ci --prefix tools/mathjax`, or maths will silently render as raw "
        "LaTeX in the PDF (issue #23)"
    )


def test_no_page_contains_literal_mermaid_source(pdf_page_texts):
    offenders = [i for i, text in enumerate(pdf_page_texts) if MERMAID_SOURCE_RE.search(text)]
    assert not offenders, (
        f"Literal Mermaid source found on PDF page(s) {offenders} - the diagram was "
        "passed through as a code block instead of being pre-rendered to an image"
    )


def test_no_page_contains_literal_tex_source(pdf_page_texts):
    offenders = [i for i, text in enumerate(pdf_page_texts) if TEX_SOURCE_RE.search(text)]
    assert not offenders, (
        f"Literal TeX source found on PDF page(s) {offenders} - the formula was not "
        "pre-rendered to an image"
    )


# The node labels of the flowchart in zensicalbasics.md's Diagrams section.
# mermaid-cli is run with htmlLabels off (WeasyPrint can't render Mermaid's
# default <foreignObject> labels), so a rendered diagram puts these into the
# PDF as real SVG <text> - which is what makes them assertable here.
DIAGRAM_NODE_LABELS = ("Start", "Error?", "Debug", "Yay!")


def test_the_diagrams_section_diagram_is_actually_present(pdf_doc):
    """Counterpart to the literal-source checks above, which on their own
    would still pass if the diagram vanished from the PDF entirely instead
    of rendering as text.

    Deliberately not `page.get_images()`: a Mermaid diagram is embedded as
    an SVG and rasterises to *vector drawings*, not a raster image, so that
    check passes or fails on whatever unrelated images (emoji, icons) happen
    to share the page - it would have reported success here even with the
    diagram missing.
    """
    # Located by the diagram's own content rather than by the surrounding
    # prose: several pages mention "Mermaid" and "Diagrams" (the Markdown
    # chapter cross-references the section, and it appears in the contents),
    # so matching on those words finds the wrong page.
    for page in pdf_doc:
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
