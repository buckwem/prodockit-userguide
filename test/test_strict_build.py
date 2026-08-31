# Copyright (c) 2025-2026 Mark Buckwell and contributors
# SPDX-License-Identifier: MIT

"""Keep the documented and deployed website build strict (issue #141)."""

from __future__ import annotations

import re
import shlex
from pathlib import Path

from prodockit.template_sync import read_config

REPO_ROOT = Path(__file__).resolve().parent.parent
STRICT_BUILD = "zensical build --clean --strict"


def _contains_command(contents):
    command = re.compile(r"(?m)^\s*-\s+(?:run:\s+)?(zensical build\b[^\n]*)$")
    for match in command.finditer(contents):
        arguments = shlex.split(match.group(1))
        if arguments[:2] == ["zensical", "build"] and {
            "--clean",
            "--strict",
        }.issubset(arguments):
            return True
    return False


def _top_level_section(contents, name):
    """Extract one top-level YAML section without needing a YAML dependency."""
    lines = contents.splitlines()
    start = lines.index(f"{name}:")
    end = len(lines)
    for line_number in range(start + 1, len(lines)):
        line = lines[line_number]
        if line and not line[0].isspace() and not line.startswith("#"):
            end = line_number
            break
    return "\n".join(lines[start:end])


def test_github_pages_workflow_uses_the_strict_build():
    workflow = REPO_ROOT / ".github" / "workflows" / "docs.yml"
    contents = workflow.read_text(encoding="utf-8")
    assert _contains_command(contents)
    assert contents.index("zensical build --clean --strict") < contents.index(
        "run: prodockit pdf"
    )


def test_gitlab_pages_job_uses_the_strict_build():
    workflow = REPO_ROOT / ".gitlab-ci.yml"
    pages_job = _top_level_section(workflow.read_text(encoding="utf-8"), "pages")
    assert _contains_command(pages_job)
    assert pages_job.index("zensical build --clean --strict") < pages_job.index(
        "prodockit pdf"
    )


def test_contributing_builds_the_strict_site_before_the_pdf():
    contents = (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    assert f"`{STRICT_BUILD}`" in contents
    assert "run `zensical build --clean --strict`, then `prodockit pdf`" in contents


def test_macro_rendering_errors_also_stop_non_strict_builds():
    config = read_config((REPO_ROOT / "zensical.toml").read_text(encoding="utf-8"))
    macros = config["project"]["markdown_extensions"]["zensical"]["extensions"][
        "macros"
    ]
    guide = (REPO_ROOT / "docs" / "customise.md").read_text(encoding="utf-8")

    assert macros["on_error_fail"] is True
    assert "allowing a broken site to be published" in guide
    assert "https://prodockit.org/macros/" in guide
