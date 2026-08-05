---
icon: lucide/book-open 
---

<!-- 
Copyright (c) 2025-2026 Mark Buckwell and contributors
SPDX-License-Identifier: MIT
-->

{{ heading_counter_reset(page) }}

# Install tooling

This section takes you through the core installation steps for the tools needed to edit your static website. The instructions are for macOS, Windows 11, and Linux (Ubuntu/Debian). If you are using a different operating system, please refer to the official documentation for that operating system.

<div class="web-only" markdown>
!!! Tip
    The screenshots below may have small text on your screen. You can click on an image to enlarge it.
</div>

The install and configuration starts with the setup of Visual Studio Code.

## Install Visual Studio Code

[Visual Studio Code](https://code.visualstudio.com){target="_blank"} (VS Code) is the selected primary editor for developing your documentation website using Zensical. You can use other editors, but the availability of many plugins in Visual Studio Code will help you edit your documentation more efficiently.

The steps below will help you install \index{VS Code} and some essential plugins to edit your documentation. If you have already installed VS Code, check through the steps so you have the plugins installed.

### Install Visual Studio Code

Start with installing [Visual Studio Code](https://code.visualstudio.com){target="_blank"}. Instructions for macOS, Windows 11, and Linux (Ubuntu/Debian) are below.

<div class="grid cards one-column" markdown>
    
-   :material-clock-fast:{ .lg .middle } __Install Visual Studio Code__

    === "macOS using Homebrew"

        !!! note "You need Homebrew first"
            These instructions use [Homebrew](https://brew.sh){target="_blank"}, the package manager
            most of the macOS steps in this guide rely on. If you don't have it,
            install it by following the single command on
            [brew.sh](https://brew.sh){target="_blank"}.

            **Close and reopen your Terminal after installing it.** The installer
            adds `brew` to your `PATH`, and a session that was already open won't
            pick that up - the `brew` command will simply not be found until you
            start a new one.

        1. If you use the Homebrew package manager, run this command in your Terminal:
            ``` bash
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

            If you use the Homebrew package manager, run this command in your Terminal to either install or update `git` to the latest stable version:
                
            ``` bash
            brew update
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

1. Register for an account on the **GitLab** or **GitHub** cloud instance you will use. If you have already registered, you can skip this step.

{% if is_surrey %}
!!! Info "University of Surrey GitLab"
    For the University of Surrey, you will be using the GitLab instance provided by the university at [https://gitlab.surrey.ac.uk](https://gitlab.surrey.ac.uk){target="_blank"}. When you get to the login page, select the button **Surrey Login**{: .bg-grey} and use your university credentials.

    If you'd also like an account on the public GitLab at [https://gitlab.com](https://gitlab.com){target="_blank"} - for example, to keep using GitLab for personal projects after you graduate - you can register for one separately; the steps below work the same for both.
{% endif %}

### Generate and configure ssh keys for Git

Now generate the \index{Git!ssh keys} to use for authentication with your GitLab or GitHub account and configure your ssh settings to use these keys. 

1. Follow the instructions below to generate a new SSH key pair and add it to your GitLab or GitHub account. It's best practice to use modern, secure `ed25519` keys and create separate ones for GitHub and GitLab.

    <div class="grid cards one-column" markdown>
    
    -   :material-clock-fast:{ .lg .middle } __Generate SSH keys__

        === "macOS using Homebrew"

            1. Open the **Terminal** application.
            2. Run the following command to generate a new SSH key pair for GitHub and GitLab. Make sure to replace `your.gitxxx.email@example.com` with your actual email address:
            
                ``` bash
                ssh-keygen -t ed25519 -C "your.github.email@example.com" -f ~/.ssh/id_ed25519_github
                ssh-keygen -t ed25519 -C "your.gitlab.email@example.com" -f ~/.ssh/id_ed25519_gitlab
                ```
            3. When prompted, type a strong passphrase.

        === "Windows 11 using PowerShell"

            1. Open the **PowerShell** application.
            2. Run the following command to generate a new SSH key pair for GitHub and GitLab. Make sure to replace `your.gitxxx.email@example.com` with your actual email address:
            
                ``` powershell
                ssh-keygen -t ed25519 -C "your.github.email@example.com" -f $env:USERPROFILE\.ssh\id_ed25519_github
                ssh-keygen -t ed25519 -C "your.gitlab.email@example.com" -f $env:USERPROFILE\.ssh\id_ed25519_gitlab
                ```
            3. When prompted, type a strong passphrase.
            
        === "Linux (Ubuntu/Debian) using bash"

            1. Open the **Terminal** application.
            2. Run the following command to generate a new SSH key pair for GitHub and GitLab. Make sure to replace `your.gitxxx.email@example.com` with your actual email address:
            
                ``` bash
                ssh-keygen -t ed25519 -C "your.github.email@example.com" -f ~/.ssh/id_ed25519_github
                ssh-keygen -t ed25519 -C "your.gitlab.email@example.com" -f ~/.ssh/id_ed25519_gitlab
                ```
            3. When prompted, type a strong passphrase.
    
    </div>

1. Then configure the SSH Config file to use the correct SSH key for each service. Open the SSH config file in your preferred [text editor](shcommands.md#editing-files) (create it if it doesn't exist) and add the following lines:

    For example using `nano` on macOS or Linux:

    ```bash
    nano ~/.ssh/config
    ```
    
    paste the following configuration into the file:

{% if is_surrey %}
    ```text
    # GitLab
    Host gitlab.com
        HostName gitlab.com
        User git
        IdentityFile ~/.ssh/id_ed25519_gitlab

    # GitLab (University of Surrey)
    Host gitlab.surrey.ac.uk
        HostName gitlab.surrey.ac.uk
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

    The same key works for multiple GitLab/GitHub instances - you just need to add the public key (`~/.ssh/id_ed25519_gitlab.pub`) to each account separately in [Integrate Visual Studio Code with Git](#integrate-visual-studio-code-with-git) below. 

    Then save and close the file (`Ctrl+O` to save and `Ctrl+X` to exit in nano). On Windows, you can use `Notepad` or any text editor to create the `config` file in the `.ssh` directory.

    Make sure to replace the paths with the correct paths to your SSH keys if you used different names or locations.

1. Set the correct permissions for the SSH config file and the private keys to ensure they're secure. If you are using macOS or Linux, run the following commands in your terminal:

    ```bash
    chmod 600 ~/.ssh/config
    chmod 600 ~/.ssh/id_ed25519_github
    chmod 600 ~/.ssh/id_ed25519_gitlab
    ```

    Windows handles permissions differently and are normally set to only allow access to the user, but ensure that the private keys aren't accessible to other users.

1. You've set a passphrase for the SSH keys, so you'll need to enter it every time you use a key. To avoid this, you can use an SSH agent to cache your passphrase. Follow the instructions below to start the SSH agent and add your keys.

    <div class="grid cards one-column" markdown>
    
    -   :material-clock-fast:{ .lg .middle } __Adding SSH keys__

        === "macOS using Homebrew"

            1. macOS normally starts an SSH agent for you automatically. Add your SSH private keys to it:

                ``` bash
                ssh-add ~/.ssh/id_ed25519_github
                ssh-add ~/.ssh/id_ed25519_gitlab
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
            2. Back in your normal (non-administrator) PowerShell window, add your SSH private keys to the agent:

                ``` powershell
                ssh-add $env:USERPROFILE\.ssh\id_ed25519_github
                ssh-add $env:USERPROFILE\.ssh\id_ed25519_gitlab
                ```

        === "Linux (Ubuntu/Debian) using bash"

            1. Add your SSH private keys to the running SSH agent:

                ``` bash
                ssh-add ~/.ssh/id_ed25519_github
                ssh-add ~/.ssh/id_ed25519_gitlab
                ```

                Unlike macOS, Linux doesn't always start an SSH agent automatically. If the command above fails with an error about not being able to connect to the agent, start one first, then repeat the command above:

                ``` bash
                eval "$(ssh-agent -s)"
                ```
    </div>

!!! Note "Essential Practice Moving Forward"
    When cloning repositories from now on, always use the SSH address, never the HTTPS address.

    * **Use:** `git clone git@github.com:username/repo.git`
    * **Avoid:** `https://github.com/username/repo.git`

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
                stays valid until you delete it, so there is nothing to set. The
                date that *does* need attention on GitHub is the one on the personal
                access token you create in
                [Fork the prodockit-template](#fork-the-prodockit-template) below.

    </div>

1. Test the SSH connection to GitHub and GitLab to ensure that the keys are working correctly. Run the following commands in your terminal:

    ```bash
    ssh -T git@github.com
    ssh -T git@gitlab.com
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

## Fork and cloning the prodockit-template

Forking the documentation template creates a copy of the template into your own GitLab or GitHub cloud account. You will then be able to edit the template locally in Visual Studio Code and publish your own documentation website.

Cloning the documentation template creates a local copy of the template on your computer. You will then be able to edit the template locally in Visual Studio Code and publish your own documentation website.

| Feature | Fork | Clone |
|----|----|---|
| Where's the copy made? | On the remote host (GitHub / GitLab) | On your local computer |
| Is it a Git command? | No (It's a web platform feature) | Yes (git clone `<url>`) |
| Who owns the target? | You (it's copied to your account) | You (it's on your machine) |
| Can you push to it? | Yes | Yes (if you have write access to the remote source) |
| Primary purpose | To propose changes to a project you don't own | To actually do development work, write code, and make commits |
/// table-caption | <
Fork and Clone Comparison at a Glance
///

The features of forking and cloning are complementary. You can fork a repository to create your own copy on the remote host, and then clone that fork to your local machine to work on it. The standard workflow is:

1. **Fork:** You find a project on GitHub. You click the Fork button on the website (or run `gh repo fork`/`glab repo fork` from your terminal instead - see [Fork the prodockit-template](#fork-the-prodockit-template) below). Now, you have a copy at `github.com/your-username/project`.
2. **Clone:** You run `git clone git@github.com:your-username/project.git` in your terminal. Now, the code is on your laptop.
3. **Work:** You write code, make local commits, and test your changes.
4. **Push:** You run `git push origin main` to send your local changes back up to your cloud fork.
5. **Pull Request:** You go back to the GitHub website and open a Pull Request, asking the original project owner to pull the changes from your fork into their original repository.

!!! Note
    In this case, you will be creating your own documentation website, so you won't be submitting a pull request to the original repository. You will be working on your own forked copy of the documentation template.

### Fork the prodockit-template

You may already have a GitLab or GitHub repository containing a Zensical template provided for you. If you do, you can skip this section and go to the next section to clone the repository locally.

This section forks the repository entirely from your terminal over SSH, using the \index{Git!GitHub CLI} (`gh`) or \index{Git!GitLab CLI} (`glab`), instead of clicking through the website.

1. Install the command line tool for whichever host your course uses.

    | OS | GitHub CLI (`gh`) | GitLab CLI (`glab`) |
    |---|---|---|
    | macOS (Homebrew) | `brew install gh` | `brew install glab` |
    | Windows 11 (PowerShell) | `winget install GitHub.cli` | `winget install GitLab.GLab` |
    | Linux (Ubuntu/Debian) | `sudo apt install gh` | `sudo apt install glab` |

    !!! Tip
        If `gh`/`glab` isn't packaged for your Linux distribution yet, see the [GitHub CLI](https://github.com/cli/cli/blob/trunk/docs/install_linux.md){target="_blank"} or [GitLab CLI](https://gitlab.com/gitlab-org/cli#installation){target="_blank"} install docs for an up-to-date package repository to add.

1. Generate a personal access token in your browser. The CLI needs one to talk to
   the host's API - your SSH key covers `git push` and `git pull`, but not creating
   or configuring a repository.

    === "GitLab"

        1. Log in to your **GitLab** account in a web browser.
        2. In the top-right corner, click on your **profile avatar** and select **Edit profile**.
        3. On the left-hand sidebar, select **Access > Access tokens**.
        4. Click **Add new token**{: .bg-blue} and fill out the following details:
            * **Token name:** Give it a clear name (e.g., glab CLI).
            * **Expiration date:** As with your SSH key, set this well into the
              future - the end of your course or project. GitLab will not let you
              leave it empty.
            * **Select scopes:** Tick **api**. This is the one the CLI needs; leave
              the rest unticked.
        5. Click **Create personal access token**{: .bg-blue}.
        6. **Copy the token now.** GitLab shows it exactly once - if you navigate away
           without copying it, you have to delete it and start again.

    === "GitHub"

        1. Log in to your **GitHub** account in a web browser.
        2. In the top-right corner, click on your **profile avatar** and select **Settings**.
        3. On the left-hand sidebar, scroll to the bottom and select **Developer settings**.
        4. Select **Personal access tokens > Tokens (classic)**, then
           **Generate new token > Generate new token (classic)**.
        5. Fill out the following details:
            * **Note:** Give it a clear name (e.g., gh CLI).
            * **Expiration:** Set this well into the future - the end of your course
              or project. Choosing **No expiration** works but GitHub will warn you
              against it.
            * **Select scopes:** Tick **repo**, **workflow**, **read:org** and
              **admin:public_key**. These are what `gh auth login` asks for.
        6. Click **Generate token**{: .bg-green}.
        7. **Copy the token now.** GitHub shows it exactly once.

    !!! warning "Treat the token like a password"
        A personal access token acts as your account. Don't paste it into a
        document, a chat message, or your repository - if you ever do, delete it on
        the website straight away and generate a new one.

1. Authenticate the CLI with your account, using the token from the previous step and
   choosing **SSH** as the Git protocol when prompted - SSH reuses the same keys you
   set up in [Generate and configure ssh keys for Git](#generate-and-configure-ssh-keys-for-git).

    === "GitLab"

{% if is_surrey %}
        ``` bash
        glab auth login --hostname gitlab.surrey.ac.uk --git-protocol ssh
        ```

        Use `--hostname gitlab.com` instead if you are working with a project on the public GitLab rather than the University of Surrey instance.
{% else %}
        ``` bash
        glab auth login --hostname gitlab.com --git-protocol ssh
        ```

        Use your own GitLab instance's hostname instead if your course uses a self-hosted GitLab, for example `gitlab.surrey.ac.uk`.
{% endif %}

        The command then asks you a short series of questions:

        1. **How would you like to login?** Choose **Token**.
        2. **Paste your authentication token:** Paste the token you copied above.
           Nothing appears as you paste - that is deliberate, not a failure.
        3. **Choose default git protocol:** Choose **SSH**.
        4. **Authenticate Git with your GitLab credentials?** Answer **Yes**.

        You should finish with a confirmation like:

        ``` text
        ✓ Logged in as your-username
        ```

        Check it any time with:

        ``` bash
        glab auth status
        ```

    === "GitHub"

        ``` bash
        gh auth login --hostname github.com --git-protocol ssh
        ```

        The command then asks you a short series of questions:

        1. **What account do you want to log into?** Choose **GitHub.com**.
        2. **What is your preferred protocol for Git operations?** Choose **SSH**.
        3. **Upload your SSH public key to your GitHub account?** Choose the key you
           generated earlier (e.g. `~/.ssh/id_ed25519_github.pub`), or **Skip** if you
           already added it in the previous section.
        4. **How would you like to authenticate?** Choose
           **Paste an authentication token**.
        5. Paste the token you copied above. Nothing appears as you paste - that is
           deliberate, not a failure.

        You should finish with a confirmation like:

        ``` text
        ✓ Logged in as your-username
        ```

        Check it any time with:

        ``` bash
        gh auth status
        ```

1. Fork the repository and clone it in the same step. Use whichever tab matches the host your course uses.

    === "GitLab"

{% if is_surrey %}
        ``` bash
        glab repo fork gitlab.surrey.ac.uk/mb0105/prodockit-template --name cw1-az1234 --path your-group/cw1-az1234 --clone
        ```

        This forks the University of Surrey copy of the template, [https://gitlab.surrey.ac.uk/mb0105/prodockit-template](https://gitlab.surrey.ac.uk/mb0105/prodockit-template){target="_blank"}. Replace `cw1-az1234` with the project name your course tutor specifies, and `your-group` with the namespace they direct you to fork into (leave `--path` off entirely to fork into your own personal namespace instead).
{% else %}
        ``` bash
        glab repo fork gitlab.com/your-group/prodockit-template --name cw1-az1234 --path your-group/cw1-az1234 --clone
        ```

        Replace `gitlab.com/your-group/prodockit-template` with the actual GitLab instance and path your course uses, `cw1-az1234` with the project name your course tutor specifies, and `your-group` with the namespace they direct you to fork into (leave `--path` off entirely to fork into your own personal namespace instead).
{% endif %}

        Then open the new project on the website and go to **Settings > General > Visibility, project features, permissions**, and change **Project visibility** to **Private** - `glab` has no command line switch for this yet.

    === "GitHub"

        ``` bash
        gh repo fork buckwem/prodockit-template --fork-name cw1-your-username --clone
        ```

        Replace `cw1-your-username` with the repository name your coursework specifies.

        Then set the fork to private, and switch on GitHub Pages - neither exists yet on a fresh fork, and Pages must exist before the `docs.yml` workflow's first run, or it fails with `Get Pages site failed... Not Found`:

        ``` bash
        gh repo edit your-username/cw1-your-username --visibility private --accept-visibility-change-consequences
        gh api repos/your-username/cw1-your-username/pages -X POST -f build_type=workflow
        ```

        Replace `your-username`/`cw1-your-username` with your own account and the repository name from the previous command. If the `gh api` call fails, set this up on the website instead: **Settings > Pages**, then change **Build and deployment > Source** from **Deploy from a branch** to **GitHub Actions**.

    Both commands clone the new fork straight into a `cw1-az1234`/`cw1-your-username` folder in your current directory - you don't need [Clone the prodockit-template](#clone-the-prodockit-template) below unless you skipped forking entirely (see the note at the top of this section).

!!! Warning
    Don't forget to set the visibility to private, otherwise others can see your repository. Ask someone else to check whether they can see your repository.

### Clone the prodockit-template

If you forked using `glab`/`gh repo fork --clone` above, you already have a local copy from that step - skip this section entirely. Otherwise (you were given an existing repository, or forked some other way), this section clones the template into your own local device. You will then be able to edit the template locally in Visual Studio Code and eventually publish your own documentation website.

1. Start with creating a directory for all your *GitLab* or *GitHub* projects on your local desktop. For example, create a directory called 'GitLab' in your OneDrive directory.
    
    !!! Tip
        Using OneDrive will give you an additional backup of your GitLab repository.

1. Open a terminal (Terminal on macOS/Debian, Git Bash or PowerShell on Windows 11) and navigate to the directory you created in the previous step.

1. Then run the following command to clone the documentation template into your local directory. Use whichever tab matches the host your course uses.

    === "GitLab"

{% if is_surrey %}
        ``` bash
        git clone git@gitlab.surrey.ac.uk:mb0105/prodockit-template.git
        ```

        This clones the University of Surrey copy of the template.
{% else %}
        ``` bash
        git clone git@gitlab.com:your-group/prodockit-template.git
        ```

        Replace `your-group` with the namespace your course uses on `gitlab.com`, or swap the whole host for your own self-hosted GitLab.
{% endif %}

    === "GitHub"

        ``` bash
        git clone git@github.com:buckwem/prodockit-template.git
        ```

    If you were given your own repository, or forked the template earlier, clone that
    instead - replace the address above with `git@git_website:username/your-repo.git`,
    where `git_website` is your host (for example `gitlab.com` or
    `github.organisation.com`) and `username` is your own account name.

    !!! Tip
        You can find your `username` by logging into your GitLab or GitHub account and clicking on your profile picture at the top right corner of the page. On **GitLab** your username is **below** your name in the dropdown menu. On **GitHub** your username is **above** your name in the dropdown menu.

1. Rename the directory to something meaningful for your own report. Cloning leaves you
   with a folder called `prodockit-template`, which says nothing about whose work it
   holds - and if you clone a second project later, you will not be able to tell them
   apart.

    ``` bash
    mv prodockit-template report-az1234
    ```

    Replace `report-az1234` with a name that identifies your own work - your username,
    your coursework code, or whatever your course tutor specifies.

    !!! note "Renaming the folder doesn't rename the repository"
        This changes only the folder on your own machine. The project's name on GitLab
        or GitHub is unaffected, and so is the `origin` remote inside it - `git push`
        and `git pull` carry on working exactly as before.

## Install Python and Zensical

Brief instructions for installing \index{Python} are below for macOS, Windows 11, and Linux (Ubuntu/Debian). However, it's recommended to refer to the [official Python installation documentation](https://docs.python.org/3/using/) for your operating system. 

If you already have Python installed, you can check the version by running the following command in your terminal or command prompt:

```bash
python --version
```

!!! Note
    You may need to use 'python3' and 'pip3' instead of 'python' and 'pip' depending on your system configuration.

The instructions below are for installing Python 3.8 or later. If you have an older version, please update to Python 3.8 or later.

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

Close VS Code and reopen it in the project folder to ensure that the virtual environment is activated. If the Terminal is not open at the bottom, select the menu Terminal -> New Terminal. You should see the command 'source /home/buckwem/prodockit-template/.venv/bin/activate' in the terminal. If you don't see this, you may need to activate the virtual environment manually by running the command `source .venv/bin/activate` (macOS/Linux) or `.venv\Scripts\Activate.ps1` (Windows PowerShell).

### Install Zensical Studio and other plugins

Now we'll install the \index{VS Code!Zensical Studio} plugin for Visual Studio Code, which provides a set of tools to help you work with Zensical projects, including commands to build and preview your site. Then we'll install a couple of other useful plugins for working with Markdown and TOML files.

1. Start by opening Visual Studio Code and navigating to the Extensions view by clicking on the Extensions icon in the Activity Bar on the side of the window or pressing `Ctrl+Shift+X`/`Cmd+Shift+X`.
1. Install the **Python** extension (published by Microsoft) by searching for "Python" in the Extensions view and clicking **Install**{: .bg-blue}. As well as Python support, this is what makes VS Code notice the `.venv` folder in your project and activate the virtual environment automatically in every new terminal - so you don't have to run `source .venv/bin/activate` by hand each time you open one.

    !!! Tip
        Check it worked by opening a new terminal (**Terminal > New Terminal**) - the prompt should start with `(.venv)`. If it doesn't, reopen VS Code in the project folder, then choose **Python: Select Interpreter** from the Command Palette (`Ctrl+Shift+P`/`Cmd+Shift+P`) and pick the one inside `.venv`.

1. Install the **Zensical Studio** extension by searching for "Zensical Studio" in the Extensions view and clicking **Install**{: .bg-blue} and then **Trust Publisher and Install**{: .bg-blue} when prompted. This extension provides a set of tools to help you work with Zensical projects, including commands to build and preview your site.
1. Follow the instructions on the Zensical Studio plugin page to configure the extension. Add to the `.vscode/settings.json` file in your project directory the following lines:

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

## Where to go next {: #installtooling-where-to-go-next }

You now have Visual Studio Code, Git, and Zensical installed, and your own copy of the documentation template cloned locally. Continue to [Start editing](startediting.md) to preview your changes locally and publish them to GitLab or GitHub.