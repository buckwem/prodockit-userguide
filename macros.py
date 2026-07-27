# Copyright (c) 2025-2026 Mark Buckwell and contributors
# SPDX-License-Identifier: MIT

"""This site has no branding switch, so this just re-exports
prodockit.zensical_macros.define_env() - word count, repo URL, release
tag, and heading/reference-style numbering, needed by
acronyms.md/glossary.md/references.md's {{ acronym_style() }}/
{{ glossary_style() }}/{{ reference_style() }} calls, and docs/index.md's
{{ release }} cover-page line.

`release` used to be computed locally here, before prodockit-extensions#116
promoted the identical logic into prodockit.zensical_macros itself -
requires prodockit>=0.11.0 (see requirements.txt).

Called directly here rather than via zensical.toml's documented
`modules = [...]` extension option: that option makes Zensical also watch
the module's file for auto-reload, and if the module lives outside the
project directory (true for any pip-installed package, e.g. in CI where
dependencies install outside the checkout) that watch triggers an upstream
panic in `zensical build`'s file watcher (zensical/zensical#823). Calling it
as a plain import instead gives identical behaviour without that second
watch registration."""

from prodockit.zensical_macros import define_env as define_env
