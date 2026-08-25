---
icon: lucide/book-open 
---

<!-- 
Copyright (c) 2025-2026 Mark Buckwell and contributors
SPDX-License-Identifier: MIT
-->

{{ heading_counter_reset(page) }}

# Manual install

This section explains how to prepare a computer and a project manually. It
covers macOS, Windows 11, and Linux (Ubuntu). The commands create the same
working setup whether you are starting a new project from the prodockit
template or downloading a repository that already contains work.

You do not need previous Git experience. Each section explains what the
commands change and how to check the result before continuing.

<div class="web-only" markdown>
!!! Tip
    The screenshots below may have small text on your screen but you can click on an image to enlarge it. The glightbox viewer will open the image in a new tab and you can zoom in to see the details.
</div>

Work through the sections in order. Where a tool is already installed, still
run the check shown for it before continuing.

## Install Visual Studio Code

[Visual Studio Code](https://code.visualstudio.com){target="_blank"} (VS Code) is the editor we have chosen for developing the documentation using Zensical. You can use other editors, but the availability of many plugins in Visual Studio Code will help you edit your documentation more efficiently.

The steps below will help you install \index{VS Code} and some essential plugins to edit your documentation. If you have already installed VS Code, check through the steps so you have the plugins installed.

### Install Visual Studio Code

Start with installing [Visual Studio Code](https://code.visualstudio.com){target="_blank"}. Instructions for macOS, Windows 11, and Linux (Ubuntu/Debian) are below.

<div class="grid cards one-column" markdown>
    
-   :material-clock-fast:{ .lg .middle } __Install Visual Studio Code__

    === ":material-apple: macOS"

        1. Open the **Terminal** application.
        1. You are likely to already have [Homebrew](https://brew.sh){target="_blank"} installed, but if not, follow the instructions on [brew.sh](https://brew.sh){target="_blank"} to install it.  **Close and reopen your Terminal after installing it.** As the installer adds `brew` to your `PATH`, and a session that was already open won't pick that up.

        1. Use the Homebrew package manager to install Visual Studio Code in your Terminal:
            ``` bash
            brew update
            brew install --cask visual-studio-code
            ```

    === ":fontawesome-brands-windows: Windows"

        1. Download the VS Code User setup for Windows from the [official website](https://code.visualstudio.com/download){target="_blank"}.
        2. Run the installer, `VSCodeUserSetup-{version}.exe`. By default the User setup installs Visual Studio Code to your user profile directory. You can change the install location if you want to install it for all users.
         
    === ":material-linux: Linux (Ubuntu)"

        1. Download the `.deb` package from the [official website](https://code.visualstudio.com/).
        2. Open a terminal and navigate to the directory where you downloaded the `.deb` package.
        3. Run the following command to install Visual Studio Code:
            ``` bash
            sudo apt install ./<file>.deb
            ```
        Replace `<file>` with the name of the downloaded `.deb` file.

        Further installation instructions are available on the [Visual Studio Code website](https://code.visualstudio.com/docs/setup/linux){target="_blank"}.

</div>

## Install Git with Visual Studio Code

\index{<a href="https://git-scm.com/" target="_blank">Git</a>} is a version control system that enables you to track changes to your code and collaborate with others. You will be using Git to manage your documentation website and push your changes to your **GitLab** or **GitHub** cloud repository.

Next, install the `git` command and configure it for Visual Studio Code. The instructions below are for use with both *GitLab* and *GitHub*.

### Install and configure Git

Start by installing Git and configuring it for Visual Studio Code. The instructions below are for macOS, Windows 11, and Linux (Ubuntu/Debian).

1. As a start, you need to install the `git` command. Follow the instructions below to install or update `git` to the latest stable version.

    <div class="grid cards one-column" markdown>
    
    -   :material-clock-fast:{ .lg .middle } __Install Git__

        === ":material-apple: macOS"

            Use the Homebrew package manager to install or update `git` to the latest stable version:
                
            ``` bash
            brew install git
            ```

        === ":fontawesome-brands-windows: Windows"

            Open up a **PowerShell** Administrator window and install `git` using the command, or you can download and install the official git installer from [git-scm.com](https://git-scm.com/download/win){target="_blank"}.
                
            ``` PowerShell
            winget install Git.Git
            ```
        
            If you just require an updated version of `git`, you can run the following command in **PowerShell**:
                
            ``` PowerShell
            winget upgrade Git.Git
            ```

            **Close down PowerShell** and reopen it after installing or updating `git` to ensure that the new version is available in your `PATH`. Check the version of `git` installed by running the following command in **PowerShell**:

            ``` PowerShell
            git --version
            ```

        === ":material-linux: Linux (Ubuntu)"

            Open a terminal and run the following command to install or update `git` to the latest stable version:
            
            ``` bash
            sudo apt update
            sudo apt install git
            ```
    </div>

1. Before connecting to any cloud provider, open your terminal (Terminal on macOS/Debian, Git Bash or PowerShell on Windows 11) and set your global username. This is the identity stamped onto your commits.

    ``` bash
    git config --global user.name "Your Name"
    ```

    Then set the email address to go with it. Make sure it's the same one you used to register for your GitLab or GitHub account.

    ``` bash
    git config --global user.email "your.email@example.com"
    ```

    !!! tip "Already use Git for other projects?"
        `--global` applies everywhere, on this project and every other one on your machine - the only option available right now, since you haven't cloned anything yet to scope it to. If you already have a Git identity set up for your own projects, run both commands again with `--local` instead once you've cloned the template below, so this project's commits use these details without changing your identity anywhere else.

1. Register for an account on the public [**GitLab**](https://gitlab.com){target="_blank"} or [**GitHub**](https://github.com){target="_blank"} cloud instance you will use. If you have already registered, you can skip this step.

{% if is_surrey %}
!!! Info "University of Surrey GitLab"
    For the University of Surrey, you will need to use the GitLab instance provided by the university at [https://gitlab.surrey.ac.uk](https://gitlab.surrey.ac.uk){target="_blank"} for all assignments. When you get to the login page, select the button **Surrey Login**{: .bg-grey} and use your university credentials.
{% endif %}

### Generate and configure ssh keys for Git

{% if is_surrey %}
Now generate the \index{Git!ssh keys} to use for authentication with your GitLab account and configure your ssh settings to use it. Your coursework lives on the University of Surrey's GitLab, so that's the only account you need a key for here.
{% else %}
Now generate the \index{Git!ssh keys} to use for authentication with your GitLab or GitHub account and configure your ssh settings to use these keys. 
{% endif %}

1. Follow the instructions below to generate a new SSH key pair and add it to your account. It's best practice to use a modern, secure `ed25519` key.

    <div class="grid cards one-column" markdown>
    
    -   :material-clock-fast:{ .lg .middle } __Generate SSH keys__

        === ":material-apple: macOS"

            1. Open the **Terminal** application.
{% if is_surrey %}
            2. Generate the key. Only the email address needs changing - the rest of the command is complete as written:

                ``` bash
                ssh-keygen -t ed25519 -C "your.email@example.com" -f ~/.ssh/id_ed25519_gitlab
                ```

            3. When prompted, type a strong passphrase.
{% else %}
            2. Generate the key for **GitHub**. Only the email address needs changing - the rest of the command is complete as written:

                ``` bash
                ssh-keygen -t ed25519 -C "your.github.email@example.com" -f ~/.ssh/id_ed25519_github
                ```

            3. Then generate a **separate** key for **GitLab**:

                ``` bash
                ssh-keygen -t ed25519 -C "your.gitlab.email@example.com" -f ~/.ssh/id_ed25519_gitlab
                ```

            4. When prompted, type a strong passphrase. You are asked once per key, so this happens twice.
{% endif %}

        === ":fontawesome-brands-windows: Windows"

            1. Open the **PowerShell** application.
            2. Create the `.ssh` folder, if it doesn't already exist:

                ``` powershell
                mkdir $env:USERPROFILE\.ssh -Force
                ```

{% if is_surrey %}
            3. Generate the key. Only the email address needs changing - the rest of the command is complete as written:

                ``` powershell
                ssh-keygen -t ed25519 -C "your.email@example.com" -f $env:USERPROFILE\.ssh\id_ed25519_gitlab
                ```

            4. When prompted, type a strong passphrase.
{% else %}
            3. Generate the key for **GitHub**. Only the email address needs changing - the rest of the command is complete as written:

                ``` powershell
                ssh-keygen -t ed25519 -C "your.github.email@example.com" -f $env:USERPROFILE\.ssh\id_ed25519_github
                ```

            4. Then generate a **separate** key for **GitLab**:

                ``` powershell
                ssh-keygen -t ed25519 -C "your.gitlab.email@example.com" -f $env:USERPROFILE\.ssh\id_ed25519_gitlab
                ```

            5. When prompted, type a strong passphrase. You are asked once per key, so this happens twice.
{% endif %}

        === ":material-linux: Linux (Ubuntu)"

            1. Open the **Terminal** application.
{% if is_surrey %}
            2. Generate the key. Only the email address needs changing - the rest of the command is complete as written:

                ``` bash
                ssh-keygen -t ed25519 -C "your.email@example.com" -f ~/.ssh/id_ed25519_gitlab
                ```

            3. When prompted, type a strong passphrase.
{% else %}
            2. Generate the key for **GitHub**. Only the email address needs changing - the rest of the command is complete as written:

                ``` bash
                ssh-keygen -t ed25519 -C "your.github.email@example.com" -f ~/.ssh/id_ed25519_github
                ```

            3. Then generate a **separate** key for **GitLab**:

                ``` bash
                ssh-keygen -t ed25519 -C "your.gitlab.email@example.com" -f ~/.ssh/id_ed25519_gitlab
                ```

            4. When prompted, type a strong passphrase. You are asked once per key, so this happens twice.
{% endif %}
    
    </div>

{% if is_surrey %}
    !!! tip "Also want a personal GitHub account?"
        Everything below is written for your one GitLab key. To add a GitHub account too - for personal projects, say - generate a second key the same way, naming it `id_ed25519_github` instead, then repeat each remaining step for it as well, adding a matching `Host github.com` entry to the ssh config below.
{% else %}
    !!! note "`gitxxx` in the steps that follow"
        You now have two key files, `id_ed25519_github` and
        `id_ed25519_gitlab`. The remaining steps are written once, with
        `gitxxx` standing for whichever of the two you are working on -
        so run them twice, substituting `github` and then `gitlab`.
{% endif %}

1. Then configure the SSH config file to use the correct key for each service.

    <div class="grid cards one-column" markdown>

    -   :material-clock-fast:{ .lg .middle } __Edit the SSH config file__

        === ":material-apple: macOS"

            Open the file in your preferred [text editor](shcommands.md#editing-files) (create it if it doesn't exist) - for example with `nano`:

            ```bash
            nano ~/.ssh/config
            ```

            Paste in the configuration below, then save and close (`Ctrl+O` to save, `Ctrl+X` to exit, in nano).

        === ":fontawesome-brands-windows: Windows"

            Create the file from PowerShell first, then open it - creating it directly inside an editor risks Notepad naming it `config.txt` instead of `config`:

            ``` powershell
            New-Item -ItemType File -Path $env:USERPROFILE\.ssh\config -Force
            code $env:USERPROFILE\.ssh\config
            ```

            (Use `notepad` in place of `code` if you'd rather not use VS Code.) Paste in the configuration below, then save.

            !!! warning "The file must be called `config`, with no extension"
                Notepad silently appends `.txt` unless you prevent it, and Windows hides known extensions in File Explorer, so `config.txt` looks identical to `config`. SSH reads only a file named exactly `config` - a misnamed one is ignored entirely, and `git clone` falls back to asking for a password that will never be accepted. Creating the file with `New-Item` first avoids this. To check, and fix it if needed:

                ``` powershell
                Get-ChildItem $env:USERPROFILE\.ssh
                Rename-Item $env:USERPROFILE\.ssh\config.txt config   # only if the first command lists config.txt
                ```

        === ":material-linux: Linux (Ubuntu)"

            Open the file in your preferred [text editor](shcommands.md#editing-files) (create it if it doesn't exist) - for example with `nano`:

            ```bash
            nano ~/.ssh/config
            ```

            Paste in the configuration below, then save and close (`Ctrl+O` to save, `Ctrl+X` to exit, in nano).

    </div>

    The configuration to paste in:

{% if is_surrey %}
    ```text
    # GitLab (University of Surrey)
    Host gitlab.surrey.ac.uk
        HostName gitlab.surrey.ac.uk
        User git
        IdentityFile ~/.ssh/id_ed25519_gitlab
        AddKeysToAgent yes

    # GitLab
    Host gitlab.com
        HostName gitlab.com
        User git
        IdentityFile ~/.ssh/id_ed25519_gitlab
        AddKeysToAgent yes
    ```
{% else %}
    ```text
    # GitLab
    Host gitlab.com
        HostName gitlab.com
        User git
        IdentityFile ~/.ssh/id_ed25519_gitlab
        AddKeysToAgent yes

    # GitHub
    Host github.com
        HostName github.com
        User git
        IdentityFile ~/.ssh/id_ed25519_github
        AddKeysToAgent yes
    ```
{% endif %}

    Make sure to replace the paths with the correct paths to your SSH keys if you used different names or locations. `AddKeysToAgent yes` is what makes the key-loading step below self-healing - without it, the key you add to the agent today is gone the next time the agent restarts (a reboot, a logout, on some setups just time), and SSH fails with a permission error that looks like a rejected key rather than a missing one, since the *public* half still authenticates fine and only the signing step - which needs the private half - actually fails.

    !!! tip "On macOS, add one more line"
        Add `UseKeychain yes` too, in each `Host` block above, so macOS can supply the passphrase from your login keychain instead of asking every time - paired with `--apple-use-keychain` on `ssh-add` below. This directive is Apple-specific: **don't** add it on Windows or Linux, where it isn't recognised and breaks every `ssh` command that reads this file with `Bad configuration option: usekeychain`.

{% if not is_surrey %}
    !!! tip
        Separate keys per account are safer, but if you reuse one, add its public key to each account separately in [Integrate Visual Studio Code with Git](#integrate-visual-studio-code-with-git) below.
{% endif %}

1. Set the correct permissions for the SSH config file and the private key(s) to ensure they're secure. If you are using macOS or Linux, run the following commands in your terminal{% if not is_surrey %}, substituting `gitxxx` and paths to your SSH keys if you used different names or locations{% endif %}:

{% if is_surrey %}
    ```bash
    chmod 600 ~/.ssh/config
    chmod 600 ~/.ssh/id_ed25519_gitlab
    ```
{% else %}
    ```bash
    chmod 600 ~/.ssh/config
    chmod 600 ~/.ssh/id_ed25519_gitxxx
    ```
{% endif %}

    Windows handles permissions differently and are normally set to only allow access to the user, but ensure that the private key(s) aren't accessible to other users.

1. You've set a passphrase for the SSH keys, so you'll need to enter it every time you use a key. To avoid this, you can use an SSH agent to cache your passphrase. Follow the instructions below to start the SSH agent and add your keys.

    <div class="grid cards one-column" markdown>
    
    -   :material-clock-fast:{ .lg .middle } __Adding SSH keys__

        === ":material-apple: macOS"

            1. macOS normally starts an SSH agent for you automatically. Add your SSH private key{% if not is_surrey %}s{% endif %} to it{% if not is_surrey %}, substituting `gitxxx` with either `github` or `gitlab` depending on which service you are adding the key for{% endif %} - `--apple-use-keychain` stores the passphrase in your login keychain, so the key survives a reboot instead of silently dropping out of the agent:

{% if is_surrey %}
                ``` bash
                ssh-add --apple-use-keychain ~/.ssh/id_ed25519_gitlab
                ```
{% else %}
                ``` bash
                ssh-add --apple-use-keychain ~/.ssh/id_ed25519_gitxxx
                ```
{% endif %}

                If this fails with an error about not being able to connect to the agent, start one first, then repeat the command above:

                ``` bash
                eval "$(ssh-agent -s)"
                ```

        === ":fontawesome-brands-windows: Windows"

            1. Set the SSH agent to start automatically with Windows, and then start it. Run these in a PowerShell window opened **as Administrator** (right-click the Start menu, or search for PowerShell, then select **Run as administrator**):

                ``` powershell
                Set-Service -Name ssh-agent -StartupType Automatic
                Start-Service ssh-agent
                ```

                !!! warning "Run in that order, in an Administrator window"
                    Windows ships this service **disabled**, so `Set-Service` has to take it out of that state before `Start-Service` has anything it's allowed to start - reversed, the first command fails with `Cannot start service ssh-agent`. Both commands also need elevation: an ordinary window fails with `Access is denied`, which then makes the second command fail too, for the same underlying reason.

                    An Administrator PowerShell opens in `C:\WINDOWS\system32` (an ordinary one opens in `C:\Users\yourname`), and its title bar says *Administrator*.

                Check it worked before moving on:

                ``` powershell
                Get-Service ssh-agent
                ```

                The **Status** column should read `Running`. If it still says `Stopped`, confirm the PowerShell window really is running as Administrator - the title bar says *Administrator* when it is.
            2. Back in your normal (non-administrator) PowerShell window, add your SSH private key{% if not is_surrey %}s{% endif %} to the agent{% if not is_surrey %}, substituting `gitxxx` with either `github` or `gitlab` depending on which service you are adding the key for{% endif %}:

{% if is_surrey %}
                ``` powershell
                ssh-add $env:USERPROFILE\.ssh\id_ed25519_gitlab
                ```
{% else %}
                ``` powershell
                ssh-add $env:USERPROFILE\.ssh\id_ed25519_gitxxx
                ```
{% endif %}

        === ":material-linux: Linux (Ubuntu)"

            1. Add your SSH private key{% if not is_surrey %}s{% endif %} to the running SSH agent{% if not is_surrey %}, substituting `gitxxx` with either `github` or `gitlab` depending on which service you are adding the key for{% endif %}:

{% if is_surrey %}
                ``` bash
                ssh-add ~/.ssh/id_ed25519_gitlab
                ```
{% else %}
                ``` bash
                ssh-add ~/.ssh/id_ed25519_gitxxx
                ```
{% endif %}

                Unlike macOS, Linux doesn't always start an SSH agent automatically. If the command above fails with an error about not being able to connect to the agent, start one first, then repeat the command above:

                ``` bash
                eval "$(ssh-agent -s)"
                ```
    </div>

1. Display your **public** key, so you can copy it - the next section needs it pasted into your {% if is_surrey %}GitLab account{% else %}GitLab and GitHub accounts{% endif %}. Only the public key goes there; never paste the private one (the file with no `.pub` extension).

    <div class="grid cards one-column" markdown>

    -   :material-clock-fast:{ .lg .middle } __Display the public key__

        === ":material-apple: macOS"

{% if is_surrey %}
            ``` bash
            cat ~/.ssh/id_ed25519_gitlab.pub
            ```
{% else %}
            ``` bash
            cat ~/.ssh/id_ed25519_gitxxx.pub
            ```
{% endif %}

        === ":fontawesome-brands-windows: Windows"

{% if is_surrey %}
            ``` powershell
            Get-Content $env:USERPROFILE\.ssh\id_ed25519_gitlab.pub
            ```
{% else %}
            ``` powershell
            Get-Content $env:USERPROFILE\.ssh\id_ed25519_gitxxx.pub
            ```
{% endif %}

        === ":material-linux: Linux (Ubuntu)"

{% if is_surrey %}
            ``` bash
            cat ~/.ssh/id_ed25519_gitlab.pub
            ```
{% else %}
            ``` bash
            cat ~/.ssh/id_ed25519_gitxxx.pub
            ```
{% endif %}

    </div>

    {% if is_surrey %}Select the entire line it prints - starting with `ssh-ed25519` and ending with the email address you gave it - and copy it.{% else %}Substitute `gitxxx` as before, and run it once for each key you generated. Select the entire line it prints - starting with `ssh-ed25519` and ending with the email address you gave it - and copy it.{% endif %}

### Integrate Visual Studio Code with Git

1. Now that you've generated your keys and finished the configuration, add {% if is_surrey %}it to your GitLab account{% else %}them to your GitHub and GitLab accounts{% endif %} using the instructions below.

    <div class="grid cards one-column" markdown>
    
    -   :material-clock-fast:{ .lg .middle } __Integrate Visual Studio Code with Git__

        === "GitLab"

            1. Log in to your **GitLab** account in a web browser.
            2. In the top-right corner, click on your **profile avatar** and select **Edit profile**.
            3. On the left-hand sidebar, select **Access > SSH Keys**.
            4. Click **Add new key**{: .bg-blue} and fill out the following details:
                * **Title:** Give it a clear name (e.g., VS Code Extension).
                * **Key:** Paste the contents of your public SSH key file (e.g., `~/.ssh/id_ed25519_gitlab.pub`).
                * **Expiration date:** GitLab fills this in for you, one year ahead, and
                  will not let you leave it empty. Set it well into the future - the end
                  of your course or project, say - or you will be locked out mid-way
                  through and have to generate and register a new key.
            5. Click **Add key**{: .bg-blue} to save the key.

            !!! warning "An expired key fails confusingly"
                When the date passes, `git push` and `git pull` stop working with a
                permission error that looks like a misconfigured key rather than an
                expired one. If pushing suddenly fails having worked for months, check
                this date first.
{% if not is_surrey %}
        === "GitHub"

            1. Log in to your **GitHub** account in a web browser.
            2. In the top-right corner, click on your **profile avatar** and select **Settings**.
            3. On the left-hand sidebar, select **SSH and GPG keys**.
            4. Click **New SSH key**{: .bg-green} and fill out the following details:
                * **Title:** Give it a clear name (e.g., VS Code Extension).
                * **Key:** Paste the contents of your public SSH key file (e.g., `~/.ssh/id_ed25519_github.pub`).
            5. Click **Add SSH key**{: .bg-green} to save the key.

            !!! note "No expiry date to set here"
                Unlike GitLab, GitHub SSH keys have no expiration field - the key
                stays valid until you delete it, so there is nothing to set.
{% endif %}
    </div>

{% if is_surrey %}
1. Test the SSH connection to GitLab to ensure that the key is working correctly. Run the following command in your terminal:

    ```bash
    ssh -T git@gitlab.surrey.ac.uk
    ```

    If successful, you will see a greeting like:

    ```text
    Welcome to GitLab, @username!
    ```
{% else %}
1. Test the SSH connection to GitHub and GitLab to ensure that the keys are working correctly. Run the following commands in your terminal:

    ```bash
    ssh -T git@gitxxx.com
    ```

    If successful, you will see greetings like:

    ```text
    Hi username! You've successfully authenticated, but GitHub does not provide shell access.
    Welcome to GitLab, @username!
    ```
{% endif %}

## Choose how to get the project {: #cloning-the-prodockit-template }

A **repository** is the project and its saved history. GitLab or GitHub keeps
the online copy; a **clone** is the working copy on your computer. Git calls
the online repository connected to a clone `origin`.

There are two different starting points. Choose one path and complete only
that path:

| Starting point | Path to follow |
| --- | --- |
| Your repository does not exist yet, or exists but is completely empty | [Path 1: start from the template](#manual-install-path-1) |
| Your repository already contains one or more commits | [Path 2: clone the existing repository](#manual-install-path-2) |

!!! warning "Do not replace the history of an existing repository"
    Path 1 starts a new history. Never use its history step on a repository
    that already contains work. Use Path 2 so every existing commit, branch,
    and file is preserved.

### Prepare a projects directory

Keep the project in a directory intended for Git repositories. The examples
use `GitLab`, but `GitHub` or `Projects` is equally suitable.

=== ":material-apple: macOS"

    ``` bash
    mkdir -p ~/GitLab
    cd ~/GitLab
    ```

=== ":fontawesome-brands-windows: Windows"

    ``` powershell
    New-Item -ItemType Directory -Force ~\GitLab | Out-Null
    cd ~\GitLab
    ```

=== ":material-linux: Linux (Ubuntu)"

    ``` bash
    mkdir -p ~/GitLab
    cd ~/GitLab
    ```

The `cd` command changes the current directory. The clone command creates the
project folder inside it.

### Path 1: start from the template {: #manual-install-path-1 }

Use this path when there is no repository for the project yet, or when you
have deliberately created an empty one. It copies the template files, starts
a clean history for your work, and connects that history to your own GitLab
or GitHub repository.

1. Create a **blank** repository on the service where the work will be kept.

    === "GitLab"

        On the GitLab website, select **New project > Create blank project**.
        Give it the required name, set its visibility to **Private**, and
        untick **Initialize repository with a README**.

    === "GitHub"

        On the GitHub website, select **New repository**. Give it the required
        name, set it to **Private**, and leave every **Initialize this
        repository with** option unticked.

    The repository must be empty because the template provides the README,
    licence, `.gitignore`, and first commit. Initialising any of those on the
    website creates a competing history before your files arrive.

1. Copy the repository's **SSH clone URL** from its web page and keep it for
    the `git remote add` command below. An SSH URL starts with `git@`.

1. Clone the template into a folder named after your project. Replace
    `report-az1234` with the exact repository name you chose.

{% if is_surrey %}
    ``` bash
    git clone git@gitlab.surrey.ac.uk:mb0105/prodockit-template.git report-az1234
    ```
{% else %}
    ``` bash
    git clone git@github.com:buckwem/prodockit-template.git report-az1234
    ```
{% endif %}

    `git clone` downloads both the files and the template's Git history. The
    second name tells Git what to call the new local folder.

1. Change into the project directory as a separate step:

    ``` bash
    cd report-az1234
    ```

1. Check which online repository the clone currently uses:

    ``` bash
    git remote -v
    ```

    Both lines should point to `prodockit-template`. Do not push while that
    is true: `origin` still means the template, not your repository.

1. Move the template's history to a recoverable backup, then start a new
    history. The files in the project are not moved or deleted.

    === ":material-apple: macOS"

        ``` bash
        mv .git ../.report-az1234.git.pdk-template-backup
        git init -b main
        git config core.fileMode false
        ```

    === ":fontawesome-brands-windows: Windows"

        ``` powershell
        Move-Item -LiteralPath .git -Destination ..\.report-az1234.git.pdk-template-backup
        git init -b main
        git config core.fileMode false
        ```

    === ":material-linux: Linux (Ubuntu)"

        ``` bash
        mv .git ../.report-az1234.git.pdk-template-backup
        git init -b main
        git config core.fileMode false
        ```

    !!! info "Why move `.git` instead of deleting it?"
        The hidden `.git` directory contains the template's history and its
        connection to the template repository. Moving it removes both from
        the active project, but the sibling backup remains available if you
        made a mistake. `git init` then creates a clean history owned by this
        project. `core.fileMode false` prevents file-permission changes made
        by Windows or cloud-sync software appearing as edits.

1. Connect the clean local history to your blank online repository. Use the
    SSH URL you copied earlier:

    === "University of Surrey GitLab"

        ``` bash
        git remote add origin git@gitlab.surrey.ac.uk:comm058-2026/report-az1234.git
        ```

    === "GitLab.com"

        ``` bash
        git remote add origin git@gitlab.com:your-namespace/report-az1234.git
        ```

    === "GitHub"

        ``` bash
        git remote add origin git@github.com:your-username/report-az1234.git
        ```

1. Run `git remote -v` again. Both lines must now show your repository, not
    `prodockit-template`:

    ``` bash
    git remote -v
    ```

    Do not commit or push yet. After the shared installation steps,
    `prodockit sync-repo` will replace the template's own links before your
    first commit is created.

### Path 2: clone the existing repository {: #manual-install-path-2 }

Use this path when the GitLab or GitHub repository already contains work. A
repository with a visible file list or any entry under **Commits** is not
empty. This path keeps its complete history and keeps `origin` pointing to
the same place.

1. Open the repository in GitLab or GitHub. Select **Code**, choose **SSH**,
    and copy the URL. Check the browser address and repository name carefully;
    similar project names can lead to cloning the wrong work without an error.

1. Clone that URL. For example:

    === "University of Surrey GitLab"

        ``` bash
        git clone git@gitlab.surrey.ac.uk:comm058-2026/report-az1234.git
        ```

    === "GitLab.com"

        ``` bash
        git clone git@gitlab.com:your-namespace/report-az1234.git
        ```

    === "GitHub"

        ``` bash
        git clone git@github.com:your-username/report-az1234.git
        ```

1. Change into the cloned project as a separate step:

    ``` bash
    cd report-az1234
    ```

1. Keep its history and configure this clone to ignore file-permission noise:

    ``` bash
    git config core.fileMode false
    ```

1. Confirm the clone is connected to the expected repository and has a
    commit:

    ``` bash
    git remote -v
    git log -1 --oneline
    git status --short
    ```

    `origin` should show the repository you copied. `git log` should show the
    latest saved change. `git status --short` should print nothing, meaning
    the new clone has no unsaved local changes.

You now have the project locally. The remaining sections are shared by both
paths and install everything needed to edit, build, and publish it.

### Confirm the commit identity for this project

Git records an author's name and email address with every commit. Set them
inside this repository so they do not depend on settings from another project:

``` bash
git config --local user.name "Your Name"
git config --local user.email "your.email@example.com"
```

Check what Git will use:

``` bash
git config --local user.name
git config --local user.email
```

Use the email address associated with the GitLab or GitHub account that owns
the repository.

## Install Python and Zensical

The instructions below install \index{Python}, the PDF system libraries, and
a project-specific Python virtual environment on macOS, Windows 11, and
Ubuntu. Refer to the [official Python installation
documentation](https://docs.python.org/3/using/) if you use another operating
system.

!!! tip "Automated machine setup"
    If prodockit is already installed, `prodockit bootstrap --apply` can inspect
    and carry out the same machine and project setup. In its service menu,
    University of Surrey GitLab is the default, followed by GitHub.com and
    GitLab.com. This page remains useful when you need to understand or perform
    each command yourself.

!!! Note
    You may need to use 'python3' and 'pip3' instead of 'python' and 'pip' depending on your system configuration.

The instructions below are for installing Python 3.12 or later. If you have an older version, please update to Python 3.12 or later.

1. Follow the instructions below to install Python, create a \index{Python!virtual environment}, and install Zensical inside it for your operating system.

    <div class="grid cards one-column" markdown>

    -   :material-clock-fast:{ .lg .middle } __Install Python, Zensical and prodockit__

        === ":material-apple: macOS"

            1. If you use the Homebrew package manager, run this command in your Terminal to install Python. If you don't have Homebrew installed, you can install it by following the instructions on the [Homebrew website](https://brew.sh/){target="_blank"}.

                ``` bash
                brew install python3
                ```

            2. Install \index{Pango}, which is not a Python package, so `pip` cannot install it for you:

                ``` bash
                brew install pango
                ```

            3. Install \index{Pandoc} at the version this project builds with. Homebrew always installs the newest release, which is why it is not used here - see [Which pandoc version](#which-pandoc-version) below:

                ``` bash
                curl -fsSL -o /tmp/pandoc.pkg "https://github.com/jgm/pandoc/releases/download/3.10.1/pandoc-3.10.1-arm64-macOS.pkg"
                sudo installer -pkg /tmp/pandoc.pkg -target /
                ```

                On an Intel Mac, use `pandoc-3.10.1-x86_64-macOS.pkg` instead.

                !!! info "Why Pango but a fixed Pandoc"
                    `prodockit pdf` shells out to `pandoc`, which hands the result to \index{WeasyPrint} to lay out the pages - and WeasyPrint draws text through Pango, so `pango` alone is enough (glib, HarfBuzz and fontconfig come along as its dependencies). Skipping either still looks fine right up until `prodockit pdf`, which then fails with `pandoc exited with status 43` - see [WeasyPrint cannot start (status 43)](startediting.md#startediting-pandoc-status-43) if that happens.

            4. Install the desktop font files this template's PDF uses by default - **Inter** and **JetBrains Mono**:

                ``` bash
                brew install --cask font-inter font-jetbrains-mono
                ```

                !!! info "Why this early"
                    The website loads its fonts from a CDN at view time, but the PDF has no such fallback - WeasyPrint has to embed the actual font files, and silently substitutes a fallback font instead of erroring if they are missing. See [Fonts](customisebuild.md#customisebuild-fonts) for the full picture, including how to check the right fonts actually made it into a built PDF.

            5. Open **Terminal** in your project folder and create the virtual
               environment:

                ``` bash
                /opt/homebrew/bin/python3 -m venv .venv
                ```

                Then activate it as a separate step:

                ``` bash
                source .venv/bin/activate
                ```

                Your prompt gains a `(.venv)` prefix, which is how you know the
                virtual environment is active:

                ``` text
                (.venv) yourname@Mac your-project %
                ```

                It disappears when you close the terminal, and every new one
                needs activating again - or let VS Code do it, which the
                [Python extension](#install-zensical-studio-and-other-plugins)
                below handles for you.

                !!! note "Why the full path to Python"
                    macOS ships its own older Python, and a plain `python3` may well find that one instead of Homebrew's. Naming `/opt/homebrew/bin/python3` explicitly builds the virtual environment from the version you just installed. On an Intel Mac, Homebrew installs to `/usr/local` instead, so use `/usr/local/bin/python3`.

        === ":fontawesome-brands-windows: Windows"

            1. Download and run the **Windows installer (64-bit)** from [python.org](https://www.python.org/downloads/){target="_blank"}. Use this x86-64 installer on an ARM Windows virtual machine too; Windows runs it through its x64 compatibility layer, and it then matches the UCRT64 graphics libraries installed below.

                !!! Critical "Three things to get right during install"
                    - Check **Add python.exe to PATH** on the first screen. This is what lets you run `python` from the command line at all, and also puts `pip` and every command it installs on your `PATH`.
                    - Once installation finishes, a final screen offers **Disable path length limit** - click it. Windows historically caps a full file path at 260 characters, and this project's own dependencies nest deep enough (`.venv\Lib\site-packages\...`, `tools\mermaid\node_modules\...`) to hit that limit without it.
                    - Make sure you are running the installer you just downloaded, not Windows' own placeholder. Typing `python` in a terminal with no real Python installed opens the Microsoft Store instead of running anything - if that still happens *after* installing, search **Manage app execution aliases** and turn off the **App Installer** entries for `python.exe`/`python3.exe`, which take priority over the one you just installed.

            2. Next install pandoc, which is not a Python package, so `pip` cannot install it for you. Open **PowerShell** and run the following command:

                ``` powershell
                winget install --id JohnMacFarlane.Pandoc --version 3.10.1
                ```

                !!! note "The package is under its author's name, not `Pandoc`"
                    winget identifies packages as `Publisher.Package`, and
                    Pandoc's publisher is its author, John MacFarlane. There
                    is no `Pandoc.Pandoc`, so guessing that gives:

                    ``` text
                    No package found matching input criteria.
                    ```

                    `winget search pandoc` lists the real identifier if you
                    ever need to check it.

            3. Install the graphics libraries \index{WeasyPrint} needs. Pandoc hands your document to WeasyPrint to lay out the pages, and WeasyPrint is not pure Python - it draws text through \index{Pango}, which on Windows comes from \index{MSYS2}. Install MSYS2 first:

                ``` powershell
                winget install --id MSYS2.MSYS2
                ```

                Install the matching UCRT64 Pango package from PowerShell:

                ``` powershell
                C:\msys64\usr\bin\bash.exe -lc "pacman -S --noconfirm --needed mingw-w64-ucrt-x86_64-pango"
                ```

                If that fails partway through with a download error, run it
                again. MSYS2 selects mirrors automatically, and a temporary
                mirror failure does not mean the package name is wrong.

                Tell WeasyPrint where those libraries are, both in this
                PowerShell window and in future ones:

                ``` powershell
                $MsysBin = "C:\msys64\ucrt64\bin"
                $env:WEASYPRINT_DLL_DIRECTORIES = $MsysBin
                [Environment]::SetEnvironmentVariable("WEASYPRINT_DLL_DIRECTORIES", $MsysBin, "User")

                $env:Path = "$env:Path;$MsysBin"
                $UserPath = [Environment]::GetEnvironmentVariable("Path", "User")
                if (($UserPath -split ";") -notcontains $MsysBin) {
                    [Environment]::SetEnvironmentVariable("Path", "$UserPath;$MsysBin", "User")
                }
                ```

                The first two assignments make the current installation run
                work immediately. The user-level settings make new terminals
                and VS Code find the same libraries later.

                !!! warning "Python and the DLLs must have the same architecture"
                    Error `0xc1` means Windows found a DLL built for a different
                    processor. The verified route on both Intel/AMD Windows and
                    Windows on ARM is the **Windows installer (64-bit)** for
                    Python together with MSYS2's `ucrt64` package above. Do not
                    mix that Python with `clangarm64` DLLs.

                !!! info "Why this is needed"
                    That folder is where WeasyPrint finds `libgobject-2.0-0.dll`, `libpango-1.0-0.dll`, `libharfbuzz-0.dll` and `libfontconfig-1.dll` - installing `pango` brings all four in. Skipping this still looks fine until `prodockit pdf`, which then fails with `pandoc exited with status 43` - see [WeasyPrint cannot start (status 43)](startediting.md#startediting-pandoc-status-43) if that happens.

            4. Install the desktop font files this template's PDF uses by default - **Inter** and **JetBrains Mono**. Download the desktop (`.ttf`/`.otf`) files for each - [Inter](https://fonts.google.com/specimen/Inter){target="_blank"}, [JetBrains Mono](https://fonts.google.com/specimen/JetBrains+Mono){target="_blank"} - then select them all, right-click, and choose **Install for all users**.

                !!! info "Why this early"
                    The website loads its fonts from a CDN at view time, but the PDF has no such fallback - WeasyPrint has to embed the actual font files, and silently substitutes a fallback font instead of erroring if they are missing. See [Fonts](customisebuild.md#customisebuild-fonts) for the full picture, including why a `.woff`/`.woff2` download will not do, and how to check the right fonts actually made it into a built PDF.

            5. Allow PowerShell to run scripts. Windows blocks all of them by default, and activating a virtual environment *is* a script, so this has to be done once before the next step will work:

                ``` powershell
                Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
                ```

                Depending on your PowerShell version it may ask you to confirm the change; answer `Y` if it does. Often it simply returns to the prompt, which means it worked.

                !!! info "What this changes"
                    Without it, activating the venv fails with `... cannot be loaded because running scripts is disabled on this system`. `RemoteSigned` allows locally-written scripts while still requiring signed ones from the internet; `-Scope CurrentUser` limits that to your account, so it needs no Administrator window and is a one-time, per-account change.

                    Would rather not change it at all? Use **classic CMD** instead of PowerShell and run `.\.venv\Scripts\activate.bat` in the next step - `.bat` files aren't covered by execution policy.

            6. Change into your project folder:

                ``` powershell
                cd C:\path\to\your-project
                ```

                !!! warning "Check where you are first"
                    The steps above will have moved you. The SSH agent needed an
                    Administrator window, which opens in `C:\WINDOWS\system32`, and
                    every "close and reopen PowerShell" leaves you in your home
                    directory, `C:\Users\yourname`.

                    `python -m venv .venv` does not object to either. It creates a
                    perfectly good virtual environment in the wrong place, and the
                    mistake only shows up a step later when `pip install -r
                    requirements.txt` cannot find a file that is sitting in your
                    project folder all along.

                    `pwd` prints where you are.

                Create the virtual environment:

                ``` powershell
                python -m venv .venv
                ```

                Then activate it as a separate step. Use the command matching
                your terminal:

                === "PowerShell"

                    ``` powershell
                    .\.venv\Scripts\Activate.ps1
                    ```

                === "Classic CMD"

                    ``` batch
                    .\.venv\Scripts\activate.bat
                    ```

                Your prompt gains a `(.venv)` prefix, which is how you know the
                virtual environment is active:

                ``` text
                (.venv) PS C:\path\to\your-project>
                ```

                It disappears when you close the terminal, and every new one
                needs activating again - or let VS Code do it, which the
                [Python extension](#install-zensical-studio-and-other-plugins)
                below handles for you.

        === ":material-linux: Linux (Ubuntu)"

            1. Open a terminal and run the following command to install Python, the `venv` module, pandoc, the graphics libraries \index{WeasyPrint} needs, and the fonts this template's PDF uses by default. None of these is a Python package, so `pip` cannot install them for you:

                ``` bash
                sudo apt update
                sudo apt install python3 python3-venv python3-pip curl \
                  libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0 \
                  fonts-inter fonts-jetbrains-mono
                ```

                Ubuntu's own `pandoc` package is several major versions behind, far enough to change how the PDF renders, so install the pinned release directly - see [Which pandoc version](#which-pandoc-version) below. This picks the `amd64` or `arm64` package to match your CPU, so it also works on Ubuntu running under an Apple Silicon Mac:

                ``` bash
                curl -fsSL -o /tmp/pandoc.deb "https://github.com/jgm/pandoc/releases/download/3.10.1/pandoc-3.10.1-1-$(dpkg --print-architecture).deb"
                sudo apt install -y /tmp/pandoc.deb
                ```

                !!! info "Why the three library packages"
                    Pandoc hands the result to WeasyPrint, which draws text through \index{Pango} and won't start without it. `libharfbuzz-subset0` is easy to miss - on Debian it's a *separate* package from `libharfbuzz0b`, and WeasyPrint needs this one specifically (glib and fontconfig aren't listed, since `libpango-1.0-0` already depends on them). Skipping this still looks fine until `prodockit pdf`, which then fails with `pandoc exited with status 43` - see [WeasyPrint cannot start (status 43)](startediting.md#startediting-pandoc-status-43) if that happens.

                !!! warning "Debian 12 or Ubuntu 22.04 and newer"
                    `libharfbuzz-subset0` does not exist on older releases. On those, upgrade the distribution rather than hunting for a substitute package.

                !!! info "Why the fonts, this early"
                    The website loads its fonts from a CDN at view time, but the PDF has no such fallback - WeasyPrint has to embed the actual font files, and silently substitutes a fallback font instead of erroring if they are missing. Skipping this still looks fine right up until your first `prodockit pdf`, whose test suite (if you run one - see [Testing](testing.md)) then fails with `No 'Inter' font found anywhere in the compiled PDF`. See [Fonts](customisebuild.md#customisebuild-fonts) for the full picture, including how to check the right fonts actually made it into a built PDF.

            2. Navigate to your project folder, then create a virtual
               environment:

                ``` bash
                python3 -m venv .venv
                ```

                Activate it as a separate step:

                ``` bash
                source .venv/bin/activate
                ```

                Your prompt gains a `(.venv)` prefix, which is how you know the
                virtual environment is active:

                ``` text
                (.venv) yourname@host:~/your-project$
                ```

                It disappears when you close the terminal, and every new one
                needs activating again - or let VS Code do it, which the
                [Python extension](#install-zensical-studio-and-other-plugins)
                below handles for you.
    </div>

    ### Which pandoc version {: #which-pandoc-version }

    Every command above installs pandoc **3.10.1** specifically, rather than
    whatever your package manager considers current. This project is built
    and tested against that version, and pandoc is not always compatible
    with itself across releases: 3.10 changed how it reads highlighted code
    in HTML, in a way that broke every fenced code block in the PDF while
    the build still reported success - see [Pandoc version
    drift](https://prodockit.org/devcons/continuous-integration/#ci-pandoc-version){target="_blank"}
    for what that looked like.

    Confirm which version you actually have:

    ``` bash
    pandoc --version
    ```

    The first line should read `pandoc 3.10.1`. If it doesn't - a
    Homebrew upgrade, a distribution update, or `winget upgrade` run
    without thinking about it will all move this - repeat the pandoc
    install step above for your platform to bring it back.

1. Install Zensical and prodockit inside the active virtual environment. The
    `requirements.txt` file lists the required packages, so install them with
    the environment's own Python:

    ``` bash
    python -m pip install -r requirements.txt
    ```

1. Check that the `prodockit` command actually resolves to the one you just installed:

    ``` bash
    prodockit --version
    ```

    `pip` exiting without an error only means the package landed in `.venv` - it doesn't prove your shell finds it there first. An older, separately-installed `prodockit` earlier on your `PATH` shadows it silently, and every command in this guide from here on would run against that instead.

1. Check that WeasyPrint can find its graphics libraries. This is the one part of the setup `pip` cannot verify for you, so it is worth confirming now rather than at your first PDF build:

    ``` bash
    python -c "import weasyprint; print(weasyprint.__version__)"
    ```

    A version number means everything is in place. If instead you get a long error ending in `cannot load library`, the libraries from the step above are missing or cannot be found - go back and install them.

1. Fetch the citation style your first build needs. The template enables `prodockit.bibliography` by default, pointing `csl_style` at `harvard-cite-them-right.csl` - but that file isn't part of the clone, so `zensical serve`/`zensical build`/`prodockit pdf` all fail outright until it's in place. Fetch it once, from your project root:

    <div class="grid cards one-column" markdown>

    -   :material-clock-fast:{ .lg .middle } __Fetch the citation style__

        === ":material-apple: macOS"

            ``` bash
            curl -fsSL -o harvard-cite-them-right.csl "https://www.zotero.org/styles/harvard-cite-them-right"
            ```

        === ":fontawesome-brands-windows: Windows"

            ``` powershell
            Invoke-WebRequest -Uri "https://www.zotero.org/styles/harvard-cite-them-right" -OutFile harvard-cite-them-right.csl
            ```

        === ":material-linux: Linux (Ubuntu)"

            ``` bash
            curl -fsSL -o harvard-cite-them-right.csl "https://www.zotero.org/styles/harvard-cite-them-right"
            ```

    </div>

    See [An alternative: prodockit.bibliography](customisecontent.md#an-alternative-prodockitbibliography) for what this feature does, and how to fetch a different CSL style instead.

1. Check the repository's own links against `origin`:

    ``` bash
    prodockit sync-repo --check
    ```

    Path 1 still contains the template's repository name, so the check will
    report the changes it needs. Apply them:

    ``` bash
    prodockit sync-repo
    ```

    It reports what it changed, for example:

    ``` text
    Detected GitLab remote (https://gitlab.surrey.ac.uk/az1234/report-az1234); updated: repo_url, repo_name, theme.icon.repo, README badges
    ```

    This rewrites `repo_url`, `repo_name`, `theme.icon.repo` and `edit_uri` in `zensical.toml`, plus the badge row in your `README.md`, to match the `origin` you just set - so your built site and PDF link to your own repository rather than the template's. Note `theme.icon.repo` in that list: moving from a GitHub template to a GitLab project switches the header's brand icon to match, which is easy to miss by hand. Only the values that actually needed changing are listed, so the set you see may be smaller.

    On Path 2, the check should normally report that everything already
    matches. If it reports changes, first confirm `git remote -v` shows the
    correct repository. Then run `prodockit sync-repo` to apply them.

    !!! tip "Check it any time"
        `prodockit sync-repo --check` writes nothing and exits non-zero if these have drifted
        from your remote - useful after any later change of host. See
        [Checks worth having](customisebuild.md#customisebuild-checks).

### Install Zensical Studio and other plugins

Now we'll install the \index{VS Code!Zensical Studio} plugin for Visual Studio Code, which provides a set of tools to help you work with Zensical projects, including commands to build and preview your site. Then we'll install a couple of other useful plugins for working with Markdown and TOML files.

1. Start by opening Visual Studio Code and navigating to the Extensions view by clicking on the Extensions icon in the Activity Bar on the side of the window or pressing `Ctrl+Shift+X`/`Cmd+Shift+X`.
1. Install the **Python** extension (published by Microsoft) by searching for "Python" in the Extensions view and clicking **Install**{: .bg-blue}. As well as Python support, this is what makes VS Code notice the `.venv` folder in your project and activate the virtual environment automatically in every new Terminal in VS Code - so you don't have to run `source .venv/bin/activate` by hand each time you open one.

    !!! Tip
        Check it worked by opening a new terminal (**Terminal > New Terminal**) - the prompt should start with `(.venv)`. If it doesn't, reopen VS Code in the project folder, then choose **Python: Select Interpreter** from the Command Palette (`Ctrl+Shift+P`/`Cmd+Shift+P`) and pick the one inside `.venv`.

1. Install the **Zensical Studio** extension by searching for "Zensical Studio" in the Extensions view and clicking **Install**{: .bg-blue} and then **Trust Publisher and Install**{: .bg-blue} when prompted. This extension provides a set of tools to help you work with Zensical projects, including commands to build and preview your site.
1. Follow the instructions on the Zensical Studio extension page to configure
    it. The current template already contains the required setting. If an
    older repository does not, add this to `.vscode/settings.json`:

    ```json
    {
      "files.associations": {
        "*.md": "python-markdown"
      }
    }
    ```

1. Install the **Even Better TOML** extension for Visual Studio Code by searching for "Even Better TOML" in the Extensions view and clicking **Install**{: .bg-blue} and then **Trust Publisher and Install**{: .bg-blue} when prompted. This extension provides syntax highlighting and other features for working with TOML files, which are used for configuration in Zensical projects.
1. Install the **LTeX+ – LanguageTool grammar/spell checking** plugin for Visual Studio Code by searching for "LTeX+" in the Extensions view and clicking **Install**{: .bg-blue} and then **Trust Publisher and Install**{: .bg-blue} to enable spelling and grammar checking for Markdown. Configure the plugin's *language* setting to whichever English (or other language LTeX+ supports) you're actually writing in{% if is_surrey %} - `en-GB` for British English, which is what Surrey coursework expects{% endif %}.

    !!! warning "Get this right, or corrections are confidently wrong"
        Set to the wrong variety, LTeX+ still checks every sentence - it just checks it against the wrong rules, and offers "corrections" for perfectly correct spelling and phrasing in the variety you're actually using. That's worse than no checking at all, since a wrong suggestion looks exactly as confident as a right one.

There are many other extensions available for Visual Studio Code that can help you with your documentation. You can explore the [Visual Studio Code Marketplace](https://marketplace.visualstudio.com/vscode){target="_blank"} to find more extensions that suit your needs.

## Install the diagram and maths tooling

Two things your document can contain - \index{Zensical!diagrams} and mathematical notation - need tooling that none of the steps so far has installed.

On the website they look after themselves: the reader's browser draws them as the page loads. A PDF has no browser, so `prodockit pdf` converts both into images *before* building the document, using two \index{Node.js} programs to do it.

!!! danger "Without these, the PDF is wrong rather than missing"
    `prodockit pdf` does **not** fail when they are absent. It leaves the content as it found it, so instead of a flowchart your PDF shows the diagram's own definition text - the `graph LR` line and every node written out beneath it - and instead of a typeset equation, raw LaTeX with all its backslashes and braces.

    Meanwhile the website renders both perfectly. So nothing looks wrong until somebody opens the PDF, which may be well after you have written the document.

### Install Node.js

The two tools are Node.js programs, so install Node.js first. Version 22 or newer - that is what the automated builds use.

<div class="grid cards one-column" markdown>

-   :material-clock-fast:{ .lg .middle } __Install Node.js__

    === ":material-apple: macOS"

        ``` bash
        brew install node
        ```

    === ":fontawesome-brands-windows: Windows"

        ``` powershell
        winget install OpenJS.NodeJS.LTS
        ```

        Close and reopen PowerShell afterwards, so it picks up the new
        `PATH`. The new window starts in your home directory. First change
        back to the project:

        ``` powershell
        cd C:\path\to\your-project
        ```

        Then activate its virtual environment as a separate step:

        ``` powershell
        .\.venv\Scripts\Activate.ps1
        ```

        Check the prompt starts with `(.venv)` again. The next step's `npm ci` commands are relative to your project folder, and every `prodockit` command after it lives inside the virtual environment - outside it, PowerShell reports `The term 'prodockit' is not recognized`.

    === ":material-linux: Linux (Ubuntu)"

        Ubuntu's own `nodejs` package is often several versions behind. Use NodeSource's repository to get a current release:

        ``` bash
        sudo apt update
        sudo apt install -y curl

        curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
        sudo apt install -y nodejs
        ```

        !!! warning "Don't skip the `curl` line"
            A clean Ubuntu install does not necessarily have `curl`. Without it the first command fails with `Command 'curl' not found` - and the failure does not stop there, because the `apt install` on the next line still **succeeds**, quietly fitting Ubuntu's own older Node.js instead of NodeSource's.

            You then have a `node` that looks installed but no `npm` at all, and the toolchain commands in the next section fail for what appears to be an unrelated reason. If you have already hit this, install `curl` and run the two NodeSource lines again - the correct package replaces the wrong one.

</div>

Check it worked - **both** commands, not just the first:

``` bash
node --version
npm --version
```

You should get two version numbers, with `node` at 22 or above:

``` text
v22.14.0
10.9.2
```

!!! failure "`node` answers but `npm` is not found"
    That is the signature of the NodeSource step not having run - the most likely cause on Linux being the missing `curl` described above. Node came from your distribution's own package instead, which does not always bring `npm` with it.

    Fix the earlier step and run it again rather than installing `npm` separately, so both come from the same source and stay in step.

### Install the two toolchains

Your cloned template already contains the manifests and lockfiles for both tools, in `tools/mermaid` and `tools/mathjax` - so you only need to install them.

If you're on Linux, install a native Chromium and point Puppeteer at it **before** running `npm ci` below, rather than letting `tools/mermaid`'s own `npm ci` download one for you - Puppeteer's download is not guaranteed to match your CPU's architecture. This matters most on ARM64 machines (an Apple Silicon Linux VM, an AWS Graviton instance, a Raspberry Pi), where `npm ci` would otherwise silently fetch an x86_64 Chrome build it can never run, but it costs nothing to do on any Ubuntu install:

``` bash
sudo apt update
sudo apt install -y chromium-browser
which chromium-browser || which chromium
```

The second command should print a path such as `/usr/bin/chromium-browser` or `/usr/bin/chromium` - that's what the next step needs. Point Puppeteer at it, and skip its own download entirely, for this session, then make both permanent so every future session picks them up too:

``` bash
export PUPPETEER_EXECUTABLE_PATH=$(which chromium-browser || which chromium)
export PUPPETEER_SKIP_DOWNLOAD=true
echo 'export PUPPETEER_EXECUTABLE_PATH=$(which chromium-browser || which chromium)' >> ~/.bashrc
echo 'export PUPPETEER_SKIP_DOWNLOAD=true' >> ~/.bashrc
source ~/.bashrc
```

If you opened a new terminal, change back to the project first - the
`--prefix` paths below are relative to wherever you run them from:

``` bash
cd path/to/your-project
```

Then activate the project's virtual environment as a separate step:

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

Then install both:

``` bash
npm ci --prefix tools/mermaid
npm ci --prefix tools/mathjax
```

`npm ci` installs the exact versions recorded in each lockfile, which is what the automated builds use too - so your PDF is rendered by the same versions as the published one.

This creates a `node_modules` folder inside each, which is deliberately not committed (see `.gitignore`). Run these two commands again if you ever re-clone the project.

Install the MathJax bundle and its matching configuration for the website:

``` bash
prodockit init-mathjax
```

This copies the pinned browser bundle from `tools/mathjax` and writes the
configuration before the bundle is loaded. Without that configuration, a
successful website build can still display raw TeX. The generated files are
deliberately excluded from Git, so run this command again after cloning the
project onto another computer.

!!! note "If npm reports vulnerabilities or an `allow-scripts` warning"
    Both are normal here, not a sign anything went wrong:

    ``` text
    Run `npm audit` for details.
    npm warn allow-scripts 1 package has install scripts not yet covered by allowScripts:
    npm warn allow-scripts   puppeteer@25.3.0 (postinstall: node install.mjs)
    ```

    The vulnerability count comes from `npm audit` scanning the whole dependency tree Puppeteer pulls in for known advisories, most of which don't apply to how this project uses it - a locally-run PDF build, not a public-facing server. There's nothing to fix here; running `npm audit fix` is more likely to break the pinned versions the lockfile records than to help.

    The `allow-scripts` warning is different: recent npm versions skip Puppeteer's own setup step, which downloads the headless browser Mermaid draws diagrams with. The install still succeeds - if a later PDF build reports it cannot find a browser, approve the step and reinstall:

    ``` bash
    npm approve-scripts puppeteer --prefix tools/mermaid
    npm ci --prefix tools/mermaid
    ```

!!! tip "Starting a project that isn't from the template?"
    Then you have no `tools/` directory to install from, and need `prodockit init-tools` first to create it. Running it on a copy of the template is harmless but pointless - it will just report `Kept existing tools/mermaid/package.json` for each file it finds. See [Diagrams and maths](customisebuild.md#customisebuild-diagrams-and-maths) for the full picture.

## Build and finish the setup

Build the website and PDF before publishing anything:

``` bash
zensical build --clean
prodockit pdf
```

Open both outputs and check that headings, diagrams, mathematics, tables, and
references render correctly. A command completing successfully cannot detect
every visual problem.

### Finish Path 1: make and push the first commit

Path 1 has a new local history and an empty online repository. Check exactly
what the first commit will contain:

``` bash
git status --short
```

Generated dependencies such as `.venv`, `node_modules`, and the installed
MathJax bundle should not appear because `.gitignore` excludes them. Then save
the project and send it to `origin`:

``` bash
git add -A
git commit -m "Initial commit"
git push -u origin main
```

`git commit` saves the first version locally. `git push` copies that commit to
GitLab or GitHub and `-u origin main` records where later pushes should go.

### Finish Path 2: leave existing work unchanged

Installing local dependencies should not alter an existing repository. Check:

``` bash
git status --short
git rev-parse HEAD
git rev-parse origin/main
```

An empty status means no project files changed. Matching commit identifiers
mean the local `main` branch is still at the same saved version as the online
one. Do not create an "initial" commit and do not force-push an existing
repository.

If `prodockit sync-repo` or an editor setting made an intentional change,
review it with `git diff` and follow the normal editing workflow in the next
section rather than replacing the repository's history.

## Where to go next {: #installtooling-where-to-go-next }

You now have Visual Studio Code, Git, Zensical and the diagram and maths
tooling installed, and the correct project repository cloned locally.
Continue to [Start editing](startediting.md) to preview changes and use Git
without replacing work that is already saved.
