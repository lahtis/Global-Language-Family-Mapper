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

PROJECT_ROOT = Path(__file__).resolve().parent.parent
UNIFIED = PROJECT_ROOT / "output" / "unified" / "unified_languages.json"
OUTPUT_ERRORS = PROJECT_ROOT / "output" / "unified" / "iso_errors.json"


def validate_iso():
    with open(UNIFIED, "r", encoding="utf-8") as f:
        data = json.load(f)

    errors = []

    for lang_id, info in data.items():
        iso1 = info.get("iso639_1", "")
        iso2B = info.get("iso639_2B", "")
        iso2T = info.get("iso639_2T", "")
        iso3 = info.get("iso639_3", "")
        iso5 = info.get("iso639_5", "")

        # ISO 639-1 must be 2 letters
        if iso1 and len(iso1) != 2:
            errors.append(f"{lang_id}: invalid iso639_1 '{iso1}'")

        # ISO 639-3 must be 3 letters
        if iso3 and len(iso3) != 3:
            errors.append(f"{lang_id}: invalid iso639_3 '{iso3}'")

        # ISO 639-2B/T must be 3 letters
        if iso2B and len(iso2B) != 3:
            errors.append(f"{lang_id}: invalid iso639_2B '{iso2B}'")
        if iso2T and len(iso2T) != 3:
            errors.append(f"{lang_id}: invalid iso639_2T '{iso2T}'")

        # ISO 639-5 is only for families → cannot coexist with iso639_3
        if iso5 and iso3:
            errors.append(f"{lang_id}: has both iso639_3 and iso639_5")

    # Tulostus ja JSON-raportti
    if errors:
        with open(OUTPUT_ERRORS, "w", encoding="utf-8") as f:
            json.dump(errors, f, ensure_ascii=False, indent=2)
        print(f"ISO validation FAILED, see {OUTPUT_ERRORS}")
    else:
        print("All ISO codes are valid.")


if __name__ == "__main__":
    validate_iso()

