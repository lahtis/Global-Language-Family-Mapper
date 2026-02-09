#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

CHAINS = ROOT_DIR / "maps" / "code_to_parent_chain.json"
WIKT = ROOT_DIR / "maps" / "wiktionary_families.json"
OUTPUT = ROOT_DIR / "maps" / "code_to_ultimate_macrofamilies.json"

def main():
    chains = json.load(open(CHAINS, "r", encoding="utf-8"))
    wikt = json.load(open(WIKT, "r", encoding="utf-8"))

    ultimate = {}

    for code, chain in chains.items():
        top = chain[-1] if chain else None
        if top and top in wikt:
            ultimate[code] = {
                "ultimate_code": top,
                "ultimate_name": wikt[top].get("canonicalName", top)
            }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    json.dump(ultimate, open(OUTPUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    print("Saved:", OUTPUT)
    print("Ultimate macrofamily entries:", len(ultimate))

if __name__ == "__main__":
    main()

