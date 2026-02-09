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
#
import json
from pathlib import Path

# --- Project root ---
ROOT_DIR = Path(__file__).resolve().parent.parent

# --- Paths ---
PARENT_CHAINS = ROOT_DIR / "maps" / "code_to_parent_chain.json"
LABELS = ROOT_DIR / "cache" / "cache_label_to_qid.json"
OUTPUT = ROOT_DIR / "maps" / "code_to_macrofamily.json"

def load():
    with open(PARENT_CHAINS, "r", encoding="utf-8") as f:
        chains = json.load(f)
    with open(LABELS, "r", encoding="utf-8") as f:
        labels = json.load(f)
    return chains, labels

def invert_labels(labels):
    return {v: k for k, v in labels.items()}

def find_macrofamily(chain, qid_to_label):
    # Skip generic meta-level nodes
    skip = {
        "Q20162172",  # language family
        "Q34770",     # language
        "Q17376908",  # linguistic entity
        "Q7048977",   # linguistic unit
        "Q18205125"   # grouping
    }

    for qid in chain:
        if qid not in skip:
            return qid
    return None

def main():
    chains, labels = load()
    qid_to_label = invert_labels(labels)

    macro = {}

    for code, chain in chains.items():
        if not chain:
            continue

        top = find_macrofamily(chain, qid_to_label)
        if top:
            macro[code] = {
                "macro_qid": top,
                "macro_label": qid_to_label.get(top, "(unknown)")
            }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(macro, f, indent=2, ensure_ascii=False)

    print("Saved:", OUTPUT)

if __name__ == "__main__":
    main()

