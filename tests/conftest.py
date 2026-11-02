"""Make the hyphenated script directories importable from tests."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for sub in ("blog-build", "blogger-theme"):
    sys.path.insert(0, str(ROOT / sub))
