#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
MAPS_DIR = ROOT_DIR / "maps"

LUA_FILE = DATA_DIR / "wiktionary_families.lua"
OUT_FILE = MAPS_DIR / "wiktionary_families.json"

def parse_lua_table(text: str) -> dict:
    entries = {}

    # Regex MUST be on ONE line
    pattern = re.compile(r'm\["([^"]+)"\]\s*=\s*{([^}]*)}', re.S)

    for code, body in pattern.findall(text):
        fields = {}

        for part in body.split(","):
            part = part.strip()
            if not part or "=" not in part:
                continue

            key, val = part.split("=", 1)
            key = key.strip()
            val = val.strip()

            # Remove trailing comments
            val = val.split("--", 1)[0].strip()

            # String "..." → ...
            if val.startswith('"') and val.endswith('"'):
                val = val[1:-1]

            # List {"a", "b"} → ["a", "b"]
            elif val.startswith("{") and val.endswith("}"):
                items = []
                inner = val[1:-1].strip()
                if inner:
                    for item in inner.split(","):
                        item = item.strip()
                        if item.startswith('"') and item.endswith('"'):
                            items.append(item[1:-1])
                val = items

            fields[key] = val

        entries[code] = fields

    return entries

def main():
    if not LUA_FILE.exists():
        print(f"ERROR: Lua file not found: {LUA_FILE}")
        return

    text = LUA_FILE.read_text(encoding="utf-8")
    data = parse_lua_table(text)

    MAPS_DIR.mkdir(parents=True, exist_ok=True)
    with OUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Saved: {OUT_FILE}")
    print(f"Parsed {len(data)} family entries from Wiktionary.")

if __name__ == "__main__":
    main()

