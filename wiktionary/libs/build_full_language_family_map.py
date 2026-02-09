#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

CHAINS = ROOT_DIR / "maps" / "code_to_parent_chain.json"
MACRO = ROOT_DIR / "maps" / "code_to_macrofamily.json"
SUPER = ROOT_DIR / "maps" / "code_to_supermacrofamily.json"
ULT = ROOT_DIR / "maps" / "code_to_ultimate_macrofamilies.json"
OUTPUT = ROOT_DIR / "maps" / "code_to_full_family_map.json"

def main():
    chains = json.load(open(CHAINS, "r", encoding="utf-8"))
    macro = json.load(open(MACRO, "r", encoding="utf-8"))
    superm = json.load(open(SUPER, "r", encoding="utf-8"))
    ultimate = json.load(open(ULT, "r", encoding="utf-8"))

    full = {}

    for code in chains.keys():
        full[code] = {
            "chain": chains.get(code),
            "macrofamily": macro.get(code),
            "supermacrofamily": superm.get(code),
            "ultimate": ultimate.get(code)
        }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    json.dump(full, open(OUTPUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    print("Saved:", OUTPUT)
    print("Full family map entries:", len(full))

if __name__ == "__main__":
    main()

