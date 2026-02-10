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
import gzip
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = PROJECT_ROOT / "data"

# Wiktextract raw data
WIKT_FILE = DATA_ROOT / "raw-wiktextract-data.jsonl.gz"

# Output file
OUTPUT = DATA_ROOT / "pos_stats.json"


def build_pos_stats():
    """
    Laskee POS-tilastot Wiktextractin raakadatasta.
    Tuottaa rakenteen:
    {
        "fi": {"noun": 12345, "verb": 6789, ...},
        "en": {"noun": 54321, "verb": 9876, ...},
        ...
    }
    """

    if not WIKT_FILE.exists():
        raise FileNotFoundError(f"Missing file: {WIKT_FILE}")

    pos_counts = defaultdict(lambda: defaultdict(int))

    print("Reading Wiktextract data...")

    with gzip.open(WIKT_FILE, "rt", encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            lang = entry.get("lang_code")
            pos = entry.get("pos")

            if not lang or not pos:
                continue

            pos_counts[lang][pos] += 1

    # Convert defaultdict → normal dict
    pos_counts = {lang: dict(counts) for lang, counts in pos_counts.items()}

    print(f"Saving POS stats to {OUTPUT}...")

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(pos_counts, f, ensure_ascii=False, indent=2)

    print("POS stats built successfully.")


if __name__ == "__main__":
    build_pos_stats()

