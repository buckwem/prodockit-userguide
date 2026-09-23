"""Surrey builds use the reusable analytics-free configuration."""

import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_committed_config_excludes_analytics_and_consent() -> None:
    config = (ROOT / "zensical.toml").read_text(encoding="utf-8")
    extra = tomllib.loads(config)["project"]["extra"]
    assert "analytics" not in extra
    assert "consent" not in extra
    assert not any(key.startswith("pdf_") for key in extra)
    pdf_config = tomllib.loads((ROOT / "pdk-pdf.toml").read_text(encoding="utf-8"))
    assert pdf_config["document"]["page_size"] == "A4"
    assert "project.markdown_extensions" in config


def test_pdf_policy_preserves_the_guides_layout_and_footer() -> None:
    pdf_config = tomllib.loads((ROOT / "pdk-pdf.toml").read_text(encoding="utf-8"))
    assert pdf_config["schema_version"] == 1
    assert pdf_config["document"] == {
        "copyright": (
            'Author: Mark Buckwell and contributors. Licensed under the MIT License.'
            '<br>Made with <a href="https://zensical.org/">Zensical</a> and '
            '<a href="https://prodockit.org/">prodockit</a>.'
        ),
        "extra_css": ["stylesheets/pdk-pdf.css", "stylesheets/print.css"],
        "page_size": "A4",
        "double_sided": False,
    }
    assert pdf_config["margins"] == {
        "top": "2cm",
        "right": "2cm",
        "bottom": "2.5cm",
        "left": "2cm",
        "inner": "2cm",
        "outer": "2cm",
    }
    assert pdf_config["header_footer"] == {
        "font_size": "10pt",
        "color": "#555555",
        "divider_color": "#e2e8f0",
    }
    assert pdf_config["table_of_contents"] == {
        "include": True,
        "title": "Table of Contents",
    }


def test_gitlab_build_prepares_surrey_source_for_both_outputs() -> None:
    pipeline = (ROOT / ".gitlab-ci.yml").read_text(encoding="utf-8")

    assert "tools/surrey_config.py" not in pipeline
    assert ".zensical-surrey.toml" not in pipeline
    assert "GOOGLE_ANALYTICS_ID" not in pipeline
    assert "python tools/surrey_getting_started.py verify" in pipeline
    assert "python tools/surrey_getting_started.py prepare" in pipeline
    assert "zensical build --clean --strict" in pipeline
    assert "prodockit pdf" in pipeline
    assert pipeline.index("python tools/surrey_getting_started.py prepare") < pipeline.index(
        "zensical build --clean --strict"
    )
    assert pipeline.index("zensical build --clean --strict") < pipeline.index(
        "prodockit pdf"
    )
