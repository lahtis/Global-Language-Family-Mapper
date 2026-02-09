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

import json
from pathlib import Path
import sys

# --- Project root ---
ROOT_DIR = Path(__file__).resolve().parent.parent

# --- Paths ---
SUPER_FULL = ROOT_DIR / "maps" / "code_to_super_macrofamily_full.json"
OUTPUT = ROOT_DIR / "maps" / "code_to_ultimate_macrofamily_full.json"

# Geneeriset node QID:t, joita ei lasketa ultimateksi
GENERIC = {
    "Q20162172",  # language family
    "Q34770",     # language
    "Q17376908",  # linguistic entity
    "Q7048977",   # linguistic unit
    "Q18205125"   # grouping
}

def main():
    if not SUPER_FULL.exists():
        print(f"ERROR: Required file missing: {SUPER_FULL}")
        sys.exit(1)

    with SUPER_FULL.open("r", encoding="utf-8") as f:
        data = json.load(f)

    result = {}

    for code, info in data.items():
        ancestors_list = info.get("all_ancestors", [])
        ancestors = [a.get("qid") for a in ancestors_list if a.get("qid") and a["qid"] not in GENERIC]

        if ancestors:
            # ultimate = ketjun korkein ei-geneerinen solmu
            ultimate = ancestors[-1]
        else:
            # fallback: käytä super-makroa tai Unknown
            ultimate = info.get("super_macro_qid", "Unknown")

        result[code] = {"ultimate_macro_qid": ultimate}

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Saved: {OUTPUT}")

if __name__ == "__main__":
    main()

