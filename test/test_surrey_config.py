"""Surrey builds exclude public-site analytics and consent."""

import importlib.util
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "surrey_config.py"


def _tool_module():
    spec = importlib.util.spec_from_file_location("surrey_config", TOOL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_generated_config_removes_analytics_and_consent(tmp_path: Path) -> None:
    destination = tmp_path / "zensical.toml"
    _tool_module().write_config(ROOT / "zensical.toml", destination)

    generated = destination.read_text(encoding="utf-8")
    extra = tomllib.loads(generated)["project"]["extra"]
    assert "analytics" not in extra
    assert "consent" not in extra
    assert "G-ET1T9VSNF2" not in generated
    assert extra["pdf_page_size"] == "A4"
    assert "project.markdown_extensions" in generated


def test_gitlab_build_uses_generated_config_for_both_outputs() -> None:
    pipeline = (ROOT / ".gitlab-ci.yml").read_text(encoding="utf-8")

    assert "python tools/surrey_config.py zensical.toml .zensical-surrey.toml" in pipeline
    assert "prodockit pdf --config-file .zensical-surrey.toml" in pipeline
    assert "zensical build --config-file .zensical-surrey.toml --clean --strict" in pipeline
    assert pipeline.index(
        "zensical build --config-file .zensical-surrey.toml --clean --strict"
    ) < pipeline.index("prodockit pdf --config-file .zensical-surrey.toml")
