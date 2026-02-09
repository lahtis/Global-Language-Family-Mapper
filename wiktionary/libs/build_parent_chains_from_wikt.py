#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
WIKT = ROOT_DIR / "maps" / "wiktionary_families.json"
OUTPUT = ROOT_DIR / "maps" / "code_to_parent_chain.json"

def build_chain(code, wikt):
    chain = []
    current = code

    while True:
        entry = wikt.get(current)
        if not entry:
            break

        chain.append(current)

        parent = entry.get("family")
        if not parent or parent == current:
            break

        current = parent

    return chain

def main():
    if not WIKT.exists():
        print("ERROR: Missing wiktionary_families.json")
        return

    wikt = json.load(open(WIKT, "r", encoding="utf-8"))

    chains = {}
    for code in wikt.keys():
        chains[code] = build_chain(code, wikt)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    json.dump(chains, open(OUTPUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    print("DONE:", OUTPUT)
    print("Built parent chains for", len(chains), "codes.")

if __name__ == "__main__":
    main()

