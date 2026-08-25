"""Release floor, canonical domains, and prodockit 0.42 documentation."""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_prodockit_0421_is_a_minimum_not_an_exact_pin() -> None:
    requirements = _text("requirements.txt")

    assert "prodockit[index]>=0.42.1" in requirements
    assert "prodockit[index]==" not in requirements
    assert "prodockit==" not in requirements


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
    assert "## Help with common problems {: #installtooling-help-with-common-problems }" in install
    assert "git remote add origin" in install
    assert 'git commit -m "Initial commit"' in install
    assert "git push -u origin main" in install
    assert "git log -1 --oneline" in install
    assert '{"4. Manual install" = "installtooling.md"}' in config


def test_adoption_and_bootstrap_install_precede_manual_install() -> None:
    adoption = _text("docs/adoptioninstall.md")
    bootstrap = _text("docs/bootstrapinstall.md")
    about = _text("docs/about.md")
    config = _text("zensical.toml")

    assert "# Adoption install" in adoption
    assert "/// steps" in adoption
    assert "prodockit adopt --configure" in adoption
    assert "prodockit adopt --dry-run" in adoption
    assert "prodockit adopt --apply" in adoption
    assert "Git, SSH, remotes, editors, commits, and pushes" in adoption
    assert "## Where to go next {: #adoptioninstall-where-to-go-next }" in adoption
    assert "## Manually integrate files prodockit preserves" in adoption
    assert "tools/mermaid/package.json" in adoption
    assert "tools/mathjax/tex2svg.js" in adoption
    assert "prodockit init-tools --dir ../prodockit-tools-reference" in adoption
    assert "pip3 install --upgrade prodockit" in adoption
    assert "python -m pip install --upgrade prodockit" in adoption
    assert "prodockit>=" not in adoption
    assert "# Bootstrap Install" in bootstrap
    assert "/// steps" in bootstrap
    assert "pdkboot --configure" in bootstrap
    assert "pdkboot --check" in bootstrap
    assert "pdkboot --dry-run" in bootstrap
    assert "pdkboot --apply" in bootstrap
    assert "## Where to go next {: #bootstrapinstall-where-to-go-next }" in bootstrap
    assert "prodockit-template" in bootstrap
    assert "The repository already contains work" in bootstrap
    assert "All 23 stages are set up." in bootstrap
    assert "[Adoption install](adoptioninstall.md)" in about
    assert "[Bootstrap Install](bootstrapinstall.md)" in about
    assert "recommended" not in about.lower()
    assert "formal-looking document as a head start" in about
    assert "www.youtube-nocookie.com/embed/ZlabtdA-gZE" in about
    assert "www.youtube.com/embed/ZlabtdA-gZE" not in about
    assert about.count("/// steps") >= 2
    assert config.index('{"2. Adoption install" = "adoptioninstall.md"}') < config.index(
        '{"3. Bootstrap Install" = "bootstrapinstall.md"}'
    ) < config.index('{"4. Manual install" = "installtooling.md"}')
    assert '[project.markdown_extensions."prodockit.steps"]' in config


def test_install_platform_tabs_are_separate_and_consistently_ordered() -> None:
    expected_group = [
        ":material-apple: macOS",
        ":fontawesome-brands-windows: Windows",
        ":material-linux: Linux (Ubuntu)",
    ]

    for path in (
        "docs/adoptioninstall.md",
        "docs/bootstrapinstall.md",
        "docs/installtooling.md",
    ):
        source = _text(path)
        labels = re.findall(
            r'^=== "(:(?:material-apple|fontawesome-brands-windows|material-linux): [^"]+)"$',
            source,
            flags=re.MULTILINE,
        )
        assert "macOS /" not in source
        assert labels
        assert len(labels) % 3 == 0
        assert labels == expected_group * (len(labels) // 3)


def test_guide_is_split_into_top_level_workflow_sections() -> None:
    config = _text("zensical.toml")

    assert '{"Guide" = [' not in config
    assert '{"Install" = [' in config
    assert '{"Edit" = [' in config
    assert '{"Basics" = [' in config
    assert '{"Customise" = [' in config
    assert '{"Build" = [' in config
    assert config.count('{"10. Customise build" = "customisebuild.md"}') == 1
    install = config[config.index('{"Install" = [') : config.index('{"Edit" = [')]
    build = config[config.index('{"Build" = [') : config.index('{"Reference" = [')]
    assert '{"11. Additional tooling" = "additionaltooling.md"}' in install
    assert '{"11. Additional tooling" = "additionaltooling.md"}' not in build


def test_retired_github_pages_domains_are_not_used() -> None:
    paths = [ROOT / "README.md", ROOT / "zensical.toml"]
    paths.extend((ROOT / "docs").rglob("*.md"))
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)

    assert "buckwem.github.io/prodockit-userguide" not in combined
    assert "buckwem.github.io/prodockit-extensions" not in combined
    assert "buckwem.github.io/prodockit-template" not in combined
