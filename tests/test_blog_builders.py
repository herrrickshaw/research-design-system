"""In-process runs (so coverage sees them) of the register-to-Blogger-post builders.

The scripts hard-code owner paths (/Users/.../digital-twin-for-ipa, a scratch dir) and
`~/...` inputs. The tests redirect `open()` for exactly those paths into tmp_path and point HOME at a
fixture tree, so the real script bodies run on SYNTHETIC register rows. Nothing outside tmp_path is read
or written."""
import builtins
import json
import re
import runpy
import sqlite3
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "blog-build"


def run_in_sandbox(name, tmp_path, monkeypatch, redirects=None):
    """Run blog-build/<name>.py as __main__ with __file__ in tmp_path (symlink => coverage still maps to source)."""
    link = tmp_path / f"{name}.py"
    link.symlink_to(BUILD / f"{name}.py")
    real_open = builtins.open
    redirects = redirects or {}

    def fake_open(file, *a, **k):
        f = str(file)
        for prefix, target in redirects.items():
            if f.startswith(prefix):
                return real_open(target(f), *a, **k)
        return real_open(file, *a, **k)

    monkeypatch.setattr(builtins, "open", fake_open)
    return runpy.run_path(str(link), run_name="__main__")


# ------------------------------- Lok Sabha / Rajya Sabha question registries -------------------------------

LS = [
    {"iso": "2026-07-20", "schemes": ["PLI", "FAME"], "ministry": "Heavy Industries", "lok": "18",
     "qtype": "STARRED", "qno": 5, "subject": "EV </script> & subsidy", "pdf": "http://x/1.pdf",
     "members": ["A", "B", "C", "D"], "q": "2026Q3"},
    {"iso": "2026-02-10", "schemes": ["PLI"], "ministry": "Commerce", "lok": "18",
     "qtype": "UNSTARRED", "qno": 9, "subject": "Exports", "pdf": "http://x/2.pdf",
     "members": ["E"], "q": "2026Q1"},
    {"iso": "2026-02-10", "schemes": [], "ministry": "Commerce", "lok": "18",
     "qtype": None, "qno": 3, "subject": "None qtype", "pdf": "", "members": [], "q": "2026Q1"},
]
RS = [dict(r, session="260") for r in LS]


def test_build_pq_post(tmp_path, monkeypatch, capsys):
    reg = tmp_path / "ls.json"
    reg.write_text(json.dumps(LS))
    out = tmp_path / "pq.html"
    ns = run_in_sandbox("build_pq_post", tmp_path, monkeypatch, {
        "/Users/umashankar/digital-twin-for-ipa/": lambda f: str(reg),
        "/private/tmp/": lambda f: str(out)})
    html = out.read_text(encoding="utf-8")
    printed = capsys.readouterr().out
    assert "rows=3 quarters=2 range=2026-02-10->2026-07-20 starred=1" in printed
    assert ns["schemes"] == ["FAME", "PLI"] and ns["mins"] == ["Commerce", "Heavy Industries"]
    # newest first, then by question number descending within a date
    assert [r[0] for r in ns["R"]] == ["2026-07-20", "2026-02-10", "2026-02-10"]
    assert [r[5] for r in ns["R"]][1:] == [9, 3]
    assert ns["R"][0][8] == "A, B, C & ors." and ns["R"][1][8] == "E"            # first 3 members, then "& ors."
    assert ns["R"][0][4] == 1 and ns["R"][1][4] == 0
    p = ns["payload"]
    assert p.isascii() and "<" not in p and ">" not in p and "&" not in p and "</" not in p
    assert json.loads(p)["r"][0][6] == "EV </script> & subsidy"
    assert html.count("<script") == html.count("</script>")
    assert "@media (prefers-color-scheme" not in html


def test_build_rs_post_handles_blank_and_padded_qtype(tmp_path, monkeypatch, capsys):
    rows = [dict(r) for r in RS]
    rows[1]["qtype"] = "  STARRED "
    reg = tmp_path / "rs.json"
    reg.write_text(json.dumps(rows))
    out = tmp_path / "rs.html"
    ns = run_in_sandbox("build_rs_post", tmp_path, monkeypatch, {
        "/Users/umashankar/digital-twin-for-ipa/": lambda f: str(reg),
        "/private/tmp/": lambda f: str(out)})
    assert [r[4] for r in ns["R"]] == [1, 1, 0]                       # padded STARRED counts; None -> unstarred
    assert ns["R"][0][3] == "260"
    assert "rows=3 quarters=" in capsys.readouterr().out
    assert out.read_text(encoding="utf-8").count("<script") == out.read_text(encoding="utf-8").count("</script>")
    assert ns["payload"].isascii()


# ------------------------------- scrutiny matrix -------------------------------

@pytest.fixture
def twin(tmp_path, monkeypatch):
    home = tmp_path / "home"
    (home / "digital-twin-for-ipa/scripts").mkdir(parents=True)
    (home / "digital-twin-for-ipa/data/registers").mkdir(parents=True)
    (home / "digital-twin-for-ipa/scripts/build_reportage.py").write_text(
        "def scheme_hits(title):\n    return [s for s in ('PLI', 'FAME', 'PM-KUSUM') if s.lower() in title.lower()]\n")
    d = home / "india-trade-sector-policy-recommendations/data"
    d.mkdir(parents=True)
    con = sqlite3.connect(d / "pib_index.sqlite")
    con.execute("create table pib_items (date text, title text)")
    con.executemany("insert into pib_items values (?, ?)", [
        ("2024-01-05", "PLI scheme extended"), ("2024-06-01", "pli & fame update"), ("", "PLI no date"),
        ("2025-01-01", "FAME phase"), ("2025-03-01", "PM-KUSUM <b> launch"), ("2025-04-01", "Unrelated")])
    con.commit()
    con.close()
    recent = "2099-01-01"            # always inside the 365-day window
    old = "2000-01-01"
    ls = [{"schemes": ["PLI"], "iso": recent, "qtype": "STARRED"}] * 6 + \
         [{"schemes": ["PLI", "FAME"], "iso": old, "qtype": None}] * 5 + \
         [{"schemes": ["FAME"], "iso": old, "qtype": "UNSTARRED"}]
    rs = [{"schemes": ["PLI"], "iso": recent, "qtype": " starred "}]
    (home / "digital-twin-for-ipa/data/registers/ls_pq_registry.json").write_text(json.dumps(ls))
    (home / "digital-twin-for-ipa/data/registers/rs_pq_registry.json").write_text(json.dumps(rs))
    monkeypatch.setenv("HOME", str(home))
    import sys
    monkeypatch.setattr(sys, "path", list(sys.path))
    sys.modules.pop("build_reportage", None)
    return home


def test_build_matrix_post_buckets_and_html(twin, tmp_path, monkeypatch, capsys):
    ns = run_in_sandbox("build_matrix_post", tmp_path, monkeypatch)
    rows = {r["s"]: r for r in ns["rows"]}
    assert set(rows) == {"PLI", "FAME", "PM-KUSUM"}
    pli = rows["PLI"]
    assert (pli["pib"], pli["ls"], pli["rs"], pli["star"], pli["tot"]) == (2, 11, 1, 6, 12)   # '' date skipped; " starred " (lower case) is not STARRED; " starred " (lower case) is not STARRED
    assert pli["pib_first"] == "2024-01-05" and pli["pib_last"] == "2024-06-01" and pli["last"] == "2099-01-01"
    assert pli["b"] == "A"                                  # >= 10 questions AND a recent one
    assert rows["FAME"]["b"] == "B" and rows["FAME"]["tot"] == 6      # asked, but not recent / not enough
    assert rows["PM-KUSUM"]["b"] == "C" and rows["PM-KUSUM"]["tot"] == 0
    assert [r["s"] for r in ns["A"]] == ["PLI"] and [r["s"] for r in ns["C"]] == ["PM-KUSUM"]
    html = (tmp_path / "matrix_post.html").read_text(encoding="utf-8")
    assert "A 1 / B 1 / C 1" in capsys.readouterr().out
    assert html.startswith("<style>") and "PLI" in html
    assert ns["esc"]("a&b<c>") == "a&amp;b&lt;c&gt;"
    tbl = ns["table"]([rows["PM-KUSUM"]], empty_qs=True)
    assert "&#8212;" in tbl and tbl.count("<tr>") == 2          # header row + one body row
    assert "&#8212;" not in ns["table"]([rows["PM-KUSUM"]])


def test_build_matrix_exactly_ten_recent_questions_is_active(twin, tmp_path, monkeypatch):
    regs = twin / "digital-twin-for-ipa/data/registers"
    ls = [{"schemes": ["PLI"], "iso": "2099-01-01", "qtype": None}] * 10
    (regs / "ls_pq_registry.json").write_text(json.dumps(ls))
    (regs / "rs_pq_registry.json").write_text(json.dumps([]))
    ns = run_in_sandbox("build_matrix_post", tmp_path, monkeypatch)
    assert {r["s"]: r["b"] for r in ns["rows"]}["PLI"] == "A"


@pytest.mark.xfail(strict=True, raises=IndexError,
                   reason="build_matrix_post.py:~76 does `mx = A[0][\"tot\"]` unconditionally, so a register "
                          "with no actively-scrutinised scheme (nine questions, none recent, ...) crashes "
                          "with IndexError instead of rendering an empty top-10 strip")
def test_build_matrix_with_no_active_scheme_still_renders(twin, tmp_path, monkeypatch):
    regs = twin / "digital-twin-for-ipa/data/registers"
    ls = [{"schemes": ["PLI"], "iso": "2099-01-01", "qtype": None}] * 9      # one short of ACTIVE_MIN_Q
    (regs / "ls_pq_registry.json").write_text(json.dumps(ls))
    (regs / "rs_pq_registry.json").write_text(json.dumps([]))
    run_in_sandbox("build_matrix_post", tmp_path, monkeypatch)
    assert (tmp_path / "matrix_post.html").exists()


# ------------------------------- 5a-i insert -------------------------------

def test_insert_5ai(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    ns = run_in_sandbox("insert_5ai", tmp_path, monkeypatch)
    assert len(ns["ROWS"]) == 25 and len(ns["deep"]) == 13
    html = (tmp_path / "insert_5ai.html").read_text(encoding="utf-8")
    out = capsys.readouterr().out
    assert "rows=25 deep=13" in out and "gap range: 0.75 .. 5.25" in out
    assert "Twenty-five countries are cheaper than India" in html
    assert all(v < ns["IND"] for _, v, _ in ns["ROWS"])           # every listed economy is cheaper than India
