"""Release floors, canonical domains, and coordinated documentation."""

import re
from pathlib import Path

from jinja2 import Environment


ROOT = Path(__file__).resolve().parents[1]


def _text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_required_tool_versions_are_minimums_not_exact_pins() -> None:
    requirements = _text("requirements.txt")
    test_requirements = _text("testrequirements.txt")

    assert "prodockit[index]>=0.54.0" in requirements
    assert "prodockit[testing]>=0.54.0" in test_requirements
    assert "prodockit[index]==" not in requirements
    assert "prodockit[testing]==" not in test_requirements
    assert "prodockit==" not in requirements
    assert "zensical>=0.0.57" in requirements
    assert "zensical==" not in requirements


def test_python_artifact_builds_use_the_version_file() -> None:
    version = _text(".python-version").strip()
    github = _text(".github/workflows/docs.yml")
    gitlab = _text(".gitlab-ci.yml")

    assert version == "3.14"
    assert "python-version-file: .python-version" in github
    assert "python-version: 3.x" not in github
    assert f"image: python:{version}" in gitlab


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
    css = _text("docs/stylesheets/pdk.css")
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


def test_home_page_hero_does_not_force_a_full_viewport() -> None:
    stylesheet = _text("docs/stylesheets/pdk.css")
    hero = stylesheet.split(".cover-hero {", 1)[1].split("}", 1)[0]
    graphic = stylesheet.split(".cover-hero-graphic {", 1)[1].split("}", 1)[0]

    assert "align-items: flex-start" in hero
    assert "min-height: 0" in hero
    assert "100vh" not in hero
    assert "max-width: min(540px, 44vw)" in graphic


def test_only_canonical_github_pages_receives_consent_gated_analytics() -> None:
    config = _text("zensical.toml")
    copyright = _text("overrides/partials/copyright.html")
    github = _text(".github/workflows/docs.yml")
    gitlab = _text(".gitlab-ci.yml")

    assert "[project.extra.analytics]" not in config
    assert "[project.extra.consent]" not in config
    assert "{% if config.extra.analytics %}" in copyright
    assert 'href="#__consent"' in copyright
    assert "GOOGLE_ANALYTICS_ID: ${{ secrets.GOOGLE_ANALYTICS_ID }}" in github
    assert "if: github.repository == 'buckwem/prodockit-userguide'" in github
    assert "python tools/canonical_site_config.py" in github
    assert "GOOGLE_ANALYTICS_ID" not in gitlab
    assert "canonical_site_config.py" not in gitlab


def test_new_042_behaviour_is_documented() -> None:
    customise = _text("docs/customise.md")
    customise_words = re.sub(r"\s+", " ", customise)
    content = _text("docs/customisecontent.md")
    build = _text("docs/customisebuild.md")
    install = _text("docs/installtooling.md")
    editing = _text("docs/startediting.md")

    assert "forward cross-page" in content
    assert "11pt body text" in customise_words
    assert "10pt inline or fenced code" in customise_words
    assert "prodockit template-sync --apply" in build
    assert "preserves every existing" in build
    assert "`project.extra.pdf_*` value" in build
    assert "[Bootstrap Install](bootstrapinstall.md)" in install
    assert "`prodockit bootstrap`" in install
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
    assert "prodockit>=" not in bootstrap
    assert "prodockit>=0.43.2" not in bootstrap
    assert "# Bootstrap Install" in bootstrap
    assert "/// steps" in bootstrap
    assert "prodockit bootstrap --configure" in bootstrap
    assert "prodockit bootstrap --check" in bootstrap
    assert "prodockit bootstrap --dry-run" in bootstrap
    assert "prodockit bootstrap --apply" in bootstrap
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


def test_adoption_guide_uses_the_current_shared_stylesheet_name() -> None:
    adoption = _text("docs/adoptioninstall.md")

    assert "prodockit.css" not in adoption
    assert adoption.count("pdk.css") >= 3
    assert "docs/stylesheets/pdk.css" in adoption
    assert "stylesheets/pdk.css" in adoption


def test_start_editing_explains_how_to_rebuild_a_broken_environment() -> None:
    editing = _text("docs/startediting.md")

    assert "### The virtual environment is broken" in editing
    assert "Ignoring invalid distribution" in editing
    assert "mv .venv .venv-broken" in editing
    assert "Rename-Item .venv .venv-broken" in editing
    assert "rehash" in editing
    assert "hash -r" in editing
    assert "Get-Command pdk" in editing
    assert "python -m pip show prodockit" in editing
    assert "after the rebuilt environment has passed" in editing


def test_guide_defers_product_versions_to_extensions_reference() -> None:
    guide = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((ROOT / "docs").glob("*.md"))
    )

    versioned_product = re.compile(
        r"\b(?:prodockit|Zensical|Pandoc|Node\.js|Python|MathJax)\s+v?\d+\.\d+",
        re.IGNORECASE,
    )
    assert not versioned_product.search(guide)
    assert not re.search(r"prodockit\s*[<>=]=?\s*\d", guide, re.IGNORECASE)
    assert not re.search(r"nodesource\.com/setup_\d+", guide, re.IGNORECASE)


def test_surrey_guidance_is_hidden_from_the_standard_guide() -> None:
    environment = Environment(autoescape=False)
    context = {
        "acronym_style": lambda: "",
        "glossary_style": lambda: "",
        "heading_counter_reset": lambda _page: "",
        "is_surrey": False,
        "page": None,
        "reference_style": lambda: "",
        "release": "",
        "repo_url": "",
        "site_name": "",
        "word_count": "",
    }
    standard = "\n".join(
        environment.from_string(path.read_text(encoding="utf-8")).render(context)
        for path in sorted((ROOT / "docs").glob("*.md"))
    )

    assert not re.search(
        r"University of Surrey|gitlab\.surrey|pages\.surrey|\bstudents?\b|"
        r"\bcoursework\b|\bassessed\b",
        standard,
        re.IGNORECASE,
    )

    context["is_surrey"] = True
    surrey = environment.from_string(_text("docs/installtooling.md")).render(context)
    assert "University of Surrey GitLab" in surrey
    assert "gitlab.surrey.ac.uk" in surrey


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
        "docs/additionaltooling.md",
    ):
        source = _text(path)
        labels = re.findall(
            r'^\s*=== "(:(?:material-apple|fontawesome-brands-windows|material-linux): [^"]+)"$',
            source,
            flags=re.MULTILINE,
        )
        assert "macOS /" not in source
        assert '<div class="grid cards one-column" markdown>' not in source
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
    assert '{"Build and test" = [' in config
    assert config.count(
        '{"10. Document appearance and structure" = "customise.md"}'
    ) == 1
    assert config.count(
        '{"11. Prodockit authoring features" = "customisecontent.md"}'
    ) == 1
    assert config.count('{"12. Build and publish" = "customisebuild.md"}') == 1
    assert '"testing.md"' not in config
    install = config[config.index('{"Install" = [') : config.index('{"Edit" = [')]
    build = config[
        config.index('{"Build and test" = [') : config.index('{"Reference" = [')
    ]
    assert '{"5. Additional tooling" = "additionaltooling.md"}' in install
    assert '{"5. Additional tooling" = "additionaltooling.md"}' not in build
    numbers = [
        int(number)
        for number in re.findall(r'\{"(\d+)\. [^"]+" = "[^"]+"\}', config)
    ]
    assert numbers == list(range(1, 13))


def test_additional_tooling_is_an_optional_follow_on() -> None:
    about = _text("docs/about.md")
    additional = _text("docs/additionaltooling.md")

    assert "it is not a fourth installation route" in about
    assert "Choose only the sections that match your work" in additional
    assert "SSH remains the preferred connection" in additional
    assert "[Start editing](startediting.md)" in additional

    for path in (
        "docs/adoptioninstall.md",
        "docs/bootstrapinstall.md",
        "docs/installtooling.md",
    ):
        source = _text(path)
        where_next = source[source.index("## Where to go next") :]
        assert "[Additional tooling](additionaltooling.md)" in where_next
        assert "[Start editing](startediting.md)" in where_next


def test_edit_section_follows_the_author_workflow() -> None:
    editing = _text("docs/startediting.md")

    headings = (
        "## Preview the website locally",
        "## Build and check the downloadable documents",
        "## Save and push your updates",
        "## Confirm the published website and documents",
        "## Organise larger changes with branches and issues",
        "## Help with common problems",
    )
    positions = [editing.index(heading) for heading in headings]

    assert positions == sorted(positions)
    assert '<div class="grid cards one-column" markdown>' not in editing
    assert "SSH" in editing
    assert "rm -rf public" not in editing
    assert "## Trouble shooting" not in editing
    assert "### Use the author checklist" in editing
    assert "### A cross-page reference looks stale in the live preview" in editing
    assert "### A reference opens the wrong repeated heading" in editing
    assert "### Mermaid or mathematics appears as source text" in editing
    assert "### The website and PDF do not have exactly the same layout" in editing
    assert "### The word count leaves out unexpected content" in editing
    assert "After updating prodockit" in editing


def test_basics_section_is_ordered_for_beginning_authors() -> None:
    markdown = _text("docs/markdown.md")
    zensical = _text("docs/zensicalbasics.md")
    shell = _text("docs/shcommands.md")

    assert "## Write a simple page" in markdown
    assert "Zensical Studio viewer" in markdown
    assert "zensical serve" in markdown
    assert "Markdown Live Preview" not in markdown
    assert "prodockit.steps" not in zensical
    assert "prodockit.tree" not in zensical
    assert "**four spaces**" in markdown
    assert "## Avoid common mistakes" in markdown

    assert "## Preview and build" in zensical
    assert "zensical new" not in zensical
    assert "## Follow the four-space rule" in zensical
    assert "## Add an admonition" in zensical
    assert "## Present alternatives in content tabs" in zensical
    assert "## Add a caption {: #images }" in zensical
    assert "/// figure-caption" in zensical
    assert "/// table-caption | <" in zensical
    assert "customisecontent.md#caption-a-figure" in zensical
    assert "customisecontent.md#caption-a-table" in zensical
    assert "## Avoid common mistakes" in zensical

    assert "macOS and Linux users who have not used a command line before" in shell
    assert "## Understand the prompt" in shell
    assert "## Understand a command" in shell
    assert "## Understand paths" in shell
    assert "## Activate the project environment" in shell
    assert "Do **not** type the prompt itself" in shell
    assert "Do not run `sudo pip`" in shell
    assert "rm -rf [dir]" not in shell
    assert "kill -9" not in shell
    assert "chmod" not in shell


def test_customise_content_introduces_authoring_extensions() -> None:
    customise = _text("docs/customise.md")
    content = _text("docs/customisecontent.md")
    content_words = re.sub(r"\s+", " ", content)

    assert "# Document appearance and structure" in customise
    assert "# Prodockit authoring features" in content
    assert "Most document-wide changes are made in one of four places" in customise
    assert "## Navigation structure" in customise
    assert "## Customise front page" in customise
    assert "## Customise PDF generation" in customise
    assert "/// tree\n    indent: 4" in customise
    assert "This page covers the prodockit features an author uses while writing" in content_words
    assert "### Leave a heading unnumbered or out of PDF navigation" in content
    assert ".unnumbered .unlisted .unbookmarked" in content
    assert "### Include the target's PDF page number" in content
    assert "\\autoref{changing-heading-numbering}" in content
    assert "## Write a numbered procedure" in content
    assert "start: 3" in content
    assert "## Show a directory structure" in content
    assert "indent: 4" in content
    assert "A trailing `/` marks a directory" in content
    assert "### Set table widths and alignment" in content
    assert "### Caption a figure {: #caption-a-figure }" in content
    assert "### Caption a table {: #caption-a-table }" in content
    assert "|:---|---|" in content

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
        assert f"prodockit.{name}" in content


def test_build_page_is_an_author_workflow() -> None:
    build = _text("docs/customisebuild.md")

    assert "# Build and publish" in build
    assert "## Prepare the terminal" in build
    assert "prodockit template-sync" in build
    assert "prodockit pins --check --offline" in build
    assert "prodockit config --check" in build
    assert "### Use one maintenance cycle" in build
    assert "https://prodockit.org/devcons/template-sync/" in build
    assert "https://prodockit.org/devcons/continuous-integration/" in build
    assert "https://prodockit.org/devcons/testing/" in build


def test_customise_explains_repository_synchronisation() -> None:
    customise = _text("docs/customise.md")

    assert "### Keep repository details in sync" in customise
    assert "prodockit sync-repo --check" in customise
    assert "does not change the Git remote" in customise


def test_reference_appendix_covers_the_guide_toolchain() -> None:
    references = _text("docs/references.md")

    for reference_id in (
        "chacon2014",
        "courtbuillonnodate",
        "githubnodate",
        "gitlabdocsnodate",
        "homebrewnodate",
        "macfarlanenodate",
        "msys2nodate",
        "nodesourcenodate",
        "prodockit2026",
        "pymdownextensionsnodate",
        "psfnodate",
        "skou2023",
        "zensicalnd",
        "zoteronodate",
    ):
        assert f"#{reference_id} .reference" in references


def test_acronym_and_glossary_appendices_cover_revised_guidance() -> None:
    acronyms = _text("docs/acronyms.md")
    glossary = _text("docs/glossary.md")

    for acronym_id in (
        "arm64",
        "cdn",
        "csl",
        "dll",
        "svg",
        "ucrt64",
        "vpn",
        "yaml",
    ):
        assert f"#{acronym_id} .acronym" in acronyms

    for glossary_id in (
        "build-def",
        "citation-def",
        "cross-reference-def",
        "dependency-def",
        "deployment-def",
        "origin-def",
        "pipeline-def",
        "processor-architecture-def",
        "remote-def",
        "renderer-def",
        "virtual-environment-def",
    ):
        assert f"#{glossary_id} .glossary" in glossary

    assert "Prodockit authoring features" in acronyms
    assert "Prodockit authoring features" in glossary


def test_index_balances_task_and_subject_entries() -> None:
    sources = "\n".join(
        path.read_text(encoding="utf-8") for path in (ROOT / "docs").glob("*.md")
    )
    tasks = re.findall(r"\\index\{Tasks!([^}]+)\}", sources)

    assert 8 <= len(set(tasks)) <= 15
    for task in (
        "Adopt an existing document",
        "Bootstrap a new project",
        "Install manually",
        "Preview a website",
        "Save and push changes",
        "Publish a document",
        "Synchronise repository details",
        "Update from prodockit-template",
        "Finalise a document",
    ):
        assert task in tasks

    for subject in (
        "Markdown!links",
        "Git!commit",
        "Website!navigation",
        "PDF!configuration",
        "Cross-references",
        "References",
        "Tables!width and alignment",
        "Build!website and PDF",
    ):
        assert f"\\index{{{subject}}}" in sources


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
