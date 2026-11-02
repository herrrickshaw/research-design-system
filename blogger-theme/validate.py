#!/usr/bin/env python3
"""Validate the Blogger theme. Run after every edit."""
from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

THEME = Path(__file__).resolve().parent / "masaladeutsch.xml"
# Namespaces that are legitimately referenced from the theme markup.
ALLOWED_HOSTS = r"www\.w3\.org|www\.google\.com/2005"
REQUIRED = [("b:version", "b:version='2'"), ("b namespace", "xmlns:b="),
            ("all-head-content", "name='all-head-content'"),
            ("b:skin", "<b:skin><![CDATA["), ("Blog widget", "type='Blog'")]


def _cdata_spans(src: str) -> list[tuple[int, int]]:
    """Return (start, end) offsets of every CDATA section in *src*."""
    return [m.span() for m in re.finditer(r"<!\[CDATA\[.*?\]\]>", src, re.S)]


def check_theme(src: str) -> list[str]:
    """Return a list of failure messages for the theme XML text *src* (empty = pass)."""
    fails: list[str] = []
    try:
        ET.fromstring(src.replace("<!DOCTYPE html>", ""))
    except ET.ParseError as e:
        fails.append(f"XML not well-formed: {e}")
    cda = _cdata_spans(src)

    def inc(i: int) -> bool:
        return any(a <= i < b for a, b in cda)

    for m in re.finditer(r"<!--(.*?)-->", src, re.S):  # '--' inside a comment is illegal XML
        if not inc(m.start()) and "--" in m.group(1):
            fails.append(f"illegal '--' in XML comment: {' '.join(m.group(1).split())[:50]}")
    clean = re.sub(r"<!--.*?-->", lambda m: "" if not inc(m.start()) else m.group(0), src, flags=re.S)
    fails += [f"missing {label}" for label, needle in REQUIRED if needle not in src]
    index = clean.split("cond='data:blog.pageType")[1].split("<b:else/>", 1)[1].split("</b:includable>")[0]
    if "data:post.body" in index:
        fails.append("index branch renders post.body -- will empty the post list")
    if "data:post.snippet" not in index:
        fails.append("index branch missing data:post.snippet")
    if "<script" in clean.lower():
        fails.append("contains a <script> tag")
    ext = re.findall(rf"""(?:src|href)=['"](https?://(?!{ALLOWED_HOSTS})[^'"]+)""", clean)
    if ext:
        fails.append(f"external host referenced: {ext}")
    slots = re.findall(r"<b:section[^>]*id='(main-top|main-bottom)'[^>]*showaddelement='yes'", clean)
    if len(slots) != 2:
        fails.append(f"page-body gadget slots missing: {slots}")
    return fails


def main() -> int:
    """CLI entry: validate the bundled theme; exit 1 on any failure."""
    fails = check_theme(THEME.read_text(encoding="utf-8"))
    print("\n".join("FAIL  " + f for f in fails) if fails else "PASS  all checks green")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
