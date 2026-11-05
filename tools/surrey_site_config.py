#!/usr/bin/env python3
"""Apply Surrey URLs to the disposable GitLab checkout's Zensical config.

The committed configuration remains canonical for GitHub. GitLab supplies the
actual Pages URL at job time, so a newly created mirror does not need a guessed
or hard-coded Pages address.
"""

from __future__ import annotations

import os
import re
import sys
import tomllib
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "zensical.toml"
PROJECT_PATH = "csee/mb0105/prodockit-userguide"


def _validate_url(value: str, *, pages: bool) -> str:
    parsed = urlsplit(value)
    if pages:
        valid_host = parsed.hostname == "pages.surrey.ac.uk" or (
            parsed.hostname or ""
        ).endswith(".pages.surrey.ac.uk")
    else:
        valid_host = parsed.hostname == "gitlab.surrey.ac.uk"
    if (
        parsed.scheme != "https"
        or not valid_host
        or parsed.username is not None
        or parsed.password is not None
        or parsed.port is not None
        or parsed.query
        or parsed.fragment
        or (not pages and parsed.path.rstrip("/") != "/" + PROJECT_PATH)
    ):
        raise ValueError(f"Unexpected Surrey deployment URL: {value!r}")
    return value.rstrip("/")


def _replace(source: str, name: str, value: str) -> str:
    pattern = rf'(?m)^{re.escape(name)} = "[^"]*"$'
    updated, count = re.subn(pattern, lambda _: f'{name} = "{value}"', source)
    if count != 1:
        raise ValueError(f"Expected one {name} setting, found {count}")
    return updated


def with_surrey_urls(source: str, pages_url: str, project_url: str) -> str:
    """Update deployment links, leaving all other TOML settings unchanged."""
    site_url = _validate_url(pages_url, pages=True) + "/"
    repo_url = _validate_url(project_url, pages=False)
    tomllib.loads(source)
    updated = _replace(source, "site_url", site_url)
    updated = _replace(updated, "repo_url", repo_url)
    updated = _replace(updated, "edit_uri", "-/edit/main/docs/")
    project = tomllib.loads(updated)["project"]
    if (project["site_url"], project["repo_url"], project["edit_uri"]) != (
        site_url,
        repo_url,
        "-/edit/main/docs/",
    ):
        raise ValueError("Surrey deployment URLs did not validate")
    return updated


def main() -> None:
    if os.environ.get("CI_SERVER_HOST") != "gitlab.surrey.ac.uk":
        raise ValueError("Surrey site configuration requires Surrey GitLab CI")
    if os.environ.get("CI_PROJECT_PATH", "").lower() != PROJECT_PATH:
        raise ValueError(f"Expected GitLab project {PROJECT_PATH}")
    source = CONFIG.read_text(encoding="utf-8")
    updated = with_surrey_urls(
        source, os.environ["CI_PAGES_URL"], os.environ["CI_PROJECT_URL"]
    )
    CONFIG.write_text(updated, encoding="utf-8")
    print("Applied Surrey Pages and repository URLs to the CI checkout")


if __name__ == "__main__":
    try:
        main()
    except (KeyError, OSError, ValueError, tomllib.TOMLDecodeError) as error:
        sys.exit(f"Surrey site configuration: {error}")
