"""blog-build/build_post.py run in a temp dir on a synthetic rows.json."""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "blog-build" / "build_post.py"

ROWS = [
    {"d": "2026-08-01", "s": "PLI; FAME", "m": "Ministry of Heavy Industries", "p": "200001",
     "t": "Cabinet & CCEA approve </script><script>alert(1)</script> ₹ 500 crore"},
    {"d": "2026-02-15", "s": "PLI", "m": "Cabinet", "p": "190002", "t": "Union Cabinet note"},
    {"d": "2026-03-31", "s": "FAME", "m": "Ministry of Heavy Industries", "p": "190003", "t": "Q1 end"},
]


def build(tmp_path):
    (tmp_path / "rows.json").write_text(json.dumps(ROWS))
    r = subprocess.run([sys.executable, str(SCRIPT)], cwd=tmp_path, capture_output=True,
                       text=True, timeout=60)
    assert r.returncode == 0, r.stderr
    return r.stdout, (tmp_path / "reportage_post.html").read_text(encoding="utf-8")


def _payload(html):
    return re.search(r"var D=(\{.*?\});\n", html, re.S).group(1)


def test_summary_counts(tmp_path):
    out, html = build(tmp_path)
    # 2026-08 -> Q3, 2026-02 and 2026-03 -> Q1
    assert "rows=3 quarters=2 range=2026-02-15->2026-08-01 cabinet=1" in out
    assert "<strong>3 incentive-scheme announcements</strong> across 2 quarters" in html
    assert "1 of these rows are Cabinet or CCEA items" in html


def test_payload_is_ascii_inert_and_round_trips(tmp_path):
    _, html = build(tmp_path)
    p = _payload(html)
    assert p.isascii()
    assert "</" not in p and "<" not in p and ">" not in p and "&" not in p
    data = json.loads(p)  # \\u escapes are valid JSON
    assert data["s"] == ["FAME", "PLI"]
    assert data["m"] == ["Cabinet", "Ministry of Heavy Industries"]
    # newest first; scheme indices sorted; PRID as int
    assert data["r"][0] == ["2026-08-01", [0, 1], 1, 200001, ROWS[0]["t"]]
    assert [r[0] for r in data["r"]] == ["2026-08-01", "2026-03-31", "2026-02-15"]


def test_post_is_light_only_and_carries_disclaimer_and_translate(tmp_path):
    _, html = build(tmp_path)
    assert "@media (prefers-color-scheme" not in html and "@media(prefers-color-scheme" not in html
    assert "AI-generated text can" in html
    assert 'id="google_translate_element"' in html
    assert html.count("<script") == html.count("</script>")
