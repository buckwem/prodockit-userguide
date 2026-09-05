---
icon: lucide/book-open
---

<!--
# Copyright (c) 2025-2026 Mark Buckwell and contributors
# SPDX-License-Identifier: MIT
-->

{{ heading_counter_reset(page) }}

# Build and publish

The website and PDF come from the same Markdown and `zensical.toml`, but they
are separate outputs. Build both, inspect both, and run the checks before
publishing a significant change.

## Prepare the terminal

Run all commands from the repository directory with its virtual environment
active.

/// steps

//// step | Change to the repository directory

Replace the example path with the folder containing your project:

``` bash
cd path/to/your-project
```

////

//// step | Activate the project environment

=== ":material-apple: macOS"

    ``` bash
    source .venv/bin/activate
    ```

=== ":fontawesome-brands-windows: Windows"

    ``` powershell
    .\.venv\Scripts\Activate.ps1
    ```

=== ":material-linux: Linux (Ubuntu)"

    ``` bash
    source .venv/bin/activate
    ```

The prompt normally gains `(.venv)` when activation succeeds.

////

///

## Build both outputs {: #customisebuild-two-commands }

The \index{Build!website and PDF} process builds the website first, then uses
that completed output to build the PDF:

``` bash
zensical build --clean --strict
prodockit pdf
```

The outputs are:

- `docs/site_documentation.pdf` — the finished PDF.
- `public/` — the complete website ready to publish.

`--clean` prevents files removed from the source remaining in the website.
`--strict` turns Zensical warnings into failures so they cannot pass unnoticed
in the publishing pipeline. `prodockit pdf` does not run Zensical. It reads the
generated pages and atomically adds the finished PDF to `public/`, so the
website's **Download PDF** link works without a second website build.

The [PDF guide](https://prodockit.org/pdf/){target="_blank"} documents every
PDF setting, output file, and known limitation. The
[Zensical build guide](https://zensical.org/docs/setup/building-your-site/){target="_blank"}
covers the website command in detail.

## Diagrams and maths {: #customisebuild-diagrams-and-maths }

\index{Build!Diagram and maths rendering} requires Node.js renderers for the PDF.
MathJax also needs a local browser bundle for the website. Bootstrap and
Adoption install these when the options are selected; a template project
already contains their manifests.

If the document uses these features and the dependencies have not yet been
installed, run:

``` bash
npm ci --prefix tools/mermaid
npm ci --prefix tools/mathjax
prodockit init-mathjax
```

A document that uses neither feature does not need Node.js for them.

!!! warning "Inspect the output, not only the exit code"
    Missing renderers can leave Mermaid definitions or TeX source visible in
    the finished document. Open the affected pages in both outputs after the
    build. The automated checks also look for common forms of unrendered
    source.

Use [Additional tooling](additionaltooling.md) for installation and the
[prodockit PDF guide](https://prodockit.org/pdf/#mermaid-diagrams-and-tex-maths){target="_blank"}
for renderer configuration and troubleshooting.

## Fonts {: #customisebuild-fonts }

The website can load configured \index{Fonts} when a reader opens it. A PDF builder
must find the actual desktop font files on the machine doing the build. If they
are absent, WeasyPrint may substitute another font without failing.

The template uses Inter for body text and JetBrains Mono for code. Install the
`.ttf` or `.otf` desktop versions, not `.woff` web-font files. Bootstrap and
Manual install cover the operating-system steps.

After changing a font:

1. Build the PDF again.
2. Inspect headings, body text, code, symbols, and page breaks.
3. Compare a representative page with the earlier PDF.
4. Confirm the publishing pipeline installs the same fonts.

The [PDF typography reference](https://prodockit.org/pdf/){target="_blank"}
contains the font-detection and embedding details.

## Keep the project up to date

The \index{Maintenance} workflow covers two different kinds of update:

- A **template update** brings shared workflows, styles, and configuration
    changes into a project originally made from `prodockit-template`.
- A **dependency update** changes versions of prodockit, Zensical, WeasyPrint,
    Pandoc, or another build input.

Review either kind of update before combining it with your writing.

### Update from prodockit-template {: #customisebuild-template-sync }

\index{Tasks!Update from prodockit-template} by previewing the update without changing the project:

``` bash
prodockit template-sync
```

If the preview is appropriate, apply it on the branch prepared by the command:

``` bash
prodockit template-sync --apply
```

Before changing a template file, the command checks the selected template's
paired Prodockit release and the complete supported toolchain. If the active
environment needs a different Prodockit version, it shows the exact install,
upgrade, or downgrade and asks for confirmation. It then continues under that
version in a fresh process, previews the work needed by Adopt, and asks
separately before applying it. Both questions default to **No**. A newer
Prodockit is not automatically preferred over the release paired with the
selected template.

If either confirmation is declined, or installation, handoff, Adopt, or
verification fails, the template files, applied-release stamp, and update
branch remain unchanged. Correct the reported problem and rerun the same
command; completed prerequisites are reassessed and skipped. For an explicitly
unattended update, opt in to both environment changes:

``` bash
prodockit template-sync --apply --accept-prodockit --accept-adopt
```

The manifest distinguishes template-owned files from your content. The merge
preserves every existing project-owned file and every existing
`project.extra.pdf_*` value. It can add a new setting, but it does not reset
your page size, margins, duplex choice, or other existing PDF configuration.

Review the staged changes and rebuild both outputs before committing. The
[template-sync guide](https://prodockit.org/devcons/template-sync/){target="_blank"}
explains preserved files, conflicts, `--force`, verbose output, and direct
updates to `main`.

### Validate the project configuration {: #customisebuild-config-check }

Check the settings Prodockit will actually use before starting a build:

``` bash
prodockit config --check
```

The command resolves `zensical.toml`, validates Prodockit-owned settings, and
checks that referenced navigation pages, images, citation styles, optional
renderers, and enabled extensions are available. It does not build the site,
change the configuration, or inspect unrelated Zensical settings. A failure
names the missing or invalid input so it can be corrected before a longer
website or PDF build.

Run it after changing configuration or adding an optional renderer. The
[command-line reference](https://prodockit.org/command-line/){target="_blank"}
shows the resolved values printed by the command and its available options.

### Review dependency versions {: #customisebuild-pinning }

Review \index{Dependencies!versions} without contacting package indexes:

``` bash
prodockit pins --check --offline
```

This checks every declaration in the root requirements files, including
`testrequirements.txt`, and the Python version used by the hosted builds. If
the project has a `.prodockit-shared-files.toml` manifest, the same command
also checks that each declared file matches the copy supplied by the installed
Prodockit release. The check changes nothing.

For example, the Prodockit documentation repositories share managed website
and PDF styles in `pdk.css` and `pdk-pdf.css`. Preview a missing or different
copy directly with:

``` bash
prodockit shared-files --check
```

Restore the installed release's copy only when you intend to review the
result:

``` bash
prodockit shared-files --apply
git diff -- docs/stylesheets/pdk.css docs/stylesheets/pdk-pdf.css
```

Commit the restored file only after reviewing the difference. The shared-file
check reads the installed package and the local project; it does not contact a
package index or another repository.

Use the interactive command only when you intend to review and take an update:

``` bash
prodockit pins
```

Changing a pin is not proof the new output is equivalent. Keep the earlier PDF
and website, rebuild with the proposed versions, compare them, and run the
tests. The
[version pinning guide](https://prodockit.org/devcons/pinning-drift/){target="_blank"}
explains managed packages and non-Python inputs such as Pandoc and runner
images.

### Use one maintenance cycle {: #customisebuild-taking-an-upgrade }

For a planned maintenance change:

/// steps

//// step | Preview shared template changes

``` bash
prodockit template-sync
```

////

//// step | Check declared versions and shared files

``` bash
prodockit pins --check --offline
```

////

//// step | Apply only the update you intend to review

Use `prodockit template-sync --apply` for a template update or `prodockit pins`
for an independent dependency update. Template sync already aligns the
versions and supported toolchain declared by the selected template, so do not
run a separate pin update unless it is intentional and will be reviewed with
the same release.

////

//// step | Rebuild and test

``` bash
zensical build --clean --strict
prodockit pdf
```

////

//// step | Review before committing

Inspect `git diff`, compare the website and PDF, then commit only when the
change is understood.

////

///

## Publishing {: #customisebuild-publishing }

The \index{Publishing} workflow is supplied for both repository hosts:

- `.github/workflows/docs.yml` builds and publishes through GitHub Actions.
- `.gitlab-ci.yml` builds and publishes through GitLab CI/CD.

Both install dependencies, build the PDF and website, run the project's
supplied checks, and publish Pages. In normal use you push the source and let
the selected host run the supplied pipeline; you do not upload `public/`
manually.

After pushing:

1. Open the repository's Actions or Pipelines page.
2. Wait for the complete pipeline, not only its build job.
3. Open the published site from the Pages settings.
4. Check the release marker, PDF download, maths, diagrams, and recent content.

The
[publishing guide](https://prodockit.org/publishing/){target="_blank"} explains
the supplied workflows. The
[continuous-integration reference](https://prodockit.org/devcons/continuous-integration/){target="_blank"}
covers full Git history, release rebuilds, deployment concurrency, runners,
and custom pipelines.

## Mirror to a second host {: #customisebuild-mirroring }

\index{Repository!mirroring} is needed only when the project genuinely needs to publish from two
hosts. Add the second repository as another remote:

``` bash
git remote add mirror <ssh-url-of-second-repository>
git remote -v
```

To update it, fetch release tags and push the tags before the branch so the
mirror's build can display the correct release:

``` bash
git pull origin main
git fetch origin --tags
git push mirror --tags
git push mirror main
```

Use SSH URLs and ensure the key for the second host is configured before
starting. Confirm the mirror's own pipeline and Pages site after every sync.

## Checks worth having {: #customisebuild-checks }

Run these \index{Build!checks} before publishing a release or after changing build configuration:

``` bash
prodockit sync-repo --check
prodockit pins --check --offline
prodockit config --check
zensical build --clean --strict
prodockit pdf
```

- `sync-repo --check` detects repository metadata that no longer matches the
    actual remote.
- `pins --check --offline` detects inconsistent declared versions.
- `config --check` reports invalid Prodockit settings and missing local files,
    navigation pages, images, citation styles, extensions, or renderers.
- The builds prove both outputs can be generated from a clean website tree.

Then inspect the website and PDF. Check navigation, references, captions,
diagrams, maths, page breaks, fonts, links, and the latest changed content.
Authors normally rely on the supplied publishing pipeline for its automated
checks. Maintainers who need to run or extend that test suite should use the
[Extensions testing guide](https://prodockit.org/devcons/testing/){target="_blank"}.

## Where to go next {: #customisebuild-where-to-go-next }

Build and inspect both outputs before publishing or submitting. Return to the
Extensions Guide for
[command-line details](https://prodockit.org/command-line/){target="_blank"},
[PDF options](https://prodockit.org/pdf/){target="_blank"}, or
[publishing configuration](https://prodockit.org/publishing/){target="_blank"}.
