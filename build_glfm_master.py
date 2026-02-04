# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------
# Global Language Family Mapper (GLFM)
# Copyright (c) 2026 Tuomas Lähteenmäki
# Licensed under the MIT License
# ------------------------------------------------------------------------
# This script is part of the GLFM project.
# See LICENSE file in the project root for full license text.
# ------------------------------------------------------------------------

import json
import os

BASE = "conf"
SPOKEN = os.path.join(BASE, "spoken_languages.json")
ISO_MAP = os.path.join(BASE, "iso_map.json")
URALIC = os.path.join(BASE, "uralic_languages.json")

OUTPUT = "GLFM_master_iso_only.json"

def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    spoken = load(SPOKEN)
    iso_map = load(ISO_MAP)
    uralic = set(load(URALIC))

    result = {}

    for lang in spoken:
        code = lang["code"]
        name = lang["name"]
        type_ = lang["type"]

        iso3 = code.split("-")[0].lower()
        iso2 = iso3
        iso1 = iso_map.get(iso3, "")

        key = f"{iso3.upper()}-{iso3.upper()}"

        result[key] = {
            "name": name,
            "official_name": name,
            "iso639_3": iso3,
            "iso639_2": iso2,
            "iso639_1": iso1,
            "bcp47": code,
            "fallback": code,
            "uralicNLP": iso3 in uralic,
            "type": type_
        }

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print(f"Built new ISO‑based GLFM for {len(result)} languages.")

if __name__ == "__main__":
    main()

