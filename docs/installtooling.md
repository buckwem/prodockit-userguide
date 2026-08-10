---
icon: lucide/book-open 
---

<!-- 
Copyright (c) 2025-2026 Mark Buckwell and contributors
SPDX-License-Identifier: MIT
-->

{{ heading_counter_reset(page) }}

# Install tooling

This section takes you through the core installation steps for the tools needed to author your document as a static website and PDF file. The instructions are for macOS, Windows 11, and Linux (Ubuntu/Debian). If you are using a different operating system, please refer to the official documentation for that operating system.

<div class="web-only" markdown>
!!! Tip
    The screenshots below may have small text on your screen but you can click on an image to enlarge it. The glightbox viewer will open the image in a new tab and you can zoom in to see the details.
</div>

The install and configuration starts with the setup of Visual Studio Code.

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

    # GitLab
    Host gitlab.com
        HostName gitlab.com
        User git
        IdentityFile ~/.ssh/id_ed25519_gitlab
    ```
{% else %}
    ```text
    # GitLab
    Host gitlab.com
        HostName gitlab.com
        User git
        IdentityFile ~/.ssh/id_ed25519_gitlab

    # GitHub
    Host github.com
        HostName github.com
        User git
        IdentityFile ~/.ssh/id_ed25519_github
    ```
{% endif %}

    Make sure to replace the paths with the correct paths to your SSH keys if you used different names or locations.

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

            1. macOS normally starts an SSH agent for you automatically. Add your SSH private key{% if not is_surrey %}s{% endif %} to it{% if not is_surrey %}, substituting `gitxxx` with either `github` or `gitlab` depending on which service you are adding the key for{% endif %}:

{% if is_surrey %}
                ``` bash
                ssh-add ~/.ssh/id_ed25519_gitlab
                ```
{% else %}
                ``` bash
                ssh-add ~/.ssh/id_ed25519_gitxxx
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

## Cloning the prodockit-template

Cloning the documentation template creates a local copy of the template on your computer. You will then be able to edit the template locally in Visual Studio Code and publish your own documentation website.

{% if is_surrey %}
!!! Note "University of Surrey GitLab"
    You will be working with a repo that has been created for you, which you will clone down to your local device and push updates to ongoing.
{% endif %}

### Clone the prodockit-template

Start by cloning the template into your own local device.

1. If you don't have a directory for your git repositories, create one for all your *GitLab* or *GitHub* projects on your local desktop. For example, create a directory called 'GitLab' in your home directory.

1. Open a terminal (Terminal on macOS/Debian, Git Bash or PowerShell on Windows 11) and navigate to the directory you created in the previous step.

1. Then run the following command to clone the documentation template into your local directory. Use whichever tab matches the host you use.

    <div class="grid cards one-column" markdown>

    -   :material-clock-fast:{ .lg .middle } __Clone the template__

        === "GitLab"

{% if is_surrey %}
            If you have been given a repository to work on, clone that instead of the template. For example, if your tutor has given you a repository called `report-az1234` in the namespace `comm058-2026`, run the following command:

            ``` bash
            git clone git@gitlab.surrey.ac.uk:comm058-2026/report-az1234.git
            ```

            If you have not been given a repository, clone the University of Surrey copy of the template:

            ``` bash
            git clone git@gitlab.surrey.ac.uk:mb0105/prodockit-template.git
            ```

{% else %}
            ``` bash
            git clone git@github.com:buckwem/prodockit-template.git
            ```

            The template itself lives on GitHub, so that is where you clone it from even if you intend to publish to GitLab.
{% endif %}

        === "GitHub"

            ``` bash
            git clone git@github.com:buckwem/prodockit-template.git
            ```

    </div>

    !!! Tip
        You can find your `username` by logging into your GitLab or GitHub account and clicking on your profile picture at the top right corner of the page. On **GitLab** your username is **below** your name in the dropdown menu. On **GitHub** your username is **above** your name in the dropdown menu.

### Point your clone at your own repository

If you have cloned a repository that has been given to you to work on and is not a direct copy of the template, you can skip this section.

Cloning gives you the template's *files*, but the clone still points at the template's *repository*. Push now and Git will try to write to the template itself, which you almost certainly cannot do - and would not want to if you could. This section repoints it at a repository of your own.

1. Rename the directory to something meaningful for your own report. Cloning leaves you with a folder called `prodockit-template`, which says nothing about whose work it holds - and if you clone a second project later, you will not be able to tell them apart.

    <div class="grid cards one-column" markdown>

    -   :material-clock-fast:{ .lg .middle } __Rename the project folder__

        === ":material-apple: macOS"

            ``` bash
            mv prodockit-template report-az1234
            ```

        === ":fontawesome-brands-windows: Windows"

            ``` powershell
            Rename-Item prodockit-template report-az1234
            ```

        === ":material-linux: Linux (Ubuntu)"

            ``` bash
            mv prodockit-template report-az1234
            ```

    </div>

    Replace `report-az1234` with a name that identifies your own work - your username, your coursework code, or whatever your course tutor specifies.

    !!! note "Renaming the folder doesn't rename the repository"
        This changes only the folder on your own machine. The project's name on GitLab or GitHub is unaffected, and so is the `origin` remote inside it - `git push` and `git pull` carry on working exactly as before.

1. Check what your clone currently points at:

    <div class="grid cards one-column" markdown>

    -   :material-clock-fast:{ .lg .middle } __Check the current remote__

        === ":material-apple: macOS"

            ``` bash
            cd report-az1234
            git remote -v
            ```

        === ":fontawesome-brands-windows: Windows"

            ``` powershell
            cd report-az1234
            git remote -v
            ```

        === ":material-linux: Linux (Ubuntu)"

            ``` bash
            cd report-az1234
            git remote -v
            ```

    </div>

    A fresh clone has exactly one remote, `origin`, pointing at the template:

    ``` text
    origin  git@github.com:buckwem/prodockit-template.git (fetch)
    origin  git@github.com:buckwem/prodockit-template.git (push)
    ```

    ``` mermaid
    graph LR
      L[Your local clone] -->|origin| T[prodockit-template]
    ```
    /// figure-caption
    Right after cloning: `origin` points at the template
    ///

    If you added any others of your own - a `gitlab` mirror, say - they will be listed here too. You do not need to remove any of them by hand: the next step deletes the repository's entire `.git` directory, which takes every remote with it.

1. Start with a fresh commit history. This is your own independent project, so carrying the template's entire commit log and branches from the template into it serves little purpose.

    <div class="grid cards one-column" markdown>

    -   :material-clock-fast:{ .lg .middle } __Reset the repository history__

        === ":material-apple: macOS"

            ``` bash
            rm -rf .git
            git init -b main
            git config core.fileMode false
            ```

            !!! danger "`rm -rf .git` cannot be undone"
                This permanently deletes the repository's history from your machine - every commit, branch and tag. There is no undo, and nothing to recover from, because the deleted history is the thing that would have recovered it. Make sure you are in the right directory (`pwd`) and that you have pushed anything you care about somewhere else first.

        === ":fontawesome-brands-windows: Windows"

            ``` powershell
            Remove-Item -Recurse -Force .git
            git init -b main
            git config core.fileMode false
            ```

            !!! danger "`Remove-Item -Recurse -Force .git` cannot be undone"
                This permanently deletes the repository's history from your machine - every commit, branch and tag. There is no undo, and nothing to recover from, because the deleted history is the thing that would have recovered it. Make sure you are in the right directory (`pwd`) and that you have pushed anything you care about somewhere else first.

        === ":material-linux: Linux (Ubuntu)"

            ``` bash
            rm -rf .git
            git init -b main
            git config core.fileMode false
            ```

            !!! danger "`rm -rf .git` cannot be undone"
                This permanently deletes the repository's history from your machine - every commit, branch and tag. There is no undo, and nothing to recover from, because the deleted history is the thing that would have recovered it. Make sure you are in the right directory (`pwd`) and that you have pushed anything you care about somewhere else first.

    </div>

    !!! note "Why `core.fileMode false`"
        Git records whether a file is executable, and treats a change to
        that bit as a change to the file. Cloud-sync clients - OneDrive in
        particular - rewrite those bits as they sync, so a folder that syncs
        can show every file in the project as modified when not one byte of
        content has changed. Turning it off tells git to ignore the
        executable bit entirely.

        It is set per repository and is not committed, so it has to be
        repeated on each machine and after each fresh clone. If you keep
        all your work in a synced folder, `git config --global
        core.fileMode false` saves repeating it - though `git init` and
        `git clone` each write their own local setting, which still wins.

    `rm -rf .git`/`Remove-Item -Recurse -Force .git` deletes the whole repository, remotes included, and `git init` starts a brand new one with none at all:

    ``` mermaid
    graph LR
      L[Your local clone - no remotes]
    ```
    /// figure-caption
    After resetting the history: no remotes at all
    ///

    Run `git remote -v` at this point and it prints nothing.

1. Create the new, **empty** repository on the host you are publishing to. Do **not** add a README, `.gitignore` or licence - the template brings its own, and an initial commit on the host side collides with what you are about to push.

    <div class="grid cards one-column" markdown>

    -   :material-clock-fast:{ .lg .middle } __Create the empty repository__

        === "GitLab"

            On the GitLab website, click **New project > Create blank project**. Name it, set **Visibility Level** to **Private**, and untick **Initialize repository with a README**.

        === "GitHub"

            On the GitHub website, click **New repository**. Name it, set it to **Private**, and leave every **Initialize this repository with** option unticked.

    </div>

1. Point your clone at your own repository, using the tab matching your host:

    !!! note "There is nothing to remove first"
        Deleting `.git` in step 3 took the template's `origin` with it, along
        with any other remotes you saw in step 2 - `git init` starts a
        repository with none at all. If you run `git remote remove origin`
        out of habit, Git tells you so:

        ``` text
        error: No such remote: 'origin'
        ```

        That message means the previous step did its job, not that anything
        is wrong.

    <div class="grid cards one-column" markdown>

    -   :material-clock-fast:{ .lg .middle } __Point the clone at your repository__

        === "GitLab"

{% if is_surrey %}
            ``` bash
            git remote add origin git@gitlab.surrey.ac.uk:comm058-2026/your-new-directory-name.git
            ```

            Where your-new-directory-name is the name of the repository you created on GitLab, such as `report-az1234`. Replace `comm058-2026` with your own namespace if it is different.
{% else %}
            ``` bash
            git remote add origin git@gitlab.com:your-namespace/your-new-directory-name.git
            ```

            Replace `gitlab.com` with your own GitLab instance if it is self-hosted.
{% endif %}

        === "GitHub"

            ``` bash
            git remote add origin git@github.com:your-username/your-new-directory-name.git
            ```

    </div>

    Confirm it took:

    ``` bash
    git remote -v
    ```

    ``` mermaid
    graph LR
      L[Your local clone] -->|origin| R[Your own repository]
    ```
    /// figure-caption
    After repointing: `origin` points at your own repository
    ///

    `origin` now points at your own repository rather than the template's - compare this against the first diagram in this section, where it pointed at `prodockit-template` instead.

    !!! note "Don't commit or push yet"
        Step 3 left you with an empty repository - the template's files are
        all still there, but Git is tracking none of them yet.

        Resist committing them now. The template's files still name the
        *template's* repository in several places, and `prodockit sync-repo`
        in the next section is what repoints them at yours. Committing first
        would put those stale references into your project's very first
        commit, and you would then be correcting them in the second.

        [Install Python and Zensical](#install-python-and-zensical) ends
        with the `git add`, `git commit` and `git push` that publish
        everything in one go, once there is something correct to publish.

We are not complete with the setup yet, but you now have a local copy of the template that is connected to your own repository on GitLab or GitHub. Do not start editing yet, as the next section installs Python, Zensical and prodockit, which are needed to build your documentation.

## Install Python and Zensical

Here are brief instructions for installing \index{Python} are below for macOS, Windows 11, and Linux (Ubuntu/Debian). However, it's recommended to refer to the [official Python installation documentation](https://docs.python.org/3/using/) for your operating system. 

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

            4. Open **Terminal** in your project folder and run the following commands to create a virtual environment and install Zensical inside it:

                ``` bash
                # 1. Create the virtual environment
                /opt/homebrew/bin/python3 -m venv .venv

                # 2. Activate it
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

            1. Download and run the official Python installer from [python.org](https://www.python.org/downloads/){target="_blank"}.

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

                Then open the **MSYS2 MINGW64** shell from your Start menu (not PowerShell) and run:

                ``` bash
                pacman -S mingw-w64-x86_64-pango
                ```

                If that fails partway through with a download error, just run it again - MSYS2's mirrors are occasionally flaky, and a second attempt usually goes through cleanly.

                Finally, add `C:\msys64\mingw64\bin` to your user `PATH`, the same way you added Python: search for *Edit the system environment variables*, click **Environment Variables**, select **Path** under *User variables*, and add that folder. Close and reopen PowerShell afterwards so the change takes effect - the next two steps continue in that new window.

                !!! note "No virtual environment to reactivate yet"
                    Unlike other "close and reopen PowerShell" steps on this page, there's nothing to `cd` back to or activate here. The virtual environment isn't created until step 5 below - reopening PowerShell now just gets the `PATH` change into a fresh window before continuing.

                !!! info "Why this is needed"
                    That folder is where WeasyPrint finds `libgobject-2.0-0.dll`, `libpango-1.0-0.dll`, `libharfbuzz-0.dll` and `libfontconfig-1.dll` - installing `pango` brings all four in. Skipping this still looks fine until `prodockit pdf`, which then fails with `pandoc exited with status 43` - see [WeasyPrint cannot start (status 43)](startediting.md#startediting-pandoc-status-43) if that happens.

            4. Allow PowerShell to run scripts. Windows blocks all of them by default, and activating a virtual environment *is* a script, so this has to be done once before the next step will work:

                ``` powershell
                Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
                ```

                Depending on your PowerShell version it may ask you to confirm the change; answer `Y` if it does. Often it simply returns to the prompt, which means it worked.

                !!! info "What this changes"
                    Without it, activating the venv fails with `... cannot be loaded because running scripts is disabled on this system`. `RemoteSigned` allows locally-written scripts while still requiring signed ones from the internet; `-Scope CurrentUser` limits that to your account, so it needs no Administrator window and is a one-time, per-account change.

                    Would rather not change it at all? Use **classic CMD** instead of PowerShell and run `.\.venv\Scripts\activate.bat` in the next step - `.bat` files aren't covered by execution policy.

            5. Change into your project folder, then create a virtual environment and install Zensical inside it:

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

                ``` powershell
                # 1. Create the virtual environment
                python -m venv .venv

                # 2. Activate it (choose the line matching your terminal)
                .\.venv\Scripts\Activate.ps1     # <-- Use this if you are in PowerShell
                .\.venv\Scripts\activate.bat     # <-- Use this if you are in classic CMD
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

            1. Open a terminal and run the following command to install Python, the `venv` module, pandoc, and the graphics libraries \index{WeasyPrint} needs. None of these is a Python package, so `pip` cannot install them for you:

                ``` bash
                sudo apt update
                sudo apt install python3 python3-venv python3-pip curl \
                  libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0
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

            2. Navigate to your project folder and run the following commands to create a virtual environment and install Zensical inside it:

                ``` bash
                # 1. Create the virtual environment
                python3 -m venv .venv

                # 2. Activate it
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
    drift](https://buckwem.github.io/prodockit-extensions/devcons/continuous-integration/#ci-pandoc-version){target="_blank"}
    for what that looked like.

    Confirm which version you actually have:

    ``` bash
    pandoc --version
    ```

    The first line should read `pandoc 3.10.1`. If it doesn't - a
    Homebrew upgrade, a distribution update, or `winget upgrade` run
    without thinking about it will all move this - repeat the pandoc
    install step above for your platform to bring it back.

1. Install Zensical and prodockit inside the virtual environment. The `requirements.txt` file in the template lists the required packages, so you can install them all with a single command (use `pip` if `pip3` is not available):

    ``` bash
    pip3 install -r requirements.txt
    ```

1. Check that WeasyPrint can find its graphics libraries. This is the one part of the setup `pip` cannot verify for you, so it is worth confirming now rather than at your first PDF build:

    ``` bash
    python3 -c "import weasyprint; print(weasyprint.__version__)"
    ```

    A version number means everything is in place. If instead you get a long error ending in `cannot load library`, the libraries from the step above are missing or cannot be found - go back and install them.

1. Sync the repository's own self-references to match. The template's files still name the *template's* repository in several places, and nothing about changing a Git remote updates them:

    ``` bash
    prodockit sync-repo
    ```

    It reports what it changed:

    ``` text
    Detected GitLab remote (https://gitlab.surrey.ac.uk/az1234/report-az1234); updated: repo_url, repo_name, theme.icon.repo, README badges
    ```

    This rewrites `repo_url`, `repo_name`, `theme.icon.repo` and `edit_uri` in `zensical.toml`, plus the badge row in your `README.md`, to match the `origin` you just set - so your built site and PDF link to your own repository rather than the template's. Note `theme.icon.repo` in that list: moving from a GitHub template to a GitLab project switches the header's brand icon to match, which is easy to miss by hand. Only the values that actually needed changing are listed, so the set you see may be smaller.

    !!! tip "Check it any time"
        `prodockit sync-repo --check` writes nothing and exits non-zero if these have drifted
        from your remote - useful after any later change of host. See
        [Checks worth having](customisebuild.md#customisebuild-checks).

1. Lets now commit the changes to your own repository. Run the following commands to commit and push the changes:

    ``` bash
    git add .
    git commit -m "Initial commit with Zensical and prodockit installed"
    git push -u origin main
    ```


### Install Zensical Studio and other plugins

Now we'll install the \index{VS Code!Zensical Studio} plugin for Visual Studio Code, which provides a set of tools to help you work with Zensical projects, including commands to build and preview your site. Then we'll install a couple of other useful plugins for working with Markdown and TOML files.

1. Start by opening Visual Studio Code and navigating to the Extensions view by clicking on the Extensions icon in the Activity Bar on the side of the window or pressing `Ctrl+Shift+X`/`Cmd+Shift+X`.
1. Install the **Python** extension (published by Microsoft) by searching for "Python" in the Extensions view and clicking **Install**{: .bg-blue}. As well as Python support, this is what makes VS Code notice the `.venv` folder in your project and activate the virtual environment automatically in every new Terminal in VS Code - so you don't have to run `source .venv/bin/activate` by hand each time you open one.

    !!! Tip
        Check it worked by opening a new terminal (**Terminal > New Terminal**) - the prompt should start with `(.venv)`. If it doesn't, reopen VS Code in the project folder, then choose **Python: Select Interpreter** from the Command Palette (`Ctrl+Shift+P`/`Cmd+Shift+P`) and pick the one inside `.venv`.

1. Install the **Zensical Studio** extension by searching for "Zensical Studio" in the Extensions view and clicking **Install**{: .bg-blue} and then **Trust Publisher and Install**{: .bg-blue} when prompted. This extension provides a set of tools to help you work with Zensical projects, including commands to build and preview your site.
1. Follow the instructions on the Zensical Studio plugin page to configure the extension. You may find the configuration aleady exists but if it's not there add to the `.vscode/settings.json` file in your project directory the following lines:

    ```json
    {
      "files.associations": {
       "*.md": "python-markdown"
      }
    }
    ```

1. Install the **Even Better TOML** extensiuon for Visual Studio Code by searching for "Even Better TOML" in the Extensions view and clicking **Install**{: .bg-blue} and then **Trust Publisher and Install**{: .bg-blue} when prompted. This extension provides syntax highlighting and other features for working with TOML files, which are used for configuration in Zensical projects.
1. Install the **LTeX+ – LanguageTool grammar/spell checking** plugin for Visual Studio Code by searching for "LTeX+" in the Extensions view and clicking **Install**{: .bg-blue} and then **Trust Publisher and Install**{: .bg-blue} to enable spelling and grammar checking for Markdown. Configure the plugin in the settings to use the *language* `en-GB`.

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

        Close and reopen PowerShell afterwards, so it picks up the new `PATH`. The new window starts in `C:\Users\yourname` with the virtual environment inactive, so get back to where you were before continuing:

        ``` powershell
        cd C:\path\to\your-project
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

Open a new terminal for this step, and make sure it's actually sitting in your project's root directory first - the `--prefix` paths below are relative to wherever you run them from:

``` bash
cd path/to/your-project
```

Then install both:

``` bash
npm ci --prefix tools/mermaid
npm ci --prefix tools/mathjax
```

`npm ci` installs the exact versions recorded in each lockfile, which is what the automated builds use too - so your PDF is rendered by the same versions as the published one.

This creates a `node_modules` folder inside each, which is deliberately not committed (see `.gitignore`). Run these two commands again if you ever re-clone the project.

If you're on Linux, also install a native Chromium and point Puppeteer at it, rather than relying on the Chrome that `tools/mermaid`'s `npm ci` downloaded for it - which is not guaranteed to match your CPU's architecture. This matters most on ARM64 machines (an Apple Silicon Linux VM, an AWS Graviton instance, a Raspberry Pi), where the mismatch otherwise goes unnoticed until a PDF build fails, but it costs nothing to do on any Ubuntu install:

``` bash
sudo apt update
sudo apt install -y chromium-browser
which chromium-browser || which chromium
```

The second command should print a path such as `/usr/bin/chromium-browser` or `/usr/bin/chromium` - that's what the next step needs. Point `prodockit pdf` at it for this session, then make it permanent so every future session picks it up too:

``` bash
export PUPPETEER_EXECUTABLE_PATH=$(which chromium-browser || which chromium)
echo 'export PUPPETEER_EXECUTABLE_PATH=$(which chromium-browser || which chromium)' >> ~/.bashrc
source ~/.bashrc
```

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

Test the whole thing by building the PDF - see [Generate the Source and PDF documents](startediting.md#startediting-generate-documents) in the next section. If a diagram appears as an image rather than as text, everything is set up correctly. None of this is required if your document has no diagrams or formulas, but setting it up now costs nothing and means the trap above can't catch you later when you add your first one.

## Where to go next {: #installtooling-where-to-go-next }

You now have Visual Studio Code, Git, Zensical and the diagram and maths tooling installed, and your own copy of the documentation template cloned locally. Continue to [Start editing](startediting.md) to preview your changes locally and publish them to GitLab or GitHub.