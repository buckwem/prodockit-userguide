---
icon: lucide/book-open
---

<!--
# Copyright (c) 2025-2026 Mark Buckwell and contributors
# SPDX-License-Identifier: MIT
-->

{{ heading_counter_reset(page) }}

# Customise build

[Customisation](customise.md) covers changing your *document*. This page covers changing how it gets **built and published** - the two build commands, the optional tooling some features need, and the settings that make publishing behave correctly.

!!! info "Why this page exists"
    Almost everything that goes wrong in a build goes wrong *quietly*. A missing font is substituted rather than reported. A missing diagram renderer leaves the raw diagram source in your PDF. A shallow clone makes your release number disappear. In each case the build succeeds and publishes something subtly wrong, so there is no error message to search for - you have to know the failure exists.

## The two build commands {: #customisebuild-two-commands }

Your project produces two outputs from the same source, and each has its own command:

```bash
prodockit pdf      # builds the PDF
zensical build     # builds the website
```

Both read the same `zensical.toml`, so your \index{Configuration!zensical.toml} nav, fonts, page size and settings apply to both. The website is rendered by Zensical directly; the PDF goes through [Pandoc](https://pandoc.org/){target="_blank"} and [WeasyPrint](https://weasyprint.org/){target="_blank"} instead.

That second path is the source of most of what follows. **WeasyPrint has no JavaScript engine**, so anything your website renders in the browser - diagrams, mathematical notation - has to be turned into a static image *before* the PDF is built.

!!! warning "Build the outputs before running the tests"
    The [Testing](testing.md) suite checks the *built* website and PDF, not the build process. Run both commands first, or the tests will fail on artifacts that simply aren't there yet.

## Diagrams and maths {: #customisebuild-diagrams-and-maths }

[Diagrams](zensicalbasics.md#diagrams) work on the website with no setup: Mermaid.js is part of Zensical's own bundle, and runs in the reader's browser. [Maths](zensicalbasics.md#maths) does not - MathJax is installed, not committed (it's third-party code, and a repository is redistribution), so a formula renders as raw TeX on the website too until it's been installed once. Neither works in the PDF at all: WeasyPrint has no JavaScript engine, so `prodockit pdf` pre-renders both to images using two Node.js tools.

Set them up once. Which commands you need depends on where your project came from:

**From the template**, the `tools/mermaid` and `tools/mathjax` manifests and lockfiles are already tracked, so you only install them:

```bash
npm ci --prefix tools/mermaid
npm ci --prefix tools/mathjax
```

This is the case for most readers, and [Install the diagram and maths tooling](installtooling.md#install-the-diagram-and-maths-tooling) walks through it alongside installing Node.js itself - including the extra step Maths needs afterwards, to install the MathJax bundle and config the *website* uses (not just the PDF pre-render above).

**Starting a project from scratch**, you have no `tools/` directory yet, so create it first:

```bash
prodockit init-tools
npm ci --prefix tools/mermaid
npm ci --prefix tools/mathjax
```

`prodockit init-tools` writes the `tools/mermaid` and `tools/mathjax` directories, then prints the install commands and the settings a CI pipeline needs. Commit the manifests and lockfiles it creates; the `node_modules/` directories are ignored. Still install the MathJax bundle itself afterwards, the same way.

!!! tip
    Running `init-tools` on a copy of the template does no harm - it reports `Kept existing tools/mermaid/package.json` for each file already there and changes nothing - but it has nothing to do, so it is easy to mistake that message for an error.

!!! warning "CI needs this too, and starts from nothing every run"
    Neither the MathJax bundle nor its config is committed, so a CI pipeline that builds the website - not just the PDF - needs the same install step this project's own `.github/workflows/docs.yml` and `.gitlab-ci.yml` run, right after `npm ci --prefix tools/mathjax`. Skip it and the pipeline succeeds while publishing a site where every formula is raw TeX - the same silent failure the box below describes, just reaching the website instead of stopping at the PDF.

<!-- Deliberately describes the broken output rather than reproducing it.
     test/test_pdf_rendering.py scans the built PDF for exactly that text,
     and cannot tell a documentation example from a real failure - a code
     block is indistinguishable from body text once extracted from a PDF.
     A realistic sample here fails the build. -->

!!! danger "This is the quiet one"
    If these tools are missing, `prodockit pdf` does **not** fail. It leaves the content exactly as it found it - so instead of a flowchart, your PDF shows the diagram's own definition text, the `graph LR` line and every node and connector written out beneath it. Instead of a typeset equation, it shows the raw LaTeX, backslashes and braces and all. The website renders diagrams perfectly regardless - Mermaid.js needs nothing from `tools/`, only Zensical itself - but a formula is only as reliable there as the MathJax install above; skip it and the website shows exactly the same raw TeX the PDF would.

    That is the right default for a document using neither feature - nobody should have to install Node.js to build a PDF with no diagrams in it. It is a trap for a document that *does* use them. Since prodockit 0.12.0 the build prints a warning naming the missing tool, and this project's [test suite](testing.md) fails if either reaches the PDF unrendered.

A project using neither diagrams nor maths can skip this section entirely.

## Fonts {: #customisebuild-fonts }

Your website loads its fonts from a CDN when a reader opens the page. The PDF cannot: WeasyPrint has to embed the actual font files, so they must be installed on whatever machine builds the PDF.

If they are missing, **WeasyPrint substitutes a default font without warning**. The PDF builds, publishes, and simply looks wrong.

The fonts to install are whichever ones `zensical.toml` names - see [Fonts](customise.md#fonts) for that setting. Left unset, they are \index{Fonts!Inter} **Inter** for body text and \index{Fonts!JetBrains Mono} **JetBrains Mono** for code, which is what the examples below use.

### What format to install {: #customisebuild-fonts-format }

Install the **desktop** font files - `.ttf` (TrueType) or `.otf` (OpenType). Both work equally well.

!!! warning "`.woff`/`.woff2` will not do"
    Those are web delivery formats. A browser reads them over HTTP, but they are not what your operating system's font system indexes, so WeasyPrint will not find them and will substitute silently - the exact failure this section exists to avoid. If a font is offered as a "web font" download, look for the desktop or "static" download instead.

### Where to install them {: #customisebuild-fonts-install }

<div class="grid cards one-column" markdown>

-   :material-clock-fast:{ .lg .middle } __Install the document fonts__

    === ":material-apple: macOS"

        ``` bash
        brew install --cask font-inter font-jetbrains-mono
        ```

        Homebrew puts them in `~/Library/Fonts`, which is the per-user font folder - no further step needed. To install a font you downloaded yourself instead, double-click the file and click **Install Font**, or copy the `.otf`/`.ttf` files into `~/Library/Fonts` directly.

    === ":fontawesome-brands-windows: Windows"

        Download the desktop font files, then select them all, right-click, and choose **Install for all users**.

        Installing for all users matters if a scheduled task or service builds your PDF, since those do not run as you - a font installed only for your own account is invisible to them.

    === ":material-linux: Linux (Ubuntu)"

        Where a distribution packages the font, use that - it handles the font cache for you:

        ``` bash
        sudo apt-get install -y fonts-inter fonts-jetbrains-mono
        ```

        For a font with no package, copy the files in by hand and rebuild the cache:

        ``` bash
        mkdir -p ~/.local/share/fonts
        cp *.ttf *.otf ~/.local/share/fonts/
        fc-cache -f
        ```

        Use `/usr/share/fonts` instead of `~/.local/share/fonts` to install for every user on the machine.

</div>

Your CI runner needs them too, and starts from a bare image every run - see the `fonts-inter fonts-jetbrains-mono` line in [Publishing](#customisebuild-publishing) below.

### Check they were actually used {: #customisebuild-fonts-check }

Since a missing font produces a PDF rather than an error, the only reliable check is to look at what the finished document actually embedded:

```bash
python -c "
import pymupdf
d = pymupdf.open('docs/site_documentation.pdf')
print(sorted({f[3].split('+')[-1] for p in d for f in p.get_fonts()}))
"
```

`pymupdf` is already installed - it comes with the `[index]` extra in `requirements.txt`. Run against this guide's own PDF, it prints:

```text
['Inter', 'Inter-Bold', 'Inter-Italic', 'Inter-Ultra-Bold',
 'JetBrains-Mono', 'JetBrains-Mono-Bold', 'Trebuchet-MS']
```

The configured fonts, in whichever weights the document happens to use. A name you did not configure appearing there is the substitution happening - a PDF built without Inter installed shows a default serif or sans face in its place instead.

!!! tip "The `ABCDEF+` prefix"
    Embedded fonts normally carry a random six-letter tag, as in `LNXIQZ+Inter`, marking the file as a *subset* containing only the glyphs this document actually uses. The `.split('+')[-1]` above strips it so the names read cleanly; it says nothing about whether the font is correct.

!!! note "Mermaid diagrams bring their own font"
    You will also see `Trebuchet-MS` if your document contains a \index{Zensical!diagrams} Mermaid diagram. That is not a substitution: Mermaid renders its diagrams to SVG with its own stylesheet, which asks for Trebuchet MS, and that travels into the PDF with the image. It applies only to text *inside* diagrams, and needs no action - your body text and code are unaffected.

## Pinning build inputs {: #customisebuild-pinning }

Your document has more inputs than its own content. Zensical renders the site, Pandoc and WeasyPrint lay out the PDF, and whatever runs the pipeline carries its own OS image. Left unpinned, an upgrade to any of them doesn't fail the build - it just quietly publishes a slightly different document, with nothing to indicate anything changed.

`prodockit pins` keeps these declarations - a version in `requirements.txt`, a `PANDOC_VERSION` in a workflow file, a runner label - in step with each other, wherever they're written down:

```bash
prodockit pins          # prompt per package; Enter takes the newest release
prodockit pins --check  # behind, or files disagreeing with each other? exit non-zero
```

With no `-p` flags, both commands cover five packages by default: `zensical`, `weasyprint`, `markdown`, `pymdown-extensions`, and **pandoc** - Pandoc is the fourth build input alongside Zensical and WeasyPrint, and the one that has actually caught this project family out. Pandoc 3.10 stopped treating a syntax-highlighted `<pre><code>` as a code block; on that version every fenced code block in the PDF lost its preformatting and reflowed as justified prose, while the build reported success. The published PDFs stayed correct only because CI happened to be installing an older pandoc than anyone's laptop - exactly the silent drift this section exists to catch. [Pandoc version drift](https://prodockit.org/devcons/continuous-integration/#ci-pandoc-version){target="_blank"} covers the how, and prodockit's [limitations](https://prodockit.org/devcons/limitations/){target="_blank"} page records the episode in full.

This project pins `zensical`/`weasyprint` in `requirements.txt`, and pandoc as `PANDOC_VERSION` in both `.github/workflows/docs.yml` and `.gitlab-ci.yml`:

```bash
$ prodockit pins --check
zensical
  requirements.txt:12  zensical==0.0.53
  newest on PyPI: 0.0.53
...
pandoc
  .gitlab-ci.yml:52  PANDOC_VERSION: "3.10.1
  .gitlab-ci.yml:139  PANDOC_VERSION: "3.10.1
  .github/workflows/docs.yml:50  PANDOC_VERSION: "3.10.1
  not on PyPI - set the version yourself
Every managed package is current and consistent.
```

"Not on PyPI" is the one way pandoc's entry differs from the rest: it isn't a Python package, so there's no release index to check against or take "newest" from - `prodockit pins` (no `--check`) still prompts for it like any other package, but you type the version rather than pressing Enter for the newest. `--set` works exactly the same as anywhere else:

```bash
prodockit pins --set pandoc=3.10.1
```

This project also pins the runner/image used to build it - `ubuntu-24.04` in `.github/workflows/docs.yml`, `python:3.13` in `.gitlab-ci.yml` - since a runner label or image tag has no package index either, only `--set` to a version you choose yourself, e.g. `prodockit pins -p ubuntu --set ubuntu=24.04`.

`prodockit` itself uses a minimum version rather than an exact pin: this userguide requires 0.42.1 or newer as the coordinated patch floor for the forward caption references, table grid and theme-aware cell shading demonstrated here. It isn't one of `prodockit pins`' five default packages, so managing or checking that floor needs naming explicitly:

```bash
prodockit pins --check -p zensical -p weasyprint -p prodockit
```

!!! tip
    `prodockit pins --check` only reports what's already pinned. It does not run on every push, because a pin going out of date on PyPI is expected over time rather than a failure in an unrelated document change.

!!! warning "Needs prodockit 0.17.5 or newer to see this line at all"
    `prodockit[index]>=0.42.1` has an extras bracket between the name and the version - a shape `prodockit pins` couldn't parse before 0.17.5, silently reporting "not declared anywhere" rather than failing to parse (prodockit-extensions#156). Run the check with an older `prodockit` installed and it passes for the wrong reason: it never saw the declaration to disagree with.

### Checking an upgrade manually {: #customisebuild-drift }

A normal `prodockit template-sync` preview checks whether the activated project
environment is using the latest prodockit release. For a broader check of the
versions declared throughout the project, run:

```bash
prodockit template-sync
prodockit pins --check -p zensical -p weasyprint -p prodockit
```

Neither command changes the project. Dependency drift is not checked by an
automated workflow in this repository; most routine prodockit checking is
handled by the command supplied from the extensions package.

When you need to know whether a broader upgrade changes the published output,
make the comparison manually: build the current versions, retain those
outputs, take the upgrade, then build again and compare the PDF and website.

```
build (pinned) → build (newest) → diff the PDF and website → report
```

Build the PDF before the website: `zensical build` copies the PDF into the
published site, so reversing the order would compare the newly built website
with an older PDF and create a false difference.

### Taking an upgrade {: #customisebuild-taking-an-upgrade }

When the checks show an upgrade you want to assess:

```bash
prodockit pins -p zensical -p weasyprint -p prodockit  # accept the suggested version, or type one
prodockit pdf                                          # rebuild - PDF first ...
zensical build --clean --strict                        # ... then the site
```

Then compare the built output with the copy made before the upgrade and review
the differences before committing. Repeat for the runner image if that is what
moved (`prodockit pins -p ubuntu`, or `-p python` on GitLab), since it is not
upgraded by the same command.

See prodockit-extensions' own [Taking an upgrade](https://prodockit.org/devcons/continuous-integration/#pinning-taking-an-upgrade){target="_blank"} and [Version pinning and drift](https://prodockit.org/devcons/continuous-integration/#pinning-version-pinning-and-drift){target="_blank"} sections for the full reasoning behind each step - this project's two files are that same recipe, adapted from a `pyproject.toml`-based Python package to a `requirements.txt`-based Zensical site.

## Updating from prodockit-template {: #customisebuild-template-sync }

A project made from `prodockit-template` is a copy, so later template fixes do
not arrive through `git pull`. Review them with:

```bash
prodockit template-sync          # report only; writes no project file
prodockit template-sync --apply  # create a branch, apply and stage the update
```

The template's manifest separates template-owned build files from project-owned
content. Your Markdown, assets, bibliography, licence and prose settings are not
replaced. Shared configuration is merged at key level rather than copied as one
file.

In prodockit 0.42.0 and later, that merge also preserves every existing
`project.extra.pdf_*` value: page size, margins, duplex mode, header/footer
styling and output choices remain yours. A template update can add a genuinely
new PDF parameter, but it cannot reset one your project already has.

Review the staged diff before committing it, exactly as you would any other
dependency update.

## Publishing {: #customisebuild-publishing }

This project publishes from two pipelines, kept deliberately in step:

* :material-github: `.github/workflows/docs.yml` — GitHub Actions, publishing to GitHub Pages.
* :material-gitlab: `.gitlab-ci.yml` — GitLab CI/CD, publishing to GitLab Pages, for a mirrored copy.

Both install the same tooling and run the same commands, in the same order:

```
install dependencies → prodockit pdf → zensical build --clean --strict → run tests → publish
```

The tests run *after* both builds because they check the built output - a diagram that reached the PDF as raw source fails the pipeline rather than being published.

The GitHub pipeline has one further step the GitLab one does not: after publishing, it polls the live site and fails the run if the page it fetches doesn't match what was just deployed. A successful deploy is not proof the site is actually serving it - GitHub Pages has, more than once, reported success and quietly kept serving the previous build.

### Four settings that are easy to get wrong {: #customisebuild-four-settings }

Each of these is invisible when wrong: nothing fails, the site just publishes something incorrect.

**Full git history.** The cover page's release number comes from `git describe --tags`. Both GitHub Actions and GitLab CI clone *shallowly* by default, which fetches **no tags at all**, so the release line silently disappears - while working perfectly on your own machine, where you have the full history.

```yaml
# GitHub Actions
- uses: actions/checkout@v5
  with:
    fetch-depth: 0

# GitLab CI
variables:
  GIT_DEPTH: "0"
```

**Rebuild when a release is published - but not from the tag.** A release is normally tagged *after* the commit is pushed, and that push is what triggers the deploy, so the first deploy after a release still shows the *previous* version. Something has to rebuild once the tag exists.

The obvious answer - trigger the deploy on the tag as well - is the wrong one, and fails quietly on both hosts. On GitHub, a Pages deployment carrying a tag ref is accepted, reported successful, and then never served (issue #43). On GitLab it *is* served, but it publishes whatever the tag points at, which is older than `main` whenever a release has been overtaken by newer commits (issue #58).

So neither pipeline builds tags. GitHub rebuilds against `main` from a separate `redeploy-after-release.yml` workflow; the GitLab mirror gets the same result from pushing tags before the branch, as in [Mirroring to a second host](#customisebuild-mirroring) below.

**One deploy at a time.** Publishing a release shortly after merging its version bump starts two deploys at once, and they race. The one that finishes last does not necessarily win - so the site can end up serving the older build, with nothing reporting a problem. GitHub uses a `concurrency` group; GitLab uses `resource_group`.

**The Puppeteer variable.** `mermaid-cli` drives Chrome through Puppeteer to draw diagrams. Set `PUPPETEER_SKIP_DOWNLOAD`, **not** the older `PUPPETEER_SKIP_CHROMIUM_DOWNLOAD` - Puppeteer renamed it, and the current version ignores the old name, downloading a full Chrome build on every run before discarding it.

!!! tip "Copy a working pipeline rather than assembling one"
    prodockit's own [Continuous integration](https://prodockit.org/devcons/continuous-integration/){target="_blank"} page has complete, working recipes for both GitHub Actions and GitLab CI, with the reasoning behind each step. This project's two pipeline files are the same recipe in use.

## Mirroring to a second host {: #customisebuild-mirroring }

Both pipelines above assume your code already exists on both hosts. Getting it there in the first place - and keeping it there as you keep writing - is a separate, one-off step: a plain \index{Git!remote} operation, nothing platform-specific. A \index{Git!remote} is just a name pointing at a URL; a repository can have as many as it likes, on as many different hosts as it likes, regardless of which one you originally cloned from.

Add the second host as a new remote (once):

```bash
git remote add mirror <url-of-the-second-host's-copy-of-this-repo>
```

Then, whenever you want to bring the mirror up to date with whatever you've pushed to your primary host:

```bash
git pull origin main    # bring your local main up to date with your primary host
git push mirror --tags  # release tags first, so the build below can see them
git push mirror main    # then the branch - this is the push that publishes
```

That last push is what triggers the mirror's own CI/CD pipeline - see [Publishing](#customisebuild-publishing) above. There's nothing to automate here unless you want to: pushing a fresh copy up before or after a release is a manual step, the same size as any other Git command.

!!! warning "Push the tags first, not last"
    The order matters, and getting it wrong is invisible. The cover page's release number comes from `git describe --tags`, which can only find a tag that is already on the mirror when the build runs. Push the branch first and its build sees the *previous* tag, so the mirror publishes with a release number one behind - correctly built, quietly wrong.

    Tags first, and the branch build resolves the new release by itself.

!!! tip "Fetch tags before you push them"
    A release created through the host's web interface or `gh release create` makes the tag *on the server*, not in your local clone - so `git push mirror --tags` has nothing new to send and silently pushes nothing. Refresh first:

    ```bash
    git fetch origin --tags
    git describe --tags --abbrev=0   # should show the release you just made
    ```

!!! tip "Both hosts need their own SSH key"
    Use the SSH URL for the mirror remote, not HTTPS, matching [Generate and configure ssh keys for Git](installtooling.md#generate-and-configure-ssh-keys-for-git) in Install tooling - the same guide already covers setting up a separate key per host and picking the right one automatically via `~/.ssh/config`.

### GitHub to GitHub

Mirroring between two GitHub-hosted copies - your own account and an organisation's, say, or two separate GitHub instances - looks like:

```bash
git remote add mirror git@github.com:your-org/your-repo.git
git pull origin main
git fetch origin --tags
git push mirror --tags
git push mirror main
```

### GitHub to GitLab

Mirroring to a GitLab instance - an institution's own self-hosted instance, or GitLab.com - is exactly the same pattern, just a different host in the URL:

```bash
git remote add mirror git@gitlab.example.org:your-namespace/your-repo.git
git pull origin main
git fetch origin --tags
git push mirror --tags
git push mirror main
```

Confirm both remotes are set up correctly at any point with `git remote -v`.

!!! note "Why the GitLab pipeline doesn't build tags"
    `.gitlab-ci.yml`'s `pages` job runs on the default branch only. A tag build would publish whatever the tag points at, which is older than `main` whenever a release has been overtaken by newer commits - so syncing after such a release would republish the older site over the newer one, successfully and silently. With tags pushed first, the branch build already resolves the right release number, so building tags separately gains nothing. See [prodockit-userguide#58](https://github.com/buckwem/prodockit-userguide/issues/58).

## Checks worth having {: #customisebuild-checks }

Three commands turn the quiet failures above into loud ones:

```bash
prodockit sync-repo --check   # config drifted from your git remote?
prodockit pins --check        # build inputs behind PyPI, or pinned inconsistently?
python -m pytest test/        # diagrams, maths and links in the built output
```

`prodockit sync-repo --check` writes nothing and exits non-zero if your repository links, header icon or README badges no longer match the remote you are actually publishing from - useful after forking or moving a project. `prodockit pins --check` does the same for the pins in [Pinning build inputs](#customisebuild-pinning) above. See [Testing](testing.md) for the third.

## Where to go next {: #customisebuild-where-to-go-next }

Continue to [Additional tooling](additionaltooling.md) for optional extras - VS Code extensions, GitLens, and Vale - or see [Testing](testing.md) for the checks that guard the failures described above.
