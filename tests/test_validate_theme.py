"""Tests for blogger-theme/validate.py."""
import subprocess
import sys
from pathlib import Path

import validate

ROOT = Path(__file__).resolve().parent.parent


def test_bundled_theme_passes():
    assert validate.check_theme(validate.THEME.read_text(encoding="utf-8")) == []


def _theme() -> str:
    return validate.THEME.read_text(encoding="utf-8")


def test_detects_malformed_xml():
    assert any("XML not well-formed" in f for f in validate.check_theme(_theme() + "<oops"))


def test_detects_script_tag():
    src = _theme().replace("</head>", "<script>1</script></head>", 1)
    assert any("<script>" in f for f in validate.check_theme(src))


def test_detects_external_host():
    src = _theme().replace("</head>", "<link href='https://evil.example/x.css'/></head>", 1)
    assert any("external host" in f for f in validate.check_theme(src))


def test_detects_missing_required_marker():
    src = _theme().replace("type='Blog'", "type='Other'")
    assert "missing Blog widget" in validate.check_theme(src)


def test_cli_runs_from_any_cwd(tmp_path):
    r = subprocess.run([sys.executable, str(ROOT / "blogger-theme" / "validate.py")],
                       cwd=tmp_path, capture_output=True, text=True)
    assert r.returncode == 0
    assert r.stdout.strip() == "PASS  all checks green"
