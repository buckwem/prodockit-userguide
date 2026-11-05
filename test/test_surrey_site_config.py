"""GitLab applies its deployment URLs without changing GitHub source."""

import subprocess
import tomllib
from pathlib import Path

import pytest

from tools.surrey_site_config import with_surrey_urls


ROOT = Path(__file__).resolve().parents[1]
PAGES = "https://prodockit-userguide-50edd8.pages.surrey.ac.uk"
PROJECT = "https://gitlab.surrey.ac.uk/csee/mb0105/prodockit-userguide"


def _committed_config() -> str:
    return subprocess.run(
        ["git", "show", "HEAD:zensical.toml"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout


def test_surrey_overlay_changes_only_deployment_links() -> None:
    canonical = tomllib.loads(_committed_config())["project"]
    surrey = tomllib.loads(
        with_surrey_urls(_committed_config(), PAGES, PROJECT)
    )["project"]

    assert surrey["site_url"] == PAGES + "/"
    assert surrey["repo_url"] == PROJECT
    assert surrey["edit_uri"] == "-/edit/main/docs/"
    for key in ("site_url", "repo_url", "edit_uri"):
        assert canonical[key] != surrey[key]
        surrey.pop(key)
        canonical.pop(key)
    assert surrey == canonical


@pytest.mark.parametrize(
    ("pages", "project"),
    [
        ("http://prodockit-userguide.pages.surrey.ac.uk", PROJECT),
        ("https://pages.surrey.ac.uk.evil.example", PROJECT),
        ("https://prodockit-userguide.pages.surrey.ac.uk/?next=1", PROJECT),
        (PAGES, "https://gitlab.surrey.ac.uk/mb0105/prodockit-userguide"),
        (PAGES, "https://other.example/csee/mb0105/prodockit-userguide"),
    ],
)
def test_unexpected_urls_are_rejected(pages: str, project: str) -> None:
    with pytest.raises(ValueError, match="Unexpected Surrey deployment URL"):
        with_surrey_urls(_committed_config(), pages, project)


def test_ci_config_applies_overlay_and_uses_untagged_runner() -> None:
    ci = (ROOT / ".gitlab-ci.yml").read_text(encoding="utf-8")
    assert "tags:" not in ci
    assert "python tools/surrey_site_config.py" in ci
    assert ci.index("prodockit pins --check --offline") < ci.index(
        "python tools/surrey_site_config.py"
    ) < ci.index("prodockit config --check")
    assert ci.index("python tools/surrey_site_config.py") < ci.index(
        "python tools/surrey_getting_started.py prepare"
    )
