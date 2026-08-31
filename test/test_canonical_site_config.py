"""Only the canonical GitHub Pages build receives opt-in analytics."""

import importlib.util
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "canonical_site_config.py"
OUTPUT_CHECK = ROOT / "tools" / "check_canonical_site.py"
VALID_CANONICAL_HTML = """
<script>
https://www.googletagmanager.com/gtag/js?id=G-TEST123
consent&&consent.analytics&&__md_analytics()
</script>
<p>
  We use optional analytics cookies to understand which documentation is useful
  and improve prodockit.
</p>
<input type="checkbox" name="analytics" checked>
<button class="md-button md-button--primary">Accept</button>
<label class="md-button" for="__settings">Manage settings</label>
"""


def _tool_module():
    spec = importlib.util.spec_from_file_location("canonical_site_config", TOOL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _output_check_module():
    spec = importlib.util.spec_from_file_location("check_canonical_site", OUTPUT_CHECK)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_generated_config_adds_simplified_opt_in_analytics(tmp_path: Path) -> None:
    source = tmp_path / "zensical.toml"
    destination = tmp_path / ".zensical-canonical.toml"
    original = (ROOT / "zensical.toml").read_text(encoding="utf-8")
    source.write_text(original, encoding="utf-8")

    _tool_module().write_config(source, destination, "G-TEST123")

    assert source.read_text(encoding="utf-8") == original
    source_extra = tomllib.loads(original)["project"]["extra"]
    canonical_extra = tomllib.loads(destination.read_text(encoding="utf-8"))["project"][
        "extra"
    ]
    assert "analytics" not in source_extra
    assert "consent" not in source_extra
    assert canonical_extra["analytics"] == {
        "provider": "google",
        "property": "G-TEST123",
    }
    description = " ".join(canonical_extra["consent"]["description"].split())
    assert description == (
        "We use optional analytics cookies to understand which documentation "
        "is useful and improve prodockit."
    )
    assert canonical_extra["consent"]["actions"] == ["accept", "manage"]
    assert canonical_extra["consent"]["cookies"]["analytics"] == {
        "name": "Google Analytics",
        "checked": True,
    }


@pytest.mark.parametrize(
    "measurement_id",
    ("", "BCDJ2LWJT3", "G-", "G-lowercase", "UA-12345-1", "G-ABC 123"),
)
def test_invalid_measurement_ids_are_rejected(
    tmp_path: Path, measurement_id: str
) -> None:
    with pytest.raises(ValueError, match="GA4 measurement ID"):
        _tool_module().write_config(
            ROOT / "zensical.toml", tmp_path / "canonical.toml", measurement_id
        )


def test_source_with_analytics_is_rejected() -> None:
    source = (ROOT / "zensical.toml").read_text(encoding="utf-8")
    source += "\n[project.extra.analytics]\nprovider = 'google'\n"

    with pytest.raises(ValueError, match="already contains analytics or consent"):
        _tool_module().with_canonical_analytics(source, "G-TEST123")


def test_command_fails_clearly_without_a_valid_id(tmp_path: Path) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            str(TOOL),
            str(ROOT / "zensical.toml"),
            str(tmp_path / "canonical.toml"),
            "not-an-id",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 1
    assert "GOOGLE_ANALYTICS_ID must be a GA4 measurement ID" in completed.stderr


def test_deployment_applies_the_overlay_after_reusable_checks() -> None:
    workflow = (ROOT / ".github" / "workflows" / "docs.yml").read_text(encoding="utf-8")
    reusable_build = "zensical build --clean --strict"
    reusable_tests = "python -m pytest test/ -v"
    canonical_config = (
        "python tools/canonical_site_config.py zensical.toml "
        '.zensical-canonical.toml "$GOOGLE_ANALYTICS_ID"'
    )
    canonical_build = (
        "zensical build --config-file .zensical-canonical.toml --clean --strict"
    )
    canonical_check = "python tools/check_canonical_site.py public/index.html"

    assert "GOOGLE_ANALYTICS_ID: ${{ secrets.GOOGLE_ANALYTICS_ID }}" in workflow
    assert "if: github.repository == 'buckwem/prodockit-userguide'" in workflow
    assert (
        "The canonical User Guide deployment needs the GOOGLE_ANALYTICS_ID" in workflow
    )
    assert workflow.index(reusable_build) < workflow.index(reusable_tests)
    assert workflow.index(reusable_tests) < workflow.index(canonical_config)
    assert workflow.index(canonical_config) < workflow.index(canonical_build)
    assert workflow.index(canonical_build) < workflow.index(canonical_check)


def test_rendered_canonical_consent_controls_are_validated() -> None:
    _output_check_module().validate_canonical_html(VALID_CANONICAL_HTML)


@pytest.mark.parametrize(
    "removed",
    (
        '<button class="md-button md-button--primary">Accept</button>',
        '<label class="md-button" for="__settings">Manage settings</label>',
        '<input type="checkbox" name="analytics" checked>',
        "consent&&consent.analytics&&__md_analytics()",
    ),
)
def test_rendered_canonical_validation_rejects_missing_behaviour(
    removed: str,
) -> None:
    with pytest.raises(ValueError, match="canonical output"):
        _output_check_module().validate_canonical_html(
            VALID_CANONICAL_HTML.replace(removed, "")
        )


def test_rendered_canonical_validation_rejects_a_reject_control() -> None:
    html = VALID_CANONICAL_HTML + (
        '<button type="reset" class="md-button md-button--primary">Reject</button>'
    )

    with pytest.raises(ValueError, match="still contains a Reject control"):
        _output_check_module().validate_canonical_html(html)


def test_temporary_canonical_config_is_ignored() -> None:
    ignored = (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()

    assert ".zensical-canonical.toml" in ignored
