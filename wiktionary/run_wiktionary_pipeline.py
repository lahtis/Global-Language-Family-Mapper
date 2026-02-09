#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys
import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

DATA_DIR = ROOT_DIR / "data"
CACHE_DIR = ROOT_DIR / "cache"
MAPS_DIR = ROOT_DIR / "maps"
LIBS_DIR = ROOT_DIR / "libs"

for folder in [DATA_DIR, CACHE_DIR, MAPS_DIR, LIBS_DIR]:
    if not folder.exists():
        if folder == DATA_DIR:
            print(f"ERROR: data/ directory missing: {DATA_DIR}")
            sys.exit(1)
        else:
            print(f"Creating missing directory: {folder}")
            folder.mkdir(parents=True, exist_ok=True)

SCRIPTS = [
    "wiktionary_family_api.py",               # 0) Lua -> JSON
    "build_code_to_family_qid_from_wikt.py",  # 1) ISO-639-5 -> family QID
    "build_parent_chains_from_wikt.py",       # 2) QID parent chains
    "build_code_to_macrofamily.py",           # 3) macrofamily (existing)
    "build_supermacrofamilies.py",            # 4) super-macrofamily (existing)
    "build_ultimate_macrofamilies_full.py",   # 5) ultimate-macrofamily (existing)
    "build_full_language_family_map.py"       # 6) merge everything (existing)
]

ISO_FILES = [
    "iso_639_5.json"
]

def run(script_name: str):
    script_path = LIBS_DIR / script_name

    if not script_path.exists():
        print(f"ERROR: Script not found: {script_path}")
        sys.exit(1)

    print(f"\n=== Running {script_path} ===")

    env = dict(os.environ)
    env["PYTHONPATH"] = str(LIBS_DIR.resolve()) + os.pathsep + env.get("PYTHONPATH", "")

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(ROOT_DIR),
        env=env
    )

    if result.returncode != 0:
        print(f"ERROR: {script_name} failed")
        sys.exit(1)

def main():
    print("Starting Wiktionary-based language-family pipeline...")
    print(f"Root dir: {ROOT_DIR}")
    print(f"Libs dir: {LIBS_DIR}")

    if not any((DATA_DIR / f).exists() for f in ISO_FILES):
        print(f"ERROR: No ISO-639-5 source file found in {DATA_DIR}")
        print("Expected one of:", ISO_FILES)
        sys.exit(1)

    lua_file = DATA_DIR / "wiktionary_families.lua"
    if not lua_file.exists():
        print(f"ERROR: Wiktionary Lua source missing: {lua_file}")
        sys.exit(1)

    for script in SCRIPTS:
        run(script)

    print("\nWiktionary pipeline complete!")
    print(f"Output written to: {MAPS_DIR / 'code_to_full_family_map.json'}")

if __name__ == "__main__":
    main()

