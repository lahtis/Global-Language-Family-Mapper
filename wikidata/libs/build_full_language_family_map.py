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

# --- Project root ---
ROOT_DIR = Path(__file__).resolve().parent.parent

# --- Paths ---
MACRO = ROOT_DIR / "maps" / "code_to_macrofamily.json"
SUPER = ROOT_DIR / "maps" / "code_to_super_macrofamily_full.json"
ULTIMATE = ROOT_DIR / "maps" / "code_to_ultimate_macrofamily_full.json"
PARENT = ROOT_DIR / "maps" / "code_to_parent_chain.json"
LABELS = ROOT_DIR / "cache" / "cache_label_to_qid.json"
OUTPUT = ROOT_DIR / "maps" / "code_to_full_family_map.json"

def invert_labels(labels):
    return {v: k for k, v in labels.items()}

def main():
    with open(MACRO, "r", encoding="utf-8") as f:
        macro = json.load(f)
    with open(SUPER, "r", encoding="utf-8") as f:
        superm = json.load(f)
    with open(ULTIMATE, "r", encoding="utf-8") as f:
        ultimate = json.load(f)
    with open(PARENT, "r", encoding="utf-8") as f:
        parent = json.load(f)
    with open(LABELS, "r", encoding="utf-8") as f:
        labels = json.load(f)

    qid_to_label = invert_labels(labels)

    result = {}

    for code in parent.keys():
        macro_qid = macro.get(code, {}).get("macro_qid")
        super_qid = superm.get(code, {}).get("super_macro_qid")
        ultimate_qid = ultimate.get(code, {}).get("ultimate_macro_qid")

        result[code] = {
            "macro": {
                "qid": macro_qid,
                "label": qid_to_label.get(macro_qid, "(unknown)")
            },
            "super_macro": {
                "qid": super_qid,
                "label": qid_to_label.get(super_qid, "(unknown)")
            },
            "ultimate_macro": {
                "qid": ultimate_qid,
                "label": qid_to_label.get(ultimate_qid, "(unknown)")
            },
            "all_ancestors": superm.get(code, {}).get("all_ancestors", []),
            "parent_chain": parent.get(code, [])
        }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Saved: {OUTPUT}")

if __name__ == "__main__":
    main()

