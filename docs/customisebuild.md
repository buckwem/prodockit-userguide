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

[Diagrams](zensicalbasics.md#diagrams) and [Maths](zensicalbasics.md#maths) work on the website with no setup: Mermaid.js and MathJax run in the reader's browser. The PDF cannot do that, so `prodockit pdf` pre-renders both to images using two Node.js tools.

Set them up once:

```bash
prodockit init-tools
npm ci --prefix tools/mermaid
npm ci --prefix tools/mathjax
```

`prodockit init-tools` writes the `tools/mermaid` and `tools/mathjax` directories, then prints the install commands and the settings a CI pipeline needs. Commit the manifests and lockfiles it creates; the `node_modules/` directories are ignored.

<!-- Deliberately describes the broken output rather than reproducing it.
     test/test_pdf_rendering.py scans the built PDF for exactly that text,
     and cannot tell a documentation example from a real failure - a code
     block is indistinguishable from body text once extracted from a PDF.
     A realistic sample here fails the build. -->

!!! danger "This is the quiet one"
    If those tools are missing, `prodockit pdf` does **not** fail. It leaves the content exactly as it found it - so instead of a flowchart, your PDF shows the diagram's own definition text, the `graph LR` line and every node and connector written out beneath it. Instead of a typeset equation, it shows the raw LaTeX, backslashes and braces and all. The website, meanwhile, renders both perfectly.

    That is the right default for a document using neither feature - nobody should have to install Node.js to build a PDF with no diagrams in it. It is a trap for a document that *does* use them. Since prodockit 0.12.0 the build prints a warning naming the missing tool, and this project's [test suite](testing.md) fails if either reaches the PDF unrendered.

A project using neither diagrams nor maths can skip this section entirely.

## Fonts {: #customisebuild-fonts }

Your website loads its fonts from a CDN when a reader opens the page. The PDF cannot: WeasyPrint has to embed the actual font files, so they must be installed on whatever machine builds the PDF.

If they are missing, **WeasyPrint substitutes a default font without warning**. The PDF builds, publishes, and simply looks wrong. On a Debian or Ubuntu machine:

```bash
sudo apt-get install -y fonts-inter fonts-jetbrains-mono
```

Match the packages to the fonts set in `zensical.toml` - see [Fonts](customise.md#fonts).

## Publishing {: #customisebuild-publishing }

This project publishes from two pipelines, kept deliberately in step:

* :material-github: `.github/workflows/docs.yml` — GitHub Actions, publishing to GitHub Pages.
* :material-gitlab: `.gitlab-ci.yml` — GitLab CI/CD, publishing to GitLab Pages, for a mirrored copy.

Both install the same tooling and run the same commands, in the same order:

```
install dependencies → prodockit pdf → zensical build → run tests → publish
```

The tests run *after* both builds because they check the built output - a diagram that reached the PDF as raw source fails the pipeline rather than being published.

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

**Rebuild when a release is published.** A release is normally tagged *after* the commit is pushed - and that push is what triggers the deploy. So the first deploy after a release still shows the *previous* version. Both pipelines therefore also trigger on a release, via `release: [published]` on GitHub and an `if: $CI_COMMIT_TAG` rule on GitLab.

**One deploy at a time.** Publishing a release shortly after merging its version bump starts two deploys at once, and they race. The one that finishes last does not necessarily win - so the site can end up serving the older build, with nothing reporting a problem. GitHub uses a `concurrency` group; GitLab uses `resource_group`.

**The Puppeteer variable.** `mermaid-cli` drives Chrome through Puppeteer to draw diagrams. Set `PUPPETEER_SKIP_DOWNLOAD`, **not** the older `PUPPETEER_SKIP_CHROMIUM_DOWNLOAD` - Puppeteer renamed it, and the current version ignores the old name, downloading a full Chrome build on every run before discarding it.

!!! tip "Copy a working pipeline rather than assembling one"
    prodockit's own [Continuous integration](https://buckwem.github.io/prodockit-extensions/continuous-integration/){target="_blank"} page has complete, working recipes for both GitHub Actions and GitLab CI, with the reasoning behind each step. This project's two pipeline files are the same recipe in use.

## Mirroring to a second host {: #customisebuild-mirroring }

Both pipelines above assume your code already exists on both hosts. Getting it there in the first place - and keeping it there as you keep writing - is a separate, one-off step: a plain \index{Git!remote} operation, nothing platform-specific. A \index{Git!remote} is just a name pointing at a URL; a repository can have as many as it likes, on as many different hosts as it likes, regardless of which one you originally cloned from.

Add the second host as a new remote (once):

```bash
git remote add mirror <url-of-the-second-host's-copy-of-this-repo>
```

Then, whenever you want to bring the mirror up to date with whatever you've pushed to your primary host:

```bash
git pull origin main    # bring your local main up to date with your primary host
git push mirror main    # push it up to the mirror
git push mirror --tags  # and any new release tags, so its own release number stays current
```

That push is what triggers the mirror's own CI/CD pipeline - see [Publishing](#customisebuild-publishing) above. There's nothing to automate here unless you want to: pushing a fresh copy up before or after a release is a manual step, the same size as any other Git command.

!!! tip "Both hosts need their own SSH key"
    Use the SSH URL for the mirror remote, not HTTPS, matching [Generate and configure ssh keys for Git](installtooling.md#generate-and-configure-ssh-keys-for-git) in Install tooling - the same guide already covers setting up a separate key per host and picking the right one automatically via `~/.ssh/config`.

### GitHub to GitHub

Mirroring between two GitHub-hosted copies - your own account and an organisation's, say, or two separate GitHub instances - looks like:

```bash
git remote add mirror git@github.com:your-org/your-repo.git
git pull origin main
git push mirror main
git push mirror --tags
```

### GitHub to GitLab

Mirroring to a GitLab instance - an institution's own self-hosted instance, or GitLab.com - is exactly the same pattern, just a different host in the URL:

```bash
git remote add mirror git@gitlab.example.org:your-namespace/your-repo.git
git pull origin main
git push mirror main
git push mirror --tags
```

Confirm both remotes are set up correctly at any point with `git remote -v`.

## Checks worth having {: #customisebuild-checks }

Two commands turn the quiet failures above into loud ones:

```bash
prodockit sync-repo --check   # config drifted from your git remote?
python -m pytest test/        # diagrams, maths and links in the built output
```

`prodockit sync-repo --check` writes nothing and exits non-zero if your repository links, header icon or README badges no longer match the remote you are actually publishing from - useful after forking or moving a project. See [Testing](testing.md) for the second.

## Where to go next {: #customisebuild-where-to-go-next }

Continue to [Additional tooling](additionaltooling.md) for optional extras - VS Code extensions, commit signing, and Vale - or see [Testing](testing.md) for the checks that guard the failures described above.
