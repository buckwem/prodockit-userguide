"""Surrey builds use the reusable analytics-free configuration."""

import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_committed_config_excludes_analytics_and_consent() -> None:
    config = (ROOT / "zensical.toml").read_text(encoding="utf-8")
    extra = tomllib.loads(config)["project"]["extra"]
    assert "analytics" not in extra
    assert "consent" not in extra
    assert extra["pdf_page_size"] == "A4"
    assert "project.markdown_extensions" in config


def test_gitlab_build_uses_the_committed_config_for_both_outputs() -> None:
    pipeline = (ROOT / ".gitlab-ci.yml").read_text(encoding="utf-8")

    assert "tools/surrey_config.py" not in pipeline
    assert ".zensical-surrey.toml" not in pipeline
    assert "GOOGLE_ANALYTICS_ID" not in pipeline
    assert "zensical build --clean --strict" in pipeline
    assert "prodockit pdf" in pipeline
    assert pipeline.index("zensical build --clean --strict") < pipeline.index(
        "prodockit pdf"
    )
