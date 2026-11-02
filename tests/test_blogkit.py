"""Characterisation tests for blog-build/blogkit.py (payload encoding + widget)."""
import json

import pytest

from blogkit import TRANSLATE, encode_payload


def test_payload_is_ascii_and_script_inert():
    p = encode_payload({"a": "Rs ₹ 5 & <b>x</b>", "n": [1, 2]})
    assert p.isascii()
    for bad in ("&", "<", ">"):
        assert bad not in p


def test_payload_round_trips():
    data = {"s": ["A & B", "C <x>"], "r": [["2026-01-05", [0, 1], 0, 3, "T ₹"]]}
    assert json.loads(encode_payload(data)) == data


def test_payload_is_compact():
    assert encode_payload({"a": [1, 2]}) == '{"a":[1,2]}'


def test_payload_matches_legacy_inline_logic():
    data = {"x": "a&b<c>d é"}
    legacy = json.dumps(data, ensure_ascii=True, separators=(",", ":"))
    for ch, esc in (("&", "\\u0026"), ("<", "\\u003c"), (">", "\\u003e")):
        legacy = legacy.replace(ch, esc)
    assert encode_payload(data) == legacy


def test_translate_widget_markup():
    assert 'id="google_translate_element"' in TRANSLATE
    assert "translate.google.com/translate_a/element.js" in TRANSLATE
    assert TRANSLATE.startswith("\n") and TRANSLATE.endswith("\n")


def test_assertion_guard_exists():
    # json.dumps can never emit a raw "</" after escaping, so the guard stays quiet.
    assert "</" not in encode_payload({"k": "</script>"})
    with pytest.raises(TypeError):
        encode_payload({"k": object()})
