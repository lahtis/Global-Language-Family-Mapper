#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# GLFM Project
# Copyright (c) 2026 Tuomas Lähteenmäki
#
# https://codeberg.org/lahtis/GLFM
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

# --- Tiedostopolut ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_ROOT / "output" / "unified" / "unified_languages.json"
OUTPUT_LANG_LIST = PROJECT_ROOT / "output" / "unified" / "all_languages_list.json"
OUTPUT_ERRORS = PROJECT_ROOT / "output" / "unified" / "validation_errors.json"

# --- Lataa unified data ---
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    unified = json.load(f)

errors = []
all_langs_list = []

for lang_id, lang in unified.items():
    lang_entry = {
        "id": lang_id,
        "bcp47": lang.get("bcp47"),
        "default_script": lang.get("default_script"),
        "default_region": lang.get("default_region"),
        "written": lang.get("written", False),
        "written_scripts": lang.get("written_scripts", []),
        "uralicNLP": lang.get("uralicNLP", False)
    }
    all_langs_list.append(lang_entry)

    # --- Testit ---
    # 1. default_script ei voi olla UNKNOWN
    if not lang_entry["default_script"] or lang_entry["default_script"].upper() == "UNKNOWN":
        errors.append({"id": lang_id, "type": "default_script_unknown", "value": lang_entry["default_script"]})

    # 2. default_script pitäisi olla written_scripts listassa jos written=True
    if lang_entry["written"] and lang_entry["default_script"] not in lang_entry["written_scripts"]:
        errors.append({"id": lang_id, "type": "default_script_missing_in_written_scripts", "value": lang_entry["written_scripts"]})

    # 3. written_scripts ei saa sisältää UNKNOWN
    for s in lang_entry["written_scripts"]:
        if s.upper() == "UNKNOWN":
            errors.append({"id": lang_id, "type": "written_scripts_contains_unknown", "value": lang_entry["written_scripts"]})

    # 4. BCP47 ei saa sisältää -UNKNOWN tai -001
    bcp = lang_entry["bcp47"] or ""
    if "-UNKNOWN" in bcp or "-001" in bcp:
        errors.append({"id": lang_id, "type": "bcp47_invalid_value", "value": bcp})

    # 5. default_region voi olla 001 vain jos BCP47 ei lisää sitä
    region = lang_entry["default_region"]
    if region == "001" and "-001" in bcp:
        errors.append({"id": lang_id, "type": "region_001_in_bcp47", "value": bcp})

# --- Tallenna kielilista JSON ---
with open(OUTPUT_LANG_LIST, "w", encoding="utf-8") as f:
    json.dump(all_langs_list, f, ensure_ascii=False, indent=2)

# --- Tallenna virheilista JSON ---
with open(OUTPUT_ERRORS, "w", encoding="utf-8") as f:
    json.dump(errors, f, ensure_ascii=False, indent=2)

print(f"Validation finished: {len(unified)} languages checked.")
print(f"Errors found: {len(errors)}")
print(f"All languages list saved to: {OUTPUT_LANG_LIST}")
print(f"Validation errors saved to: {OUTPUT_ERRORS}")

