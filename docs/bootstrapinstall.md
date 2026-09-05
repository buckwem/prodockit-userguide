---
icon: lucide/rocket
---

<!--
Copyright (c) 2025-2026 Mark Buckwell and contributors
SPDX-License-Identifier: MIT
-->

{{ heading_counter_reset(page) }}

# Bootstrap Install

`prodockit bootstrap` lets you \index{Tasks!Bootstrap a new project} by automating the one-time setup needed to work with
[prodockit-template](https://github.com/buckwem/prodockit-template){target="_blank"}.
It checks the computer first, shows what it proposes to change, and then works
through the installation in stages. A completed stage is checked and skipped
when the command is run again.

Use this page when you want `prodockit bootstrap` to install and configure the supported
tooling for you. If you need to perform each task yourself, or cannot allow an
installer to make the changes, use [Manual install](installtooling.md) instead.

!!! info "Automation for the prodockit template"
    `prodockit bootstrap` is designed around the files, build tools, editor settings, and
    publishing workflow supplied by prodockit-template. It is not a general
    installer for every Zensical project.

!!! note "The command is `prodockit bootstrap`"
    The `prodockit` Python package installs this command. The shorter
    `pdk boot` alias performs the same work; these instructions use the full
    command throughout.

## What it sets up

The command checks 23 stages grouped into seven phases:

| Phase | What `prodockit bootstrap` prepares |
| --- | --- |
| Preflight | A separate Python environment for running prodockit |
| Core tools | Visual Studio Code and Git |
| Git and host | Your SSH key, SSH agent, and access to GitLab or GitHub |
| Project | The correct repository, its history, remote, and commit identity |
| Build toolchain | Pandoc, WeasyPrint's libraries, fonts, Node.js, Mermaid, and MathJax |
| Editor and project | VS Code extensions and settings, citation style, and website maths |
| Publish | The first build, commit, push, and published documentation site |

Some actions must remain yours. For example, you choose an SSH-key passphrase,
sign in to GitLab or GitHub, confirm any administrator request, and approve the
first push. `prodockit bootstrap` explains these actions when it reaches them.

## Complete the automated installation

The steps below complete the automated installation while keeping
the project and the separate environment used to run `prodockit bootstrap` distinct.

/// steps

//// step | Install Python 3.14

Python is the one prerequisite `prodockit bootstrap` cannot install because Python is
needed to run the command itself. Install Python 3.14 and confirm that exact
release before creating the environment.

=== ":material-apple: macOS"

    Install [Homebrew](https://brew.sh){target="_blank"} if it is not already
    installed. Close and reopen Terminal after installing it, then run:

    ``` bash
    brew install python@3.14
    "$(brew --prefix python@3.14)/bin/python3.14" --version
    ```

    Naming Homebrew's Python avoids accidentally using the older Python that
    macOS may provide.

=== ":fontawesome-brands-windows: Windows"

    Install the 64-bit Python 3.14 release from
    [python.org](https://www.python.org/downloads/){target="_blank"}. On the
    first installer screen, tick **Add python.exe to PATH**. On the final
    screen, select **Disable path length limit**.

    Open PowerShell and check the installation:

    ``` powershell
    py -3.14 --version
    ```

    If PowerShell cannot find `py`, repeat the installer with the Python
    Launcher selected, then open a new PowerShell window.

=== ":material-linux: Linux (Ubuntu)"

    Open Terminal and run:

    ``` bash
    sudo apt update
    sudo apt install python3.14 python3.14-venv python3-pip
    python3.14 --version
    ```

    Ubuntu packages the virtual-environment support separately, so
    `python3.14-venv` is required even when `python3.14` is already present.

Each check must report `Python 3.14` before you continue.

////

//// step | Create the environment that runs prodockit bootstrap

Create a top-level `GitHub` directory in which to keep your projects. Create a
small Python setup environment named `.venv` in that directory and install
prodockit into it.

=== ":material-apple: macOS"

    ``` bash
    mkdir -p ~/GitHub
    cd ~/GitHub
    "$(brew --prefix python@3.14)/bin/python3.14" -m venv .venv
    source .venv/bin/activate
    python -m pip install --upgrade pip
    python -m pip install --upgrade prodockit
    ```

=== ":fontawesome-brands-windows: Windows"

    PowerShell normally prevents activation scripts from running. Allow
    locally created scripts for your account once:

    ``` powershell
    Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
    ```

    Then create and activate the environment:

    ``` powershell
    New-Item -ItemType Directory -Force ~\GitHub | Out-Null
    Set-Location ~\GitHub
    py -3.14 -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install --upgrade pip
    python -m pip install --upgrade prodockit
    ```

=== ":material-linux: Linux (Ubuntu)"

    ``` bash
    mkdir -p ~/GitHub
    cd ~/GitHub
    python3.14 -m venv .venv
    source .venv/bin/activate
    python -m pip install --upgrade pip
    python -m pip install --upgrade prodockit
    ```

The prompt should now begin with `(.venv)`. Confirm that the expected command
and version are active:

``` bash
python --version
```

It must still report `Python 3.14`. From this point, use `python -m pip` only
while this environment is active. Conda, Poetry, uv, and other environment
managers require you to adapt the creation, activation, and package commands;
the bootstrap stages and this guide assume the `.venv` layout shown here.

=== ":material-apple: macOS"

    ``` bash
    command -v prodockit
    prodockit --version
    ```

=== ":fontawesome-brands-windows: Windows"

    ``` powershell
    Get-Command prodockit
    prodockit --version
    ```

=== ":material-linux: Linux (Ubuntu)"

    ``` bash
    command -v prodockit
    prodockit --version
    ```

!!! important "Bootstrap creates the build environment"
    This top-level `GitHub/.venv` contains prodockit for setup. During stage
    16, `prodockit bootstrap` creates another `.venv` inside the project for
    the project's own build packages. Keep them separate. Run `prodockit
    bootstrap` from the top-level environment; use the project environment
    later when editing and building the document.

////

//// step | Describe the project

Remain in the top-level projects directory with its `.venv` active, then run:

``` bash
prodockit bootstrap --configure
```

Press ++enter++ to accept a value shown in brackets. The questions identify:

- the Git service holding the project;
- your name and email address for saved Git changes;
- your username, group or namespace, and repository name.
{% if is_surrey %}
- for supported University of Surrey assignments, the course, assessment
    stage, and year used to derive the issued repository name.
{% endif %}

The answers are saved to `.pdkboot.toml` in the current directory. This is a
local setup file and should remain outside the project repository. The legacy
filename is retained so existing Bootstrap configurations continue to work
with the promoted command.

!!! warning "Connect to the required network first"
    A private GitLab service may require an organisation's network or VPN. If
    the host cannot be reached, connect to the required network and repeat
    `prodockit bootstrap --configure`. A temporary network failure does not damage the
    configuration already entered.

////

//// step | Check what is already set up

Run the read-only check:

``` bash
prodockit bootstrap --check
```

The report uses four useful states:

| State | Meaning |
| --- | --- |
| `ok` | The stage is already correct and will be skipped. |
| `MISS` | Something needs installing or creating. |
| `WRONG` | Something exists but needs configuring or repairing. |
| `WAIT` | A previous stage must finish before this one can be checked. |

`MISS`, `WRONG`, and `WAIT` are expected on a new computer. They are a plan,
not a sign that the installation has failed.

The project path near the top of the output deserves a quick check. It should
be the new folder that `prodockit bootstrap` will create beneath the directory containing
`.pdkboot.toml`.

////

//// step | Preview every proposed change

Before installing anything, run:

``` bash
prodockit bootstrap --dry-run
```

The preview shows the outstanding stages, the commands that can be automated,
and the browser actions that need you. It does not make changes.

`prodockit bootstrap` handles the two common repository starting points:

`The repository is new or empty`

: You create a blank private repository when prompted. `prodockit bootstrap` clones
    prodockit-template locally, archives the template's Git history, starts a
    clean history for your work, points it at your repository, builds it, and
    pushes the first commit.

`The repository already contains work`

: `prodockit bootstrap` clones that repository and retains all of its existing files and
    history. It does not replace the work with the template. The output says
    that the existing repository is being cloned and kept unchanged before the
    remaining machine and project tooling is installed.

!!! danger "Check the exact repository address"
    Before confirming a host project, compare the group and repository shown
    by `prodockit bootstrap` with the address in your browser. A similarly named repository
    is not interchangeable with an assigned or organisation-issued one because
    its permissions may differ.

////

//// step | Apply the plan

Run:

``` bash
prodockit bootstrap --apply
```

Each phase and stage has a prominent heading. Before a change, `prodockit bootstrap` shows
what it will do and asks for confirmation. Press ++enter++ to accept the
default **Yes**, or enter `n` to skip that action.

!!! warning "A typed `yes` means a manual step is due"
    An ordinary automated action accepts ++enter++. If Bootstrap instead asks
    you to type the complete word `yes`, stop and check the instructions
    immediately above the prompt: you should have completed and verified the
    stated manual action before authorising Bootstrap to continue.

Routine installer output is replaced by a progress indicator so you can see
that work is continuing. Commands that require interaction, such as
`ssh-keygen` and `ssh-add`, keep control of the terminal. If a command fails,
its full output and recovery advice are displayed.

On macOS, Bootstrap also adds VS Code's application-owned command directory to
`~/.zprofile`. The current run can use `code` immediately, and new terminal
windows inherit it without requiring the Command Palette's **Shell Command:
Install 'code' command in PATH** action. Existing profile content and an
already-working `code` command are left unchanged.

You will normally need to help with these points:

- approve administrator requests made by the operating system;
- choose and re-enter a passphrase for the SSH key;
- paste the displayed public key into GitLab or GitHub;
- confirm the Git host fingerprint after comparing it with the value supplied
    by your organisation or Git service;
- create a blank private repository if the named repository does not exist;
- authorise access to a private Pages site in the browser; and
- approve the first build, commit, and push.

Bootstrap saves the selected Mermaid and maths choices in the new project's
`.prodockit-components.toml`. A later `pdk adopt` run can therefore inspect or
repair that toolchain without asking you to configure those choices again.

!!! note "A browser sign-in page means the private site exists"
    A private GitLab Pages address may redirect to a GitLab authorisation page.
    That redirect confirms the published page exists. Authorise GitLab Pages
    to continue to the site.

////

//// step | Resume safely if work stops

An installation can be interrupted by a lost network connection, a package
service returning a temporary error, a closed terminal, or a computer restart.
Return to the directory containing `.pdkboot.toml`, reactivate its environment,
and run the same apply command again.

=== ":material-apple: macOS"

    ``` bash
    cd ~/GitHub
    source .venv/bin/activate
    prodockit bootstrap --apply
    ```

=== ":fontawesome-brands-windows: Windows"

    ``` powershell
    Set-Location ~\GitHub
    .\.venv\Scripts\Activate.ps1
    prodockit bootstrap --apply
    ```

=== ":material-linux: Linux (Ubuntu)"

    ``` bash
    cd ~/GitHub
    source .venv/bin/activate
    prodockit bootstrap --apply
    ```

Completed stages are checked and skipped. Partially completed package installs
are checked for their actual result before another repair is proposed. The
recovery record is stored as `.pdkboot.last-run.json` beside the configuration
file; it records what happened but does not replace the live checks.

If a package service reports a temporary `503`, timeout, or connection error,
wait briefly and resume. Do not delete a project or environment merely because
one download failed.

////

//// step | Confirm all stages

When the apply run finishes, perform one final read-only check:

``` bash
prodockit bootstrap --check
```

The final line should say:

``` text
All 23 stages are set up.
```

The project repository should also be clean and connected to the intended
online repository:

``` bash
cd report-az1234
git status --short
git remote -v
git log -1 --oneline
```

Replace `report-az1234` with the project directory printed by `prodockit bootstrap`. An
empty `git status --short` result means there are no unsaved file changes.

Continue to [Start editing](startediting.md) to open the project, preview the
website, build its PDF, and publish later changes.

////

///

## Help with common problems

### `prodockit` is not recognised

Change to the directory containing the top-level `.venv` and activate it again.
Every new Terminal or PowerShell window needs this step. If `prodockit --version`
still fails, reinstall prodockit with the same environment active:

``` bash
python -m pip install --upgrade prodockit
```

### The Git service cannot be reached

Check the network or VPN first. A website loading in a browser does not always
prove that its SSH service on port 22 is reachable. Resume `prodockit bootstrap` after the
service is available; the SSH and repository stages will be checked again.

### An installed command is not found on Windows

Windows installers update the environment used by future terminals. `prodockit bootstrap`
refreshes its own environment during an apply run, but commands you type by
hand may still require a new PowerShell window. Open a new window, return to the
setup directory, activate `.venv`, and resume.

### WeasyPrint cannot load its graphics libraries

Run `prodockit bootstrap --apply` again from the setup directory. On macOS, `prodockit bootstrap`
configures the project activation script to expose Homebrew's libraries. On
Windows, it selects MSYS2 libraries that match the architecture of the Python
executable rather than relying on the machine label alone. On Ubuntu, it
installs the required Pango libraries through `apt`.

### The published site is still being prepared

The first pipeline commonly takes several minutes. Open **Build > Pipelines**
on GitLab or **Actions** on GitHub and wait for the publishing job to finish.
Then rerun `prodockit bootstrap --apply` or `prodockit bootstrap --check` and confirm the page in your
browser.

## Where to go next {: #bootstrapinstall-where-to-go-next }

You now have the supported tools, a local prodockit project, and a formal-looking
document as a head start. Add any useful, non-essential editor or conversion
tools from [Additional tooling](additionaltooling.md), or continue directly to
[Start editing](startediting.md) to open the project, preview the website, build
its PDF, and use Git for later changes. Then use
[Document appearance and structure](customise.md) to replace the example content and adapt the
document's branding, structure, and build settings for your own work.
