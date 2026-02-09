#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

CHAINS = ROOT_DIR / "maps" / "code_to_parent_chain.json"
WIKT = ROOT_DIR / "maps" / "wiktionary_families.json"
OUTPUT = ROOT_DIR / "maps" / "code_to_macrofamily.json"

def main():
    chains = json.load(open(CHAINS, "r", encoding="utf-8"))
    wikt = json.load(open(WIKT, "r", encoding="utf-8"))

    macro = {}

    for code, chain in chains.items():
        for fam in chain[::-1]:  # highest first
            entry = wikt.get(fam)
            if entry and entry.get("canonicalName"):
                macro[code] = {
                    "macrofamily_code": fam,
                    "macrofamily_name": entry["canonicalName"]
                }
                break

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    json.dump(macro, open(OUTPUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    print("Saved:", OUTPUT)
    print("Macrofamily entries:", len(macro))

if __name__ == "__main__":
    main()

