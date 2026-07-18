# Copyright (c) 2025-2026 Mark Buckwell and contributors
# SPDX-License-Identifier: MIT

"""Unlike prodockit-template's own macros.py, this site has no branding
switch, so most of this just re-exports prodockit.zensical_macros.
define_env() - word count, repo URL, and heading/reference-style numbering,
needed by acronyms.md/glossary.md/references.md's {{ acronym_style() }}/
{{ glossary_style() }}/{{ reference_style() }} calls. The one addition is
`release`, used on the cover page (docs/index.md) - this project has no
build_pdf.py of its own to fetch a release tag from a host API, so it's
computed locally from git instead, resolving identically for the website
and for `prodockit pdf` since both render through this same macro
environment.

Called directly here rather than via zensical.toml's documented
`modules = [...]` extension option: that option makes Zensical also watch
the module's file for auto-reload, and if the module lives outside the
project directory (true for any pip-installed package, e.g. in CI where
dependencies install outside the checkout) that watch triggers an upstream
panic in `zensical build`'s file watcher (zensical/zensical#823). Calling it
as a plain import instead gives identical behaviour without that second
watch registration."""

import subprocess

from prodockit.zensical_macros import define_env as _prodockit_define_env


def _get_release() -> str:
    """Latest git tag reachable from HEAD (e.g. "0.1.0"), or "" if this
    checkout has no tags at all - same defensive shell-out pattern as
    prodockit.zensical_macros._get_repo_url()."""
    try:
        return (
            subprocess.check_output(
                ["git", "describe", "--tags", "--abbrev=0"],
                stderr=subprocess.DEVNULL,
            )
            .decode("utf-8")
            .strip()
        )
    except Exception:
        return ""


def define_env(env):
    _prodockit_define_env(env)
    env.variables["release"] = _get_release()
