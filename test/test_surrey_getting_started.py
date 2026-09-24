"""The Surrey overlay must leave the public guide and its links intact."""

import re
import subprocess
import tomllib
from pathlib import Path
from urllib.parse import unquote, urlsplit

from bs4 import BeautifulSoup

from tools import surrey_getting_started as surrey


ROOT = Path(__file__).resolve().parents[1]


def test_snapshot_is_complete_and_pinned() -> None:
    data = surrey.manifest()
    surrey.verify_snapshot(data)
    assert data["version"] == "0.73.0"
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
    assert (
        '[manual](https://prodockit.org/commands/bootstrap/#cmd-bootstrap-phases)'
        '{target="_blank" rel="noopener"}'
    ) in result
    assert '[site](https://prodockit.org/publishing/){target="_blank" rel="noopener"}' in result

    for page in included:
        markdown = (surrey.SOURCE / "docs" / page).read_text(encoding="utf-8")
        rewritten = surrey.rewrite_external_links(markdown, page, included)
        for match in surrey.LINK.finditer(rewritten):
            target = surrey._relative_target(page, match.group("url"))
            assert target is None or target in included, (page, match.group("url"))


def test_donation_section_is_removed_only_from_surrey_copy() -> None:
    source = (surrey.SOURCE / "docs/gettingstarted.md").read_text(encoding="utf-8")
    copied = surrey.omit_surrey_support_section(source)
    assert "## Project status" in copied
    assert "## Support prodockit" not in copied
    assert "Buy me a coffee" not in copied
    assert "## Support prodockit" in source
    assert "Buy me a coffee" in source


def test_pinned_surrey_pages_use_the_theme_aware_stag_for_remotelabs_tabs() -> None:
    counts = {"installation.md": 5, "getting-started.md": 3, "devcons/bootstrap.md": 4}
    for page, count in counts.items():
        source = (surrey.SOURCE / "docs" / page).read_text(encoding="utf-8")
        assert source.count('=== ":stag-stag_icon_32: Surrey RemoteLabs"') == count
        assert '=== ":material-linux: Surrey RemoteLabs"' not in source

    icon = ROOT / "overrides/.icons/stag/stag_icon_32.svg"
    assert 'fill="currentColor"' in icon.read_text(encoding="utf-8")


def test_surrey_nav_puts_about_first_and_preserves_upstream_numbering() -> None:
    config_text = (ROOT / "zensical.toml").read_text(encoding="utf-8")
    if config_text.startswith(surrey.START_MARKER):
        config_text = subprocess.check_output(
            ["git", "show", "HEAD:zensical.toml"], cwd=ROOT, text=True
        )
    canonical = tomllib.loads(config_text)
    data = surrey.manifest()
    nav = surrey.surrey_nav(canonical, data)
    assert nav[0] == {"Home": ["index.md"]}
    assert nav[1] == {"About": [{"About this guide": "about.md"}]}
    assert next(iter(nav[2])) == "Getting started"
    section = nav[2]["Getting started"]
    assert [next(iter(item.values())) for item in section[:7]] == surrey.page_paths(data)
    assert next(iter(section[0])) == "1. prodockit overview"
    assert section[-1] == {"8. Additional tooling": "additionaltooling.md"}
    assert nav[3] == {"Edit": [{"9. Start editing": "startediting.md"}]}
    assert tomllib.loads("[project]\nnav = " + surrey._render_nav(nav))["project"]["nav"] == nav
    assert (ROOT / "docs/gettingstarted.md").read_text(encoding="utf-8").startswith("---")


def test_built_surrey_top_menu_places_about_before_getting_started() -> None:
    if not (ROOT / "zensical.toml").read_text(encoding="utf-8").startswith(surrey.START_MARKER):
        return  # The canonical GitHub site has its own navigation build.
    home = BeautifulSoup((ROOT / "public/index.html").read_text(encoding="utf-8"), "html.parser")
    labels = [link.get_text(" ", strip=True) for link in home.select(".md-tabs__link")]
    assert labels.index("About") < labels.index("Getting started")


def test_other_guide_pages_link_only_to_the_local_start_page() -> None:
    tracked = subprocess.check_output(
        ["git", "ls-files", "docs/*.md"], cwd=ROOT, text=True
    ).splitlines()
    for relative in tracked:
        page = ROOT / relative
        if page.name == "gettingstarted.md":
            continue
        text = page.read_text(encoding="utf-8")
        assert not re.search(
            r"https://prodockit\.org/(?:gettingstarted|choosing-installation|"
            r"installation|getting-started|manual-install|troubleshooting-installs)/",
            text,
        ), page


def test_built_surrey_pages_have_local_targets_and_assets() -> None:
    if not (ROOT / "zensical.toml").read_text(encoding="utf-8").startswith(surrey.START_MARKER):
        return  # The normal GitHub build intentionally has only the summary.
    public = ROOT / "public"
    assert public.is_dir()
    for page in surrey.page_paths(surrey.manifest()):
        route = page.removesuffix(".md")
        html = public / route / "index.html"
        assert html.is_file(), html
        article = BeautifulSoup(html.read_text(encoding="utf-8"), "html.parser").select_one(".md-content")
        assert article is not None
        if page == "gettingstarted.md":
            assert "Buy me a coffee" not in article.get_text(" ", strip=True)
            assert "Support prodockit" not in article.get_text(" ", strip=True)
        for element in article.select("a[href], img[src]"):
            url = element.get("href") or element.get("src")
            parsed = urlsplit(url)
            if parsed.netloc == "prodockit.org":
                assert element.get("target") == "_blank", (html, url)
                continue
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            if parsed.path.startswith("/"):
                target = public / parsed.path.lstrip("/")
            else:
                target = html.parent / unquote(parsed.path)
            target = target.resolve()
            assert target.is_relative_to(public.resolve()), (html, url)
            if url.endswith("/") or not target.suffix:
                target = target / "index.html"
            assert target.is_file(), (html, url, target)
            if parsed.fragment and target.suffix == ".html":
                destination = BeautifulSoup(target.read_text(encoding="utf-8"), "html.parser")
                assert destination.find(id=unquote(parsed.fragment)) is not None, (html, url)


def test_imported_pages_render_the_selected_host_text() -> None:
    if not (ROOT / "zensical.toml").read_text(encoding="utf-8").startswith(surrey.START_MARKER):
        return  # The GitHub site publishes the canonical summary, not these pages.

    from macros import _detect_is_surrey

    def article(page: str) -> BeautifulSoup:
        html = ROOT / "public" / page / "index.html"
        content = BeautifulSoup(html.read_text(encoding="utf-8"), "html.parser").select_one(".md-content")
        assert content is not None
        assert "{%" not in content.get_text(" ", strip=True)
        return content

    choose = article("choosing-installation").get_text(" ", strip=True)
    adopt = article("getting-started").get_text(" ", strip=True)
    bootstrap = article("devcons/bootstrap")
    manual = article("manual-install").get_text(" ", strip=True)
    troubleshooting = article("troubleshooting-installs").get_text(" ", strip=True)

    if _detect_is_surrey():
        assert "Coursework with a prepared repository" in choose
        assert "This stage publishes your working local site on Surrey GitLab Pages." in adopt
        assert "This stage publishes your working local site on GitHub Pages or GitLab Pages." not in adopt
        assert bootstrap.select_one('a[href="https://gitlab.surrey.ac.uk/mb0105/prodockit-template"]')
        assert "use Surrey GitLab for your coursework" in manual
        assert "Check the connection to Surrey GitLab" in troubleshooting
        assert "Check the connection to GitLab or GitHub" not in troubleshooting
    else:
        assert "Coursework with a prepared repository" not in choose
        assert "This stage publishes your working local site on GitHub Pages or GitLab Pages." in adopt
        assert "This stage publishes your working local site on Surrey GitLab Pages." not in adopt
        assert bootstrap.select_one('a[href="https://github.com/buckwem/prodockit-template"]')
        assert "chosen Git host; you do not need both GitHub and GitLab" in manual
        assert "Check the connection to GitLab or GitHub" in troubleshooting
        assert "Check the connection to Surrey GitLab" not in troubleshooting


def test_imported_pdf_renders_the_selected_host_text() -> None:
    if not (ROOT / "zensical.toml").read_text(encoding="utf-8").startswith(surrey.START_MARKER):
        return  # The canonical GitHub PDF has no imported section.

    import pymupdf

    from macros import _detect_is_surrey

    pdf = ROOT / "docs/site_documentation.pdf"
    assert pdf.is_file()
    with pymupdf.open(pdf) as document:
        text = " ".join(page.get_text() for page in document)

    assert "Buy me a coffee" not in text
    assert ("Coursework with a prepared repository" in text) == _detect_is_surrey()
    assert ("Surrey GitLab Pages" in text) == _detect_is_surrey()
    assert ("GitHub Pages or GitLab Pages" in text) != _detect_is_surrey()
