"""Shared helpers for the Blogger post generators in this directory.

Invariants (violating them broke production; see ../blogger-theme/README.md):
the JSON payload is 7-bit ASCII with &, < and > \\u-escaped, and every post
carries the Google-Translate widget.
"""
from __future__ import annotations

import json
from typing import Any

#: Characters Blogger's editor rewrites inside <script>, and their JSON escapes.
_BLOGGER_UNSAFE = (("&", "\\u0026"), ("<", "\\u003c"), (">", "\\u003e"))

#: Google-Translate widget markup appended after the post CSS.
TRANSLATE = ('\n<div id="google_translate_element" style="margin:8px 0 16px;"></div>'
 '<script type="text/javascript">function googleTranslateElementInit(){'
 'new google.translate.TranslateElement({pageLanguage:"en",'
 'layout:google.translate.TranslateElement.InlineLayout.SIMPLE,autoDisplay:false},'
 '"google_translate_element");}</script>'
 '<script type="text/javascript" '
 'src="https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit">'
 '</script>\n')


def encode_payload(data: Any) -> str:
    """Serialise *data* to compact JSON that is pure ASCII and inert inside <script>."""
    payload = json.dumps(data, ensure_ascii=True, separators=(",", ":"))
    for ch, escaped in _BLOGGER_UNSAFE:
        payload = payload.replace(ch, escaped)
    assert payload.isascii() and "</" not in payload
    return payload
