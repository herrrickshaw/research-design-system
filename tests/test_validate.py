"""blogger-theme/validate.py run as a subprocess against fixture themes in a
temp dir (it reads ./masaladeutsch.xml from its cwd)."""
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
VALIDATE = ROOT / "blogger-theme" / "validate.py"

GOOD = """<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE html>
<html b:version='2' xmlns='http://www.w3.org/1999/xhtml' xmlns:b='http://www.google.com/2005/gml/b' xmlns:data='http://www.google.com/2005/gml/data' xmlns:expr='http://www.google.com/2005/gml/expr'>
<head><b:include data='blog' name='all-head-content'/>
<!-- theme head -->
<b:skin><![CDATA[ body{color:#111} /* a -- b */ ]]></b:skin></head>
<body>
<b:section id='main-top' showaddelement='yes'/>
<b:section id='main' showaddelement='no'>
<b:widget id='Blog1' type='Blog' title='Posts'>
<b:includable id='main'>
<b:if cond='data:blog.pageType == "item"'><data:post.body/><b:else/><data:post.snippet/></b:if>
</b:includable>
</b:widget>
</b:section>
<b:section id='main-bottom' showaddelement='yes'/>
</body></html>
"""


def run(tmp_path, xml):
    (tmp_path / "masaladeutsch.xml").write_text(xml, encoding="utf-8")
    r = subprocess.run([sys.executable, str(VALIDATE)], cwd=tmp_path,
                       capture_output=True, text=True, timeout=60)
    return r.returncode, r.stdout


def test_minimal_good_theme_passes(tmp_path):
    rc, out = run(tmp_path, GOOD)
    assert rc == 0 and out.startswith("PASS"), out


def test_shipped_theme_passes(tmp_path):
    shutil.copy(ROOT / "blogger-theme" / "masaladeutsch.xml", tmp_path / "x.xml")
    rc, out = run(tmp_path, (tmp_path / "x.xml").read_text(encoding="utf-8"))
    assert rc == 0, out


@pytest.mark.parametrize("mutate,expect", [
    (lambda s: s.replace("<!-- theme head -->", "<!-- old -- note -->"), "illegal '--' in XML comment"),
    (lambda s: s.replace("</b:widget>", "<script>x()</script></b:widget>"), "contains a <script> tag"),
    (lambda s: s.replace("<!-- theme head -->", "<link href='https://cdn.example.com/a.css'/>"),
     "external host referenced"),
    (lambda s: s.replace("<b:else/><data:post.snippet/>", "<b:else/><data:post.body/>"),
     "index branch renders post.body"),
    (lambda s: s.replace("id='main-bottom' showaddelement='yes'", "id='main-bottom' showaddelement='no'"),
     "page-body gadget slots missing"),
    (lambda s: s.replace("<head>", "<head><b:if>"), "XML not well-formed"),
    (lambda s: s.replace("b:version='2'", "b:version='1'"), "missing b:version"),
])
def test_each_rule_fails_when_violated(tmp_path, mutate, expect):
    rc, out = run(tmp_path, mutate(GOOD))
    assert rc == 1
    assert expect in out, out


def test_required_markers_only_inside_comments_do_not_count(tmp_path):
    """A Blog widget that exists only in a commented-out block is not in the
    theme Blogger will render; the presence checks must look at the
    comment-stripped source like the other checks do."""
    xml = GOOD.replace("type='Blog'", "type='HTML'").replace(
        "<!-- theme head -->", "<!-- removed: <b:widget type='Blog'/> -->")
    rc, out = run(tmp_path, xml)
    assert rc == 1 and "missing Blog widget" in out, out


def test_missing_pagetype_branch_is_reported_not_crashed(tmp_path):
    xml = GOOD.replace("cond='data:blog.pageType == \"item\"'", "cond='true'")
    rc, out = run(tmp_path, xml)
    assert rc == 1
    assert "FAIL" in out and "pageType" in out, out
