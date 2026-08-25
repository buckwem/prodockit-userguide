---
icon: lucide/wrench
---

<!--
Copyright (c) 2025-2026 Mark Buckwell and contributors
SPDX-License-Identifier: MIT
-->

{{ heading_counter_reset(page) }}

# Additional tooling

The three installation routes provide everything needed to write, build, and
publish a document. This page contains optional tools that may make particular
authoring tasks easier. Choose only the sections that match your work; none is
required before you continue with the guide.

## Choose what you need

| If you want to... | Consider... | What it adds |
| --- | --- | --- |
| work with issues and reviews inside Visual Studio Code | the GitLab or GitHub extension | access to the hosting service from the editor |
| understand who changed a line and when | GitLens | additional Git history views |
| catch spelling mistakes while typing | Code Spell Checker | a lightweight editor-only check |
| apply shared writing rules | Vale | repeatable spelling, grammar, and style checks |
| reuse a Word, PowerPoint, spreadsheet, or PDF document | anydoc | an initial Markdown conversion to review |
| reduce the size of screenshots and diagrams | an image optimiser | smaller repository and PDF files |

!!! note

    Bootstrap Install already adds LTeX+ to Visual Studio Code. Start with that
    writing check and add Code Spell Checker or Vale only if it serves a
    different need.

## Work with GitLab or GitHub in Visual Studio Code

Visual Studio Code can commit, pull, and push with Git without either extension.
Use the SSH connection configured by the installation route for those Git
operations. Install one of these extensions only if you also want to view
issues, review changes, or inspect pipelines without leaving the editor.

=== "GitLab"

    1. Open Visual Studio Code.
    2. Open **Extensions** from the Activity Bar, or press `Cmd+Shift+X` on
        macOS and `Ctrl+Shift+X` on Windows or Linux.
    3. Search for `GitLab`.
    4. Select **GitLab** published by GitLab, then select **Install**.

=== "GitHub"

    1. Open Visual Studio Code.
    2. Open **Extensions** from the Activity Bar, or press `Cmd+Shift+X` on
        macOS and `Ctrl+Shift+X` on Windows or Linux.
    3. Search for `GitHub Pull Requests and Issues`.
    4. Select **GitHub Pull Requests and Issues** published by GitHub, then
        select **Install**.


### Connect the extension to the repository service

SSH remains the preferred connection for cloning, pulling, and pushing. The
extension needs a second, separate account connection because issues, reviews,
and pipeline information come from the GitLab or GitHub web API rather than
from Git. This account connection does not replace or reconfigure SSH.

=== "GitLab"

    1. Open the Command Palette with `Cmd+Shift+P` on macOS or
        `Ctrl+Shift+P` on Windows or Linux.
    2. Run `GitLab: Authenticate`.
    3. Select GitLab.com, or enter the full address of your organisation's
        GitLab service.
    4. Select the account connection supported by your organisation. For a
        personal access token, create one in GitLab with the `api` scope,
        give it a clear name and suitable expiry date, then paste it into
        Visual Studio Code. If OAuth is provided, complete the browser
        sign-in instead.

    Follow GitLab's
    [official setup instructions](https://docs.gitlab.com/editor_extensions/visual_studio_code/setup/){target="_blank"}
    if the labels differ in your installed version.

=== "GitHub"

    1. Select the GitHub icon in the Activity Bar.
    2. Select **Sign In** and allow Visual Studio Code to open GitHub in the
        browser.
    3. Approve the request and return to Visual Studio Code.
    4. If the browser shows a code instead of returning automatically,
        copy it, select the `Signing in to github.com...` message in Visual
        Studio Code's status bar, and paste the code there.

    A personal access token is normally needed only for a separately hosted
    GitHub Enterprise Server. See Visual Studio Code's
    [official GitHub guide](https://code.visualstudio.com/docs/sourcecontrol/github){target="_blank"}
    for that case.


!!! warning "Treat an access token like a password"

    Never put a token in a Markdown file, configuration file, screenshot,
    commit, or message. If a token is exposed, revoke it in GitLab or GitHub
    immediately and create a replacement.

### Help with repository sign-in

- If GitLab rejects a token, check that it has not expired, that it includes
    the `api` scope, and that you selected the correct GitLab address.
- If browser sign-in does not return to Visual Studio Code, copy the code shown
    by the browser and use the sign-in message in the editor's status bar.
- If an old account keeps appearing, sign out from the **Accounts** menu in
    Visual Studio Code, then authenticate again.
- If Git works in a terminal but the extension does not, do not replace a
    working SSH key. Git access and extension sign-in are separate connections;
    authenticate the extension again instead.

## Inspect Git history with GitLens

\index{GitLens} ([website](https://www.gitkraken.com/gitlens){target="_blank"}) adds more detailed
history views to Visual Studio Code. It can show the commit that last changed a
line and provide a visual commit graph.

1. Open **Extensions** in Visual Studio Code.
2. Search for `GitLens`.
3. Select **GitLens — Git supercharged** published by GitKraken, then select
    **Install**.
4. Open a tracked file and place the cursor on a line to see its most recent
    change. Open the GitLens view from the Activity Bar for the wider history.

Use this when the built-in **Source Control** history is not detailed enough.
Some GitLens features may require an account or paid plan; the extension shows
which features are available before you use them.

## Check spelling and writing style

Choose the smallest tool that meets the project's needs.

### Add lightweight spelling checks

Code Spell Checker underlines words that are not in its dictionary. It requires
little setup and is useful for an individual author.

1. Open **Extensions** in Visual Studio Code.
2. Search for `Code Spell Checker`.
3. Select **Code Spell Checker** published by Street Side Software, then select
    **Install**.
4. Right-click an underlined word to correct it or add a genuine project term
    to a dictionary.

### Add shared checks with Vale

\index{Vale} ([website](https://vale.sh/){target="_blank"}) applies writing rules stored with the
project. Choose it when a team needs the same checks on every computer or in an
automated pipeline.

1. Install Vale for the operating system.

    === ":material-apple: macOS"

        ``` bash
        brew install vale
        ```

    === ":fontawesome-brands-windows: Windows"

        Open PowerShell, then run:

        ``` powershell
        winget install --id errata-ai.Vale
        ```

    === ":material-linux: Linux (Ubuntu)"

        ``` bash
        sudo snap install vale
        ```

        If Snap is not installed, follow Vale's
        [Linux installation choices](https://vale.sh/docs/install/){target="_blank"}
        instead of adding a new package manager only for this tool.


2. In the top-level project directory, create `.vale.ini` with an initial
    configuration:

    ``` ini
    StylesPath = styles
    MinAlertLevel = suggestion
    Packages = Microsoft, Readability, proselint

    [*.{md,rst,asciidoc,html}]
    BasedOnStyles = Vale, Microsoft, Readability, proselint
    ```

3. Open a terminal in the same directory and download the selected rule sets:

    ``` bash
    vale sync
    ```

4. Check the Markdown files:

    ``` bash
    vale docs
    ```

5. To see results while typing, install the **Vale** extension published by
    Chris Chinchilla in Visual Studio Code, then restart the editor.

Treat Vale's results as advice. Agree the rules with the people reviewing the
document before spending time correcting every suggestion.

## Convert an existing document to Markdown

\index{anydoc} ([repository](https://github.com/firecrawl/anydoc){target="_blank"}) can convert Word,
PowerPoint, Excel, OpenDocument, RTF, EPUB, CSV, and PDF files into Markdown.
The result is a starting point, not a finished page.

The simplest route is the
[anydoc browser tool](https://firecrawl.github.io/anydoc/){target="_blank"}.
The conversion runs in the browser, and its interface states that the selected
file does not leave the computer.

To convert several files from a terminal, use `npx` after installing Node.js:

``` bash
npx @firecrawl/anydoc report.docx -o report.md
```

Replace the two filenames with the source and destination. Compare the result
with the original, paying particular attention to tables, footnotes, images,
and complex layouts before moving it into `docs/`.

## Optimise images before committing

\index{Images!Optimisation} keeps large screenshots from making a repository slower to clone or increasing the PDF
size. Keep an original outside the repository, optimise a copy, and check that
text and important details remain legible before committing it.

The simplest option is [Squoosh](https://squoosh.app/){target="_blank"}, which
runs in a browser. For regular use, install a desktop or command-line tool:

=== ":material-apple: macOS"

    ``` bash
    brew install --cask imageoptim
    ```

    Drag copies of the images onto ImageOptim. It replaces each selected
    file with its optimised version.

=== ":fontawesome-brands-windows: Windows"

    Download [FileOptimizer](https://nikkhokkho.sourceforge.io/?page=FileOptimizer){target="_blank"}
    from its project site, install it, and drag copies of the images into
    its window.

=== ":material-linux: Linux (Ubuntu)"

    ``` bash
    sudo apt update
    sudo apt install pngquant jpegoptim
    ```

    Compress a copy of a PNG or JPEG, for example:

    ``` bash
    pngquant --ext .png --force example.png
    jpegoptim example.jpg
    ```


## Where to go next {: #additionaltooling-where-to-go-next }

Optional tooling is now complete. Continue to [Start editing](startediting.md)
to open the project, preview the website, build the PDF, and save changes with
Git. Return to this page later if a new authoring need appears.
