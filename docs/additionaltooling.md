---
icon: lucide/book-open
---

<!-- 
# Copyright (c) 2025-2026 Mark Buckwell and contributors
# SPDX-License-Identifier: MIT
-->

{{ heading_counter_reset(page) }}

# Additional tooling

This page covers optional tooling you can add on top of the core Zensical workflow covered in [Install tooling](installtooling.md) and [Start editing](startediting.md): Visual Studio Code extensions that connect the editor directly to GitLab or GitHub, view Git history, and check your writing; and keeping your document's images small. You don't need any of this to write or publish your document - add whichever pieces are useful to you, and skip the rest. Each section below assumes no prior Linux or command-line experience, and spells out every step.

## Installing Visual Studio Code extensions

An extension is a small add-on that adds extra features to Visual Studio Code. The extensions covered here let you manage GitLab or GitHub directly from the editor, view your Git history inline, and check your writing for spelling, grammar, and style issues as you type.

### Installing GitLab or GitHub extensions

VS Code doesn't require any extensions to work with GitLab or GitHub, but installing the relevant extension can make it easier to manage your documentation without leaving the editor. Some features of these extensions include:

* Viewing issues and merge requests directly in VS Code.
* Creating and managing issues and merge requests directly in VS Code.
* Viewing and managing your GitLab or GitHub repositories directly in VS Code.
* Viewing and managing your GitLab or GitHub CI/CD pipelines directly in VS Code.

<div class="grid cards one-column" markdown>

-   :material-clock-fast:{ .lg .middle } __Install the extension__

    === "GitLab"

        1. Open VS Code.
        2. Click the **Extensions** icon in the left-hand Activity Bar (or press `Ctrl+Shift+X` on Windows/Linux, `Cmd+Shift+X` on macOS).
        3. In the search box at the top of the Extensions view, type `GitLab`.
        4. Find **GitLab** (published by GitLab) in the results and select **Install**.
        5. Wait for the installation to finish - VS Code shows a notification once it's ready.

    === "GitHub"

        1. Open VS Code.
        2. Click the **Extensions** icon in the left-hand Activity Bar (or press `Ctrl+Shift+X` on Windows/Linux, `Cmd+Shift+X` on macOS).
        3. In the search box at the top of the Extensions view, type `GitHub Pull Requests and Issues`.
        4. Find **GitHub Pull Requests and Issues** (published by GitHub) in the results and select **Install**.
        5. Wait for the installation to finish - VS Code shows a notification once it's ready.

</div>

### Configuring GitLab or GitHub extensions

Once you've installed the extension, it needs permission to access your GitLab or GitHub account. The most reliable way to do this is with a personal access token (PAT) - a long, randomly generated code that works like a password, but you can limit it to just this purpose, give it an expiry date, and revoke it at any time without changing your main account password.

1. Create a personal access token (PAT) for your account:

    <div class="grid cards one-column" markdown>

    -   :material-clock-fast:{ .lg .middle } __Create a Personal Access Token (PAT)__

        === "GitLab"

            1. Log in to **GitLab** (either [gitlab.com](https://gitlab.com) or your organisation's self-managed instance) in a web browser.
            2. In the top-right corner, click on your **profile avatar** and select **Edit profile**.
            3. On the left-hand sidebar, select **Access > Personal access tokens**.
            4. Click **Add new token**{: .bg-blue} and fill out the following details:
                * **Token name:** Give it a clear name (for example, `VS Code Extension`).
                * **Expiration date:** (Optional) Set an expiration date according to your team's security policy. You can click on the date and select the last date available.
            5. Under **Select scopes**, check the **api** scope.
            6. Click **Create token**{: .bg-blue} and copy the token string.

            !!! Warning
                Copy the token string **immediately**. GitLab will only show it to you once; if you refresh or leave the page, it is gone forever.

        === "GitHub"

            VS Code's built-in GitHub integration normally signs you in through your browser (OAuth) rather than a token, so you usually won't need a PAT for GitHub. If you use GitHub Enterprise Server and the browser sign-in doesn't work, create a personal access token instead:

            1. Log in to **GitHub** (either [github.com](https://github.com) or your organisation's self-managed instance).
            2. In the top-right corner, click on your **profile avatar** and select **Settings**.
            3. On the left-hand sidebar, select **Developer settings > Personal access tokens > Fine-grained tokens**.

                !!! Note
                    GitHub may ask you to reauthenticate before you can proceed to the next step.

            4. Click **Generate new token**{: .bg-green} and fill out the following details:
                * **Token name:** Give it a clear name (for example, `VS Code Extension`).
                * **Expiration date:** (Optional) Set an expiration date according to your team's security policy. You can click on the date and select the last date available.
            5. Select the **Repository access** level for the token. Choose **All repositories** if you want the token to have access to all your repositories, or choose **Only select repositories** and specify the repositories you want to grant access to.
            6. Under **Permissions**, select **+ Add permissions** and add the following:
                * **Read and Write** access to **Contents** and **Pull Requests**.
                * **Read-only** access to **Metadata**.
            7. Click **Generate token**{: .bg-green} and copy the token string.

            !!! Warning
                Copy the token string **immediately**. GitHub will only show it to you once; if you refresh or leave the page, it is gone forever.

    </div>

2. Configure the extension to use the token you just created:

    <div class="grid cards one-column" markdown>

    -   :material-clock-fast:{ .lg .middle } __Configure VS Code for Git repo access__

        === "GitLab"

            GitLab's browser sign-in (OAuth) may not work in some environments, so we'll use the personal access token (PAT) instead.

            1. Open VS Code and open the **Command Palette**:
                * For **macOS**, press `Cmd+Shift+P`.
                * For **Windows** or **Linux**, press `Ctrl+Shift+P`.
            2. Type `GitLab: Authenticate` and press `Enter`.
            3. Choose your GitLab instance:
                * Select **GitLab.com** if you use a public cloud instance.
                * Select **Add new instance URL** if you use a self-hosted instance, and type your full domain (for example, `https://gitlab.yourorganisation.com`).
            4. Select **Enter an existing token**.
            5. Paste in the personal access token (PAT) you created earlier and press `Enter`.

            The extension instantly validates the token. If successful, your GitLab status updates in the bottom status bar, and your GitLab sidebar panel populates with your issues and merge requests.

        === "GitHub"

            The built-in GitHub Authentication provider in VS Code uses a browser sign-in (OAuth) by default.

            1. Click the **Accounts** icon (the profile silhouette) in the bottom-left corner of VS Code.
            2. Select **Sign in with GitHub** (this may appear under a Copilot or Settings Sync prompt, depending on your VS Code version).
            3. Click **Allow** when asked to open the external website.
            4. Your browser opens GitHub to authorize the app. Click **Authorize Visual Studio Code**.
            5. **If the browser doesn't redirect back to VS Code:** GitHub displays a page saying *"If your browser does not redirect you..."* alongside a **blue box containing an authorization token.** Copy that token.
            6. Return to VS Code. Look at the very bottom **Status Bar**; it says `Signing in to github.com....`.
            7. Click that status bar text. An input box opens at the top of your editor.
            8. Paste the token you copied from the browser page and press `Enter`.

            !!! Note "Note for GitHub Enterprise Server users"
                If your company hosts its own private GitHub Enterprise Server, the browser flow won't always work out of the box. To use a PAT directly, start the sign-in prompt, click **Cancel** on the browser authorization pop-ups, and VS Code automatically changes its prompt to a direct text field asking you to paste your Enterprise PAT.

    </div>

### Installing GitLens for commit history and blame

[GitLens](https://www.gitkraken.com/gitlens){target="_blank"} is a VS Code extension that adds inline "blame" annotations - showing who last changed each line, and when - directly above your text, along with a visual commit graph and richer history browsing. It's especially useful once you're using the branches and issues workflow from [Managing branches and issues](startediting.md#managing-branches-and-issues).

1. Click the **Extensions** icon in the left-hand Activity Bar (or press `Ctrl+Shift+X` on Windows/Linux, `Cmd+Shift+X` on macOS).
2. In the search box, type `GitLens`.
3. Find **GitLens — Git supercharged** (published by GitKraken) in the results and select **Install**.
4. Once installed, a small annotation appears above the line your cursor is on, showing the last commit that changed it. Hover over it for full details, or select the **\index{VS Code!GitLens}** icon in the Activity Bar for the commit graph and history views.

### Installing Code Spell Checker for lightweight spell checking

If [Vale](#install-vale-to-check-for-grammar-spelling-and-style-issues) below feels like more setup than you need right now, \index{VS Code!Code Spell Checker} is a lighter alternative (or a useful complement to it) that underlines misspelled words directly in the editor as you type, with no configuration files required.

1. Click the **Extensions** icon in the left-hand Activity Bar (or press `Ctrl+Shift+X` on Windows/Linux, `Cmd+Shift+X` on macOS).
2. In the search box, type `Code Spell Checker`.
3. Find **Code Spell Checker** (published by Street Side Software) in the results and select **Install**.
4. Misspelled words are now underlined in the editor as you type. Right-click an underlined word for suggested corrections, or to add it to your personal dictionary if it's a term you use often (such as a project name or acronym).

### Install vale to check for grammar, spelling, and style issues

[Vale](https://vale.sh/){target="_blank"} is a syntax and style checker for writing. You can use it to check your documentation for grammar, spelling, and style issues.

1. Install Vale for your operating system. [Open a terminal](startediting.md#open-a-terminal) if you don't already have one open, then follow the steps below:

    <div class="grid cards one-column" markdown>

    -   :material-clock-fast:{ .lg .middle } __Install Vale__

        === ":material-apple: macOS"

            ``` bash
            brew install vale
            ```

        === ":fontawesome-brands-windows: Windows"

            1. Open PowerShell as an administrator: press the `Windows` key, type `PowerShell`, then either press `Ctrl+Shift+Enter`, or right-click **Windows PowerShell** in the results and select **Run as administrator**.
            2. Use the Microsoft Windows Package Manager (winget) to install Vale:

                ``` powershell
                winget install --id errata-ai.Vale
                ```

        === ":material-linux: Linux (Ubuntu)"

            1. If you don't already have `snapd` installed, install it:

                ``` bash
                sudo apt update
                sudo apt install snapd
                ```

            2. Once you've installed `snapd`, install Vale:

                ``` bash
                sudo snap install vale
                ```

            See the [Vale installation page](https://vale.sh/docs/install/){target="_blank"} for other Linux distributions.

    </div>

2. Create a `.vale.ini` file in the top-level directory of your project (the same folder that contains `zensical.toml`). This file configures Vale and specifies the rules and styles used to check your documentation.

    In VS Code, right-click your project's root folder in the Explorer pane and select **New File...**. Name the file `.vale.ini` (including the leading dot), then paste in the following content as a starting point:

    ```ini
    StylesPath = styles
    MinAlertLevel = suggestion
    Packages = Microsoft, Readability, proselint

    [*.{md,rst,asciidoc,html}]
    BasedOnStyles = Vale, Microsoft, Readability, proselint

    Vale.Terms = YES
    Vale.Avoid = YES
    Vale.Spelling = YES

    Microsoft.OxfordComma = YES
    Microsoft.Passive = YES
    Microsoft.Dashes = YES
    Microsoft.Spacing = YES
    Microsoft.Wordiness = YES
    Microsoft.We = YES
    ```

3. Create a `styles` directory in the top-level directory of your project. In VS Code, right-click your project's root folder in the Explorer pane and select **New Folder...**, then name it `styles`.

    Then synchronise the styles specified in `.vale.ini`. Open a new terminal (or PowerShell) for this, and make sure it's actually sitting in your project's root directory first:

    ```bash
    cd path/to/your-project
    ```

    Then run:

    ```bash
    vale sync
    ```

4. Install the [Vale VS Code extension](https://marketplace.visualstudio.com/items?itemName=ChrisChinchilla.vale-vscode){target="_blank"} so Vale's suggestions appear directly in the editor:

    1. Click the **Extensions** icon in the left-hand Activity Bar (or press `Ctrl+Shift+X` on Windows/Linux, `Cmd+Shift+X` on macOS).
    2. In the search box, type `Vale`.
    3. Find **Vale** (published by Chris Chinchilla) in the results and select **Install**.
    4. Restart Visual Studio Code once the installation finishes.

    When you open a Markdown file in Visual Studio Code, the Vale extension automatically checks it for grammar, spelling, and style issues based on the rules and styles you configured. View the results in the **Problems** panel: **View > Problems**, or the keyboard shortcut `Ctrl+Shift+M` (`Cmd+Shift+M` on macOS).

    \index{VS Code!Vale} generates a large number of suggestions, some of which aren't relevant to your documentation. You can ignore these and focus on the suggestions that are relevant to your writing style and the requirements of your documentation.

5. One of the most prominent suggestions is to change from passive voice to active voice. This is a good suggestion and recommended in business writing, but it can take time to change all instances of passive voice to active voice.

    If you need some help with this, here are a few websites that can help you understand how to change from passive voice to active voice:

    * [BBC Bitesize](https://www.bbc.co.uk/bitesize/articles/zkttng8){target="_blank"}
    * [Communication for Professionals](https://courses.lumenlearning.com/suny-esc-communicationforprofessionals/chapter/active-voice/){target="_blank"}
    * [University of York](https://subjectguides.york.ac.uk/academic-language/voice){target="_blank"}

    You can also change the `Microsoft.Passive` rule in the `.vale.ini` file to `NO` if you find it too difficult to change all instances of passive voice to active voice.

## Optimising images before committing

When you commit screenshots and diagrams to the Git repository, the PDF build also embeds them in the generated PDF, so a handful of large, uncompressed images can noticeably slow down cloning the repository and increase the size of the published PDF. Optimising (compressing) an image before you commit it usually shrinks it considerably with no visible loss of quality.

The simplest option, needing no installation, is [Squoosh](https://squoosh.app/){target="_blank"} - a free, browser-based image compressor from Google. Drag your screenshot into the page, choose a format and quality, and download the smaller result to use in place of the original.

If you'd rather compress images from your desktop without opening a browser each time, install a dedicated tool instead:

<div class="grid cards one-column" markdown>

-   :material-clock-fast:{ .lg .middle } __Install an image optimiser__

    === ":material-apple: macOS"

        ``` bash
        brew install --cask imageoptim
        ```

        Once installed, drag image files onto the \index{Image optimisation!ImageOptim} window (or its Dock icon) to compress them in place.

    === ":fontawesome-brands-windows: Windows"

        Download and run the installer for [FileOptimizer](https://nikkhokkho.sourceforge.io/?page=FileOptimizer){target="_blank"} - there's no reliable single winget package for it. Once installed, drag image files onto the FileOptimizer window to compress them in place.

    === ":material-linux: Linux (Ubuntu)"

        ``` bash
        sudo apt update
        sudo apt install pngquant jpegoptim
        ```

        Then compress an image from the terminal, for example:

        ``` bash
        pngquant --ext .png --force docs/starthere/images/example.png
        jpegoptim docs/starthere/images/example.jpg
        ```

</div>

## Where to go next {: #additionaltooling-where-to-go-next }

This is the last of the step-by-step "Start Here" chapters. [Shell commands](shcommands.md) is a standalone reference you can return to any time you need a reminder of a terminal command - it isn't something you need to read in order.
