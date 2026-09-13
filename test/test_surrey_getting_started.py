"""The Surrey overlay must leave the public guide and its links intact."""

import re
import tomllib
from pathlib import Path

from tools import surrey_getting_started as surrey


ROOT = Path(__file__).resolve().parents[1]


def test_snapshot_is_complete_and_pinned() -> None:
    data = surrey.manifest()
    surrey.verify_snapshot(data)
    assert data["version"] == "0.65.4"
    assert len(data["revision"]) == 40
    assert len(data["pages"]) == 7
    assert data["pages"][0]["path"] == "gettingstarted.md"

    assets = set(data["assets"])
    for page in surrey.page_paths(data):
        markdown = (surrey.SOURCE / "docs" / page).read_text(encoding="utf-8")
        for match in surrey.LINK.finditer(markdown):
            if not match.group("open").startswith("!["):
                continue
            target = surrey._relative_target(page, match.group("url"))
            if target is not None:
                continue  # Markdown-page links are checked separately.
            url = match.group("url")
            if url.startswith(("http://", "https://", "/")):
                continue
            resolved = surrey.posixpath.normpath(surrey.posixpath.join(surrey.posixpath.dirname(page), url))
            assert resolved in assets, (page, url)


def test_external_manual_links_are_rewritten_only_inside_imported_pages() -> None:
    data = surrey.manifest()
    included = set(surrey.page_paths(data))
    source = (
        "[local](../installation.md#installation-preparation) "
        "[manual](../commands/bootstrap.md#cmd-bootstrap-phases) "
        "[site](../publishing.md)"
    )
    result = surrey.rewrite_external_links(source, "devcons/bootstrap.md", included)
    assert "[local](../installation.md#installation-preparation)" in result
    assert "[manual](https://prodockit.org/commands/bootstrap/#cmd-bootstrap-phases)" in result
    assert "[site](https://prodockit.org/publishing/)" in result

    for page in included:
        markdown = (surrey.SOURCE / "docs" / page).read_text(encoding="utf-8")
        rewritten = surrey.rewrite_external_links(markdown, page, included)
        for match in surrey.LINK.finditer(rewritten):
            target = surrey._relative_target(page, match.group("url"))
            assert target is None or target in included, (page, match.group("url"))


def test_surrey_nav_preserves_upstream_numbering_and_relabels_following_pages() -> None:
    canonical = tomllib.loads((ROOT / "zensical.toml").read_text(encoding="utf-8"))
    data = surrey.manifest()
    nav = surrey.surrey_nav(canonical, data)
    assert nav[0] == {"Home": ["index.md"]}
    assert next(iter(nav[1])) == "Getting started"
    section = nav[1]["Getting started"]
    assert [next(iter(item.values())) for item in section[:7]] == surrey.page_paths(data)
    assert next(iter(section[0])) == "1. prodockit overview"
    assert section[-1] == {"8. Additional tooling": "additionaltooling.md"}
    assert nav[2] == {"About": [{"9. About this guide": "about.md"}]}
    assert tomllib.loads("[project]\nnav = " + surrey._render_nav(nav))["project"]["nav"] == nav
    assert (ROOT / "docs/gettingstarted.md").read_text(encoding="utf-8").startswith("---")


def test_other_guide_pages_link_only_to_the_local_start_page() -> None:
    for page in (ROOT / "docs").glob("*.md"):
        if page.name == "gettingstarted.md":
            continue
        text = page.read_text(encoding="utf-8")
        assert not re.search(
            r"https://prodockit\.org/(?:gettingstarted|choosing-installation|"
            r"installation|getting-started|manual-install|troubleshooting-installs)/",
            text,
        ), page
