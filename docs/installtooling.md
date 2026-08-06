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

    === "macOS using Homebrew"

        1. Open the **Terminal** application.
        1. You are likely to already have [Homebrew](https://brew.sh){target="_blank"} installed, but if not, follow the instructions on [brew.sh](https://brew.sh){target="_blank"} to install it.  **Close and reopen your Terminal after installing it.** As the installer adds `brew` to your `PATH`, and a session that was already open won't pick that up.

        1. Use the Homebrew package manager to install Visual Studio Code in your Terminal:
            ``` bash
            brew update
            brew install --cask visual-studio-code
            ```

    === "Windows 11 using PowerShell"

        1. Download the VS Code User setup for Windows from the [official website](https://code.visualstudio.com/download){target="_blank"}.
        2. Run the installer, `VSCodeUserSetup-{version}.exe`. By default the User setup installs Visual Studio Code to your user profile directory. You can change the install location if you want to install it for all users.
         
    === "Linux (Ubuntu/Debian) using bash"

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

        === "macOS using Homebrew"

            Use the Homebrew package manager to install or update `git` to the latest stable version:
                
            ``` bash
            brew install git
            ```

        === "Windows 11 using PowerShell"

            Open up a **PowerShell** window and install `git` using the command, or you can download and install the official git installer from [git-scm.com](https://git-scm.com/download/win){target="_blank"}.
                
            ``` PowerShell
            winget install Git.Git
            ```
        
            If you just require an updated version of `git`, you can run the following command in **PowerShell**:
                
            ``` PowerShell
            winget upgrade Git.Git
            ```

        === "Linux (Ubuntu/Debian) using bash"

            Open a terminal and run the following command to install or update `git` to the latest stable version:
            
            ``` bash
            sudo apt update
            sudo apt install git
            ```
    </div>

1. Before connecting to any cloud provider, open your terminal (Terminal on macOS/Debian, Git Bash or PowerShell on Windows 11) and set your global username and email. This is the identity stamped onto your commits. Make sure you use the same email address that you used to register for your GitLab or GitHub account.

    ``` bash
    git config --global user.name "Your Name"
    git config --global user.email "your.email@example.com"
    ```

1. Register for an account on the public [**GitLab**](https://gitlab.com){target="_blank"} or [**GitHub**](https://github.com){target="_blank"} cloud instance you will use. If you have already registered, you can skip this step.

{% if is_surrey %}
!!! Info "University of Surrey GitLab"
    For the University of Surrey, you will need to use the GitLab instance provided by the university at [https://gitlab.surrey.ac.uk](https://gitlab.surrey.ac.uk){target="_blank"} for all assignments. When you get to the login page, select the button **Surrey Login**{: .bg-grey} and use your university credentials.
{% endif %}

### Generate and configure ssh keys for Git

Now generate the \index{Git!ssh keys} to use for authentication with your GitLab or GitHub account and configure your ssh settings to use these keys. 

1. Follow the instructions below to generate a new SSH key pair and add it to your GitLab or GitHub account. It's best practice to use modern, secure `ed25519` keys and create separate ones for GitHub and GitLab.

    <div class="grid cards one-column" markdown>
    
    -   :material-clock-fast:{ .lg .middle } __Generate SSH keys__

        === "macOS using Homebrew"

            1. Open the **Terminal** application.
            2. Run the following command to generate a new SSH key pair for GitHub and GitLab. Make sure to replace `your.gitxxx.email@example.com` with your actual email address and `gitxxx` with either `github` or `gitlab` depending on which service you are generating the key for:
            
                ``` bash
                ssh-keygen -t ed25519 -C "your.gitxxx.email@example.com" -f ~/.ssh/id_ed25519_gitxxx
                ```
            3. When prompted, type a strong passphrase.

        === "Windows 11 using PowerShell"

            1. Open the **PowerShell** application.
            2. Run the following command to generate a new SSH key pair for GitHub and GitLab. Make sure to replace `your.gitxxx.email@example.com` with your actual email address and `gitxxx` with either `github` or `gitlab` depending on which service you are generating the key for:
            
                ``` powershell
                ssh-keygen -t ed25519 -C "your.gitxxx.email@example.com" -f $env:USERPROFILE\.ssh\id_ed25519_gitxxx
                ```
            3. When prompted, type a strong passphrase.
            
        === "Linux (Ubuntu/Debian) using bash"

            1. Open the **Terminal** application.
            2. Run the following command to generate a new SSH key pair for GitHub and GitLab. Make sure to replace `your.gitxxx.email@example.com` with your actual email address and `gitxxx` with either `github` or `gitlab` depending on which service you are generating the key for:
            
                ``` bash
                ssh-keygen -t ed25519 -C "your.gitxxx.email@example.com" -f ~/.ssh/id_ed25519_gitxxx
                ```
            3. When prompted, type a strong passphrase.
    
    </div>

1. Then configure the SSH Config file to use the correct SSH key for each service. Open the SSH config file in your preferred [text editor](shcommands.md#editing-files) (create it if it doesn't exist) and add the following lines:

    For example using `nano` on macOS or Linux:

    ```bash
    nano ~/.ssh/config
    ```
    
    paste the relevant configuration into the config file:

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

    # GitHub
    Host github.com
        HostName github.com
        User git
        IdentityFile ~/.ssh/id_ed25519_github
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

    Then save and close the file (`Ctrl+O` to save and `Ctrl+X` to exit in nano). On Windows, you can use `Notepad` or any text editor to create the `config` file in the `.ssh` directory.

    Make sure to replace the paths with the correct paths to your SSH keys if you used different names or locations.

    !!! Tip
        You can use the same SSH key for multiple GitLab/GitHub accounts, but it's recommended to use separate keys for each account for better security and management. If you do use the same key, make sure to add the public key to each account separately as documented in [Integrate Visual Studio Code with Git](#integrate-visual-studio-code-with-git) below.

1. Set the correct permissions for the SSH config file and the private keys to ensure they're secure. If you are using macOS or Linux, run the following commands in your terminal, substituting `gitxxx` and paths to your SSH keys if you used different names or locations:

    ```bash
    chmod 600 ~/.ssh/config
    chmod 600 ~/.ssh/id_ed25519_gitxxx
    ```

    Windows handles permissions differently and are normally set to only allow access to the user, but ensure that the private keys aren't accessible to other users.

1. You've set a passphrase for the SSH keys, so you'll need to enter it every time you use a key. To avoid this, you can use an SSH agent to cache your passphrase. Follow the instructions below to start the SSH agent and add your keys.

    <div class="grid cards one-column" markdown>
    
    -   :material-clock-fast:{ .lg .middle } __Adding SSH keys__

        === "macOS using Homebrew"

            1. macOS normally starts an SSH agent for you automatically. Add your SSH private keys to it, substituting `gitxxx` with either `github` or `gitlab` depending on which service you are adding the key for:

                ``` bash
                ssh-add ~/.ssh/id_ed25519_gitxxx
                ```

                If this fails with an error about not being able to connect to the agent, start one first, then repeat the command above:

                ``` bash
                eval "$(ssh-agent -s)"
                ```

        === "Windows 11 using PowerShell"

            1. Start the SSH agent in the background and set it to start automatically with Windows. Run this in a PowerShell window opened **as Administrator** (right-click the Start menu, or search for PowerShell, then select **Run as administrator**):

                ``` powershell
                Start-Service ssh-agent
                Set-Service -Name ssh-agent -StartupType Automatic
                ```
            2. Back in your normal (non-administrator) PowerShell window, add your SSH private keys to the agent, substituting `gitxxx` with either `github` or `gitlab` depending on which service you are adding the key for:

                ``` powershell
                ssh-add $env:USERPROFILE\.ssh\id_ed25519_gitxxx
                ```

        === "Linux (Ubuntu/Debian) using bash"

            1. Add your SSH private keys to the running SSH agent, substituting `gitxxx` with either `github` or `gitlab` depending on which service you are adding the key for:

                ``` bash
                ssh-add ~/.ssh/id_ed25519_gitxxx
                ```

                Unlike macOS, Linux doesn't always start an SSH agent automatically. If the command above fails with an error about not being able to connect to the agent, start one first, then repeat the command above:

                ``` bash
                eval "$(ssh-agent -s)"
                ```
    </div>

### Integrate Visual Studio Code with Git

1. Now that you've generated your keys and finished the configuration, add them to your GitHub and GitLab accounts using the instructions below.

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

    </div>

1. Test the SSH connection to GitHub and GitLab to ensure that the keys are working correctly. Run the following commands in your terminal:

    ```bash
    ssh -T git@gitxxx.com
    ```

{% if is_surrey %}
    If you're using the University of Surrey GitLab, test that connection too:

    ```bash
    ssh -T git@gitlab.surrey.ac.uk
    ```
{% endif %}

    If successful, you will see greetings like:

    ```text
    Hi username! You've successfully authenticated, but GitHub does not provide shell access.
    Welcome to GitLab, @username!
    ```

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

    !!! Tip
        You can find your `username` by logging into your GitLab or GitHub account and clicking on your profile picture at the top right corner of the page. On **GitLab** your username is **below** your name in the dropdown menu. On **GitHub** your username is **above** your name in the dropdown menu.

### Point your clone at your own repository

If you have cloned a repository that has been given to you to work on and is not a direct copy of the template, you can skip the remaining steps in this section.

Cloning gives you the template's *files*, but the clone still points at the template's *repository*. Push now and Git will try to write to the template itself, which you almost certainly cannot do - and would not want to if you could. This section repoints it at a repository of your own.

1. Rename the directory to something meaningful for your own report. Cloning leaves you with a folder called `prodockit-template`, which says nothing about whose work it holds - and if you clone a second project later, you will not be able to tell them apart.

    ``` bash
    mv prodockit-template report-az1234
    ```

    Replace `report-az1234` with a name that identifies your own work - your username, your coursework code, or whatever your course tutor specifies.

    !!! note "Renaming the folder doesn't rename the repository"
        This changes only the folder on your own machine. The project's name on GitLab or GitHub is unaffected, and so is the `origin` remote inside it - `git push` and `git pull` carry on working exactly as before.

1. Check what your clone currently points at:

    ``` bash
    cd report-az1234
    git remote -v
    ```

    A fresh clone has exactly one remote, `origin`, pointing at the template:

    ``` text
    origin  git@github.com:buckwem/prodockit-template.git (fetch)
    origin  git@github.com:buckwem/prodockit-template.git (push)
    ```

    If you added any others of your own - a `gitlab` mirror, say - they will be listed here too, and need removing in step 4 alongside `origin`.

1. Start with a fresh commit history. This is your own independent project, so carrying the template's entire commit log and branches from the template into it serves little purpose.

    ``` bash
    rm -rf .git
    git init -b main
    git add .
    git commit -m "Initial commit from prodockit-template"
    ```

    !!! danger "`rm -rf .git` cannot be undone"
        This permanently deletes the repository's history from your machine - every commit, branch and tag. There is no undo, and nothing to recover from, because the deleted history is the thing that would have recovered it. Make sure you are in the right directory (`pwd`) and that you have pushed anything you care about somewhere else first.

1. Create the new, **empty** repository on the host you are publishing to. Do **not** add a README, `.gitignore` or licence - the template brings its own, and an initial commit on the host side collides with what you are about to push.

    === "GitLab"

        On the GitLab website, click **New project > Create blank project**. Name it, set **Visibility Level** to **Private**, and untick **Initialize repository with a README**.

    === "GitHub"

        On the GitHub website, click **New repository**. Name it, set it to **Private**, and leave every **Initialize this repository with** option unticked.

1. Remove the template's remote first, along with any others you spotted in step 1:

    ``` bash
    git remote remove origin
    ```

    Then add your own, using the tab matching your host:

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

    Confirm it took, then push:

    ``` bash
    git remote -v
    git push -u origin main
    ```

1. Sync the repository's own self-references to match. The template's files still name the *template's* repository in several places, and nothing about changing a Git remote updates them:

    ``` bash
    source .venv/bin/activate
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

    You will need the virtual environment from [Install Python and Zensical](#install-python-and-zensical) below before this command exists, so if you have not set that up yet, come back to this step once you have.

## Install Python and Zensical

Brief instructions for installing \index{Python} are below for macOS, Windows 11, and Linux (Ubuntu/Debian). However, it's recommended to refer to the [official Python installation documentation](https://docs.python.org/3/using/) for your operating system. 

If you already have Python installed, you can check the version by running the following command in your terminal or command prompt:

```bash
python --version
```

!!! Note
    You may need to use 'python3' and 'pip3' instead of 'python' and 'pip' depending on your system configuration.

The instructions below are for installing Python 3.12 or later. If you have an older version, please update to Python 3.12 or later.

Follow the instructions below to install Python, create a \index{Python!virtual environment}, and install Zensical inside it for your operating system.

<div class="grid cards one-column" markdown>

-   :material-clock-fast:{ .lg .middle } __Install Python, Zensical and prodockit__

    === "macOS using Homebrew"

        1. If you use the Homebrew package manager, run this command in your Terminal to install Python. If you don't have Homebrew installed, you can install it by following the instructions on the [Homebrew website](https://brew.sh/){target="_blank"}.

            ``` bash
            brew install python3
            ```

        2. Install \index{Pandoc} as well. `prodockit pdf` shells out to the `pandoc`
           command to build your PDF, and it is not a Python package, so `pip` cannot
           install it for you:

            ``` bash
            brew install pandoc
            ```

        3. Open **Terminal** in your project folder and run the following commands to create a virtual environment and install Zensical inside it:

            ``` bash
            # 1. Create the virtual environment
            /opt/homebrew/bin/python3 -m venv .venv

            # 2. Activate it
            source .venv/bin/activate

            # 3. Install Zensical
            pip3 install -r requirements.txt
            ```

            !!! note "Why the full path to Python"
                macOS ships its own older Python, and a plain `python3` may well find
                that one instead of Homebrew's. Naming
                `/opt/homebrew/bin/python3` explicitly builds the virtual environment
                from the version you just installed. On an Intel Mac, Homebrew
                installs to `/usr/local` instead, so use
                `/usr/local/bin/python3`.

    === "Windows 11 using PowerShell"

        1. Download and run the official Python installer from [python.org](https://www.python.org/downloads/){target="_blank"}.

           !!! Critical
                Make sure to check the box to add Python to your `PATH` during the installation process. This allows you to run Python from the command line.

        2. Open **PowerShell** in your project folder and run the following commands to create a virtual environment and install Zensical inside it:
            

            ``` powershell
            # 1. Create the virtual environment
            python -m venv .venv

            # 2. Activate it (choose the line matching your terminal)
            .\.venv\Scripts\Activate.ps1     # <-- Use this if you are in PowerShell
            .\.venv\Scripts\activate.bat     # <-- Use this if you are in classic CMD

            # 3. Install Zensical inside the environment
            pip install -r requirements.txt
            ```

    === "Linux (Ubuntu/Debian) using bash"

        1. Open a terminal and run the following command to install Python and the `venv` module:

            ``` bash
            sudo apt update
            sudo apt install python3 python3-venv python3-pip
            ```

        2. Navigate to your project folder and run the following commands to create a virtual environment and install Zensical inside it:

            ``` bash
            # 1. Create the virtual environment
            python3 -m venv .venv

            # 2. Activate it
            source .venv/bin/activate

            # 3. Install Zensical
            pip3 install -r requirements.txt
            ```

</div>

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

Your PDF needs two more tools, and this is the step most easily skipped - because skipping it doesn't break anything visibly.

\index{Zensical!diagrams} and mathematical notation render on the website by themselves: the reader's browser draws them. The PDF has no browser, so `prodockit pdf` has to convert both into images *before* building the document, and it uses two \index{Node.js} programs to do it.

!!! danger "Without these, the PDF is wrong rather than missing"
    `prodockit pdf` does **not** fail when they are absent. It leaves the content as it found it, so instead of a flowchart your PDF shows the diagram's own definition text - the `graph LR` line and every node written out beneath it - and instead of a typeset equation, raw LaTeX with all its backslashes and braces.

    Meanwhile the website renders both perfectly. So nothing looks wrong until somebody opens the PDF, which may be well after you have written the document.

### Install Node.js

The two tools are Node.js programs, so install Node.js first. Version 22 or newer - that is what the automated builds use.

<div class="grid cards one-column" markdown>

-   :material-clock-fast:{ .lg .middle } __Install Node.js__

    === "macOS using Homebrew"

        ``` bash
        brew install node
        ```

    === "Windows 11 using PowerShell"

        ``` powershell
        winget install OpenJS.NodeJS.LTS
        ```

        Close and reopen PowerShell afterwards, so it picks up the new `PATH`.

    === "Linux (Ubuntu/Debian) using bash"

        Ubuntu's own `nodejs` package is often several versions behind. Use NodeSource's repository to get a current release:

        ``` bash
        curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
        sudo apt install -y nodejs
        ```

</div>

Check it worked:

``` bash
node --version
npm --version
```

### Install the two toolchains

Your cloned template already contains the manifests and lockfiles for both tools, in `tools/mermaid` and `tools/mathjax` - so you only need to install them. From your project's root directory:

``` bash
npm ci --prefix tools/mermaid
npm ci --prefix tools/mathjax
```

`npm ci` installs the exact versions recorded in each lockfile, which is what the automated builds use too - so your PDF is rendered by the same versions as the published one.

This creates a `node_modules` folder inside each, which is deliberately not committed (see `.gitignore`). Run these two commands again if you ever re-clone the project.

!!! note "If npm warns about install scripts"
    Recent versions of npm print a warning during the Mermaid install and skip the package's own setup step:

    ``` text
    npm warn allow-scripts 1 package has install scripts not yet covered by allowScripts:
    npm warn allow-scripts   puppeteer@25.4.0 (postinstall: node install.mjs)
    ```

    That step is what downloads the headless browser Mermaid draws diagrams with. The install still succeeds, and if the browser is already on your machine from something else, diagrams render fine. If instead a later PDF build reports that it cannot find a browser, approve the step and reinstall:

    ``` bash
    npm approve-scripts puppeteer --prefix tools/mermaid
    npm ci --prefix tools/mermaid
    ```

!!! tip "Starting a project that isn't from the template?"
    Then you have no `tools/` directory to install from, and need `prodockit init-tools` first to create it. Running it on a copy of the template is harmless but pointless - it will just report `Kept existing tools/mermaid/package.json` for each file it finds. See [Diagrams and maths](customisebuild.md#customisebuild-diagrams-and-maths) for the full picture.

Test the whole thing by building the PDF - see [Generate the Source and PDF documents](startediting.md#startediting-generate-documents) in the next section. If a diagram appears as an image rather than as text, everything is set up correctly.

!!! note "You can skip this if your document has neither"
    A document with no diagrams and no formulas never calls either tool, so nothing here is required for it. It costs nothing to set up now though, and means the trap above cannot catch you later when you add your first diagram.

## Where to go next {: #installtooling-where-to-go-next }

You now have Visual Studio Code, Git, Zensical and the diagram and maths tooling installed, and your own copy of the documentation template cloned locally. Continue to [Start editing](startediting.md) to preview your changes locally and publish them to GitLab or GitHub.