# Copyright (c) 2025-2026 Mark Buckwell and contributors
# SPDX-License-Identifier: MIT

"""This project's own Zensical macros - institution branding (Surrey vs.
default). Everything else the guide needs (word count, repo URL, release
tag, and heading/reference-style numbering for acronyms.md/glossary.md/
references.md's {{ acronym_style() }}/{{ glossary_style() }}/
{{ reference_style() }} calls, plus docs/index.md's {{ release }}
cover-page line) comes from prodockit.zensical_macros, not duplicated here.

prodockit.zensical_macros.define_env() is called directly below rather than
via zensical.toml's documented `modules = [...]` extension option: that
option makes Zensical also watch the module's file for auto-reload, and if
the module lives outside the project directory (true for any pip-installed
package, e.g. in CI where dependencies install outside the checkout) that
watch triggers an upstream panic in `zensical build`'s file watcher
(zensical/zensical#823). Calling it as a plain import instead gives
identical behaviour without that second watch registration - remove this
workaround and switch back to `modules = [...]` in zensical.toml once that
is fixed upstream.

The branding logic mirrors prodockit-template's, including the hostname
fix from prodockit-template#132/#133 - see _host_is_surrey() below.
"""

import os
import shutil
import subprocess
from pathlib import Path

from prodockit.zensical_macros import define_env as _prodockit_define_env

TARGET_DOMAIN = "surrey.ac.uk"


def _host_is_surrey(host):
    """True if `host` is the Surrey domain itself or a host beneath it.

    A hostname comparison rather than a substring one, because that is what
    CI_SERVER_HOST holds. prodockit-template originally compared it with
    `==` against 'surrey.ac.uk', which could never match - GitLab sets
    CI_SERVER_HOST to the instance hostname, and Surrey's is
    'gitlab.surrey.ac.uk' - so that branch silently never ran (see
    prodockit-template#132). Carried here in its fixed form rather than
    copying the original.

    A plain substring test, the obvious alternative, would wrongly accept
    'notsurrey.ac.uk' and 'surrey.ac.uk.example.com'.

    Kept as its own function so the comparison can be tested directly: the
    checks in _detect_is_surrey() read the git remote and Zensical's
    config, so testing that as a whole gives a different answer depending
    on which clone it runs in - which is exactly how the original defect
    stayed invisible.
    """
    host = (host or "").strip().lower().rstrip(".")
    return host == TARGET_DOMAIN or host.endswith("." + TARGET_DOMAIN)


def _detect_is_surrey(env=None):
    """True if this checkout appears to be building for the University of
    Surrey - checked via the GitLab CI/CD pipeline's own CI_SERVER_HOST env
    var, the local git remote (covers `zensical serve` on a locally-cloned
    Surrey checkout), and - when env is given - a scan of Zensical's config
    as a fallback.

    Extracted as a standalone function (rather than inlined in define_env()
    below) so the test suite can call the exact same detection logic instead
    of hardcoding an assumption about which remote CI happens to be running
    against.
    """
    # Check 1: GitLab CI/CD pipeline environment.
    if _host_is_surrey(os.getenv("CI_SERVER_HOST")):
        return True

    # Check 2: local git remote - covers `zensical serve` on a Surrey clone.
    try:
        remote_url = (
            subprocess.check_output(
                ["git", "config", "--get", "remote.origin.url"],
                stderr=subprocess.DEVNULL,
            )
            .decode("utf-8")
            .strip()
        )
        if TARGET_DOMAIN in remote_url:
            return True
    except Exception:
        # git missing or no remote configured - fall through rather than fail
        # the build; the other checks still apply.
        pass

    # Check 3: whatever Zensical's own config says, as a last resort.
    if env is not None:
        if hasattr(env, "config") and TARGET_DOMAIN in str(env.config):
            return True
        if hasattr(env, "variables") and TARGET_DOMAIN in str(env.variables):
            return True

    return False


def _apply_branding_logos(is_surrey):
    """Copies the chosen logo pair over the active logo_black/white.png.

    docs/stylesheets/extra.css points `.md-logo img`'s `content` at these
    two files by relative url(), so overwriting them is what actually
    changes the header logo. That only works because they are real files:
    this stylesheet used to inline them as base64 data: URIs, which would
    have made this copy a silent no-op. prodockit.pdf's own
    _inline_css_urls() re-inlines them for the PDF build, so the relative
    references cost nothing there.
    """
    source = "logo_surrey" if is_surrey else "logo_default"
    assets = Path("docs/assets")
    try:
        assets.mkdir(parents=True, exist_ok=True)
        for variant in ("black", "white"):
            shutil.copy2(assets / f"{source}_{variant}.png", assets / f"logo_{variant}.png")
        print(f"[Zensical Startup] Applied {'Surrey' if is_surrey else 'default'} branding logos.")
    except FileNotFoundError as error:
        print(f"[Zensical Startup Warning] Could not copy logos: {error}")
        print("Ensure logo_surrey_*.png and logo_default_*.png exist in docs/assets/")


def define_env(env):
    _prodockit_define_env(env)

    is_surrey = _detect_is_surrey(env)
    env.variables["is_surrey"] = is_surrey
    _apply_branding_logos(is_surrey)
