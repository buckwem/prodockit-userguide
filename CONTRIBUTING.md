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
2. Install the Python prerequisites: `pip install -r requirements.txt`.
3. Preview the site locally: `zensical serve`.
4. If your change affects the PDF build, also run `prodockit pdf` - see [Install tooling](https://buckwem.github.io/prodockit-userguide/installtooling/) for the full setup. The one Mermaid diagram in [Diagrams](https://buckwem.github.io/prodockit-userguide/zensicalbasics/#diagrams) only renders as an image in the PDF if `mermaid-cli` (`mmdc`) is available on your `PATH`; without it, the PDF build silently skips it rather than failing.

## Making a change

1. Create a branch off `main` for your change.
2. Make your change and verify it locally:
   - Website changes: `zensical serve` and check the page in a browser.
   - PDF-affecting changes: run `prodockit pdf` and check `docs/site_documentation.pdf`.
   - Prose changes: optionally run `vale docs/` if you have [Vale](https://vale.sh/) installed (see [Install vale to check for grammar, spelling, and style issues](https://buckwem.github.io/prodockit-userguide/additionaltooling/) in the User Guide); it's not enforced in CI.
3. Open a pull request against `main`. `main` is protected, so all changes - including from maintainers - go through a reviewed PR.
4. Reference the issue your PR addresses (e.g. `Fixes #123`) where applicable.

## Reporting bugs and requesting features

Please use the issue templates when opening an issue - they help make sure we get the information needed to act on it.

## License

By contributing, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).
