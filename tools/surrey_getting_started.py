"""Prepare the Surrey-only Getting started pages in an ephemeral checkout.

The committed User Guide stays canonical for GitHub. GitLab CI and local
previews run ``prepare`` in a disposable checkout before Zensical and the PDF
builder, so both outputs see the same source and navigation. Stage 1 copies
the upstream text without changing its GitHub/GitLab instructions.
"""

from __future__ import annotations

import argparse
import json
import os
import posixpath
import re
import subprocess
import sys
import tomllib
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "surrey-source"
MANIFEST = SOURCE / "manifest.toml"
START_MARKER = "# Surrey Getting started overlay (generated; do not commit)\n"
LINK = re.compile(r"(?P<open>!?\[[^\]]*\]\()(?P<url>[^\s)]+)(?P<close>[^)]*\))")
NAV = re.compile(r"^nav = \[\n.*?^\]\n", re.MULTILINE | re.DOTALL)
NUMBERED = re.compile(r"^\d+\.\s+")
SUPPORT_SECTION = re.compile(r"^## Support prodockit\s*$", re.MULTILINE)
REMOTELABS_TAB = '=== ":material-linux: Surrey RemoteLabs"'
STAG_REMOTELABS_TAB = '=== ":stag-stag_icon_32: Surrey RemoteLabs"'


def manifest() -> dict:
    return tomllib.loads(MANIFEST.read_text(encoding="utf-8"))


def page_paths(data: dict) -> list[str]:
    return [item["path"] for item in data["pages"]]


def _safe_path(relative: str) -> PurePosixPath:
    path = PurePosixPath(relative)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise ValueError(f"Unsafe snapshot path: {relative}")
    return path


def verify_snapshot(data: dict) -> None:
    pages = page_paths(data)
    if not pages or pages[0] != "gettingstarted.md" or len(pages) != len(set(pages)):
        raise ValueError("Snapshot must start at a unique gettingstarted.md")
    if len(data["assets"]) != len(set(data["assets"])):
        raise ValueError("Duplicate snapshot asset")
    for relative in [*pages, *data["assets"]]:
        file = SOURCE / "docs" / _safe_path(relative)
        if not file.is_file():
            raise FileNotFoundError(file)
    if not (SOURCE / "LICENSE.md").is_file():
        raise FileNotFoundError(SOURCE / "LICENSE.md")


def _relative_target(page: str, url: str) -> str | None:
    """Return a source-doc-relative Markdown target, or None for other URLs."""
    parsed = urlsplit(url)
    if parsed.scheme or parsed.netloc or not parsed.path.endswith(".md"):
        return None
    target = posixpath.normpath(posixpath.join(posixpath.dirname(page), parsed.path))
    if target == ".." or target.startswith("../"):
        raise ValueError(f"Link leaves the Extensions docs tree: {page}: {url}")
    return target


def rewrite_external_links(markdown: str, page: str, included: set[str]) -> str:
    """Keep links among copied pages local; point other pages to the manual."""

    def replace(match: re.Match[str]) -> str:
        url = match.group("url")
        target = _relative_target(page, url)
        if target is None or target in included:
            return match.group(0)
        parsed = urlsplit(url)
        route = target.removesuffix(".md")
        if route == "index":
            route = ""
        elif route.endswith("/index"):
            route = route.removesuffix("/index")
        absolute = f"https://prodockit.org/{route}/"
        if parsed.query:
            absolute += f"?{parsed.query}"
        if parsed.fragment:
            absolute += f"#{parsed.fragment}"
        return (
            match.group("open")
            + absolute
            + match.group("close")
            + '{target="_blank" rel="noopener"}'
        )

    return LINK.sub(replace, markdown)


def omit_surrey_support_section(markdown: str) -> str:
    """Leave the pinned overview intact but omit its donation subsection."""
    matches = list(SUPPORT_SECTION.finditer(markdown))
    if len(matches) != 1:
        raise ValueError("Expected one Support prodockit section in the pinned overview")
    start = matches[0].start()
    following = re.search(r"^## (?!#)", markdown[matches[0].end() :], re.MULTILINE)
    end = matches[0].end() + following.start() if following else len(markdown)
    removed = markdown[start:end]
    if "Buy me a coffee" not in removed:
        raise ValueError("The support section no longer contains the expected donation link")
    return markdown[:start].rstrip() + "\n\n" + markdown[end:].lstrip()


def use_stag_for_remotelabs(markdown: str) -> str:
    """Use the User Guide's theme-aware stag icon in imported Surrey tabs."""
    return markdown.replace(REMOTELABS_TAB, STAG_REMOTELABS_TAB)


def _render_nav(items: list[dict | str], indent: int = 0) -> str:
    lines = [" " * indent + "["]
    for item in items:
        if isinstance(item, str):
            lines.append(" " * (indent + 2) + json.dumps(item) + ",")
            continue
        title, value = next(iter(item.items()))
        if isinstance(value, list):
            children = _render_nav(value, indent + 2).splitlines()
            lines.append(" " * (indent + 2) + "{" + json.dumps(title) + " = " + children[0].strip())
            lines.extend(children[1:-1])
            lines.append(" " * (indent + 2) + children[-1].strip() + "},")
        else:
            lines.append(" " * (indent + 2) + "{" + json.dumps(title) + " = " + json.dumps(value) + "},")
    lines.append(" " * indent + "]")
    return "\n".join(lines)


def surrey_nav(config: dict, data: dict) -> list[dict]:
    items = config["project"]["nav"]
    groups = {next(iter(item)): item for item in items}
    if not {"Home", "Getting started", "About"}.issubset(groups):
        raise ValueError("Expected User Guide navigation groups are missing")
    start = groups["Getting started"]["Getting started"]
    if len(start) != 2 or start[0] != {"2. Getting started": "gettingstarted.md"}:
        raise ValueError("The canonical Getting started navigation has changed")
    if list(start[1].values()) != ["additionaltooling.md"]:
        raise ValueError("Additional tooling must remain after the imported pages")
    imported = [{item["title"]: item["path"]} for item in data["pages"]]
    groups["Getting started"]["Getting started"] = [*imported, start[1]]

    # About precedes the imported manual in the top menu, but is unnumbered:
    # imported prose refers to chapters such as "section 3.1" and must retain
    # the upstream 1..N chapter numbers.
    about = groups["About"]["About"]
    if about != [{"1. About this guide": "about.md"}]:
        raise ValueError("The canonical About navigation has changed")
    about[0] = {"About this guide": "about.md"}
    ordered = [
        groups["Home"],
        groups["About"],
        groups["Getting started"],
        *[
            item for item in items
            if item is not groups["Home"]
            and item is not groups["About"]
            and item is not groups["Getting started"]
        ],
    ]
    chapter = 0

    def renumber(nodes: list[dict]) -> None:
        nonlocal chapter
        for node in nodes:
            label, value = next(iter(node.items()))
            if isinstance(value, list) and value and isinstance(value[0], dict):
                renumber(value)
            elif NUMBERED.match(label) or node in imported:
                chapter += 1
                node.clear()
                node[f"{chapter}. {NUMBERED.sub('', label)}"] = value

    renumber(ordered)
    return ordered


def prepare(data: dict, *, preview: bool = False) -> None:
    host = os.environ.get("CI_SERVER_HOST", "").lower().rstrip(".")
    if not preview and host != "surrey.ac.uk" and not host.endswith(".surrey.ac.uk"):
        print("Non-Surrey host: keeping the canonical Getting started summary")
        return
    config_path = ROOT / "zensical.toml"
    config_text = config_path.read_text(encoding="utf-8")
    if config_text.startswith(START_MARKER):
        print("Surrey Getting started overlay already prepared")
        return
    # sync-repo may legitimately update repository metadata in the disposable
    # GitLab checkout before this step. The nav shape is validated below; only
    # the landing Markdown itself must still match the committed summary.
    landing = ROOT / "docs/gettingstarted.md"
    original = subprocess.check_output(["git", "show", "HEAD:docs/gettingstarted.md"], cwd=ROOT)
    if landing.read_bytes() != original:
        raise ValueError(f"Refusing to overwrite modified canonical file: {landing}")
    config = tomllib.loads(config_text)
    nav = surrey_nav(config, data)
    replacement = "nav = " + _render_nav(nav) + "\n"
    if len(NAV.findall(config_text)) != 1:
        raise ValueError("Could not identify exactly one canonical nav block")
    new_config = NAV.sub(replacement, config_text, count=1)
    tomllib.loads(new_config)  # Do not write malformed configuration.

    included = set(page_paths(data))
    outputs: dict[Path, bytes] = {}
    for page in included:
        source = SOURCE / "docs" / page
        text = source.read_text(encoding="utf-8")
        if page == "gettingstarted.md":
            text = omit_surrey_support_section(text)
        text = rewrite_external_links(text, page, included)
        text = use_stag_for_remotelabs(text)
        outputs[ROOT / "docs" / page] = text.encode("utf-8")
    for asset in data["assets"]:
        outputs[ROOT / "docs" / asset] = (SOURCE / "docs" / asset).read_bytes()

    # A disposable checkout may contain the canonical landing page, but no
    # other imported file may overwrite a pre-existing User Guide file.
    for target in outputs:
        if target.exists() and target != ROOT / "docs/gettingstarted.md":
            raise FileExistsError(f"Refusing to overwrite existing User Guide file: {target}")
    for target, content in outputs.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
    config_path.write_text(START_MARKER + new_config, encoding="utf-8")
    print(f"Prepared {len(included)} Surrey Getting started pages and {len(data['assets'])} assets")


def verify_upstream(data: dict, checkout: Path) -> None:
    revision = data["revision"]

    def show(relative: str) -> bytes:
        return subprocess.check_output(["git", "-C", str(checkout), "show", f"{revision}:{relative}"])

    upstream = tomllib.loads(show("zensical.toml").decode("utf-8"))
    section = next(item["Getting started"] for item in upstream["project"]["nav"] if "Getting started" in item)
    actual = [{"title": re.sub(r"^\d+\.\s+", "", next(iter(item))), "path": next(iter(item.values()))} for item in section]
    if actual != data["pages"]:
        raise ValueError("Snapshot pages/order differ from the pinned upstream nav")
    for relative in [*page_paths(data), *data["assets"]]:
        source = show("docs/" + relative)
        if source != (SOURCE / "docs" / relative).read_bytes():
            raise ValueError(f"Snapshot differs from pinned upstream: {relative}")
    if show("LICENSE.md") != (SOURCE / "LICENSE.md").read_bytes():
        raise ValueError("Snapshot licence differs from pinned upstream")
    print(f"Snapshot matches {data['repository']} at {revision}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("verify", "verify-upstream", "prepare"))
    parser.add_argument("--extensions-checkout", type=Path)
    parser.add_argument("--preview", action="store_true", help="prepare in an isolated local checkout")
    args = parser.parse_args()
    data = manifest()
    verify_snapshot(data)
    if args.action == "verify-upstream":
        if args.extensions_checkout is None:
            parser.error("verify-upstream requires --extensions-checkout")
        verify_upstream(data, args.extensions_checkout)
    elif args.action == "prepare":
        prepare(data, preview=args.preview)
    else:
        print("Surrey Getting started snapshot files are present")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"Surrey Getting started: {error}", file=sys.stderr)
        raise SystemExit(1) from error
