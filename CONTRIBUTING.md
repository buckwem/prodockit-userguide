<!--
# Copyright (c) 2025-2026 Mark Buckwell and contributors
# SPDX-License-Identifier: MIT
-->

# Contributing

Thanks for your interest in improving the prodockit User Guide. This is the full setup, authoring, customisation, and testing guide for [prodockit-template](https://github.com/buckwem/prodockit-template) and other Zensical projects built on the [prodockit](https://github.com/buckwem/prodockit-extensions) package - hosted independently of any individual fork, so it can be kept current without every existing fork being stuck with whatever it looked like the day it was forked. If you're a student using the template to write your own assignment, you don't need any of this: just follow the guide itself at <https://buckwem.github.io/prodockit-userguide/>.

## Before you start

For anything beyond a small fix (typos, broken links), please open an issue first to discuss the change. This avoids duplicated effort and lets us agree on the approach before you spend time on an implementation.

## Getting set up

1. Fork the repository and clone your fork.
2. Install Python 3.14, create the project environment, and activate it:

   ```bash
   python3.14 -m venv .venv
   source .venv/bin/activate
   python --version
   ```

   On Windows, use `py -3.14 -m venv .venv` followed by
   `.\.venv\Scripts\Activate.ps1`. The version check must report Python 3.14.
   If you use Conda, Poetry, uv, or another environment manager, adapt these
   and the remaining package commands for that environment.
3. Install the Python prerequisites into the active environment:

   ```bash
   python -m pip install -r requirements.txt
   ```
4. Preview the site locally: `zensical serve`. Website maths uses the committed
   MathJax configuration and Zensical's browser runtime, without npm.
5. Make a clean, strict website build with `zensical build --clean --strict`.
   If your change affects the PDF, run `pdk pdf` afterwards. It reads the
   completed site and prepares project-local renderers on first use. PDF maths
   requires Node.js on `PATH`; no npm packages or browser are required.

## Making a change

1. Create a branch off `main` for your change.
2. Make your change and verify it locally:
   - Website changes: `zensical serve` and check the page in a browser.
   - PDF-affecting changes: run `zensical build --clean --strict`, then `prodockit pdf`, and check `docs/site_documentation.pdf`.
   - Prose changes: optionally run `vale docs/` if you have [Vale](https://vale.sh/) installed (see [Install vale to check for grammar, spelling, and style issues](https://buckwem.github.io/prodockit-userguide/additionaltooling/) in the User Guide); it's not enforced in CI.
   - Before opening a pull request with website or documentation changes, make sure the strict website build has completed before the PDF build. Keep `zensical serve` for interactive previewing; the strict build additionally fails on broken internal links, missing anchors, and other validation warnings.
3. Open a pull request against `main`. `main` is protected, so all changes - including from maintainers - go through a reviewed PR.
4. Reference the issue your PR addresses (e.g. `Fixes #123`) where applicable.

## Reporting bugs and requesting features

During release cascades, keep `.prodockit-toolchain.toml`, `requirements.txt`
and CI declarations aligned using `prodockit pins`. The manifest records the
supported combination; the explicit Markdown requirement prevents an immediate
Adopt alignment after installation.

Please use the issue templates when opening an issue - they help make sure we get the information needed to act on it.

## License

By contributing, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).
