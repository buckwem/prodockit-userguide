---
icon: lucide/package-plus
---

<!--
Copyright (c) 2025-2026 Mark Buckwell and contributors
SPDX-License-Identifier: MIT
-->

{{ heading_counter_reset(page) }}

# Adoption install

`prodockit adopt` lets you \index{Tasks!Adopt an existing document} by adding prodockit's authoring components to an existing
Zensical or MkDocs document. It keeps the project's own template, structure,
appearance, Git history, editor, remote repository, and publishing workflow.
The command first reports what is needed, lets you choose Mermaid diagrams and
mathematical notation independently, and applies only the stages you approve.

Use this route when the document already builds and you want to add prodockit
without starting again from prodockit-template. If you do not have a template
of your own and want a formal-looking document as a head start, use
[Bootstrap Install](bootstrapinstall.md). To install and configure every part
of prodockit-template yourself, use [Manual install](installtooling.md).

!!! info "For an existing documentation project"
    Adoption assumes that Git, SSH, your preferred editor, and the project's
    normal Python environment already work. It does not configure or change
    them, and it never commits or pushes your work.

!!! important "Start with a working build"
    Build the existing website before adopting prodockit. A successful
    baseline makes it possible to distinguish an existing project problem
    from a change introduced during adoption.

## What adoption adds

The standard adoption adds:

- a `prodockit` requirement to the project's existing requirements
    file, or a new `requirements.txt` when the project has none;
- the standard prodockit Markdown extensions to the existing Zensical or
    MkDocs configuration;
- `docs/stylesheets/pdk.css`, loaded before the project's own
    stylesheets so its existing rules can still override the shared styles;
- `.prodockit-components.toml`, recording the optional renderers selected for
    the project; and
- project-local Mermaid and MathJax tooling only when those options are
    selected.

The standard extensions provide the building blocks for professional and
academic documents, including numbering and cross-references, citations and
bibliographies, glossaries and indexes, enhanced tables, steps, and directory
trees. Existing Markdown does not have to use every feature.

Mermaid and mathematics are off by default. A document using neither does not
need Node.js, Mermaid CLI, MathJax, or a browser renderer.

## How the stages work

The command presents seven stages in four phases, using the same prominent
phase and stage headings as `prodockit bootstrap`:

| Phase | What `prodockit adopt` checks |
| --- | --- |
| Assess | A supported project configuration and the active project environment |
| Integrate | The prodockit dependency, standard extensions, and shared website stylesheet |
| Optional renderers | Mermaid diagrams and mathematical notation, according to the saved choices |
| Verify | Whether the selected components are ready for a clean local build |

A satisfied stage is reported as `ok` and left alone. A stage needing a local
change is described before anything is written.

## Complete the adoption

/// steps

//// step | Check the existing project

Before changing packages or configuration, make sure the project builds and
that you understand any work already waiting to be committed.

Change to the repository directory containing one supported configuration:

- `zensical.toml`, `zensical.yml`, or `zensical.yaml`; or
- `mkdocs.yml` or `mkdocs.yaml`.

=== ":material-apple: macOS"

    ``` bash
    cd /path/to/your-document
    git status --short
    ```

=== ":fontawesome-brands-windows: Windows"

    In PowerShell:

    ``` powershell
    cd C:\path\to\your-document
    git status --short
    ```

=== ":material-linux: Linux (Ubuntu)"

    ``` bash
    cd /path/to/your-document
    git status --short
    ```

Replace the example path with the real project directory. If `git status`
lists unfinished changes, commit them through the project's normal workflow
or note them carefully before continuing. Adoption does not commit them.

Build the unmodified site:

=== "Zensical project"

    ``` bash
    zensical build --clean
    ```

=== "MkDocs project"

    ``` bash
    mkdocs build --clean
    ```

Fix an unsuccessful baseline build before adoption.

////

//// step | Activate the project's environment

Use the Python environment the project already uses. For the common `.venv`
name:

=== ":material-apple: macOS"

    ``` bash
    source .venv/bin/activate
    ```

=== ":fontawesome-brands-windows: Windows"

    In PowerShell:

    ``` powershell
    .\.venv\Scripts\Activate.ps1
    ```

=== ":material-linux: Linux (Ubuntu)"

    ``` bash
    source .venv/bin/activate
    ```

The prompt normally begins with `(.venv)` after activation. If the project
uses a different environment name or an environment manager, activate that
environment instead. Do not create a second environment merely for adoption.

////

//// step | Install or update prodockit

Install the command into the active project environment.

=== ":material-apple: macOS"

    ``` bash
    pip3 install --upgrade prodockit
    ```

=== ":fontawesome-brands-windows: Windows"

    In PowerShell:

    ``` powershell
    python -m pip install --upgrade prodockit
    ```

=== ":material-linux: Linux (Ubuntu)"

    ``` bash
    python -m pip install --upgrade prodockit
    ```

Confirm that the command comes from the environment you activated:

``` bash
prodockit --version
```

The upgrade option installs the latest available prodockit release, including
the current `adopt` command and extension updates.

////

//// step | Assess the project without changing it

Run:

``` bash
prodockit adopt
```

This first report is read-only. Near the top, check:

- the **Project** path is the repository you intended to change;
- **Mermaid** and **maths** show the expected current choices; and
- **Excluded** lists Git, SSH, remotes, editors, commits, and pushes.

The phases then show what is already correct and which selected stages need
work. No files or packages are changed.

////

//// step | Choose optional renderers

Run:

``` bash
prodockit adopt --configure
```

The command asks two separate questions:

``` text
Does this document contain Mermaid diagrams? [y/N]:
Does this document contain mathematical notation? [y/N]:
```

Answer **Yes** to Mermaid only when the Markdown contains `mermaid` fenced
blocks. Answer **Yes** to mathematics only when the document contains TeX
notation that MathJax must render. Selecting one does not select the other.

The answers are saved in `.prodockit-components.toml`. Commit this small file
with the project so colleagues and automated builds use the same choices.

You can change the choices later by running `--configure` again. Command-line
options can also make an explicit selection for one run:

``` bash
prodockit adopt --mermaid --no-maths --dry-run
prodockit adopt --no-mermaid --maths --dry-run
```

////

//// step | Preview every proposed change

Run:

``` bash
prodockit adopt --dry-run
```

The preview identifies each file and optional toolchain that needs attention,
but makes no changes. Add `--verbose` when you need the detailed files and
commands behind the concise stage descriptions:

``` bash
prodockit adopt --dry-run --verbose
```

Check that the project path, configuration file, requirements file, and
optional-renderer choices are the ones you expect.

////

//// step | Apply the reviewed stages

Run:

``` bash
prodockit adopt --apply
```

The command asks before each stage that writes files or installs an optional
renderer. Press ++enter++ to accept the default **Yes**, or enter `n` to skip
that stage.

If Mermaid or mathematics is selected, its Node packages are installed below
`tools/`. They belong to this project and are not installed globally for
unrelated documents. Routine installer output is hidden while work continues;
full output and recovery advice are shown if a command fails.

The command stops after changing local project files. It does not commit,
push, alter a remote, or publish the site.

If prodockit keeps an existing file or says that a configuration form cannot
be updated safely, do not force an overwrite. Follow
[Manually integrate files prodockit preserves](#adoptioninstall-manual-integration)
before building the result.

////

//// step | Build and review the result

Build the adopted site from its real content and configuration:

=== "Zensical project"

    ``` bash
    zensical build --clean
    ```

=== "MkDocs project"

    ``` bash
    mkdocs build --clean
    ```

Open the local result and check representative pages. The project's own
stylesheet remains later in the configuration than `pdk.css`, so its
intentional appearance should take precedence.

Review exactly what adoption changed:

``` bash
git diff
git status --short
```

Commit and publish the reviewed files through the repository's normal pull or
merge request workflow. Adoption deliberately leaves that decision to you.

////

//// step | Confirm the completed adoption

Run the assessment once more:

``` bash
prodockit adopt
```

The selected stages should now report `ok`, followed by:

``` text
All selected prodockit components are configured.
```

Continue to [Start editing](startediting.md) for the everyday preview, build,
commit, and publishing workflow, or go directly to
[Prodockit authoring features](customisecontent.md) to start using prodockit's
document features.

////

///

## Manually integrate files prodockit preserves {: #adoptioninstall-manual-integration }

Manually integrate preserved files when adoption reports that a
shared file contains project changes that it must not overwrite.

Adoption changes a file automatically only when it can preserve the project's
existing settings. A file already maintained by the project's developer may
therefore be kept, or an unusual configuration layout may be reported for
manual attention. This is a safety result, not a failed installation.

Start with `git status --short` and `git diff`. If another developer is
currently changing the same file, let that work finish and obtain its latest
version before merging prodockit's requirements. Do not use `--force` merely
to make the message disappear.

### Check what each shared file needs

| File | Result required after manual integration |
| --- | --- |
| The existing requirements file | Retain its current packages and include a `prodockit` dependency. |
| `zensical.toml`, `zensical.yml`, `zensical.yaml`, `mkdocs.yml`, or `mkdocs.yaml` | Retain the project's settings; enable the standard prodockit extensions and load `stylesheets/pdk.css` before the project's own stylesheets. |
| `tools/mermaid/package.json` | Retain project-specific scripts and dependencies; include `@mermaid-js/mermaid-cli` when Mermaid was selected. |
| `tools/mathjax/package.json` | Retain project-specific scripts and dependencies; include `mathjax-full` when mathematics was selected. |
| `tools/mathjax/tex2svg.js` | Preserve intentional local changes while ensuring the script still reads TeX from standard input and writes an SVG to standard output. |

The standard extensions are:

``` text
prodockit.headings
prodockit.refs
prodockit.citations
prodockit.glossary
prodockit.bibliography
prodockit.tables
prodockit.steps
prodockit.tree
prodockit.index
```

When mathematics is selected, retain or add `pymdownx.arithmatex` with
`generic` enabled and load `javascripts/mathjax.js` followed by
`javascripts/vendor/mathjax/tex-svg-full.js`. When Mermaid is selected, retain
the existing `pymdownx.superfences` settings and add a `mermaid` custom fence
rather than replacing the project's other custom fences.

### Create reference copies of optional renderer files

Generate current prodockit copies in a sibling comparison directory. This
does not touch the existing files under the project's `tools/` directory.

=== ":material-apple: macOS"

    ``` bash
    prodockit init-tools --dir ../prodockit-tools-reference
    ```

=== ":fontawesome-brands-windows: Windows"

    In PowerShell:

    ``` powershell
    prodockit init-tools --dir ..\prodockit-tools-reference
    ```

=== ":material-linux: Linux (Ubuntu)"

    ``` bash
    prodockit init-tools --dir ../prodockit-tools-reference
    ```

Add `--no-mathjax` when only Mermaid was selected, or `--no-mermaid` when only
mathematics was selected. Open each existing file beside its reference copy
and merge only the missing dependency, setting, or script change. Keep the
project's name, scripts, additional dependencies, comments, and other
intentional customisations.

Do not run `prodockit init-tools --force` against the real project unless the
developer has reviewed the difference and explicitly chosen to replace the
whole file. The sibling reference directory is temporary and should not be
committed with the project.

### Install and reassess the merged files

Install the dependencies from the real project directories that were merged:

``` bash
npm install --prefix tools/mermaid
npm install --prefix tools/mathjax
```

Run only the command for each selected renderer. Then reassess and build:

``` bash
prodockit adopt
zensical build --clean
git diff
git status --short
```

For an MkDocs project, replace the Zensical build command with
`mkdocs build --clean`. The adoption report should now show the selected
components as configured. Review the combined changes through the project's
normal development process before committing them.

## Resume safely if work stops

Resume an interrupted adoption by running the command again; it
reassesses completed stages before proposing further changes.

The stages are idempotent: a completed stage is checked and left alone. If a
network failure, closed terminal, or package-service error interrupts the
installation, return to the project, activate its environment, and apply
again:

=== ":material-apple: macOS"

    ``` bash
    cd /path/to/your-document
    source .venv/bin/activate
    prodockit adopt --apply
    ```

=== ":fontawesome-brands-windows: Windows"

    In PowerShell:

    ``` powershell
    cd C:\path\to\your-document
    .\.venv\Scripts\Activate.ps1
    prodockit adopt --apply
    ```

=== ":material-linux: Linux (Ubuntu)"

    ``` bash
    cd /path/to/your-document
    source .venv/bin/activate
    prodockit adopt --apply
    ```

The command reassesses the live files and continues only with stages that
still need work. It does not overwrite an existing project stylesheet or
remove existing Zensical or MkDocs settings.

## Help with common problems {: #adoption-help-with-common-problems }

### `prodockit adopt` is not recognised

Confirm that the project environment is active, then repeat the installation
command for your operating system. A newly opened terminal must reactivate the
environment before it can find project-local commands.

### More than one configuration is found

Adoption needs one active Zensical or MkDocs configuration. Remove an obsolete
duplicate only after checking which file the existing build actually uses. Do
not delete a configuration merely to make the warning disappear.

### The build changes unexpectedly

Review `git diff` first. The shared stylesheet is deliberately loaded before
the project's own styles, but an existing rule may depend on a different
extension order. Keep the project-specific rule, adjust the configuration
after review, and rebuild. Adoption does not force its styling over a later
project stylesheet.

### An optional renderer fails to install

A temporary npm or network error can be retried safely with
`prodockit adopt --apply`. If the document does not contain that kind of
content, run `prodockit adopt --configure`, turn the unused renderer off, and
apply again.

## Where to go next {: #adoptioninstall-where-to-go-next }

Your existing document now has prodockit's standard authoring components while
retaining its own template, editor, Git setup, and publishing workflow.
Add any useful, non-essential editor or conversion tools from
[Additional tooling](additionaltooling.md), or continue directly to
[Start editing](startediting.md) for the everyday preview, build, commit, and
publishing workflow. Use
[Prodockit authoring features](customisecontent.md) when you are ready to add
numbering, cross-references, citations, indexes, enhanced tables, steps, or
directory trees to the document.
