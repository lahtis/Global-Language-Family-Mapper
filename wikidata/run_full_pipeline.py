#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2026 Tuomas Lähteenmäki
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

#!/usr/bin/env python3
import subprocess
import sys
import os
from pathlib import Path

# --- Project root directory (this script is in root) ---
ROOT_DIR = Path(__file__).resolve().parent

DATA_DIR = ROOT_DIR / "data"
CACHE_DIR = ROOT_DIR / "cache"
MAPS_DIR = ROOT_DIR / "maps"
LIBS_DIR = ROOT_DIR / "libs"

# --- 1. Check that basic directories exist ---
for folder in [DATA_DIR, CACHE_DIR, MAPS_DIR, LIBS_DIR]:
    if not folder.exists():
        if folder == DATA_DIR:
            print(f"ERROR: data/ directory missing: {DATA_DIR}")
            sys.exit(1)
        else:
            print(f"Creating missing directory: {folder}")
            folder.mkdir(parents=True, exist_ok=True)

# --- 2. Pipeline scripts in correct order (libs/) ---
SCRIPTS = [
    "wikidata_api_query.py",                 # 0) Build raw ISO → macrofamily
    "build_code_to_family_qid.py",           # 1) ISO-639-5 → QID
    "build_parent_chains.py",                # 2) QID → parent chains
    "build_code_to_macrofamily.py",          # 3) macrofamily
    "build_supermacrofamilies.py",           # 4) super-macrofamily (full)
    "build_ultimate_macrofamilies_full.py",  # 5) ultimate-macrofamily (full)
    "build_full_language_family_map.py"      # 6) merge everything
]

# Optional: ISO-639-5 source files
ISO_FILES = [
    "iso_639_5.json",
    "iso_639_5.txt",
    "iso_639_5_codes.csv"
]

def run(script_name: str):
    script_path = LIBS_DIR / script_name

    if not script_path.exists():
        print(f"ERROR: Script not found: {script_path}")
        sys.exit(1)

    print(f"\n=== Running {script_path} ===")

    # Ensure libs/ is available for imports
    env = dict(os.environ)
    env["PYTHONPATH"] = str(LIBS_DIR.resolve()) + os.pathsep + env.get("PYTHONPATH", "")

    # Run from project root so data/cache/maps paths work normally
    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(ROOT_DIR),
        env=env
    )

    if result.returncode != 0:
        print(f"ERROR: {script_name} failed")
        sys.exit(1)

def main():
    print("Starting full language-family pipeline (fresh build)...")
    print(f"Root dir: {ROOT_DIR}")
    print(f"Libs dir: {LIBS_DIR}")

    # --- Check ISO-639-5 source exists BEFORE running scripts 1+ ---
    if not any((DATA_DIR / f).exists() for f in ISO_FILES):
        print(f"ERROR: No ISO-639-5 source file found in {DATA_DIR}")
        print("Expected one of:", ISO_FILES)
        sys.exit(1)

    for i, script in enumerate(SCRIPTS):
        # Special case: skip Wikidata input check for the first script
        if i == 0:
            run(script)
            # After first script, check that wikidata-query.json exists
            wd_file = DATA_DIR / "wikidata-query.json"
            if not wd_file.exists():
                print(f"ERROR: {wd_file} missing after running {script}")
                sys.exit(1)
            continue

        # Run other scripts normally
        run(script)

    print("\nPipeline complete!")
    print(f"Output written to: {MAPS_DIR / 'code_to_full_family_map.json'}")

if __name__ == "__main__":
    main()

