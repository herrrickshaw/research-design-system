"""Smoke test: every hand-written script byte-compiles under the supported Python."""
import py_compile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = sorted(list((ROOT / "blog-build").glob("*.py")) + list((ROOT / "blogger-theme").glob("*.py")))


@pytest.mark.parametrize("path", SCRIPTS, ids=lambda p: p.name)
def test_compiles(path, tmp_path):
    py_compile.compile(str(path), cfile=str(tmp_path / "x.pyc"), doraise=True)
