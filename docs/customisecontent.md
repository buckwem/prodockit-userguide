---
icon: lucide/book-open
---

<!--
# Copyright (c) 2025-2026 Mark Buckwell and contributors
# SPDX-License-Identifier: MIT
-->

{{ heading_counter_reset(page) }}

# Prodockit authoring features

[Document appearance and structure](customise.md) covers the appearance and structure of the
website and PDF. This page covers the prodockit features an author uses while
writing. They are already enabled in the template and work in both outputs
unless a section says otherwise.

Use this page to get a feature working. Follow its link to the
[Extensions Guide](https://prodockit.org/extensions/){target="_blank"} when you
need every option or the generated HTML details.

| When you want to… | Use |
|---|---|
| Number headings and appendixes | `prodockit.headings` |
| Link to a heading, figure, or table | `prodockit.refs` |
| Write a procedure | `prodockit.steps` |
| Show folders and files | `prodockit.tree` |
| Maintain a hand-written reference list | `prodockit.citations` |
| Generate references from a `.bib` file | `prodockit.bibliography` |
| Define acronyms and glossary terms | `prodockit.glossary` |
| Format complex tables | `prodockit.tables` |
| Produce a PDF index | `prodockit.index` |
/// table-caption | <
    attrs: {id: table-authoring-features}

Authoring features
///

## Changing heading numbering

\index{Headings!numbering} is enabled for the website and PDF by default. To turn it
off, set this in `zensical.toml`:

``` toml
[project.extra]
heading_numbering = false
```

Set it back to `true` to restore them. The numbers written in the `nav` titles
are separate and must be kept in sequence manually:

``` toml
{"6. Case study" = "casestudy.md"}
```

### Leave a heading unnumbered or out of PDF navigation

Add classes to a heading when it should not behave like an ordinary numbered
section:

``` markdown
# Cover page {: .unnumbered .unlisted .unbookmarked }
```

- `.unnumbered` removes its number without consuming the next number.
- `.unlisted` leaves it out of the PDF's Table of Contents page.
- `.unbookmarked` leaves it out of the PDF reader's bookmark outline.

Use only the classes you need. The heading keeps its id and remains a valid
link target. See the
[`prodockit.headings` reference](https://prodockit.org/extensions/headings/){target="_blank"}
for numbering modes and advanced configuration.

## Section cross-references

\index{Cross-references} need an important target with a short, stable id so a later wording change does not
break its links:

``` markdown
## Deployment process {: #deployment }
```

Link to it from any page with `\ref{id}`:

``` markdown
Follow the process in \ref{deployment}.
```

The displayed number and heading text update automatically when content moves.
Targets may appear on a later page: a forward cross-page reference resolves on
the first complete build. The same syntax links to a figure or table when its
caption has an id.

If the target is missing or mistyped, the link displays `??`. Search for that
marker in both the website and PDF before publishing.

### Include the target's PDF page number

Use `\autoref{id}` where someone reading a printed copy may need to turn to the
target:

``` markdown
The numbering rules are explained in \autoref{changing-heading-numbering}.
```

On the website it looks like `\ref{id}`. In the PDF it also says “on page N”.
Use `\ref` for ordinary links and `\autoref` when the page number helps the
printed reader. See the
[`prodockit.refs` reference](https://prodockit.org/extensions/refs/){target="_blank"}
for caption references and troubleshooting.

## Write a numbered procedure

Use `prodockit.steps` for \index{Numbered procedures} when a reader must carry out actions in order. Use an
ordinary numbered list when the items are facts.

```` markdown
/// steps

//// step | Preview the website

``` bash
zensical serve
```

Leave the preview running while you edit.

////

//// step | Stop the preview

Return to the terminal and press `Ctrl+C`.

////

///
````

The outer block uses three slashes. Each nested step uses four and closes with
the same number. A step can contain paragraphs, commands, admonitions, or tabs.

Continue after a break by setting the next number:

``` markdown
/// steps
    start: 3

//// step | Build the finished website

Run `zensical build --clean --strict`.

////

///
```

Options go immediately below `/// steps`, indented by four spaces, followed by
a blank line. See the
[`prodockit.steps` reference](https://prodockit.org/extensions/steps/){target="_blank"}
for ids and more complex content.

## Show a directory structure

Use `prodockit.tree` to create \index{Directory trees} instead of drawing a directory with box characters:

``` markdown
/// tree
    indent: 4

docs/ - source files for the document
    index.md - home page
    images/ - images used by the document
        architecture.png - system architecture diagram
zensical.toml - website configuration
///
```

A trailing `/` marks a directory. An entry without one is a file. Add a
description after ` - `, including the spaces on both sides of the hyphen.
`indent: 4` makes each four-space level one level of the tree. See the
[`prodockit.tree` reference](https://prodockit.org/extensions/tree/){target="_blank"}
for icon choices and error explanations.

## References and bibliography

The template supports \index{References} and a generated \index{Bibliography}. Pick the approach that matches how your
sources are maintained; both can coexist, but most documents need only one.

| Approach | Best when | Markers |
|---|---|---|
| Hand-written references | You need complete control over a short reference list | `\citeref{id}` |
| BibTeX bibliography | You already use a `.bib` file or need a formal CSL style | `\cite{id}` and `\bibliography` |
/// table-caption | <
    attrs: {id: table-source-management}

Ways to manage sources
///

### Maintain a hand-written reference list

Add each source to `docs/references.md` and give it a unique id, display text,
and `.reference` class:

``` markdown
Skoulikari, A. (2023) *Learning Git: A Hands-On and Visual Guide to the Basics
of Git*. Sebastopol, CA: O'Reilly Media.
{: #skou2023 .reference data-cite-text="Skoulikari, 2023" }
```

Leave a blank line around every entry. Cite it from any page with:

``` markdown
Git records changes to a project.\citeref{skou2023}
```

Use a comma inside one marker to cite several sources:
`\citeref{skou2023,chacon2014}`. A missing id displays `?`.

The template's default `reference_style = "european"` keeps entries close
together. Change it to `"global"` in `[project.extra]` for larger spacing and
a hanging indent. See the
[`prodockit.citations` reference](https://prodockit.org/extensions/citations/){target="_blank"}
for the layout settings and generated links.

### An alternative: prodockit.bibliography

Put BibTeX or BibLaTeX entries in `references.bib`. Cite an entry by its key:

``` markdown
Git is a distributed version control system \cite{chacon2014}.
```

Place the generated list where it belongs:

``` markdown
# References

\bibliography
```

The template points to `harvard-cite-them-right.csl`; change `csl_style` under
`[project.markdown_extensions."prodockit.bibliography"]` when another style is
required. Pandoc must be installed for website and PDF builds using this
extension. See the
[`prodockit.bibliography` reference](https://prodockit.org/extensions/bibliography/){target="_blank"}
for `.bib` files, CSL styles, locators, and multiple bibliographies.

## Acronyms and abbreviations

Define \index{Acronyms} once in `docs/acronyms.md`:

``` markdown
**CSS** - Cascading Style Sheets
{: #css .acronym data-term="CSS" }
```

Insert it from any page with `\gls{id}`:

``` markdown
The website uses \gls{css} for its appearance.
```

Keep ids short, lowercase, and unique. A missing id displays `?`.

## Glossary {: #glossary-page-setup }

\index{Glossary} terms use the same extension and syntax in `docs/glossary.md`:

``` markdown
**Markdown** - A lightweight markup language for formatting plain text.
{: #markdown-def .glossary data-term="Markdown" }
```

Insert the term with `\gls{markdown-def}`. Acronyms and glossary terms share
one id namespace, so do not reuse an id. Use an ordinary Markdown link when
the sentence needs different link text, such as “see the glossary”.

See the
[`prodockit.glossary` reference](https://prodockit.org/extensions/glossary/){target="_blank"}
for plural forms, first-use expansion, styling, and cross-links.

## Appendixes

Mark \index{Appendixes} in the page's front matter:

``` markdown
---
icon: lucide/book-open
is_appendix: true
exclude_from_word_count: true
---
```

Appendixes receive letters in `nav` order without consuming a chapter number.
Their visible `nav` labels are still written manually:

``` toml
{"Appendix A. Acronyms" = "acronyms.md"}
```

The template already configures its acronym, glossary, and reference pages as
appendixes.

## Back-of-book index

Create a \index{Back-of-book index} by marking a term where it is discussed:

``` markdown
A \index{merge conflict} occurs when Git cannot combine two changes.
```

Use `Parent!Child` to group entries and backticks for commands:

``` markdown
Load the \index{Git!ssh key} before running \index{`git push`}.
```

The text remains normal on the website. The PDF collects every marker into an
alphabetical index because `include = true` is set for `prodockit.index` in
`zensical.toml`. See the
[`prodockit.index` reference](https://prodockit.org/extensions/index-terms/){target="_blank"}
for ranges, hidden markers, sorting, and configuration.

## Captions

\index{Captions} identify every figure and table that a reader may need to discuss or reference.
Put the caption block immediately after its image or table.

### Caption a figure {: #caption-a-figure }

Give the caption a stable id when the figure will be referenced elsewhere:

``` markdown
![Architecture overview](images/architecture.png)
/// figure-caption
    attrs: {id: figure-architecture}

Architecture overview
///
```

Refer to it with `\ref{figure-architecture}`. Add the `.screenshot` class to
the image when it is a screenshot rather than a diagram, logo, or photograph.

### Caption a table {: #caption-a-table }

Add `| <` so a table caption is displayed above its table even though the
caption block remains after it in the Markdown:

``` markdown
| Option | Purpose |
|---|---|
| `--clean` | Remove the previous output before building |
/// table-caption | <
    attrs: {id: table-build-options}

Build options
///
```

Give the caption an id when it will be referenced with
`\ref{table-build-options}`. Use plain `/// caption` only for an unnumbered
decorative image. The
[PyMdown Blocks caption reference](https://facelessuser.github.io/pymdown-extensions/extensions/blocks/plugins/caption/){target="_blank"}
explains fixed numbers, extra classes, and positioning.

### Set table widths and alignment

Adjust \index{Tables!width and alignment} when the automatic widths do not read well:

``` markdown
| Name {: width="30%" } | Description |
|:---|---|
| Headings | Heading ids and section numbers |
| References | Cross-references resolved by number |
```

The colon in `:---` left-aligns that column. Use `:---:` to centre it or
`---:` to right-align it. Width and alignment work together.

### Make a dense table compact

Add `.compact` to any header cell to reduce the padding and minimum widths for
the whole table:

``` markdown
| Threat {: .compact } | Likelihood | Impact | Risk |
|---|---|---|---|
| Credential theft | H | H | H |
```

### Merge cells and use more than one header row

Use `colspan` and `rowspan` on the cells that survive a merge. Keep empty
placeholder cells so every Markdown row still has the same number of columns:

``` markdown
| Target {: rowspan=2 } | Measured {: colspan=2 } | | Note {: rowspan=2 } |
|---|---|---|---|
| | Before {: .header } | After | |
| Widget | 1 | 2 | ok |
```

The `.header` class promotes the second row into the repeating table header.
Put it on a cell containing text.

### Shade a cell

Header cells have a subtle 5% shade by default. Remove it from one cell with
`shade="off"`, or set a percentage on a header or body cell:

``` markdown
| Unshaded {: shade="off" } | Grouped heading {: colspan=2 shade="8%" } | |
|---|---|---|
| Normal | Highlighted {: shade="5%" } | Normal |
```

Shading belongs to the surviving cell and therefore works with merged cells.

### Fit an unusually wide table

First try shorter headings, `.compact`, and sensible column widths. If a
heading still makes a narrow data column too wide, rotate it with `rotate=270`
and give it both a `width` and a `height`:

``` markdown
| Item | Availability {: rotate=270 width="2em" height="90pt" } |
|---|---|
| Investment data | H |
```

For a table or diagram that genuinely needs a landscape PDF page, wrap it and
its caption in:

``` markdown
<div class="landscape-page" markdown="1">

| ID | Description |
|---|---|
| 1 | A wide item |
/// table-caption | <
    attrs: {id: table-landscape-example}

A wide reference table
///

</div>
```

The website remains in its normal layout. The PDF places the complete block on
a landscape page. See the
[`prodockit.tables` reference](https://prodockit.org/extensions/tables/){target="_blank"}
for validation rules and the remaining cell options.

## Finalising your document

\index{Tasks!Finalise a document} before publishing it:

1. Delete the author's warning admonition at the start of `originality.md`.
2. Search the website and PDF for unresolved `??` references and `?`
    citations or glossary terms.
3. Check every figure and table has the intended caption and number.
4. Check appendix labels and manually written numbers in `nav` remain in order.
5. Build both outputs and complete the review in
    [Build and publish](customisebuild.md#customisebuild-checks).

## Where to go next {: #customisecontent-where-to-go-next }

Continue to [Build and publish](customisebuild.md) to change how the website and
PDF are built and published. Use the
[Extensions Guide](https://prodockit.org/extensions/){target="_blank"} when a
feature needs an option not covered by this author workflow.
