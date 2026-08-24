"""Release floor, canonical domains, and prodockit 0.42 documentation."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_prodockit_0421_is_a_minimum_not_an_exact_pin() -> None:
    requirements = _text("requirements.txt")

    assert "prodockit[index]>=0.42.1" in requirements
    assert "prodockit[index]==" not in requirements
    assert "prodockit==" not in requirements


def test_dependency_drift_automation_is_not_shipped() -> None:
    assert not (ROOT / ".github" / "workflows" / "drift.yml").exists()
    gitlab = _text(".gitlab-ci.yml")
    assert "\ndrift:" not in gitlab
    assert "DRIFT_TOKEN" not in gitlab


def test_custom_domain_is_consistent() -> None:
    config = _text("zensical.toml")
    readme = _text("README.md")
    cname = _text("docs/CNAME").strip()

    assert cname == "docs.prodockit.org"
    assert f'site_url = "https://{cname}/"' in config
    assert f"https://{cname}/" in readme


def test_table_styles_keep_the_five_percent_default_and_cell_overrides() -> None:
    css = _text("docs/stylesheets/extra.css")
    guide = _text("docs/customisecontent.md")

    assert "background-color: rgba(var(--prodockit-table-shade-rgb), 0.05)" in css
    assert "table th.prodockit-table-cell-shaded" in css
    assert "table td.prodockit-table-cell-unshaded" in css
    assert ".md-typeset th.prodockit-rotate" in css
    assert ".md-typeset span.prodockit-rotate" in css
    assert "Header cells have a subtle 5% shade by default" in guide
    assert 'shade="off"' in guide
    assert 'shade="8%"' in guide
    assert "colspan=2" in guide


def test_new_042_behaviour_is_documented() -> None:
    customise = _text("docs/customise.md")
    content = _text("docs/customisecontent.md")
    build = _text("docs/customisebuild.md")
    install = _text("docs/installtooling.md")
    editing = _text("docs/startediting.md")

    assert "forward cross-page" in content
    assert "11pt body text" in customise
    assert "10pt inline or fenced code" in customise
    assert "prodockit template-sync --apply" in build
    assert "preserves every existing" in build
    assert "`project.extra.pdf_*` value" in build
    assert "prodockit bootstrap --apply" in install
    assert "University of Surrey GitLab is the" in install
    assert "generated root files" in editing


def test_manual_install_explains_both_repository_starting_points() -> None:
    install = _text("docs/installtooling.md")
    config = _text("zensical.toml")

    assert "# Manual install" in install
    assert "### Path 1: start from the template" in install
    assert "### Path 2: clone the existing repository" in install
    assert "git remote add origin" in install
    assert 'git commit -m "Initial commit"' in install
    assert "git push -u origin main" in install
    assert "git log -1 --oneline" in install
    assert '{"2. Manual install" = "installtooling.md"}' in config


def test_every_prodockit_markdown_extension_is_enabled() -> None:
    config = _text("zensical.toml")

    for name in (
        "headings",
        "refs",
        "citations",
        "glossary",
        "bibliography",
        "tables",
        "steps",
        "tree",
        "index",
    ):
        assert f'[project.markdown_extensions."prodockit.{name}"]' in config


def test_retired_github_pages_domains_are_not_used() -> None:
    paths = [ROOT / "README.md", ROOT / "zensical.toml"]
    paths.extend((ROOT / "docs").rglob("*.md"))
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)

    assert "buckwem.github.io/prodockit-userguide" not in combined
    assert "buckwem.github.io/prodockit-extensions" not in combined
    assert "buckwem.github.io/prodockit-template" not in combined
