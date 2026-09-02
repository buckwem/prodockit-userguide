---
icon: lucide/book-open
---

<!--
# Copyright (c) 2025-2026 Mark Buckwell and contributors
# SPDX-License-Identifier: MIT
-->

{{ heading_counter_reset(page) }}

# Document appearance and structure

Most document-wide changes are made in one of four places:

| What you are changing | File or directory |
|---|---|
| Site details, navigation, theme, and PDF settings | `zensical.toml` |
| Cover-page content | `docs/index.md` |
| Logos, header backgrounds, and other images | `docs/assets/` |
| Managed website and PDF styling | `docs/stylesheets/pdk.css` and `pdk-pdf.css` |
| Your styling overrides | `docs/stylesheets/extra.css` and `print.css` |
/// table-caption | <
    attrs: {id: table-customisation-locations}

Where document-wide changes are made
///

Make one kind of change at a time, preview the website with `zensical serve`,
and build the PDF before committing. Use
[Prodockit authoring features](customisecontent.md) for headings, references,
citations, glossary terms, captions, tables, steps, trees, and the index.

## Customise the website

Open `zensical.toml` to change the \index{Website!configuration}. The `[project]` section contains the site's identity and
the `[project.theme]` section controls its appearance. The examples below cover
the settings most authors change; the
[Zensical setup guide](https://zensical.org/docs/setup/){target="_blank"}
contains the complete reference.

### Set the site details

Review these values first:

``` toml
[project]
site_name = "Project report"
site_description = "Design and evaluation of the project"
site_author = "Your Name"
site_url = "https://example.github.io/project/"
copyright = "Copyright &copy; 2026 Your Name"
repo_url = "https://github.com/username/project"
repo_name = "project"
```

`site_name` also appears in the PDF's running header and on the cover. The
repository settings create the website's repository link; they do not change
the Git remote used for pushing.

### Keep repository details in sync

\index{Tasks!Synchronise repository details} after the project is moved,
renamed, or copied from the template. First check that
the displayed repository details still match its `origin` remote:

1. Change to the repository directory with `cd`.
2. Activate its virtual environment as shown in
    [Prepare the terminal](customisebuild.md#prepare-the-terminal).
3. Run the read-only check:

``` bash
prodockit sync-repo --check
```

If the check reports differences, apply them with:

``` bash
prodockit sync-repo
```

The command updates `repo_url`, `repo_name`, `edit_uri`, the repository icon,
and the badges in `README.md`. It does not change the Git remote or push any
files. Review the reported changes and `git diff` before committing them.

The [command-line guide](https://prodockit.org/command-line/){target="_blank"}
provides the full `sync-repo` reference.

Set a PDF-only copyright value when its footer needs different content:

``` toml
[project.extra]
pdf_copyright = "Copyright &copy; 2026 Your Name"
```

### Replace the site logo

Replace both default logo files so light and dark mode remain readable:

- `docs/assets/logo_default_black.png`
- `docs/assets/logo_default_white.png`

Do not edit `logo_black.png` or `logo_white.png`; each build regenerates those
working copies.

{% if is_surrey %}
A project published through University of Surrey services uses the Surrey logo
automatically.
{% endif %}

To add a browser-tab icon, put the image under `docs/` and set:

``` toml
[project.theme]
favicon = "images/favicon.png"
```

### Choose colours and the page heading

The existing palette blocks provide light and dark modes. Change their schemes
or toggle icons only when the defaults do not suit the document:

``` toml
[[project.theme.palette]]
media = "(prefers-color-scheme: light)"
scheme = "default"
toggle.icon = "lucide/sun"
toggle.name = "Switch to dark mode"

[[project.theme.palette]]
media = "(prefers-color-scheme: dark)"
scheme = "slate"
toggle.icon = "lucide/moon"
toggle.name = "Switch to light mode"
```

Replace `header-background.jpg` and `header-background-dark.jpg` under
`docs/assets/` to change the website header. Check contrast in both modes.

### Fonts

Set the proportional and monospace fonts in `zensical.toml`:

``` toml
[project.theme.font]
text = "Inter"
code = "Jetbrains Mono"
```

The website and PDF use the same families. The PDF defaults to **11pt body
text** and **10pt inline or fenced code**, keeping code one point smaller than
the surrounding prose. Ensure custom fonts are installed wherever local PDF
builds run.

### Choose icons and website features

`[project.theme.icon]` controls the edit, view, and repository icons. Use an
icon name supported by Zensical:

``` toml
[project.theme.icon]
edit = "lucide/pencil"
view = "lucide/eye"
repo = "fontawesome/brands/github"
```

The `features` list under `[project.theme]` enables website behaviour such as
sticky navigation, search highlighting, and the back-to-top button. The
comments in `zensical.toml` link each feature to its Zensical documentation.
Change only the feature line you understand, then test desktop and mobile
layouts.

### Extra CSS and JavaScript

The project already loads its shared website style sheet and local MathJax
files:

``` toml
extra_css = ["stylesheets/pdk.css", "stylesheets/extra.css"]
extra_javascript = [
    "javascripts/mathjax.js",
    "javascripts/vendor/mathjax/tex-svg-full.js",
    "javascripts/extra.js",
]
```

Keep the MathJax configuration before its bundle. Prefer a versioned local copy
of a library to a floating CDN address so builds remain reproducible and work
offline.

Load the managed PDF defaults before your PDF-only overrides:

``` toml
[project.extra]
pdf_extra_css = ["stylesheets/pdk-pdf.css", "stylesheets/print.css"]
```

The complete PDF cascade is `pdk.css`, `extra.css`, `pdk-pdf.css`, then
`print.css`; your two override files therefore take precedence over the
corresponding managed defaults.

### Add footer links

Add a social or organisation link by repeating this block:

``` toml
[[project.extra.social]]
icon = "fontawesome/brands/github"
link = "https://github.com/username"
```

## Navigation structure

The \index{Website!navigation} `nav` list in `zensical.toml` controls the page order for both the website
and PDF. A top-level group becomes a website tab; entries inside it become
pages or collapsible groups.

``` toml
nav = [
    {"Cover" = [
        "index.md",
    ]},
    {"Report" = [
        {"1. Introduction" = "introduction.md"},
        {"2. Design" = "design.md"},
        {"3. Evaluation" = "evaluation.md"},
    ]},
    {"Appendixes" = [
        {"Appendix A. Acronyms" = "acronyms.md"},
        {"Appendix B. Glossary" = "glossary.md"},
        {"Appendix C. References" = "references.md"},
    ]},
]
```

To add a page:

1. Create its `.md` file beneath `docs/`.
2. Give it one level-one heading.
3. Add its path to `nav` in the required position.
4. Renumber the visible `nav` labels after it where necessary.
5. Preview the website and build the PDF.

Do not put a second level-one heading in the same file. Create another page
instead. [Changing heading numbering](customisecontent.md#changing-heading-numbering)
explains automatic in-page numbers and appendixes.

## Customise front page

Edit `docs/index.md` to change the \index{Website!front page}. Keep the surrounding HTML classes and
Jinja markers until you have confirmed what each one supplies.

### Institution branding

{% if is_surrey %}
The cover uses one branch for University of Surrey projects and another for
other organisations:

``` markdown
{% raw %}
{% if is_surrey %}
... Surrey content ...
{% else %}
... other institution or organisation ...
{% endif %}
{% endraw %}
```

Edit the `{% raw %}{% else %}{% endraw %}` branch for another institution,
including its name, programme text, and logo paths. The build detects Surrey
from the repository host and configured addresses.
{% else %}
The cover contains a default organisation branch. Edit its organisation name,
programme or document description, and logo paths. Preserve any surrounding
Jinja markers: they allow the same source to select different institutional
branding when a project needs it.
{% endif %}

The template sets `on_error_fail = true` for Zensical's macros extension.
Keep that setting when changing `zensical.toml`: if Jinja cannot render a page
variable or macro call, the preview or build then stops instead of returning
the unrendered page and allowing a broken site to be published. The
[website-macros reference](https://prodockit.org/macros/){target="_blank"}
shows the complete configuration.

### PDF-only and web-only content

Add `.pdf-only` to content intended only for the PDF and `.web-only` to content
intended only for the website. For example:

``` markdown
<p class="pdf-only">Word count: {WORDCOUNT}</p>

[Download PDF](site_documentation.pdf){ .md-button .web-only }
```

Use these classes only when the two outputs genuinely need different content.

### Site name

Zensical exposes the `site_name` from `zensical.toml` through its native
`config` variable:

``` markdown
<p class="title-ctr-b4">{% raw %}{{ config.site_name }}{% endraw %}</p>
```

Edit `site_name` rather than typing a second copy into the cover. Remove the
line from both branding branches if the cover should not show it.

### Word count and repository link

The shipped cover can display these PDF markers:

``` markdown
<p class="pdf-only">Word count: {WORDCOUNT}</p>
<p class="pdf-only">Repo: {REPOURL}</p>
<p class="pdf-only">Release: {RELEASE}</p>
```

- `{WORDCOUNT}` counts the built document, excluding the cover, contents page,
    and pages marked `exclude_from_word_count: true`.
- `{REPOURL}` uses the repository's `origin` remote.
- `{RELEASE}` uses the latest published repository release and disappears when
    none exists.

Exclude another page from the word count in its front matter:

``` markdown
---
icon: lucide/book-open
exclude_from_word_count: true
---
```

For the website, ProDocKit supplies `{% raw %}{{ word_count }}{% endraw %}` and
`{% raw %}{{ repo_url }}{% endraw %}`. Zensical supplies the release through its
native `{% raw %}{{ git.short_tag }}{% endraw %}` variable. The website count is
an estimate and can differ slightly from the final PDF count.

### Download PDF button

The cover's `.web-only` button links to `site_documentation.pdf`:

``` markdown
[:material-file-pdf-box: Download PDF](site_documentation.pdf){ .md-button .web-only }
```

Keep the filename aligned with the build output. Remove the line if the site
does not publish a PDF.

## Customise PDF generation

The \index{PDF!configuration} is read when you run `prodockit pdf`. It uses the same `zensical.toml` and
rendered Markdown as the website, so site name, fonts, extensions, and most
content customisations carry across automatically. See
[Build the PDF](startediting.md#build-the-pdf) for the working command and
[Build and publish](customisebuild.md) for build configuration.

### Page header

The running header shows `site_name` on the left and the current chapter on the
right. Change `site_name` for the shared title. The chapter title comes from
the page's level-one heading.

### Page footer

The footer shows the copyright on the left and “Page X of Y” on the right. Set
shared appearance values only when the defaults need changing:

``` toml
[project.extra]
pdf_header_footer_font_size = "10pt"
pdf_header_footer_color = "#555555"
pdf_header_footer_divider_color = "#e2e8f0"
```

The cover does not show the running header or footer.

### Page size and margins

Set the physical page and margins in `[project.extra]`:

``` toml
pdf_page_size = "A4"
pdf_margin_top = "2cm"
pdf_margin_right = "2cm"
pdf_margin_bottom = "2cm"
pdf_margin_left = "2cm"
```

These values affect only the PDF. Build and inspect pages containing wide
tables, figures, and long headings after changing them.

### Double-sided printing

For a bound document, mirror the inner and outer margins and begin chapters on
right-hand pages:

``` toml
[project.extra]
pdf_double_sided = true
pdf_margin_inner = "2.5cm"
pdf_margin_outer = "1.5cm"
```

Use `recto_title: "Short title"` in a page's front matter if its chapter title
is too long for the running header.

### Source-code bundling

Build a separate PDF containing the authored Markdown, configuration, and root
README when a submission requires its source:

``` bash
prodockit source-bundle
```

It writes `source_bundle.pdf` alongside `site_documentation.pdf`. It does not
include the entire repository or generated template-maintenance files. The
[PDF source-bundle reference](https://prodockit.org/pdf/#prodockitpdfsource_bundle){target="_blank"}
describes programmatic full-repository bundling for the less common case that
requires it.

### Screenshots

Give screenshots the `.screenshot` class and a numbered figure caption:

``` markdown
![Initial commit](images/initial-commit.png){ width="40%" .screenshot }
/// figure-caption
    attrs: {id: figure-screenshot-example}

Initial commit
///
```

The class adds a border and shadow in both outputs. Do not apply it to logos,
icons, or diagrams.

## Directory structure

The \index{Project!directory structure} below shows the files an author most often changes:

/// tree
    indent: 4

docs/ - document source
    index.md - cover page
    originality.md - originality and AI-use declaration
    section1.md - report content
    acronyms.md - acronym definitions
    glossary.md - glossary definitions
    references.md - hand-written reference list
    assets/ - logos and header backgrounds
    images/ - content images and screenshots
    stylesheets/ - managed styles followed by your overrides
        pdk.css - managed website and shared component styles
        pdk-pdf.css - managed PDF styles
        extra.css - your website and shared overrides
        print.css - your PDF-only overrides
    javascripts/ - local website scripts and MathJax files
tools/ - Mermaid and mathematics renderers
test/ - website and PDF checks
zensical.toml - configuration, navigation, extensions, and PDF settings
references.bib - BibTeX or BibLaTeX sources
requirements.txt - Python dependencies
README.md - repository front page
///

Use [Prodockit authoring features](customisecontent.md) for the authoring files
and [Build and publish](customisebuild.md) for build tools and publishing files.

## Where to go next {: #customise-where-to-go-next }

Continue to [Prodockit authoring features](customisecontent.md) for headings,
references, sources, captions, tables, procedures, directory trees, and the
index. Then use [Build and publish](customisebuild.md) for local and published
build behaviour.
