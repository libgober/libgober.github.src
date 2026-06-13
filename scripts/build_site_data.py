#!/usr/bin/env python3
"""Run website data generators with the project virtualenv when available."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENV_PYTHON = ROOT / ".venv" / "bin" / "python"


def main() -> int:
    python = VENV_PYTHON if VENV_PYTHON.exists() else Path(sys.executable)
    scripts = [
        ROOT / "scripts" / "build_publications_listing.py",
        ROOT / "scripts" / "build_site_partials.py",
    ]
    for script in scripts:
        result = subprocess.run([str(python), str(script)], cwd=ROOT, check=False)
        if result.returncode != 0:
            return result.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
