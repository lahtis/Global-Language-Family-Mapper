#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
MAPS_DIR = ROOT_DIR / "maps"

ISO_FILE = DATA_DIR / "iso_639_5.json"
WIKT_FILE = MAPS_DIR / "wiktionary_families.json"
OUT_FILE = MAPS_DIR / "code_to_family_qid.json"

def load_iso_codes():
    # Oletus: iso_639_5.json on lista tai dict, jossa on koodit.
    data = json.load(open(ISO_FILE, "r", encoding="utf-8"))
    if isinstance(data, dict):
        return list(data.keys())
    return data

def main():
    if not ISO_FILE.exists():
        print(f"ERROR: Missing ISO-639-5 file: {ISO_FILE}")
        return
    if not WIKT_FILE.exists():
        print(f"ERROR: Missing Wiktionary family file: {WIKT_FILE}")
        return

    iso_codes = load_iso_codes()
    wikt = json.load(open(WIKT_FILE, "r", encoding="utf-8"))

    result = {}
    missing = []

    for code in iso_codes:
        entry = wikt.get(code)
        if not entry:
            result[code] = None
            missing.append(code)
            continue

        qid = entry.get("wikidata_item")
        result[code] = qid

    MAPS_DIR.mkdir(parents=True, exist_ok=True)
    json.dump(result, open(OUT_FILE, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    print(f"DONE: {OUT_FILE}")
    print(f"Missing QID for {len(missing)} codes (but they still have Wiktionary family entries).")

if __name__ == "__main__":
    main()

