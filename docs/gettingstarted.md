---
icon: lucide/signpost
---

<!--
Copyright (c) 2025-2026 Mark Buckwell and contributors
SPDX-License-Identifier: MIT
-->

{{ heading_counter_reset(page) }}

# Getting started

Use this page to choose how to add prodockit to a Zensical project. The
[prodockit reference manual](https://prodockit.org/gettingstarted/){target="_blank"}
contains the maintained installation instructions for each path, including
prerequisites, platform-specific commands, verification, and troubleshooting.
Complete one path there, then return to this User Guide for the everyday
writing and publishing workflow.

## Choose a path

The [installation choices in the prodockit reference
manual](https://prodockit.org/choosing-installation/){target="_blank"} explain
these alternatives in detail. Each path provides step-by-step instructions
for setting up a Zensical project with prodockit.

| Starting point | Path | Result |
| --- | --- | --- |
| A new or existing Zensical site that should keep its own structure and workflow | [Adopt Prodockit](https://prodockit.org/choosing-installation/){target="_blank"} | Adoption adds the selected authoring features and PDF support without replacing the site's design or repository history. The [first-site walkthrough](https://prodockit.org/getting-started/){target="_blank"} shows this from an empty directory. |
| A new site that should use the maintained `prodockit-template` | [Build a template site](https://prodockit.org/choosing-installation/){target="_blank"} | Bootstrap guides and checks the computer, repository, project environment, build tools, and publishing setup. |
| A project whose author needs direct control of every setup command | [Build site manually](https://prodockit.org/manual-install/){target="_blank"} | Follow the platform-specific steps and verify the same tools yourself. |
/// table-caption | <
Choose one Prodockit installation path
///

All paths begin with [Prepare to install](https://prodockit.org/installation/){target="_blank"}.
It establishes the supported Python and a setup environment outside the
project. Follow the chosen path in the prodockit reference manual for the
project-specific environment and checks; do not rely on copied commands from
this User Guide.

If an installation check fails, use the [installation troubleshooting in the
prodockit reference manual](https://prodockit.org/troubleshooting-installs/){target="_blank"}.

## Continue with this guide

Once the selected installation route passes its checks, continue to
[Start editing](startediting.md) for the preview, build, commit, and publish
cycle. [Additional tooling](additionaltooling.md) is optional and can be added
later for particular writing or repository tasks.
