"""Release floors, canonical domains, and coordinated documentation."""

import re
import json
import subprocess
import tomllib
from pathlib import Path

from bs4 import BeautifulSoup
from jinja2 import Environment


ROOT = Path(__file__).resolve().parents[1]


def _text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _canonical_text(path: str) -> str:
    """Read committed source when CI has prepared its Surrey-only overlay."""
    if not _text("zensical.toml").startswith("# Surrey Getting started overlay"):
        return _text(path)
    return subprocess.check_output(
        ["git", "show", f"HEAD:{path}"], cwd=ROOT, text=True
    )


def _canonical_guide_pages() -> list[str]:
    if not _text("zensical.toml").startswith("# Surrey Getting started overlay"):
        return [str(path.relative_to(ROOT)) for path in sorted((ROOT / "docs").glob("*.md"))]
    return subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", "HEAD", "docs"],
        cwd=ROOT,
        text=True,
    ).splitlines()


def test_required_tool_versions_are_minimums_not_exact_pins() -> None:
    requirements = _text("requirements.txt")
    test_requirements = _text("testrequirements.txt")

    versions = tomllib.loads(_text(".prodockit-toolchain.toml"))["versions"]
    pdf_requirements = _text("pdf-requirements.txt")
    assert f"prodockit>={versions['prodockit']}" in requirements
    assert f"prodockit[testing]>={versions['prodockit']}" in test_requirements
    assert "prodockit[index]" not in requirements
    assert "weasyprint" not in requirements
    assert "pymupdf" not in requirements
    assert "weasyprint==69.0" in pdf_requirements
    assert "pymupdf>=1.24" in pdf_requirements
    assert "prodockit[testing]==" not in test_requirements
    assert "prodockit==" not in requirements
    assert f"zensical>={versions['zensical']}" in requirements
    assert f"markdown=={versions['markdown']}" in requirements
    assert "zensical==" not in requirements


def test_page_outline_uses_the_right_sidebar() -> None:
    config = tomllib.loads(_text("zensical.toml"))
    assert "toc.integrate" not in config["project"]["theme"]["features"]

    # Start editing is present in both the canonical and Surrey builds.
    page = BeautifulSoup(_text("public/startediting/index.html"), "html.parser")
    assert page.select_one('.md-sidebar--secondary[data-md-type="toc"]') is not None


def test_canonical_manual_links_open_in_new_tabs() -> None:
    checked = 0
    for page in _canonical_guide_pages():
        if not page.endswith(".md"):
            continue
        for match in re.finditer(
            r"\]\(https://prodockit\.org/[^)]*\)(\{[^}]*\})?",
            _canonical_text(page),
        ):
            checked += 1
            assert match.group(1) and 'target="_blank"' in match.group(1), page
    assert checked > 10

    rendered = 0
    for html in (ROOT / "public").rglob("*.html"):
        page = BeautifulSoup(html.read_text(encoding="utf-8"), "html.parser")
        for link in page.select('a[href^="https://prodockit.org/"]'):
            rendered += 1
            assert link.get("target") == "_blank", (html, link.get("href"))
    assert rendered > 10


def test_diagnostic_recovery_directory_is_ignored() -> None:
    assert ".prodockit-quarantine/" in _text(".gitignore").splitlines()


def test_adopt_release_keeps_renderers_selected_and_declares_browser() -> None:
    components = tomllib.loads(_text(".prodockit-components.toml"))["components"]
    assert components == {"mermaid": True, "maths": True}
    manifest = json.loads(_text("tools/mermaid/package.json"))
    lock = json.loads(_text("tools/mermaid/package-lock.json"))
    assert "puppeteer" in manifest["dependencies"]
    assert lock["packages"][""]["dependencies"] == manifest["dependencies"]
    assert "/.prodockit-adopt-backups/" in _text(".gitignore").splitlines()


def test_mathjax_cascade_includes_browser_checks_and_patched_xml() -> None:
    manifest = json.loads(_text("tools/mathjax/package.json"))
    lock = json.loads(_text("tools/mathjax/package-lock.json"))
    assert "puppeteer-core" in manifest["dependencies"]
    assert lock["packages"][""]["dependencies"] == manifest["dependencies"]
    assert manifest["overrides"]["@xmldom/xmldom"] == "0.9.12"
    assert lock["packages"]["node_modules/@xmldom/xmldom"]["version"] == "0.9.12"
    for workflow in (".github/workflows/docs.yml", ".gitlab-ci.yml"):
        text = _text(workflow)
        assert text.index("npm ci --prefix tools/mathjax") < text.index("python tools/prepare_website_mathjax.py")
        assert text.index("python tools/prepare_website_mathjax.py") < text.index("zensical build")




def test_repository_setup_documents_editor_free_options_and_safe_recovery() -> None:
    customise = _text("docs/customise.md")
    for option in ("--create-readme", "--site-name", "--site-url"):
        assert option in customise
    assert "does not prove that the website has been published" in customise


def test_publishing_installs_pdf_fonts_before_diagnostics() -> None:
    for workflow in (".github/workflows/docs.yml", ".gitlab-ci.yml"):
        text = _text(workflow)
        install_lines = [
            line for line in text.splitlines()
            if "apt-get install" in line and "libpango-1.0-0" in line
        ]
        assert len(install_lines) == 1, workflow
        for package in ("fontconfig", "fonts-inter", "fonts-jetbrains-mono"):
            assert package in install_lines[0].split(), (workflow, package)
        assert text.index(install_lines[0]) < text.index("pdk diag"), workflow


def test_python_artifact_builds_use_the_version_file() -> None:
    version = _text(".python-version").strip()
    github = _text(".github/workflows/docs.yml")
    gitlab = _text(".gitlab-ci.yml")

    assert version == "3.14"
    assert "python-version-file: .python-version" in github
    assert "python-version: 3.x" not in github
    assert f"image: python:{version}" in gitlab


def test_retired_automation_and_paths_are_not_shipped() -> None:
    assert not (ROOT / ".github" / "workflows" / "drift.yml").exists()
    assert not (ROOT / "docs" / "javascript").exists()
    assert not (ROOT / "sync_repo_icon.py").exists()
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


def test_guide_uses_native_zensical_site_and_release_variables() -> None:
    home = _text("docs/index.md")
    customise = _text("docs/customise.md")
    macro_module = _text("macros.py")
    workflows = "\n".join(
        (
            _text(".github/workflows/docs.yml"),
            _text(".github/workflows/redeploy-after-release.yml"),
            _text(".gitlab-ci.yml"),
        )
    )

    assert "{% if git.short_tag %}" in home
    assert "{{ git.short_tag }}" in home
    assert "{{ config.site_name }}" in customise
    assert "release tag" not in macro_module
    assert "word count, repo URL" in macro_module
    assert "`git.short_tag`" in workflows


def test_built_home_page_renders_the_native_git_short_tag() -> None:
    short_tag = subprocess.run(
        ["git", "describe", "--tags", "--abbrev=0"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    home = _text("public/index.html")

    assert f"Release: {short_tag}" in home
    assert "{{ git.short_tag }}" not in home


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
    editing = _text("docs/startediting.md")

    assert "forward cross-page" in content
    assert "11pt body text" in customise_words
    assert "10pt inline or fenced code" in customise_words
    assert "prodockit template-sync --apply" in build
    assert "preserves every existing" in build
    assert "`pdk-pdf.toml`" in build
    assert "generated root files" in editing




def test_getting_started_replaces_the_duplicated_install_manual() -> None:
    guide = _canonical_text("docs/gettingstarted.md")
    about = _text("docs/about.md")
    config = _canonical_text("zensical.toml")

    for old_page in (
        "installing.md",
        "adoptioninstall.md",
        "bootstrapinstall.md",
        "installtooling.md",
    ):
        assert not (ROOT / "docs" / old_page).exists()
        assert old_page not in config
        assert old_page not in "\n".join(
            path.read_text(encoding="utf-8")
            for path in (ROOT / "docs").glob("*.md")
        )

    assert "# Getting started" in guide
    assert "https://prodockit.org/gettingstarted/" in guide
    assert "https://prodockit.org/choosing-installation/" in guide
    assert "https://prodockit.org/installation/" in guide
    assert "https://prodockit.org/getting-started/" in guide
    assert "https://prodockit.org/manual-install/" in guide
    for path in ("Adopt Prodockit", "Build a template site", "Build site manually"):
        assert path in guide
    assert "[Start editing](startediting.md)" in guide
    assert "[Additional tooling](additionaltooling.md)" in guide
    assert "## Choose how to install" in about
    assert "[Getting started](gettingstarted.md)" in about
    assert '{"2. Getting started" = "gettingstarted.md"}' in config
    assert '[project.markdown_extensions."prodockit.steps"]' in config


def test_other_guide_pages_link_to_the_local_getting_started_entry() -> None:
    installation_routes = (
        "gettingstarted/",
        "introduction/",
        "choosing-installation/",
        "installation/",
        "getting-started/",
        "manual-install/",
        "troubleshooting-installs/",
    )
    for path in _canonical_guide_pages():
        if not path.endswith(".md") or path == "docs/gettingstarted.md":
            continue
        text = _canonical_text(path)
        assert not any(
            f"https://prodockit.org/{route}" in text
            for route in installation_routes
        ), path




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
        _canonical_text(path)
        for path in _canonical_guide_pages()
        if path.endswith(".md") and path.count("/") == 1
    )

    versioned_product = re.compile(
        r"\b(?:prodockit|Zensical|Pandoc|Node\.js|MathJax)\s+v?\d+\.\d+",
        re.IGNORECASE,
    )
    assert not versioned_product.search(guide)
    assert not re.search(r"prodockit\s*[<>=]=?\s*\d", guide, re.IGNORECASE)
    assert not re.search(r"nodesource\.com/setup_\d+", guide, re.IGNORECASE)
    assert set(re.findall(r"\bPython\s+v?(\d+\.\d+)", guide, re.IGNORECASE)) == {
        "3.14"
    }


def test_guide_uses_zensical_commands_with_legacy_config_names_only() -> None:
    guide = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((ROOT / "docs").rglob("*.md"))
    )
    without_legacy_config_names = re.sub(
        r"mkdocs\.ya?ml", "", guide, flags=re.IGNORECASE
    )

    assert "mkdocs" not in without_legacy_config_names.lower()
    assert not re.search(
        r"\bmkdocs\s+(?:build|serve|new|gh-deploy)\b", guide, re.IGNORECASE
    )
    assert "legacy `mkdocs.yml` file that Zensical reads directly" in guide


def test_install_preparation_is_deferred_to_extensions() -> None:
    guide = _canonical_text("docs/gettingstarted.md")
    editing = _text("docs/startediting.md")

    assert "https://prodockit.org/installation/" in guide
    assert "supported Python" in guide
    assert "project-specific" in guide
    assert "Python 3.14" in editing
    assert "every new terminal prompt begins" in editing
    assert "pip install" not in guide


def test_optional_homebrew_install_actions_remain_prominent() -> None:
    additional = _text("docs/additionaltooling.md")
    css = _text("docs/stylesheets/extra.css")
    button = (
        "[:simple-homebrew: Install Homebrew](https://brew.sh/)"
        '{ .md-button .homebrew-button target="_blank" rel="noopener" }'
    )

    assert additional.count(button) == 2
    vale = additional[
        additional.index("### Add shared checks with Vale") : additional.index(
            "## Convert an existing document to Markdown"
        )
    ]
    imageoptim = additional[additional.index("## Optimise images before committing") :]
    assert vale.index(button) < vale.index("brew --version") < vale.index(
        "brew install vale"
    )
    assert imageoptim.index(button) < imageoptim.index(
        "brew --version"
    ) < imageoptim.index("brew install --cask imageoptim")
    assert ".md-typeset .homebrew-button" in css
    assert "background-color: #fbb040" in css
    assert "color: #171717" in css


def test_surrey_guidance_is_hidden_from_the_standard_guide() -> None:
    environment = Environment(autoescape=False)
    context = {
        "acronym_style": lambda: "",
        "config": {"site_name": ""},
        "git": {"short_tag": ""},
        "glossary_style": lambda: "",
        "heading_counter_reset": lambda _page: "",
        "is_surrey": False,
        "page": None,
        "reference_style": lambda: "",
        "repo_url": "",
        "word_count": "",
    }
    standard = "\n".join(
        environment.from_string(_canonical_text(path)).render(context)
        for path in _canonical_guide_pages()
        if path.endswith(".md") and path.count("/") == 1
    )

    assert not re.search(
        r"University of Surrey|gitlab\.surrey|pages\.surrey|\bstudents?\b|"
        r"\bcoursework\b|\bassessed\b",
        standard,
        re.IGNORECASE,
    )



def test_optional_tooling_platform_tabs_are_consistently_ordered() -> None:
    source = _text("docs/additionaltooling.md")
    labels = re.findall(
        r'^\s*=== "(:(?:material-apple|fontawesome-brands-windows|material-linux): [^"]+)"$',
        source,
        flags=re.MULTILINE,
    )
    expected_group = [
        ":material-apple: macOS",
        ":fontawesome-brands-windows: Windows",
        ":material-linux: Linux (Ubuntu)",
    ]
    assert labels
    assert len(labels) % 3 == 0
    assert labels == expected_group * (len(labels) // 3)


def test_guide_is_split_into_top_level_workflow_sections() -> None:
    config = _canonical_text("zensical.toml")

    assert '{"Guide" = [' not in config
    assert '{"Getting started" = [' in config
    assert '{"Edit" = [' in config
    assert '{"Basics" = [' in config
    assert '{"Customise" = [' in config
    assert '{"Build and test" = [' in config
    assert config.count('{"8. Document appearance and structure" = "customise.md"}') == 1
    assert config.count('{"9. Prodockit authoring features" = "customisecontent.md"}') == 1
    assert config.count('{"10. Build and publish" = "customisebuild.md"}') == 1
    assert '"testing.md"' not in config
    install = config[config.index('{"Getting started" = [') : config.index('{"Edit" = [')]
    build = config[
        config.index('{"Build and test" = [') : config.index('{"Reference" = [')
    ]
    assert '{"2. Getting started" = "gettingstarted.md"}' in install
    assert '{"3. Additional tooling" = "additionaltooling.md"}' in install
    assert '{"3. Additional tooling" = "additionaltooling.md"}' not in build
    numbers = [
        int(number)
        for number in re.findall(r'\{"(\d+)\. [^"]+" = "[^"]+"\}', config)
    ]
    assert numbers == list(range(1, 11))


def test_additional_tooling_is_an_optional_follow_on() -> None:
    guide = _canonical_text("docs/gettingstarted.md")
    additional = _text("docs/additionaltooling.md")

    assert "[Additional tooling](additionaltooling.md) is optional" in guide
    assert "[installation route you chose](gettingstarted.md)" in additional
    assert "sections that match your work" in additional
    assert "SSH remains the preferred connection" in additional
    assert "[Start editing](startediting.md)" in additional


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
    assert "Most document-wide changes are made in one of six places" in customise
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
        "Choose an installation route",
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
