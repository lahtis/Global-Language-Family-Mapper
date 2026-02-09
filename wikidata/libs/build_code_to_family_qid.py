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
INPUT = ROOT_DIR / "data" / "iso_639_5.json"           # raw ISO-639-5 data
LABEL_TO_QID_FILE = ROOT_DIR / "cache" / "cache_label_to_qid.json"
OUT = ROOT_DIR / "maps" / "code_to_family_qid.json"

def main():
    print("=== BUILD CODE -> FAMILY QID MAP ===")

    # Load input
    with open(INPUT, "r", encoding="utf-8") as f:
        raw = json.load(f)

    # Accept either direct dict or {"matches": {...}}
    if "matches" in raw and isinstance(raw["matches"], dict):
        code_to_label = raw["matches"]
    else:
        code_to_label = raw

    # Check if label->QID cache exists, create empty if missing
    if not LABEL_TO_QID_FILE.exists():
        print(f"WARNING: {LABEL_TO_QID_FILE} missing, creating empty cache.")
        LABEL_TO_QID_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LABEL_TO_QID_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)

    # Load label -> QID cache
    with open(LABEL_TO_QID_FILE, "r", encoding="utf-8") as f:
        label_to_qid = json.load(f)

    result = {}
    missing = 0

    for code, label in code_to_label.items():
        qid = label_to_qid.get(label)
        if qid:
            result[code] = qid
        else:
            print(f"WARNING: no QID for label '{label}' (code {code})")
            result[code] = None
            missing += 1

    # Ensure output folder exists
    OUT.parent.mkdir(parents=True, exist_ok=True)

    # Write result
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print("DONE:", OUT)
    print("Missing:", missing)

if __name__ == "__main__":
    main()

