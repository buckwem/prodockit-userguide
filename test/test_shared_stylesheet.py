# Copyright (c) 2026 Mark Buckwell and contributors
# SPDX-License-Identifier: MIT

"""Managed website, PDF, and JavaScript assets follow Prodockit."""

from pathlib import Path

import pytest
from click.testing import CliRunner

from prodockit.cli import main
from prodockit.shared_files import MANIFEST, inspect


ROOT = Path(__file__).resolve().parents[1]


def test_shared_assets_match_the_installed_release() -> None:
    states = inspect(ROOT)

    assert [state.file.source for state in states] == [
        "pdk.css",
        "pdk-pdf.css",
        "pdk.js",
    ]
    assert [state.file.target for state in states] == [
        "docs/stylesheets/pdk.css",
        "docs/stylesheets/pdk-pdf.css",
        "docs/javascripts/pdk.js",
    ]
    assert all(state.status == "current" for state in states)


def test_javascript_assets_have_the_required_ownership_and_order() -> None:
    config = (ROOT / "zensical.toml").read_text(encoding="utf-8")
    managed = '"javascripts/pdk.js"'
    mathjax_config = '"javascripts/mathjax.js"'
    mathjax_bundle = '"javascripts/vendor/mathjax/tex-svg-full.js"'
    user_managed = '"javascripts/extra.js"'

    assert config.index(managed) < config.index(mathjax_config)
    assert config.index(mathjax_config) < config.index(mathjax_bundle)
    assert config.index(mathjax_bundle) < config.index(user_managed)
    assert (ROOT / "docs" / "javascripts" / "extra.js").read_text(
        encoding="utf-8"
    ) == ""


@pytest.mark.parametrize("state", ["different", "missing"])
def test_shared_stylesheet_drift_fails_with_recovery(
    tmp_path: Path, state: str
) -> None:
    (tmp_path / MANIFEST).write_bytes((ROOT / MANIFEST).read_bytes())
    target = tmp_path / "docs" / "stylesheets" / "pdk.css"
    if state == "different":
        target.parent.mkdir(parents=True)
        target.write_text("duplicated or stale rules\n", encoding="utf-8")

    result = CliRunner().invoke(
        main, ["shared-files", "--root", str(tmp_path), "--check"]
    )

    assert result.exit_code == 1
    expected_label = "WRONG" if state == "different" else "MISS"
    assert expected_label in result.output
    assert "docs/stylesheets/pdk.css" in result.output
    assert "prodockit shared-files --apply" in result.output


def test_both_publishing_workflows_enforce_prodockit_checks() -> None:
    github = (ROOT / ".github" / "workflows" / "docs.yml").read_text(
        encoding="utf-8"
    )
    gitlab = (ROOT / ".gitlab-ci.yml").read_text(encoding="utf-8")

    for workflow in (github, gitlab):
        assert "pdk diag" in workflow
        assert "prodockit pins --check --offline" in workflow
        assert "prodockit config --check" in workflow
        assert workflow.index("pip install -r requirements.txt -r testrequirements.txt") < (
            workflow.index("pdk diag")
        )
        assert workflow.index("prodockit init-mathjax") < workflow.index("pdk diag")
        assert workflow.index("pdk diag") < workflow.index(
            "prodockit pins --check --offline"
        )
