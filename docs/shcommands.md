---
icon: lucide/book-open
---

<!--
# Copyright (c) 2025-2026 Mark Buckwell and contributors
# SPDX-License-Identifier: MIT
-->

{{ heading_counter_reset(page) }}

# Shell commands

This page is for macOS and Linux users who have not used a command line before.
It explains the small set of \index{Shell commands} used elsewhere in this guide.
macOS normally uses \index{Shell commands!zsh} **zsh** and Ubuntu normally uses
\index{Shell commands!bash} **bash**; the commands on this page work in both.

You do not need to memorise them. Keep this page open, copy one command at a
time, and check what happened before continuing.

!!! warning "Commands act immediately"
    A terminal does not normally put deleted files in the Trash or ask you to
    confirm every change. Do not add `sudo`, `-f`, or `-r` to a command unless
    the instructions explicitly require it and you understand the target.

## Understand the prompt

When the terminal is waiting for a command, it displays a prompt similar to:

``` text
(.venv) mark@macbook my-report %
```

The prompt provides context:

- `(.venv)` means the project's Python virtual environment is active.
- `mark@macbook` identifies the user and computer.
- `my-report` is usually the current directory.
- `%` is a common macOS prompt marker; Ubuntu often uses `$` instead.

Do **not** type the prompt itself. If an instruction shows:

``` console
$ zensical serve
```

type only:

``` bash
zensical serve
```

Press `Enter` to run it. Most successful shell commands print little or
nothing; the next prompt means the command has finished.

## Understand a command

A command normally consists of a program name followed by options and
arguments:

``` text
command  option  argument
ls       -la     docs
```

- The **command** selects the program to run.
- An **option** changes its behaviour and commonly starts with `-` or `--`.
- An **argument** tells it what to work on, such as a file or directory.

Words such as `PROJECT-DIRECTORY`, `FILE`, and `USERNAME` in this guide are
placeholders. Replace them with your own value; do not type the capitalised
placeholder or its surrounding angle or square brackets.

Shell commands are case-sensitive. `Docs`, `docs`, and `DOCS` can be three
different names. Spaces also separate arguments, so put a path containing a
space inside quotes:

``` bash
cd "/Users/mark/My Documents/report"
```

Use straight quotes copied from a code block, not typographic “smart quotes”.

## Understand paths

A \index{Shell commands!path} path tells a command where a file or directory is.
These short forms are used throughout the guide:

| Path | Meaning |
|---|---|
| `/` | The top of the filesystem. |
| `~` | Your home directory, such as `/Users/mark` or `/home/mark`. |
| `.` | The current directory. |
| `..` | The current directory's parent. |
| `docs/index.md` | A path relative to the current directory. |
| `/home/mark/report/docs/index.md` | An absolute path starting at `/`. |
/// table-caption | <
    attrs: {id: table-path-forms}

Common path forms
///

The forward slash `/` separates directories on both macOS and Linux.

## Find and change the current directory

The **current directory** is the directory a command works from unless you give
it another path. Before running a project command, confirm that you are in the
project directory—the one containing `zensical.toml` or `mkdocs.yml`.

| Command | What it does |
|---|---|
| \index{Shell commands!`pwd`} `pwd` | Prints the full path of the current directory. |
| \index{Shell commands!`ls`} `ls` | Lists the visible files and directories here. |
| `ls -la` | Also shows hidden entries such as `.venv` and `.git`. |
| `cd DIRECTORY` | Changes to `DIRECTORY`. |
| `cd ..` | Moves to the parent directory. |
| `cd ~` | Returns to your home directory. |
/// table-caption | <
    attrs: {id: table-navigation-commands}

Navigation commands
///

A safe way to start a session is:

``` bash
cd "/path/to/your/project"
pwd
ls
```

Read the output from `pwd` and `ls`. Continue only when you can see the expected
configuration file.

!!! tip "Use Tab completion"
    Type the first few characters of a file or directory, then press `Tab`.
    The shell completes an unambiguous name, reducing typing and spelling
    errors. Press `Tab` twice to see possible matches.

## Activate the project environment

Prodockit and Zensical are installed inside the project's `.venv` directory.
After changing to the project directory, activate it with:

``` bash
source .venv/bin/activate
```

The prompt gains a `(.venv)` prefix. Activation applies only to this terminal
window; repeat it after opening a new one.

Useful checks are:

``` bash
command -v python
python --version
command -v prodockit
prodockit --version
```

`command -v` prints the program that the shell will run. For the project Python
and prodockit commands, the path should normally pass through the project's
`.venv` directory.

Run `deactivate` when you deliberately want to leave the environment. Closing
the terminal also ends it.

## Create, copy, move, and remove files

Prefer your editor, Finder on macOS, or Files on Ubuntu for ordinary file
management. When a guide asks you to use the shell, these commands are the
common ones:

| Command | What it does |
|---|---|
| `mkdir NAME` | Creates a directory called `NAME`. |
| `mkdir -p PATH` | Creates a path and any missing parent directories. |
| `cp SOURCE DESTINATION` | Copies one file. |
| `cp -R SOURCE DESTINATION` | Copies a directory and its contents. |
| `mv SOURCE DESTINATION` | Moves or renames a file or directory. |
| `rm -i FILE` | Asks before permanently removing one file. |
| `rmdir DIRECTORY` | Removes an empty directory. |
/// table-caption | <
    attrs: {id: table-file-directory-commands}

File and directory commands
///

Before copying, moving, or removing anything, use `pwd` and `ls` to verify the
source and destination. Put paths containing spaces in quotes.

!!! danger "Avoid recursive forced deletion"
    `rm -rf` removes a directory tree without confirmation. A typing mistake
    can delete an entire project or home directory. It is intentionally not
    part of the normal workflow in this guide; use Finder or Files when you
    need a recoverable deletion.

## Read a text file

| Command | What it does |
|---|---|
| `cat FILE` | Prints a short file in full. |
| `less FILE` | Opens a longer file for scrolling; press `q` to leave. |
| `head -n 20 FILE` | Prints its first 20 lines. |
| `tail -n 20 FILE` | Prints its last 20 lines. |
| `nl -ba FILE` | Prints it with line numbers, including blank lines. |
/// table-caption | <
    attrs: {id: table-reading-files}

Commands for reading files
///

These commands do not edit the file. For example:

``` bash
less zensical.toml
```

Inside `less`, use the arrow keys or Page Up/Page Down to move, type `/word` to
search, press `n` for the next match, and press `q` to return to the prompt.

## Edit a text file {: #editing-files }

Use your normal editor for document work. If an installation instruction asks
you to change a small configuration file directly in the terminal, `nano` is a
beginner-friendly editor available on macOS and Ubuntu:

``` bash
nano FILE
```

Replace `FILE` with the path from the instruction. Inside `nano`:

- Type and use the arrow keys as you would in a simple text editor.
- Press `Ctrl+O`, then `Enter`, to save the file.
- Press `Ctrl+X` to leave.
- If it asks whether to save modified content, press `Y` to save or `N` to
    discard it, then follow the filename prompt.

The `^` shown in nano's shortcut bar means `Ctrl`; `^X` therefore means
`Ctrl+X`. Do not use `sudo nano` unless the relevant platform instructions
explicitly include `sudo`.

## Find files and text

Use `find` to locate a file and \index{Shell commands!`grep`} `grep` to locate text
inside files:

``` bash
find . -name "*.md"
grep -n "site_name" zensical.toml
grep -R -n "old wording" docs
```

- `find .` starts in the current directory.
- `*.md` means every name ending in `.md`; quotes stop the shell expanding it
    before `find` receives it.
- `grep -n` includes line numbers.
- `grep -R` searches through subdirectories.

A pipe, written `|`, sends the output of one command into another. This example
shows only Markdown files whose paths contain `install`:

``` bash
find . -name "*.md" | grep "install"
```

## Control a running command

Some commands, including `zensical serve`, deliberately keep running. The
terminal is not stuck merely because no new prompt appears.

| Key | What it does |
|---|---|
| `Ctrl+C` | Stops the command currently running in the terminal. |
| `Ctrl+L` | Clears the visible screen without deleting command history. |
| `Up` / `Down` | Moves through commands previously entered. |
| `Left` / `Right` | Edits the current command before it is run. |
| `Tab` | Completes a command or path where possible. |
/// table-caption | <
    attrs: {id: table-terminal-keys}

Useful terminal keys
///

If the prompt changes to `quote>`, `dquote>`, or `>`, the shell is usually
waiting for a closing quote or bracket. Press `Ctrl+C` to abandon the incomplete
command, then enter it again carefully.

## Use administrator access carefully

`sudo COMMAND` runs a command with administrator privileges. Use it only when a
platform-specific instruction in this guide includes it—for example, Ubuntu's
`apt` package installation. Do not add it merely because another command
reported an error.

When `sudo` asks for your password, the terminal shows no characters, dots, or
asterisks while you type. That is normal. Type the password and press `Enter`.

!!! warning
    Do not run `sudo pip`, `sudo prodockit`, or `sudo zensical`. Python packages
    belong in the activated virtual environment and do not need administrator
    access.

## Understand common errors

### `command not found`

Check the spelling. If the missing command is `prodockit`, `zensical`, or
`python`, change to the project directory and activate `.venv`. If an installer
has just changed `PATH`, open a new terminal and activate `.venv` again.

### `No such file or directory`

Run `pwd` and `ls` to check your location and the exact spelling and case of the
path. Quote a path containing spaces.

### `Permission denied`

First check that the path is correct and belongs to you. Do not immediately
retry with `sudo`; the command may be targeting a system file or the wrong
directory. Follow the relevant installation instructions when administrator
access is genuinely required.

### A command prints nothing

Many commands report errors but say nothing on success. Run a read-only check
such as `ls`, `git status`, or the `--version` command given by the instructions
to confirm the expected result.

## Where to go next {: #shcommands-where-to-go-next }

Return to [Start editing](startediting.md) and use this page whenever a command
or path is unfamiliar. Continue to [Document appearance and structure](customise.md) when you are
comfortable previewing, building, and saving routine document changes.
