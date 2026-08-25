---
icon: lucide/book-open
is_appendix: true
---

<!--
# Copyright (c) 2025-2026 Mark Buckwell and contributors
# SPDX-License-Identifier: MIT
-->

{{ heading_counter_reset(page) }}
{{ glossary_style() }}

# Glossary

The following key terms are used throughout this document.
`\gls{markdown-def}` is also used by the live example in
[Prodockit authoring features](customisecontent.md).

**Admonition** - A labelled, coloured callout box (Note, Tip, Warning, and so on) used to highlight information set apart from the main body text, without interrupting the flow of a paragraph.
{: #admonition-def .glossary data-term="Admonition" }

**Attribute list** - Markdown syntax (`{: ... }`) that attaches an id, CSS class, or other HTML attribute to the element directly above it - the mechanism the cross-reference, citation, acronym, and glossary features are all built on.
{: #attribute-list-def .glossary data-term="Attribute list" }

**Bibliography** - A list of sources generated from structured records, commonly a BibTeX or BibLaTeX file, using a selected citation style.
{: #bibliography-def .glossary data-term="Bibliography" }

**Branch** - An independent line of development within a repository, letting you make changes without affecting the default branch until they're ready to be merged.
{: #branch-def .glossary data-term="Branch" }

**Build** - The process of turning the project's source files and configuration into an output such as the website or PDF.
{: #build-def .glossary data-term="Build" }

**Caption** - A numbered description attached to a figure or table so it can be identified and cross-referenced consistently.
{: #caption-def .glossary data-term="Caption" }

**Cascading Style Sheets** - The language used to control the visual appearance (colours, spacing, fonts, layout) of a web page, kept separate from its content. See the [Acronyms](acronyms.md#css) entry for the expansion.
{: #css-def .glossary data-term="Cascading Style Sheets" }

**CI/CD** - The practice of automatically building, testing, and publishing a project every time a change is pushed, rather than as a separate manual step. See the [Acronyms](acronyms.md#ci-cd) entry for the expansion.
{: #cicd-def .glossary data-term="CI/CD" }

**Citation** - A marker in the document that acknowledges a source and connects the statement to its full entry in a reference list or bibliography.
{: #citation-def .glossary data-term="Citation" }

**Clone** - Creating a full local copy of a remote repository, including its entire history, so you can edit it on your own computer.
{: #clone-def .glossary data-term="Clone" }

**Commit** - A saved snapshot of your changes in Git, together with a message describing what changed and why.
{: #commit-def .glossary data-term="Commit" }

**Cross-reference** - A link from one part of a document to a numbered heading, figure, table, or other labelled target whose displayed number can be generated automatically.
{: #cross-reference-def .glossary data-term="Cross-reference" }

**Default branch** - The branch a repository treats as its main line of work, normally named `main`, and the branch publishing workflows usually build.
{: #default-branch-def .glossary data-term="Default branch" }

**Dependency** - A package, program, font, or system library that another part of the project needs in order to build or run correctly.
{: #dependency-def .glossary data-term="Dependency" }

**Deployment** - The act of placing a successfully built website or other output onto the service from which readers access it.
{: #deployment-def .glossary data-term="Deployment" }

**Docs-as-code** - An approach to writing documentation that uses the same tools and workflow as software development - plain text files, version control, and peer review - rather than a word processor or wiki.
{: #docs-as-code-def .glossary data-term="Docs-as-code" }

**Fenced code block** - A block of code set apart from the surrounding text by a line of three or more backticks before and after it, optionally labelled with a language name for syntax highlighting.
{: #fenced-code-block-def .glossary data-term="Fenced code block" }

**Fork** - Your own copy of someone else's repository, created on the hosting service (GitLab or GitHub) itself, which you can then clone and edit independently of the original.
{: #fork-def .glossary data-term="Fork" }

**Front matter** - A block of YAML metadata at the top of a Markdown file, delimited by `---` lines, that configures how that page is built or displayed (its icon, whether it's an appendix, and so on) without appearing in the rendered content.
{: #front-matter-def .glossary data-term="Front matter" }

**HEAD** - Git's pointer to the commit your working directory currently reflects - normally the tip of whichever branch you have checked out.
{: #head-def .glossary data-term="HEAD" }

**Markdown** - A lightweight markup language for formatting plain text, using a simple, readable syntax that converts into HTML for web publishing.
{: #markdown-def .glossary data-term="Markdown" }

**Merge conflict** - A situation where Git cannot safely combine two changes to the same content and needs a person to choose the intended result.
{: #merge-conflict-def .glossary data-term="Merge conflict" }

**Origin** - The conventional name Git gives to the remote repository from which a project was cloned and to which it normally pushes.
{: #origin-def .glossary data-term="Origin" }

**Pages** - The website-hosting service provided by GitHub or GitLab for publishing a repository's generated static site.
{: #pages-def .glossary data-term="Pages" }

**Personal access token** - A long, randomly generated code that acts as a substitute for a password, scoped to a single purpose and revocable at any time without changing your main account credentials. See the [Acronyms](acronyms.md#pat) entry for the expansion.
{: #pat-def .glossary data-term="Personal access token" }

**Pipeline** - An automated sequence of jobs that checks, builds, and may deploy a project after a change is pushed.
{: #pipeline-def .glossary data-term="Pipeline" }

**Portable Document Format** - A fixed-layout document format that looks the same regardless of the software, hardware, or operating system used to open it. See the [Acronyms](acronyms.md#pdf) entry for the expansion.
{: #pdf-def .glossary data-term="Portable Document Format" }

**Processor architecture** - The instruction set used by a computer's processor, such as ARM64 or x86-64. Executable programs and native libraries must use compatible architectures.
{: #processor-architecture-def .glossary data-term="Processor architecture" }

**Pull request** - A request to merge changes from one branch into another, reviewed and discussed by collaborators before it's accepted. See the [Acronyms](acronyms.md#pr) entry for the expansion - GitLab calls the same thing a [Merge Request](acronyms.md#mr).
{: #pull-request-def .glossary data-term="Pull request" }

**Remote** - A named connection from a local Git repository to another copy hosted elsewhere. `origin` is the usual name for the main remote.
{: #remote-def .glossary data-term="Remote" }

**Renderer** - A program that converts source notation into its visible form, such as turning Mermaid or TeX source into a diagram or mathematical expression.
{: #renderer-def .glossary data-term="Renderer" }

**Repository** - The complete collection of a project's files and their full history of changes, tracked by Git and stored on a service such as GitLab or GitHub.
{: #repository-def .glossary data-term="Repository" }

**Secure Shell** - An encrypted network protocol used to authenticate with, and send commands to, a remote computer - most commonly used here to connect securely to GitLab or GitHub without typing a password each time. See the [Acronyms](acronyms.md#ssh) entry for the expansion.
{: #ssh-def .glossary data-term="Secure Shell" }

**Static site generator** - A tool that converts a set of source files (such as Markdown) into a complete website of plain HTML pages ahead of time, rather than generating each page on demand when a visitor requests it.
{: #static-site-generator-def .glossary data-term="Static site generator" }

**Template** - A reusable starting project containing an initial structure, configuration, styling, and publishing workflow that authors adapt for their own document.
{: #template-def .glossary data-term="Template" }

**Version control** - A system for recording changes to a set of files over time, so you can review the history, compare versions, and revert to an earlier one if needed.
{: #version-control-def .glossary data-term="Version control" }

**Virtual environment** - A project-specific Python environment that keeps its packages and commands separate from the computer's system Python and from other projects.
{: #virtual-environment-def .glossary data-term="Virtual environment" }
