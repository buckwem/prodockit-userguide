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

# A rendered diagram contributes vector drawings, not text, so a Mermaid
# diagram-type keyword still present as text means the fenced ```mermaid
# block was passed through as a literal code block.
#
# The keyword alone is not enough to conclude that, though: line breaks in a
# PDF fall wherever the text happens to wrap, and several of these words are
# ordinary English. "...adds a visual commit graph and richer history
# browsing" in additionaltooling.md wrapped so that "graph" began a line,
# which a bare keyword check read as an unrendered diagram - green locally,
# failing in CI purely because different fonts there wrapped the line
# differently.
#
# So require a diagram-type keyword *and* Mermaid's own link syntax shortly
# after it: an unrendered fence dumps the whole block, so the arrows are
# always there, while prose that happens to start a line with "graph" has
# nothing resembling them.
_MERMAID_KEYWORD_RE = re.compile(
    r"^\s*(graph|flowchart|sequenceDiagram|stateDiagram(?:-v2)?|classDiagram|erDiagram|"
    r"gantt|journey|pie|gitGraph|mindmap|timeline)\b",
)
_MERMAID_LINK_RE = re.compile(r"--+>|--+\||-\.->|==+>|->>|--\s*$")
# How far after the keyword line to look for that syntax - a diagram's first
# link is on the very next line in practice; a few lines of slack covers a
# declaration or comment in between.
_MERMAID_LOOKAHEAD_LINES = 6


def find_literal_mermaid_source(text):
    """Returns True if `text` (one PDF page) looks like it contains a
    Mermaid block that was never rendered."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if not _MERMAID_KEYWORD_RE.match(line):
            continue
        window = lines[i : i + 1 + _MERMAID_LOOKAHEAD_LINES]
        if any(_MERMAID_LINK_RE.search(candidate) for candidate in window):
            return True
    return False

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
    offenders = [i for i, text in enumerate(pdf_page_texts) if find_literal_mermaid_source(text)]
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


def test_prose_that_merely_starts_a_line_with_a_diagram_keyword_is_not_flagged():
    """Regression test for the false positive that broke the first CI run of
    this suite: additionaltooling.md's "a visual commit graph and richer
    history browsing" wrapped, in CI's fonts, so that "graph" began a line.
    A keyword-only check read that as an unrendered diagram - and passed
    locally, where the same sentence wrapped elsewhere."""
    wrapped_prose = (
        "annotations - showing who last changed each line, and when -\n"
        "directly above your text, along with a visual commit\n"
        "graph and richer history browsing. It's especially useful once\n"
        "you're using the branches and issues workflow.\n"
    )
    assert not find_literal_mermaid_source(wrapped_prose)


def test_a_genuinely_unrendered_block_is_still_flagged():
    """The other half of the pair above - narrowing the check must not have
    cost it the failure it exists to catch."""
    unrendered = (
        "the page:\n"
        "graph LR\n"
        "  A[Start] --> B{Error?};\n"
        "  B -->|Yes| C[Hmm...];\n"
    )
    assert find_literal_mermaid_source(unrendered)
