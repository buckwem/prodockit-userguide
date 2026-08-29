# Copyright (c) 2025-2026 Mark Buckwell and contributors
# SPDX-License-Identifier: MIT

"""Institution branding (issue #31).

`macros.py` swaps the header logo between a Surrey and a default pair,
depending on where this checkout is being built. Two things need testing,
and they need testing differently:

- The hostname comparison, which is pure and gives the same answer in every
  clone, so it can be asserted directly.
- The swap itself, which depends on the git remote and Zensical's config,
  so its *result* differs between a GitHub clone and a Surrey one - asserted
  only for consistency, the way prodockit-template does it.

That split is deliberate. prodockit-template#132 was a check that could
never fire, invisible to tests precisely because they only ever asserted
consistency with the detection rather than the detection itself.
"""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session")
def macros():
    """macros.py loaded by path - it sits at the repo root, not on sys.path."""
    spec = importlib.util.spec_from_file_location("macros", REPO_ROOT / "macros.py")
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(REPO_ROOT))
    spec.loader.exec_module(module)
    return module


def _sha256(path: Path) -> str:
    """Digest rather than raw bytes: pytest's assertion introspection would
    otherwise try to diff two ~250KB PNGs into the failure message."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


# --- The hostname comparison (pure, environment-independent) ---------------


def test_surrey_gitlab_hostname_is_recognised(macros):
    """The case a plain `== 'surrey.ac.uk'` could never match, since GitLab
    sets CI_SERVER_HOST to the instance hostname."""
    assert macros._host_is_surrey("gitlab.surrey.ac.uk")


def test_bare_surrey_domain_is_recognised(macros):
    assert macros._host_is_surrey("surrey.ac.uk")


def test_hostname_matching_ignores_case_and_trailing_dot(macros):
    assert macros._host_is_surrey("GitLab.Surrey.AC.UK")
    assert macros._host_is_surrey("gitlab.surrey.ac.uk.")


def test_non_surrey_hosts_are_rejected(macros):
    assert not macros._host_is_surrey("github.com")
    assert not macros._host_is_surrey("gitlab.com")


def test_missing_host_is_rejected(macros):
    """CI_SERVER_HOST is unset outside GitLab CI - the common case here, and
    it must not raise."""
    assert not macros._host_is_surrey(None)
    assert not macros._host_is_surrey("")


def test_lookalike_hosts_are_rejected(macros):
    """A substring test would accept both: the first is a different domain
    ending the same way, the second embeds ours in someone else's."""
    assert not macros._host_is_surrey("notsurrey.ac.uk")
    assert not macros._host_is_surrey("surrey.ac.uk.example.com")


def test_ci_server_host_alone_triggers_detection(macros, monkeypatch):
    """End to end through _detect_is_surrey(). Passes in any clone, because
    Check 1 returns before the git-remote and config checks run.

    Only the positive direction is asserted - a negative would depend on
    those other checks, and so on which repository the tests run against.
    """
    monkeypatch.setenv("CI_SERVER_HOST", "gitlab.surrey.ac.uk")
    assert macros._detect_is_surrey()


# --- The logo swap ---------------------------------------------------------


def test_both_branding_pairs_are_present(macros):
    """The swap copies from these; a missing one degrades to a warning at
    build time rather than an error, so it needs asserting here."""
    assets = REPO_ROOT / "docs" / "assets"
    for name in ("logo_surrey_black", "logo_surrey_white", "logo_default_black", "logo_default_white"):
        assert (assets / f"{name}.png").is_file(), f"{name}.png missing"


def test_active_logo_matches_the_pair_for_this_checkout(macros):
    """The active logo_black/white.png must match whichever pair
    _detect_is_surrey() selects - reusing the same check define_env() does,
    rather than hardcoding an assumption about which CI is running."""
    assets = REPO_ROOT / "docs" / "assets"
    expected = "logo_surrey" if macros._detect_is_surrey() else "logo_default"
    other = "logo_default" if expected == "logo_surrey" else "logo_surrey"
    for variant in ("black", "white"):
        active = _sha256(assets / f"logo_{variant}.png")
        assert active == _sha256(assets / f"{expected}_{variant}.png")
        assert active != _sha256(assets / f"{other}_{variant}.png"), (
            f"logo_{variant}.png matches the {other} pair - the branding swap "
            "picked the wrong one, or never ran"
        )


def test_logo_css_references_files_not_inlined_data(macros):
    """The swap only works because the stylesheet points at these files by
    relative url(). It previously inlined them as base64 data: URIs, which
    would make the copy a silent no-op - the header logo would never change
    however the detection went.

    prodockit.pdf's own _inline_css_urls() re-inlines them for the PDF, so
    the relative references cost nothing there.
    """
    shared_css = (REPO_ROOT / "docs" / "stylesheets" / "pdk.css").read_text(
        encoding="utf-8"
    )
    css = (REPO_ROOT / "docs" / "stylesheets" / "branding.css").read_text(
        encoding="utf-8"
    )
    config = (REPO_ROOT / "zensical.toml").read_text(encoding="utf-8")
    logo_rules = [line for line in css.splitlines() if ".md-logo img" in line or "logo_" in line]
    assert any("../assets/logo_white.png" in line for line in logo_rules)
    assert any("../assets/logo_black.png" in line for line in logo_rules)
    assert ".md-logo img" not in shared_css
    assert config.index('"stylesheets/pdk.css"') < config.index(
        '"stylesheets/branding.css"'
    ) < config.index('"stylesheets/extra.css"')
    assert "data:image/png;base64" not in css, (
        "a base64 logo payload is in branding.css - the branding swap would "
        "silently stop having any visible effect"
    )
