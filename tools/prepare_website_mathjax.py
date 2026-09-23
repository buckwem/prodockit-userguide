"""Prepare the guide's pinned, local MathJax 3 website assets.

Prodockit's PDF renderer owns a separate project-local MathJax runtime.
This script keeps the existing website build offline-capable after the
legacy ``pdk init-mathjax`` command was removed.
"""

from pathlib import Path
from shutil import copyfile


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "tools" / "mathjax" / "node_modules" / "mathjax-full"
DESTINATION = ROOT / "docs" / "javascripts" / "vendor" / "mathjax"
CONFIG = ROOT / "docs" / "javascripts" / "mathjax.js"

CONFIG_SOURCE = r'''// Loaded before the pinned MathJax bundle.
window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true,
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex",
  },
};

if (typeof document$ !== "undefined") {
  document$.subscribe(() => {
    if (window.MathJax.typesetPromise) window.MathJax.typesetPromise();
  });
}
'''


def main() -> None:
    sources = {
        "tex-svg-full.js": PACKAGE / "es5" / "tex-svg-full.js",
        "LICENSE": PACKAGE / "LICENSE",
    }
    for source in sources.values():
        if not source.is_file():
            raise SystemExit(f"Missing {source}; run npm ci --prefix tools/mathjax")
    DESTINATION.mkdir(parents=True, exist_ok=True)
    for name, source in sources.items():
        copyfile(source, DESTINATION / name)
    CONFIG.write_text(CONFIG_SOURCE, encoding="utf-8")


if __name__ == "__main__":
    main()
