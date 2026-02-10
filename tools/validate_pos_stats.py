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
OUTPUT_ERRORS = PROJECT_ROOT / "output" / "unified" / "pos_stats_errors.json"


def validate_pos_stats():
    with open(UNIFIED, "r", encoding="utf-8") as f:
        data = json.load(f)

    errors = []

    for lang_id, info in data.items():
        pos = info.get("pos_stats", {})

        if not pos:
            continue

        for tag, count in pos.items():
            if not isinstance(count, int):
                errors.append(f"{lang_id}: POS '{tag}' is not an integer ({count})")
            elif count < 0:
                errors.append(f"{lang_id}: POS '{tag}' has negative count ({count})")

    # Tulostus ja JSON-raportti
    if errors:
        with open(OUTPUT_ERRORS, "w", encoding="utf-8") as f:
            json.dump(errors, f, ensure_ascii=False, indent=2)
        print(f"POS stats validation FAILED, see {OUTPUT_ERRORS}")
    else:
        print("POS stats validation OK")


if __name__ == "__main__":
    validate_pos_stats()

