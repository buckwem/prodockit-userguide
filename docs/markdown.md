---
icon: lucide/book-open
---

<!--
# Copyright (c) 2025-2026 Mark Buckwell and contributors
# SPDX-License-Identifier: MIT
-->

{{ heading_counter_reset(page) }}

# Markdown basics

[Markdown](https://www.markdownguide.org/){target="_blank"} is plain text with
small punctuation markers that describe its structure. A file ending in `.md`
remains readable in an editor, while Zensical turns it into the formatted
website and prodockit turns the same source into a PDF.

This page teaches the syntax used in ordinary writing. Start with headings,
paragraphs, links, images, and lists; return to the remaining sections when you
need them. Use [Zensical basics](zensicalbasics.md) for callouts, tabs,
diagrams, mathematics, and other extended features.

!!! note "The Markdown used by this project"
    Zensical uses [Python Markdown](https://python-markdown.github.io/){target="_blank"}
    with the extensions configured in `zensical.toml`. Markdown dialects differ
    in details, especially indentation and extended blocks. Treat the local
    Zensical preview as authoritative for this project.

!!! tip "Preview with this project's renderer"
    Use the **Zensical Studio viewer** while editing in Visual Studio Code, or
    activate the project environment and run:

    ``` bash
    zensical serve
    ```

    Both routes load the extensions and settings from this project's
    `zensical.toml`. A generic online Markdown preview does not, so features
    such as admonitions, captions, references, numbered headings, and tables
    can look incomplete or different there. See
    [Preview the website locally](startediting.md#preview-the-website-locally)
    for the complete preview workflow.

## Write a simple page

Write a \index{Markdown!page} with one level-one heading, followed by
paragraphs and lower-level headings:

``` markdown
# Project overview

This paragraph introduces the project. A blank line ends the paragraph.

## Purpose

This section explains why the project exists.

## Scope

This section explains what the project includes and excludes.
```

Leave a blank line between paragraphs, headings, lists, code blocks, and other
block elements. A line wrapping in the editor does not start a new paragraph;
an empty line does.

## Headings

The number of `#` characters sets the heading level:

``` markdown
# Page title
## Main section
### Subsection
#### Lower-level subsection
```

Use one `#` heading per page. The template uses it as the chapter title and
numbers the lower headings beneath it. Do not choose a heading level for its
visual size or skip from `##` to `####`; headings describe the structure of the
content.

Zensical generates a linkable id from each heading. Add a short, stable id when
another page will refer to it or when repeated headings could collide:

``` markdown
## Test results {: #integration-test-results }
```

See [Section cross-references](customisecontent.md#section-cross-references)
for using that id.

## Format text

``` markdown
**bold text**
*italic text*
***bold and italic text***
~~deleted text~~
`inline code`
```

Use emphasis to communicate meaning, not to imitate headings. Use inline code
for commands, file names, configuration keys, and short code fragments.

This project also supports underline, superscript, subscript, highlighting, and
keyboard keys; see [Formatting](zensicalbasics.md#formatting).

## Add links and images

Add \index{Markdown!links} and \index{Markdown!images} with descriptive text:

``` markdown
[Descriptive link text](https://example.com)
[Link with a title](https://example.com "Extra information")
![A description of what the diagram communicates](images/diagram.png)
```

Write link text that makes sense out of context rather than “click here”. Write
alternative text that communicates the image's purpose rather than its file
name. Paths are relative to the Markdown file: a page in `docs/` can use
`images/diagram.png` for `docs/images/diagram.png`.

Add attributes immediately after a link or image when needed:

``` markdown
[External reference](https://example.com){target="_blank"}
![Architecture](images/architecture.png){ width="70%" }
```

The `target` affects the website only. A printed PDF has no browser tab.

## Write lists

Write \index{Markdown!lists} with `-` for a bulleted list:

``` markdown
- First item
- Second item
    - Nested item
```

Use a number followed by a full stop for an ordered list:

``` markdown
1. First step
2. Second step
3. Third step
```

Python Markdown renumbers the items from the first number, so using `1.` for
every source item is also valid and avoids manual renumbering after an edit.

!!! warning "Use four spaces for nested content"
    Indent a nested list—and any paragraph, image, code block, admonition, or
    other content belonging to a list item—by exactly **four spaces**. Two spaces
    may work in another Markdown dialect but do not work reliably in this
    implementation.

Use task-list markers when the list represents work to complete:

``` markdown
- [x] Draft completed
- [ ] Diagram still required
```

## Write a definition list

``` markdown
Static site generator
:   A tool that builds a website from source files.

Repository
:   A project directory whose history is managed by Git.
```

The definition is indented beneath its term. Leave a blank line before the next
term.

## Show code and commands {: #markdown-code-blocks }

Show \index{Markdown!code} and commands by wrapping a short fragment in backticks:
`zensical.toml`.

For several lines, use three backticks and name the language after the opening
fence:

```` markdown
``` python
def greet(name):
    print(f"Hello, {name}!")
```
````

The language enables syntax highlighting. Use `bash` for macOS/Linux shell
commands, `powershell` for Windows commands, `toml` for `zensical.toml`, and
`text` for output that should not be highlighted. See
[Code blocks](zensicalbasics.md#zensicalbasics-code-blocks) for titles, line
highlighting, and annotations.

## Write tables

Write a basic \index{Markdown!table} using pipes for columns and a delimiter row beneath the header. Colons set text
alignment:

``` markdown
| Left-aligned | Centred | Right-aligned |
|:-------------|:-------:|--------------:|
| Row 1 | Data | 12 |
| Row 2 | Data | 34 |
```

Every row must describe the same number of columns. Use
[Prodockit authoring features](customisecontent.md#captions) for captions,
column widths, merged headers, cell shading, and wide tables.

## Add quotations and thematic breaks

Start each quoted paragraph with `>`:

``` markdown
> This is a quotation.
>
> It contains a second paragraph.
>
> > This sentence is nested inside the quotation.
```

Use an admonition rather than a quotation for your own note, warning, or tip.

Three hyphens on a line of their own create a thematic break:

``` markdown
---
```

## Avoid common mistakes {: #markdown-common-mistakes }

- **Missing blank lines:** Separate block elements with a blank line. Without
    one, a heading, list, attribute list, or code fence can become ordinary
    visible text.
- **Incorrect indentation:** Use four spaces for nested content. Tabs and two
    spaces are not interchangeable with this rule.
- **More than one level-one heading:** Use one `#` heading per page, then `##`
    and `###` beneath it.
- **Skipped heading levels:** Move from `##` to `###`, not directly to `####`.
- **Broken image paths:** Check images through Zensical and use paths relative
    to the Markdown page.
- **Visible punctuation:** To display a Markdown punctuation character
    literally, put a backslash before it; `\*` displays an asterisk instead of
    starting emphasis.

## Where to go next {: #markdown-where-to-go-next }

Continue to [Zensical basics](zensicalbasics.md) for the extended authoring
features configured by this project. If terminal commands are unfamiliar, use
[Shell commands](shcommands.md) as a beginner's reference while following the
rest of the guide.
