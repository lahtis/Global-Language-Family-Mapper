#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

CHAINS = ROOT_DIR / "maps" / "code_to_parent_chain.json"
WIKT = ROOT_DIR / "maps" / "wiktionary_families.json"
OUTPUT = ROOT_DIR / "maps" / "code_to_supermacrofamily.json"


def load():
    with open(CHAINS, "r", encoding="utf-8") as f:
        chains = json.load(f)
    with open(WIKT, "r", encoding="utf-8") as f:
        wikt = json.load(f)
    return chains, wikt


def find_supermacro(chain, wikt):
    """
    Supermacro: ketjun "korkeampi" taso – käytännössä sama logiikka
    kuin macrofamilylle, mutta voit halutessasi säätää tätä myöhemmin.
    Nyt: ketjun ylin canonicalName-perhe.
    """
    for fam in reversed(chain):
        entry = wikt.get(fam)
        if entry and entry.get("canonicalName"):
            return fam, entry["canonicalName"]
    return None, None


def main():
    chains, wikt = load()
    supermacro = {}

    for code, chain in chains.items():
        if not chain:
            continue

        fam_code, fam_name = find_supermacro(chain, wikt)
        if fam_code:
            supermacro[code] = {
                "supermacro_code": fam_code,
                "supermacro_name": fam_name,
            }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(supermacro, f, indent=2, ensure_ascii=False)

    print("Saved:", OUTPUT)
    print("Supermacro entries:", len(supermacro))


if __name__ == "__main__":
    main()

