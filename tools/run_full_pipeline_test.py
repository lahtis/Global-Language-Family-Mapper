#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# GLFM Project
# Copyright (c) 2026 Tuomas Lähteenmäki
#
# https://codeberg.org/lahtis/GLFM
#
# Licensed under the MIT License.
# You may obtain a copy of the License at:
# https://opensource.org/licenses/MIT
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TOOLS = PROJECT_ROOT / "tools"
OUTPUT = PROJECT_ROOT / "output"

# Skriptit
BUILD_UNIFIED = PROJECT_ROOT / "build_unified.py"
VALIDATE_BCP47 = TOOLS / "validate_bcp47.py"
VALIDATE_FALLBACKS = TOOLS / "validate_fallbacks.py"
VALIDATE_ISO = TOOLS / "validate_iso_consistency.py"
VISUALIZE_FALLBACKS = TOOLS / "visualize_fallbacks.py"

ALL_SCRIPTS = [
    (BUILD_UNIFIED, "Build unified_languages.json"),
    (VALIDATE_BCP47, "Validate BCP-47 tags"),
    (VALIDATE_FALLBACKS, "Validate fallback chains"),
    (VALIDATE_ISO, "Validate ISO consistency"),
    (VISUALIZE_FALLBACKS, "Visualize fallback graph"),
]


def run_script(path: Path, title: str) -> bool:
    """Ajaa yksittäisen skriptin ja tulostaa stdout/stderr."""
    print(f"\n=== {title} ===")
    print(f"Running: {path}")

    result = subprocess.run(
        [sys.executable, str(path)],
        capture_output=True,
        text=True
    )

    if result.stdout.strip():
        print(result.stdout.strip())

    if result.stderr.strip():
        print("ERROR:", result.stderr.strip())

    if result.returncode != 0:
        print(f"{title} FAILED")
        return False

    print(f"✔ {title} OK")
    return True


def main():
    print("========================================")
    print(" FULL PIPELINE TEST")
    print("========================================")

    all_ok = True

    for script, title in ALL_SCRIPTS:
        ok = run_script(script, title)
        if not ok:
            all_ok = False

    print("\n========================================")
    if all_ok:
        print(" ALL TESTS PASSED")
    else:
        print(" SOME TESTS FAILED")
    print("========================================")


if __name__ == "__main__":
    main()

