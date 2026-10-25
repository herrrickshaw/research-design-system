"""README rule: components never reference a raw palette value; themes only
rebind semantic --c-* tokens. Checked statically on the CSS."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_COLOR = re.compile(r"#[0-9a-fA-F]{3,8}\b|\brgba?\(|\bhsla?\(")


def test_components_use_only_tokens_for_color():
    css = (ROOT / "components" / "components.css").read_text()
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    hits = [f"line {css[:m.start()].count(chr(10)) + 1}: {m.group(0)}" for m in RAW_COLOR.finditer(css)]
    assert hits == []


def test_every_theme_binds_the_semantic_tokens_components_use():
    comp = (ROOT / "components" / "components.css").read_text()
    used = set(re.findall(r"var\(\s*(--c-[\w-]+)", comp))
    base = (ROOT / "tokens" / "tokens.css").read_text()
    for theme in sorted((ROOT / "themes").glob("*.css")):
        defined = set(re.findall(r"(--c-[\w-]+)\s*:", theme.read_text() + base))
        assert used <= defined, (theme.name, sorted(used - defined))
