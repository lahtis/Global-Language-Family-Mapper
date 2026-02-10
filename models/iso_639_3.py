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

import csv
import json
from pathlib import Path

DATA = Path("data")
TAB = DATA / "iso-639-3.tab"

iso1 = {}
iso2 = {}
iso3 = {}

with open(TAB, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="\t")
    for row in reader:
        code3 = row["Id"]
        part2b = row["Part2B"] or ""
        part2t = row["Part2T"] or ""
        part1 = row["Part1"] or ""
        name = row["Ref_Name"]

        # ISO 639-3
        iso3[code3] = {
            "name": name,
            "iso639_3": code3,
            "iso639_2B": part2b,
            "iso639_2T": part2t,
            "iso639_1": part1,
        }

        # ISO 639-2
        if part2b or part2t:
            iso2[code3] = {
                "name": name,
                "iso639_2B": part2b,
                "iso639_2T": part2t,
                "iso639_1": part1,
                "iso639_3": code3,
            }

        # ISO 639-1
        if part1:
            iso1[part1] = {
                "name": name,
                "iso639_1": part1,
                "iso639_3": code3,
            }

# Save
with open(DATA / "iso_639_3.json", "w", encoding="utf-8") as f:
    json.dump(iso3, f, ensure_ascii=False, indent=2)

with open(DATA / "iso_639_2.json", "w", encoding="utf-8") as f:
    json.dump(iso2, f, ensure_ascii=False, indent=2)

with open(DATA / "iso_639_1.json", "w", encoding="utf-8") as f:
    json.dump(iso1, f, ensure_ascii=False, indent=2)

print("ISO files regenerated successfully.")

